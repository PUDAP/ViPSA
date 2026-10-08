"""STAGED Keithley 2450 SCPI finite-trigger acquisition; injected session only.

Manual: 2450-901-01 Rev E (2019). No VISA opening, language switching,
route selection, matrix control, deployment or hardware qualification here.
"""
from __future__ import annotations
import copy
import csv
import hashlib
import json
import math
import re
import threading
import time
import uuid


class CapabilityError(RuntimeError):
    """Required firmware, transport or physical bound is unverified."""


def _number(value, name, low=0.0, high=math.inf, positive=False):
    if isinstance(value, bool):
        raise ValueError(name + ' cannot be boolean')
    value = float(value)
    if not math.isfinite(value) or value < low or value > high or (positive and value <= 0):
        raise ValueError(name + ' is outside its finite allowable bounds')
    return value


def _text(raw):
    return raw.decode('ascii') if isinstance(raw, bytes) else str(raw)


class Guarded2450:
    """Wrap an EXISTING exclusive SCPI session; never open one.

    Qualification is externally supplied evidence of worst-case FULL measurement
    (including source readback/reference/filter work), update/settling, dispatch
    and shutdown times plus actual voltage/current upper bounds. Offline fixtures
    may use kind=offline ONLY with session.offline_simulator=True.
    """
    def __init__(self, session, qualification=None, recover_after_timeout=None):
        self.session = session
        self.qualification = copy.deepcopy(qualification)
        self.recover_after_timeout = recover_after_timeout
        self._lock = threading.Lock()
        self._plan = None
        self._state = 'UNPREPARED'
        self._raw = []
        self._device_reserved_by_id = {}
        self._output_off_verified = None
        self._scpi_verified = False
        self._transport_synchronized = True

    def _write(self, command):
        self.session.write(command)

    def _query(self, command):
        if not self._transport_synchronized:
            raise CapabilityError('Response stream synchronization unknown; no further query or INIT')
        try:
            if callable(getattr(self.session, 'read_raw', None)):
                self.session.write(command)
                query_delay = getattr(self.session, 'query_delay', 0)
                if query_delay: time.sleep(query_delay)
                raw = self.session.read_raw()
            else:
                raw = self.session.query(command)
            self._raw.append({'command': command, 'response': raw})
            return _text(raw).strip()
        except BaseException:
            self._transport_synchronized = False
            raise

    def _errors(self):
        errors = []
        for _ in range(32):
            raw = self._query(':SYST:ERR?')
            if int(raw.split(',')[0]) == 0:
                return errors
            errors.append(raw)
        raise CapabilityError('Error queue did not terminate within 32 entries')

    def get_acquisition_capabilities(self):
        q = self.qualification or {}
        return {'deployment': 'staged', 'command_set': 'SCPI (not SCPI2400/TSP)',
                'physical_qualified': False,
                'qualification_claim_supplied': q.get('kind') == 'physical',
                'qualification_evidence_verified': False,
                'firmware_verified': self._plan is not None,
                'protection': 'conservative full-exposure reservation + finite model + timer branch',
                'asynchronous_measurement_preemption': False,
                'live_cumulative_measured_joule_cutoff': False,
                'source_readback': ':SOUR:VOLT:READ:BACK ON; buffer SOUR',
                'aperture_readback': 'NPLC? / SYST:LFR? (manual-defined native integration)',
                'independent_aperture_query': False,
                'matrix_owned': False, 'max_points': 2500,
                'qualification_evidence': q.get('evidence'),
                'methods': ['prepare_guarded_acquisition', 'execute_guarded_acquisition',
                            'guarded_source_voltage_measure_current',
                            'guarded_hold_voltage_measure_current', 'get_terminals',
                            'get_exposure_guard_state', 'abort_guarded_acquisition']}

    def get_terminals(self):
        if not self._scpi_verified:
            if self._query('*LANG?').upper() != 'SCPI':
                raise CapabilityError('Requires native SCPI to query terminals')
            self._scpi_verified = True
        return self._query(':ROUT:TERM?').upper()

    def _verify_prepared(self, p):
        start = len(self._raw)
        errors = []
        try:
            model = self._query(':TRIG:BLOC:LIST?')
            checks = [model == p['model_readback'],
                      math.isclose(float(self._query(':TRIG:TIM1:DEL?')), p['deadline_s'], rel_tol=1e-6),
                      int(self._query(':TRIG:TIM1:COUN?')) == 1,
                      self._query(':TRIG:TIM1:STAR:STIM?').upper() in ('NOT1','NOTIFY1'),
                      self._query(':TRIG:TIM1:STAR:GEN?').upper() in ('0','OFF'),
                      self._query(':TRIG:TIM1:STAT?').upper() in ('1','ON'),
                      self._query(':OUTP?').upper() in ('0','OFF'),
                      self._query(':ROUT:TERM?').upper() == 'REAR',
                      self._query(':SOUR:VOLT:READ:BACK?').upper() in ('1','ON'),
                      math.isclose(float(self._query(':SENS:CURR:NPLC?')),p['nplc'],rel_tol=1e-6)]
            matched = all(checks)
            if not matched: errors.append('Prepared configuration/model readback differs from accepted baseline')
        except BaseException as exc:
            matched = False
            errors.append('Prepared readback unknown: '+type(exc).__name__+': '+str(exc))
        return matched, copy.deepcopy(self._raw[start:]), errors

    def get_exposure_guard_state(self):
        p = self._plan or {}
        matched, readbacks, errors = (False, [], [])
        if self._state == 'PREPARED':
            matched, readbacks, errors = self._verify_prepared(p)
        return {'state': self._state, 'plan_id': p.get('plan_id'),
                'plan_digest': p.get('plan_digest'),
                'autonomous_configured': self._state == 'PREPARED' and matched,
                'configuration_verified': matched, 'raw_readbacks': readbacks,
                'verification_errors': errors,
                'timer_activation': 'INIT block 1 NOTIFY1, before output ON',
                'timer_running': False if self._state == 'PREPARED' and matched else None,
                'output_off_verified': self._output_off_verified,
                'device_reserved_j': self._device_reserved_by_id.get(p.get('device_id'), 0.0),
                'boundary': copy.deepcopy(p.get('boundary')),
                'device_id': p.get('device_id'),
                'envelope_bounds': copy.deepcopy(p.get('envelope_bounds')),
                'prepared_bounds': copy.deepcopy(p.get('envelope_bounds'))}

    def _cleanup(self, query_safe=True):
        errors = []
        self._output_off_verified = None
        if not self._scpi_verified:
            return ['Output state unknown: native SCPI not verified; no wrong-dialect cleanup sent']
        for cmd in (':ABOR', ':OUTP OFF'):
            try:
                self._write(cmd)
            except BaseException as exc:
                errors.append(f'{cmd}: {type(exc).__name__}: {exc}')
        if query_safe and self._transport_synchronized:
            try:
                self._output_off_verified = self._query(':OUTP?') in ('0', 'OFF')
                if not self._output_off_verified:
                    errors.append('Output OFF readback not confirmed')
            except BaseException as exc:
                errors.append('OFF readback unknown: ' + str(exc))
        return errors

    def abort_guarded_acquisition(self):
        # Deliberately not waiting on acquisition lock: exclusive transport must
        # support caller cancellation policy. Never resend INIT or clear traces.
        try:
            if not self._scpi_verified:
                self._scpi_verified = self._query('*LANG?').upper() == 'SCPI'
        except BaseException:
            pass
        errors = self._cleanup()
        self._state = 'ABORTED'
        return {**self.get_exposure_guard_state(), 'cleanup_errors': errors}

    def prepare_guarded_acquisition(self, voltages, current_compliance, *,
            delay_s=0.0, nplc=0.1, current_range=None, voltage_range=None,
            reset=True, deadline_s, operation_limit_j, device_limit_j=5.0,
            category='forming', branch_ids=None, device_id=None,
            remaining_device_j=None, warning_waiver_scopes=()):
        """Output-OFF programming; returns immutable digest/id, not output-on.

        Compliance may be a scalar or an ordered per-point sequence. Current
        range defaults to each point's compliance (fixed), NPLC=.1, reset=True.
        No chunk execution: one ordered native configuration-list model.
        """
        with self._lock:
            if self._state in ('PREPARED', 'RUNNING'):
                raise CapabilityError('Abort existing prepared/running plan first')
            vs = [_number(v, 'voltage', -200, 200) for v in voltages]
            if not 1 <= len(vs) <= 2500:
                raise ValueError('wave must contain 1..2500 ordered points; no silent chunks')
            cs = (list(current_compliance) if isinstance(current_compliance, (list, tuple))
                  else [current_compliance] * len(vs))
            if len(cs) != len(vs):
                raise ValueError('compliance length must equal voltage length')
            cs = [_number(v, 'compliance', high=1.05, positive=True) for v in cs]
            delay = _number(delay_s, 'delay_s', high=10000)
            if 0 < delay < 167e-9:
                raise ValueError('nonzero trigger delay must be >=167 ns')
            nplc = _number(nplc, 'nplc', .01, 10)
            if not isinstance(reset, bool):
                raise ValueError('reset must be boolean')
            deadline = _number(deadline_s, 'deadline_s', 8e-6, 100000)
            op = _number(operation_limit_j, 'operation_limit_j', positive=True)
            device = _number(device_limit_j, 'device_limit_j', positive=True)
            caps = {'forming': .01, 'recovery': .01, 'read': 1e-5, 'conditioning': 5., 'write': 5.}
            if category not in caps or op > caps[category] or device > 5:
                raise ValueError('hard limits: forming/recovery .01 J, read 1e-5 J, device/other 5 J')
            if not isinstance(warning_waiver_scopes, (list, tuple, set)) or any(s not in ('conditioning','write') for s in warning_waiver_scopes):
                raise ValueError('warning waivers must list exact conditioning/write scopes')
            if category in ('conditioning','write') and op > .05 and category not in warning_waiver_scopes:
                raise ValueError('operation exceeds .05 J warning without exact category waiver scope')
            branches = list(branch_ids) if branch_ids is not None else [None] * len(vs)
            if len(branches) != len(vs) or any(x is not None and not isinstance(x, (str, int)) for x in branches):
                raise ValueError('branch_ids must be ordered strings/integers matching points')
            ranges = [_number(current_range if current_range is not None else c,
                              'current_range', high=1, positive=True) for c in cs]
            vr = _number(voltage_range if voltage_range is not None else max(.02, max(map(abs, vs))),
                         'voltage_range', high=200, positive=True)
            if vr < max(map(abs, vs)):
                raise ValueError('voltage range below waveform peak')
            q = copy.deepcopy(self.qualification or {})
            envelopes = q.pop('envelopes', None)
            if envelopes is not None:
                phase = 'forming' if category == 'recovery' else category
                if not isinstance(envelopes, dict) or phase not in envelopes or not isinstance(envelopes[phase], dict):
                    raise CapabilityError('Missing exact category qualification envelope: ' + phase)
                q.update(copy.deepcopy(envelopes[phase]))
            if q.get('kind') == 'physical' and (device_id is None or remaining_device_j is None):
                raise CapabilityError('Physical execution requires canonical device_id and durable-parent remaining_device_j')
            device_id = device_id if device_id is not None else 'offline-fixture-device'
            if not isinstance(device_id, str) or not device_id.strip() or device_id != device_id.strip():
                raise ValueError('device_id must be the exact canonical nonempty parent identity, not an alias')
            remaining = _number(device if remaining_device_j is None else remaining_device_j, 'remaining_device_j', high=device)
            if q.get('kind') not in ('offline', 'physical') or not q.get('evidence'):
                raise CapabilityError('Missing qualification: measured voltage/current and full measurement/update/shutdown/block upper bounds required')
            if q['kind'] == 'offline' and not getattr(self.session, 'offline_simulator', False):
                raise CapabilityError('Offline timing qualification cannot enable a real VISA session')
            for key in ('voltage_bound_v', 'current_bound_a', 'measurement_max_s',
                        'source_update_max_s', 'shutdown_max_s', 'block_max_s'):
                q[key] = _number(q.get(key), key, positive=True)
            if q['voltage_bound_v'] < max(map(abs, vs)) or q['current_bound_a'] < max(cs):
                raise ValueError('Qualification bounds do not cover requested waveform/compliance')
            if q['kind'] == 'physical' and nplc > _number(q.get('nplc_max'), 'qualified nplc_max', .01, 10):
                raise CapabilityError('NPLC outside physically qualified timing scope')
            tail = q['source_update_max_s'] + delay + q['measurement_max_s'] + 5*q['block_max_s']
            exposure = deadline + tail + q['shutdown_max_s']
            reservation = q['voltage_bound_v'] * q['current_bound_a'] * exposure
            if reservation > op or reservation > remaining or self._device_reserved_by_id.get(device_id, 0.0) + reservation > device:
                raise ValueError('Full-exposure worst-case reservation exceeds operation/device joule budget')
            self._raw = []
            self._state = 'PREPARING'
            try:
                self._scpi_verified = self._query('*LANG?').upper() == 'SCPI'
                if not self._scpi_verified:
                    raise CapabilityError('Requires native SCPI; no silent language switch/reboot')
                idn = self._query('*IDN?')
                firmware = idn.split(',')[-1].strip()
                parsed = re.search(r'(\d+)\.(\d+)\.(\d+)', firmware)
                if '2450' not in idn or not parsed or tuple(map(int, parsed.groups())) < (1, 7, 0):
                    raise CapabilityError('2450 firmware >=1.7.0 required for MDIG; IDN firmware unverified')
                if firmware != q.get('firmware'):
                    raise CapabilityError('IDN firmware does not match qualification firmware')
                self._write(':ABOR'); self._write(':OUTP OFF')
                if self._query(':OUTP?') not in ('0', 'OFF'):
                    raise CapabilityError('Output OFF not verified before programming')
                terminals = self.get_terminals()
                if terminals != 'REAR':
                    raise CapabilityError('Requires operator-selected REAR terminals; driver will not change terminals')
                pre_errors = self._errors()
                if pre_errors:
                    raise CapabilityError('Preexisting instrument errors: ' + repr(pre_errors))
                if reset:
                    self._write('*RST')
                self._write(':OUTP OFF')
                if reset:
                    # Manual 12-42: reset defaults to FRONT. Restore the already
                    # verified terminal, output OFF; never touch a matrix route.
                    self._write(':ROUT:TERM REAR')
                if self.get_terminals() != terminals:
                    raise CapabilityError('Terminal restore/readback failed after reset')
                setup = [':FORM ASC', ':CALC:CURR:MATH:STAT OFF',
                         ':SOUR:FUNC VOLT', ':SENS:FUNC "CURR"',
                         ':SENS:CURR:UNIT AMP', ':SOUR:VOLT:READ:BACK ON',
                         ':SOUR:VOLT:DEL:AUTO OFF', ':SOUR:VOLT:DEL 0',
                         ':SOUR:VOLT:RANG:AUTO OFF', f':SOUR:VOLT:RANG {vr:.17g}',
                         ':SENS:CURR:RANG:AUTO OFF', ':SENS:CURR:AVER OFF',
                         ':SENS:CURR:AZER ON', f':SENS:CURR:NPLC {nplc:.17g}']
                for cmd in setup: self._write(cmd)
                actual_nplc = float(self._query(':SENS:CURR:NPLC?'))
                frequency = float(self._query(':SYST:LFR?'))
                if not math.isclose(actual_nplc, nplc, rel_tol=1e-6) or frequency not in (50, 60):
                    raise CapabilityError('Native NPLC / mains-frequency readback did not verify')
                aperture = actual_nplc / frequency
                if q['kind'] == 'physical':
                    qualified_duration = _number(q.get('qualified_duration_s'), 'qualified duration', positive=True)
                    if not q.get('timing_evidence_reference') or not math.isclose(qualified_duration, aperture, rel_tol=1e-6):
                        raise CapabilityError('qualified native duration / timing evidence does not match aperture readback')
                if aperture > q['measurement_max_s']:
                    raise CapabilityError('Actual native aperture exceeds qualified FULL measurement bound')
                if self._query(':SOUR:VOLT:READ:BACK?') not in ('1', 'ON'):
                    raise CapabilityError('Measured source readback is not ON')
                suffix = uuid.uuid4().hex[:12]
                source_list, measure_list = 'gsrc_'+suffix, 'gmeas_'+suffix
                self._write(f':SOUR:CONF:LIST:CRE "{source_list}"')
                self._write(f':SENS:CONF:LIST:CRE "{measure_list}"')
                self._write(f':TRAC:POIN {max(10, len(vs))}, "defbuffer1"')
                self._write(':TRAC:FILL:MODE ONCE, "defbuffer1"')
                self._write(':TRAC:CLE "defbuffer1"')
                actual_source_range = float(self._query(':SOUR:VOLT:RANG?'))
                if not math.isfinite(actual_source_range) or actual_source_range < max(map(abs, vs)):
                    raise CapabilityError('Source range readback cannot cover waveform')
                actual_current_ranges = []
                for v, c, cr in zip(vs, cs, ranges):
                    self._write(f':SOUR:VOLT:LEV {v:.17g}')
                    self._write(f':SENS:CURR:RANG {cr:.17g}')
                    self._write(f':SOUR:VOLT:ILIM {c:.17g}')
                    actual_limit = float(self._query(':SOUR:VOLT:ILIM?'))
                    if not math.isclose(actual_limit, c, rel_tol=1e-6, abs_tol=1e-12):
                        raise CapabilityError('Compliance readback differs from requested point limit')
                    actual_range = float(self._query(':SENS:CURR:RANG?'))
                    if not math.isfinite(actual_range) or actual_range <= 0:
                        raise CapabilityError('Current range readback invalid')
                    actual_current_ranges.append(actual_range)
                    self._write(f':SOUR:CONF:LIST:STORE "{source_list}"')
                    self._write(f':SENS:CONF:LIST:STORE "{measure_list}"')
                program = [':TRIG:LOAD "Empty"', ':TRIG:TIM1:STAT OFF',
                           ':TRIG:TIM1:CLE', f':TRIG:TIM1:DEL {deadline:.17g}',
                           ':TRIG:TIM1:COUN 1', ':TRIG:TIM1:STAR:GEN OFF',
                           ':TRIG:TIM1:STAR:STIM NOTIFY1', ':TRIG:TIM1:STAT ON',
                           ':TRIG:BLOC:NOT 1, 1', ':TRIG:BLOC:BRAN:EVEN 2, TIMER1, 9',
                           f':TRIG:BLOC:CONF:NEXT 3, "{source_list}", "{measure_list}"',
                           ':TRIG:BLOC:SOUR:STAT 4, ON',
                           f':TRIG:BLOC:DEL:CONS 5, {delay:.17g}',
                           ':TRIG:BLOC:MDIG 6, "defbuffer1", 1',
                           ':TRIG:BLOC:BRAN:EVEN 7, TIMER1, 9',
                           f':TRIG:BLOC:BRAN:COUN 8, {len(vs)}, 2',
                           ':TRIG:BLOC:SOUR:STAT 9, OFF']
                for cmd in program: self._write(cmd)
                errors = self._errors()
                if errors: raise CapabilityError('SCPI configuration rejected: ' + repr(errors))
                self._output_off_verified = self._query(':OUTP?') in ('0', 'OFF')
                if not self._output_off_verified: raise CapabilityError('Preparation unexpectedly enabled output')
                model_readback = self._query(':TRIG:BLOC:LIST?')
                if not model_readback:
                    raise CapabilityError('Trigger model list readback is empty')
                parameters = dict(model_readback=model_readback, voltages=vs, compliance_a=cs, branch_ids=branches,
                                  delay_s=delay, nplc=nplc, current_ranges=ranges,
                                  voltage_range=vr, voltage_range_readback=actual_source_range,
                                  current_ranges_readback=actual_current_ranges,
                                  reset=reset, deadline_s=deadline,
                                  operation_limit_j=op, device_limit_j=device, category=category,
                                  qualification=q, program=program, device_id=device_id, remaining_device_j=remaining,
                                  warning_waiver_scopes=sorted(warning_waiver_scopes))
                digest = hashlib.sha256(json.dumps(parameters, sort_keys=True, allow_nan=False).encode()).hexdigest()
                self._plan = dict(parameters, plan_id=uuid.uuid4().hex, plan_digest=digest,
                    capabilities=self.get_acquisition_capabilities(),
                    aperture={'nplc_requested': nplc, 'nplc_readback': actual_nplc,
                              'mains_frequency_hz': frequency,
                              'effective_native_aperture_s': aperture,
                              'provenance': 'SENS:CURR:NPLC? / SYST:LFR?; manual 12-50,12-114',
                              'independent_aperture_measurement': False},
                    boundary={'deadline_s': deadline, 'maximum_one_point_tail_s': tail,
                              'shutdown_max_s': q['shutdown_max_s'],
                              'full_exposure_bound_s': exposure, 'reserved_energy_j': reservation,
                              'coverage': 'output enable through verified shutdown, including first/last unmeasured intervals',
                              'actual_output_on_time': None, 'actual_output_off_time': None,
                              'actual_boundary_timestamps_available': False,
                              'chunk_count': 1, 'continuous_output_between_points': True},
                    envelope_bounds={**{k:q[k] for k in ('voltage_bound_v', 'current_bound_a', 'measurement_max_s', 'source_update_max_s', 'shutdown_max_s', 'block_max_s')},
                                     'deadline_s': deadline, 'full_exposure_bound_s': exposure,
                                     'reserved_energy_j': reservation},
                    list_names=(source_list, measure_list))
                self._state = 'PREPARED'
                return copy.deepcopy({k:self._plan[k] for k in ('plan_id', 'plan_digest', 'aperture', 'boundary', 'device_id', 'envelope_bounds')})
            except BaseException:
                self._cleanup(query_safe=False)
                self._state = 'PREPARATION_FAILED'
                raise

    def _rows(self, p):
        count_text = self._query(':TRAC:ACT? "defbuffer1"')
        count = int(count_text)
        if not 0 <= count <= len(p['voltages']):
            raise CapabilityError('Trace count invalid: no inferred fallback count or replay')
        if count == 0: return []
        raw = self._query(f':TRAC:DATA? 1, {count}, "defbuffer1", SOUR, READ, REL, SOURSTAT, STAT, SEC, FRAC')
        values = next(csv.reader([raw]))
        if len(values) != count*7: raise CapabilityError('Trace length mismatch; raw response retained')
        rows = []
        for i in range(count):
            v, current, relative, source_status, status, seconds, fractional = map(float, values[7*i:7*i+7])
            if not all(map(math.isfinite, (v, current, relative, source_status, status, seconds, fractional))):
                raise CapabilityError('Nonfinite trace; raw response retained')
            ss = int(source_status)
            if not ss & 8:
                raise CapabilityError('Trace SOURCE lacks measured-readback status (manual 14-40 bit 3)')
            rows.append({'index':i, 'Time(T)':relative, 'Voltage (V)':v,
                         'V_meas (V)':v, 'V_cmd (V)':p['voltages'][i],
                         'Current (A)':current, 'I_meas (A)':current,
                         'instrument_seconds':seconds, 'instrument_fractional_seconds':fractional,
                         'source_status':ss, 'measurement_status':int(status),
                         'compliance':bool(ss & 32), 'output_on':bool(ss & 128),
                         'branch_id':p['branch_ids'][i], 'compliance_a':p['compliance_a'][i],
                         'programmed_delay_s':p['delay_s'],
                         'measured_power_w':abs(v*current)})
        return rows

    def execute_guarded_acquisition(self, plan_id, *, host_timeout_s=30.0):
        with self._lock:
            if self._state != 'PREPARED' or self._plan['plan_id'] != plan_id:
                raise CapabilityError('Only the exact previously PREPARED plan may execute once')
            timeout = _number(host_timeout_s, 'host_timeout_s', positive=True)
            p = copy.deepcopy(self._plan)
            matched, readbacks, verification_errors = self._verify_prepared(p)
            if not matched:
                self._cleanup(query_safe=False)
                self._state = 'PREPARED_INVALID'
                raise CapabilityError('prepared configuration not independently reverified: ' + repr(verification_errors))
            self._state = 'RUNNING'
            # Burn full reservation BEFORE INIT; unknown/partial exposure never refunds.
            self._device_reserved_by_id[p['device_id']] = self._device_reserved_by_id.get(p['device_id'], 0.0) + p['boundary']['reserved_energy_j']
            rows, errors, cleanup_errors = [], [], []
            query_safe, completed_model = True, False
            cancelled = None
            start = time.monotonic()
            try:
                # No reset, clearing or reconfiguration after prepare.
                self._write(':INIT')
                while True:
                    state = self._query(':TRIG:STAT?').upper()
                    if state.startswith('IDLE'):
                        completed_model = True; break
                    if state.startswith(('FAILED', 'ABORTED', 'ABORTING', 'EMPTY', 'BUILDING')):
                        raise CapabilityError('Trigger did not complete: ' + state)
                    if time.monotonic()-start >= timeout:
                        raise TimeoutError('Host polling deadline; autonomous instrument guard remains independent')
                    time.sleep(.01)
            except BaseException as exc:
                errors.append(type(exc).__name__ + ': ' + str(exc))
                if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    cancelled = exc
                # A query exception can leave a response pending. Only explicit
                # transport recovery may establish safe non-triggering queries.
                query_safe = False
                if self.recover_after_timeout:
                    try:
                        query_safe = bool(self.recover_after_timeout(self.session))
                        self._transport_synchronized = query_safe
                    except BaseException as recovery: errors.append('Recovery failed: '+str(recovery))
            finally:
                cleanup_errors = self._cleanup(query_safe=query_safe)
                self._state = 'FINISHED' if completed_model and self._output_off_verified else 'FAULT_UNKNOWN'
            if query_safe:
                try:
                    rows = self._rows(p)
                    errors.extend(self._errors())
                except BaseException as exc:
                    errors.append('Partial retrieval: '+type(exc).__name__+': '+str(exc))
            else:
                errors.append('Partial buffer retrieval deferred: transport synchronization unknown; never replay INIT')
            # Postrun sampled energy is diagnostic, NOT live protection or a
            # bound. Single reading integral is UNKNOWN, not zero joules.
            sampled = None
            if len(rows) > 1:
                sampled = sum((a['measured_power_w']+b['measured_power_w'])/2 *
                              (b['Time(T)']-a['Time(T)']) for a,b in zip(rows, rows[1:]))
            result = {'rows':rows, 'plan_id':plan_id, 'plan_digest':p['plan_digest'],
                      'complete':completed_model and len(rows)==len(p['voltages']) and
                                 self._output_off_verified is True and not errors and not cleanup_errors,
                      'boundary':p['boundary'], 'aperture':p['aperture'],
                      'read_metadata':{
                          'integrated_current': True,
                          'duration_s': p['aperture']['effective_native_aperture_s'],
                          'duration_provenance': p['aperture']['provenance'],
                          'elapsed_s': None,
                          'elapsed_provenance': 'actual source-apply to sample-start timestamp not available in SCPI trace',
                          'programmed_delay_s': p['delay_s'],
                          'qualified_duration_s': p['qualification'].get('qualified_duration_s') if p['qualification']['kind']=='physical' else None,
                          'timing_evidence_reference': p['qualification'].get('timing_evidence_reference') if p['qualification']['kind']=='physical' else None},
                      'capabilities':self.get_acquisition_capabilities(),
                      'sampled_energy_j':sampled,
                      'energy_accounting':{'sampled_measured_energy_j':sampled,
                          'full_exposure_energy_upper_bound_j':p['boundary']['reserved_energy_j'],
                          'unobserved_intervals_upper_bound_j':p['boundary']['reserved_energy_j'],
                          'unobserved_intervals':'before first sample, between finite-aperture readings, and after last sample through shutdown',
                          'protection_basis':'full-exposure reservation, never postrun sampled integration'},
                      'prepared_bounds':p['envelope_bounds'],
                      'sampled_energy_coverage':'between sample timestamps only; not full exposure or live cutoff',
                      'errors':errors, 'cleanup_errors':cleanup_errors,
                      'output_off_verified':self._output_off_verified,
                      'raw_responses':copy.deepcopy(self._raw),
                      'device_reserved_j':self._device_reserved_by_id[p['device_id']],
                      'device_id':p['device_id'], 'replay_allowed':False}
            if cancelled is not None:
                cancelled.partial_result = result
                raise cancelled
            return result

    def guarded_source_voltage_measure_current(self, voltages, current_compliance, **kwargs):
        host_timeout = kwargs.pop('host_timeout_s', 30.0)
        plan = self.prepare_guarded_acquisition(voltages, current_compliance, **kwargs)
        return self.execute_guarded_acquisition(plan['plan_id'], host_timeout_s=host_timeout)

    def guarded_hold_voltage_measure_current(self, voltage=0.1, current_compliance=100e-6,
                                            settle_s=0.01, read_count=1, **kwargs):
        if isinstance(read_count, bool) or not isinstance(read_count, int) or not 1 <= read_count <= 2500:
            raise ValueError('read_count must be an integer in 1..2500')
        kwargs.setdefault('category', 'read')
        kwargs.setdefault('operation_limit_j', 1e-5)
        return self.guarded_source_voltage_measure_current([voltage]*read_count,
                          current_compliance, delay_s=settle_s, **kwargs)

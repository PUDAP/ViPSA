"""Pure PyVISA + native SCPI wrapper for the Keithley 2450 SourceMeter."""

from __future__ import annotations

from typing import Any, Sequence
import time
import math

import pyvisa
from puda import command


def _record(
    timestamp: float,
    v_cmd: float | None = None,
    i_cmd: float | None = None,
    v_meas: float | None = None,
    i_meas: float | None = None,
    cycle_number: float | None = None,
) -> dict[str, Any]:
    """Build one normalized measurement record, allowing provenance metadata."""
    v_error = None
    i_error = None

    if v_cmd is not None and v_meas is not None:
        v_error = float(v_meas) - float(v_cmd)

    if i_cmd is not None and i_meas is not None:
        i_error = float(i_meas) - float(i_cmd)

    return {
        "Time(T)": float(timestamp),
        "Voltage (V)": float(v_cmd) if v_cmd is not None else v_meas,
        "Current (A)": float(i_meas) if i_meas is not None else i_cmd,
        "V_cmd (V)": float(v_cmd) if v_cmd is not None else None,
        "I_cmd (A)": float(i_cmd) if i_cmd is not None else None,
        "V_meas (V)": float(v_meas) if v_meas is not None else None,
        "I_meas (A)": float(i_meas) if i_meas is not None else None,
        "V_error (V)": v_error,
        "I_error (A)": i_error,
        "Cycle Number": cycle_number,
    }


class NativeIntegrityError(RuntimeError):
    """Fail-closed native integrity error retaining unmodified diagnostic replies."""

    def __init__(self, message: str, evidence: dict[str, Any]):
        self.evidence = evidence
        super().__init__(message + ': ' + repr(evidence))


class Driver:
    """Keithley 2450 source-measure unit for DC sourcing and IV measurements.

    The class keeps a persistent VISA session and provides thin measurement
    primitives. Higher-level voltage-list splitting lives in
    ``Source_Measure_Unit.py``.
    """

    instrument_family = "keithley_2450"
    supports_native_pulse = False
    supports_dual_channel = False

    def __init__(
        self,
        device_no: int = 0,
        address: str | None = None,
        switch: Any | None = None,
        switch_channel: Any | None = None,
        connect_switch: bool = False,
    ) -> None:
        """Initialize the driver and open the main VISA session."""
        self.rm = pyvisa.ResourceManager()
        address_list = list(self.rm.list_resources())
        self.address = address if address is not None else address_list[device_no]
        self.switch = switch
        self.switch_channel = switch_channel
        self.switch_profile = "keithley"
        self.smu = self._open_resource(self.address, timeout=10000)

        if connect_switch and self.switch is not None:
            self.connect_switch_path()

        self.initialize()

    def _get_guarded_2450(self):
        """Lazily wrap the existing session; no resource opening or initialization."""
        from guarded_2450 import Guarded2450
        if not hasattr(self, '_guarded_2450'):
            import os
            import json
            from pathlib import Path
            from guarded_2450 import CapabilityError
            # Exact case-sensitive opt-in: VIPSA_GUARD_QUALIFICATION_FILE.
            # Resolve relative paths ONCE against the loading process cwd.
            configured = os.environ.get('VIPSA_GUARD_QUALIFICATION_FILE')
            path = Path(configured).resolve() if configured else None
            qualification = None
            if path is not None:
                try:
                    qualification = json.loads(path.read_text())
                    if not isinstance(qualification, dict):
                        raise ValueError('qualification must be an object')
                except (OSError, ValueError) as exc:
                    raise CapabilityError('External qualification unavailable or invalid') from exc
            self._guard_qualification_path = path
            self._guarded_2450 = Guarded2450(self.smu, qualification)
        return self._guarded_2450

    @command
    def get_acquisition_capabilities(self) -> dict[str, Any]:
        """Return conservative acquisition capabilities without instrument I/O."""
        guard = self._get_guarded_2450()
        caps = guard.get_acquisition_capabilities()
        q = guard.qualification or {}
        path = self._guard_qualification_path
        caps['qualification_evidence'] = None  # never serialize external contents
        caps['qualification_configured'] = guard.qualification is not None
        caps['qualification_file_reference'] = str(path) if path else None
        caps['qualification_scope_reference'] = q.get('scope_reference') if isinstance(q.get('scope_reference'), str) else None
        caps['methods'] = ['prepare_guarded_acquisition', 'execute_guarded_acquisition',
                           'get_exposure_guard_state', 'get_acquisition_capabilities',
                           'get_terminals', 'abort_guarded_acquisition',
                           'get_protection_deployment_state']
        return caps

    @command
    def get_exposure_guard_state(self) -> dict[str, Any]:
        """Read guard state and query-only prepared configuration verification."""
        return self._get_guarded_2450().get_exposure_guard_state()

    @command
    def prepare_guarded_acquisition(
        self, voltages: list[float], current_compliance: float | list[float], *,
        delay_s: float = 0.0, nplc: float = 0.1,
        current_range: float | None = None, voltage_range: float | None = None,
        reset: bool = True, deadline_s: float, operation_limit_j: float,
        device_limit_j: float = 5.0, category: str = 'forming',
        branch_ids: list[str | int | None] | None = None,
        device_id: str | None = None, remaining_device_j: float | None = None,
        warning_waiver_scopes: list[str] | tuple[str, ...] = (),
    ) -> dict[str, Any]:
        """Prepare an output-OFF one-shot plan using external qualification only."""
        from guarded_2450 import CapabilityError
        guard = self._get_guarded_2450()
        q = dict(guard.qualification or {})
        envelopes = q.pop('envelopes', None)
        if envelopes is not None:
            phase = 'forming' if category == 'recovery' else category
            if not isinstance(envelopes, dict) or not isinstance(envelopes.get(phase), dict):
                raise CapabilityError('Missing exact category qualification envelope: ' + phase)
            q.update(envelopes[phase])
        if q:
            required = ['voltage_bound_v', 'current_bound_a', 'measurement_max_s',
                        'source_update_max_s', 'shutdown_max_s', 'block_max_s']
            if q.get('kind') == 'physical':
                required += ['nplc_max', 'qualified_duration_s', 'timing_evidence_reference']
            missing = [key for key in required if q.get(key) is None]
            if missing:
                raise CapabilityError('Missing qualification bounds: ' + ', '.join(missing))
        return guard.prepare_guarded_acquisition(
            voltages, current_compliance, delay_s=delay_s, nplc=nplc,
            current_range=current_range, voltage_range=voltage_range,
            reset=reset, deadline_s=deadline_s, operation_limit_j=operation_limit_j,
            device_limit_j=device_limit_j, category=category, branch_ids=branch_ids,
            device_id=device_id, remaining_device_j=remaining_device_j,
            warning_waiver_scopes=warning_waiver_scopes)

    @command
    def execute_guarded_acquisition(self, plan_id: str, *, host_timeout_s: float = 30.0) -> dict[str, Any]:
        """Execute the exact prepared plan once; never retry INIT or infer proof."""
        result = self._get_guarded_2450().execute_guarded_acquisition(plan_id, host_timeout_s=host_timeout_s)
        result['capabilities'] = self.get_acquisition_capabilities()
        return result

    @command
    def get_terminals(self) -> str:
        """Query native SCPI terminals without changing output, language or route."""
        return self._get_guarded_2450().get_terminals()

    @command
    def abort_guarded_acquisition(self) -> dict[str, Any]:
        """Abort guarded acquisition and attempt verified output OFF; no replay."""
        return self._get_guarded_2450().abort_guarded_acquisition()

    @command
    def get_protection_deployment_state(self) -> dict[str, Any]:
        """Read code/config fingerprints; never infer physical qualification.

        Only VIPSA_GUARD_QUALIFICATION_FILE is read, never default-profile
        secrets. Relative paths are resolved at first guard access. File hashes
        describe current disk contents, not a claim of deployed/qualified proof.
        """
        import hashlib
        import re
        import subprocess
        from pathlib import Path
        caps = self.get_acquisition_capabilities()
        directory = Path(__file__).resolve().parent
        revision = None
        try:
            completed = subprocess.run(
                ['git', '-C', str(directory.parent), 'rev-parse', 'HEAD'],
                check=True, capture_output=True, text=True, timeout=2)
            candidate = completed.stdout.strip()
            if re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', candidate):
                revision = candidate
        except (OSError, subprocess.SubprocessError):
            pass

        def digest(path):
            try:
                return hashlib.sha256(path.read_bytes()).hexdigest() if path else None
            except OSError:
                return None

        return {
            'git_commit': revision,
            'scope_qualified': False,
            'physical_qualified': False,
            'code_sha256': {name: digest(directory / name)
                            for name in ('driver.py', 'guarded_2450.py')},
            'configuration_sha256': {'guard_qualification': digest(self._guard_qualification_path)},
            'qualification_configured': caps['qualification_configured'],
            'qualification_file_reference': caps['qualification_file_reference'],
            'qualification_scope_reference': caps['qualification_scope_reference'],
        }

    # Machine-template lifecycle methods

    @command
    def shutdown(self) -> bool:
        """Release the VISA session and disconnect any switch path."""
        self.close_session()
        return True

    @command
    def home(self) -> bool:
        """No homing sequence is defined for this SMU."""
        return True

    @command
    def get_position(self) -> dict[str, float]:
        """Return a fixed position payload for edge telemetry."""
        return {"x": 0.0, "y": 0.0, "z": 0.0}


    # Public driver interface

    @command
    def initialize(self) -> dict[str, bool]:
        """Apply a conservative default state suitable for lab automation."""
        self._write("*RST")
        self._write("*CLS")
        self._write(":ROUT:TERM REAR")
        self._write(":SOUR:FUNC VOLT")
        self._write(':SENS:FUNC "CURR"')
        self._write(":SENS:CURR:RANG:AUTO ON")
        self._write(":OUTP OFF")
        return {"ok": True}

    @command
    def identify(self) -> str:
        """Return the instrument ID string."""
        return self._query("*IDN?")

    @command
    def clear(self) -> dict[str, bool]:
        """Clear the Keithley status and error queues."""
        self._write("*CLS")
        return {"ok": True}

    @command
    def reset(self) -> dict[str, bool]:
        """Reset the Keithley and reapply the ViPSA default setup."""
        self._write("*RST")
        self.clear()
        return self.initialize()

    @command
    def set_source_function(self, function: str) -> None:
        """Select voltage or current source mode."""
        func = self._normalize_function(function)
        self._write(f":SOUR:FUNC {func}")

    @command
    def set_sense_function(self, function: str) -> None:
        """Select the primary sense function (``VOLT`` or ``CURR``)."""
        func = self._normalize_function(function)
        self._write(f':SENS:FUNC "{func}"')

    @command
    def set_source_range(
        self,
        function: str,
        value: float | None = None,
        auto: bool = True,
    ) -> None:
        """Configure the source range or source autorange."""
        func = self._normalize_function(function)
        if auto:
            self._write(f":SOUR:{func}:RANG:AUTO ON")
            return
        if value is None:
            raise ValueError("A source range value is required when auto is False.")
        self._write(f":SOUR:{func}:RANG:AUTO OFF")
        self._write(f":SOUR:{func}:RANG {float(value):.12g}")

    @command
    def set_sense_range(
        self,
        function: str,
        value: float | None = None,
        auto: bool = True,
    ) -> None:
        """Configure the measurement range or measurement autorange."""
        func = self._normalize_function(function)
        if auto:
            self._write(f":SENS:{func}:RANG:AUTO ON")
            return
        if value is None:
            raise ValueError("A sense range value is required when auto is False.")
        self._write(f":SENS:{func}:RANG:AUTO OFF")
        self._write(f":SENS:{func}:RANG {float(value):.12g}")

    @command
    def set_protection(self, function: str, value: float) -> None:
        """Configure current or voltage protection / compliance."""
        func = self._normalize_function(function)
        numeric = float(value)
        if func == "VOLT":
            # Native ILIM replaces Model 2400 SENS:CURR:PROT (manual section 18).
            self._write(f":SOUR:VOLT:ILIM {numeric:.17g}")
            return
        self._write(f":SENS:VOLT:PROT {numeric:.12g}")
        self._write(f":SOUR:CURR:VLIM {numeric:.12g}")

    @command
    def set_source_level(self, function: str, value: float) -> None:
        """Set the immediate source level for voltage or current."""
        func = self._normalize_function(function)
        self._write(f":SOUR:{func}:LEV {float(value):.12g}")

    @command
    def set_output(self, enabled: bool) -> None:
        """Turn the output on or off."""
        self._write(":OUTP ON" if enabled else ":OUTP OFF")

    @command
    def configure_measurement_format(self, functions: str | list[str]) -> None:
        """Configure the response fields for immediate readback.

        The 2450 uses ``:FORM:ELEM`` rather than the Keysight ``:FORM:ELEM:SENS``
        variant. Typical values are ``CURR`` or ``VOLT,CURR``.
        """
        if isinstance(functions, str):
            payload = functions
        else:
            payload = ",".join(str(item).strip().upper() for item in functions)
        self._write(f":FORM:ELEM {payload}")

    @command
    def query_reading(self) -> str:
        """Query one reading from the active source-measure setup."""
        return self._query(":READ?")

    def get_error(self, SMU: Any | None = None) -> list[str]:
        """Return all currently queued Keithley instrument errors."""
        dev = self.smu if SMU is None else SMU
        errors: list[str] = []
        while True:
            msg = dev.query(":SYST:ERR?").strip()
            if msg.startswith("+0") or msg.startswith("0"):
                break
            errors.append(msg)
        return errors
        
    @command
    def get_output(self) -> str:
        "Returns whether the output is on"
        return self._query(":OUTP?")

    @command
    def read_errors(self) -> list[str]:
        """Drain the instrument error queue using the active session."""
        return self.get_error()

    @command
    def connect_switch_path(self) -> None:
        """Connect the assigned switch path if a switch wrapper is available.

        Best effort: force the SMU output off before changing the active route.
        """
        if self.switch is None:
            return
        self._prepare_for_route_change()

        route = self.switch_channel if self.switch_channel is not None else self.switch_profile
        route_name = route.lower() if isinstance(route, str) else None

        if hasattr(self.switch, "connect_named_route") and route_name in {"keithley", "keysight"}:
            self.switch.connect_named_route(route_name)
            return

        if hasattr(self.switch, "open_all"):
            self.switch.open_all()

        if hasattr(self.switch, "close_channel"):
            self.switch.close_channel(route)

    @command
    def disconnect_switch_path(self) -> None:
        """Open the assigned switch path if a switch wrapper is available.

        Best effort: force the SMU output off before changing the active route.
        """
        if self.switch is None:
            return
        self._prepare_for_route_change()

        if hasattr(self.switch, "open_all"):
            self.switch.open_all()
            return

        if self.switch_channel is not None and hasattr(self.switch, "open_channel"):
            self.switch.open_channel(self.switch_channel)

    def close_session(self) -> None:
        """Abort output, disconnect the switch, and close the VISA session."""
        try:
            self.abort_measurement()
        except Exception:
            pass

        try:
            self.disconnect_switch_path()
        except Exception:
            pass

        try:
            if self.smu is not None:
                self.smu.close()
        finally:
            self.smu = None

    def reset_device(self) -> None:
        """Reset and reinitialize the driver."""
        self.initialize()

    @command
    def stop_output(self) -> None:
        """Turn the output off."""
        self.set_output(False)

    @command
    def abort_measurement(self) -> None:
        """Abort any active operation and leave the output off."""
        try:
            self._write(":ABOR")
        except Exception:
            pass
        try:
            self.set_output(False)
        except Exception:
            pass

    @command
    def hold_voltage_measure_current(
        self,
        voltage: float,
        current_compliance: float,
        settle_s: float = 0.0,
        current_range: float | None = None,
        voltage_range: float | None = None,
        nplc: float | None = None,
        read_count: int = 1,
        reset: bool = True,
        adr: str | None = None,
    ) -> list[dict[str, float | None]]:
        """Apply a constant voltage bias and measure current one or more times."""
        smu, temporary = self._get_session(adr=adr, timeout=30000)
        evidence: dict[str, Any] = {'read_count': max(1, int(read_count)), 'raw_reads': []}
        self._last_native_hold_evidence = evidence
        try:
            smu.write(":OUTP OFF")
            if reset:
                smu.write("*RST")
                smu.write("*CLS")
            smu.write(":ROUT:TERM REAR")
            smu.write(":SOUR:FUNC VOLT")
            smu.write(':SENS:FUNC "CURR"')
            smu.write(f":SOUR:VOLT:ILIM {float(current_compliance):.17g}")

            if voltage_range is not None:
                smu.write(":SOUR:VOLT:RANG:AUTO OFF")
                smu.write(f":SOUR:VOLT:RANG {float(voltage_range):.12g}")
            else:
                smu.write(":SOUR:VOLT:RANG:AUTO ON")

            if current_range is not None:
                smu.write(":SENS:CURR:RANG:AUTO OFF")
                smu.write(f":SENS:CURR:RANG {float(current_range):.12g}")
            else:
                smu.write(":SENS:CURR:RANG:AUTO ON")

            if nplc is not None:
                smu.write(f":SENS:CURR:NPLC {float(nplc):.12g}")

            smu.write(":FORM:DATA ASC")
            smu.write(":SOUR:VOLT:READ:BACK ON")
            smu.write(":SENS:COUN 1")
            smu.write(f":SOUR:VOLT:LEV {float(voltage):.12g}")
            evidence['configuration'] = {cmd: smu.query(cmd).strip() for cmd in (
                ':SOUR:FUNC?', ':SENS:FUNC?', ':SOUR:VOLT:READ:BACK?',
                ':SOUR:VOLT:ILIM?', ':SOUR:VOLT:LEV?', ':SENS:COUN?')}
            config = evidence['configuration']
            evidence['pre_enable_error'] = smu.query(':SYST:ERR?').strip()
            if (config[':SOUR:FUNC?'].upper() != 'VOLT'
                    or config[':SENS:FUNC?'].strip('"').upper() not in {'CURR', 'CURR:DC'}
                    or config[':SOUR:VOLT:READ:BACK?'].upper() not in {'1', 'ON'}
                    or float(config[':SENS:COUN?']) != 1
                    or format(float(config[':SOUR:VOLT:ILIM?']), '.6g') != format(float(current_compliance), '.6g')
                    or format(float(config[':SOUR:VOLT:LEV?']), '.6g') != format(float(voltage), '.6g')
                    or int(evidence['pre_enable_error'].split(',', 1)[0]) != 0):
                raise ValueError('Native voltage hold configuration/error mismatch')
            smu.write(":OUTP ON")
            if settle_s > 0:
                time.sleep(settle_s)
            t0 = time.perf_counter()
            records = []
            previous_time = None
            for index in range(max(1, int(read_count))):
                raw = smu.query(':READ? "defbuffer1", SOUR, READ, REL').strip()
                evidence['raw_reads'].append(raw)
                parts = raw.split(',')
                if len(parts) != 3:
                    raise ValueError('Native voltage hold requires measured V/I/REL triple')
                v_meas, i_meas, timestamp = [float(v.strip()) for v in parts]
                if not all(math.isfinite(v) for v in (v_meas, i_meas, timestamp)):
                    raise ValueError('Native voltage hold nonfinite V/I/REL')
                if previous_time is not None and timestamp < previous_time:
                    raise ValueError('Native voltage hold time is not monotonic')
                previous_time = timestamp
                record = _record(timestamp=time.perf_counter() - t0, v_cmd=voltage, v_meas=v_meas,
                    i_meas=i_meas, cycle_number=float(index))
                record['native_buffer_relative_s'] = timestamp
                record['native_integrity'] = evidence
                records.append(record)
            evidence['host_elapsed_s'] = time.perf_counter() - t0
            evidence['time_provenance'] = 'host_perf_counter_after_settle; native_buffer_REL_retained_separately'
            evidence['raw_error'] = smu.query(':SYST:ERR?').strip()
            if int(evidence['raw_error'].split(',', 1)[0]) != 0:
                raise ValueError('Native voltage hold instrument error')
            return records
        except Exception as exc:
            evidence['failure'] = str(exc)
            if 'raw_error' not in evidence:
                try:
                    evidence['raw_error'] = smu.query(':SYST:ERR?').strip()
                except Exception as diagnostic_exc:
                    evidence['diagnostic_failure'] = str(diagnostic_exc)
            raise NativeIntegrityError('Native voltage hold failure', evidence) from exc
        finally:
            try:
                smu.write(':OUTP OFF')
            finally:
                self._close_temp(smu, temporary)

    @command
    def hold_current_measure_voltage(
        self,
        current: float,
        voltage_compliance: float,
        settle_s: float = 0.0,
        current_range: float | None = None,
        voltage_range: float | None = None,
        nplc: float | None = None,
        read_count: int = 1,
        reset: bool = True,
        adr: str | None = None,
    ) -> list[dict[str, float | None]]:
        """Apply a constant current bias and measure voltage one or more times."""
        smu, temporary = self._get_session(adr=adr, timeout=30000)
        try:
            if reset:
                smu.write("*RST")
                smu.write("*CLS")
            smu.write(":ROUT:TERM REAR")
            smu.write(":SOUR:FUNC CURR")
            smu.write(':SENS:FUNC "VOLT"')
            smu.write(f":SENS:VOLT:PROT {float(voltage_compliance):.12g}")
            smu.write(f":SOUR:CURR:VLIM {float(voltage_compliance):.12g}")

            if current_range is not None:
                smu.write(":SOUR:CURR:RANG:AUTO OFF")
                smu.write(f":SOUR:CURR:RANG {float(current_range):.12g}")
            else:
                smu.write(":SOUR:CURR:RANG:AUTO ON")

            if voltage_range is not None:
                smu.write(":SENS:VOLT:RANG:AUTO OFF")
                smu.write(f":SENS:VOLT:RANG {float(voltage_range):.12g}")
            else:
                smu.write(":SENS:VOLT:RANG:AUTO ON")

            if nplc is not None:
                smu.write(f":SENS:VOLT:NPLC {float(nplc):.12g}")

            smu.write(":FORM:ELEM VOLT,CURR")
            smu.write(f":SOUR:CURR:LEV {float(current):.12g}")
            smu.write(":OUTP ON")

            if settle_s > 0:
                time.sleep(settle_s)

            t0 = time.perf_counter()
            records: list[dict[str, float | None]] = []
            for index in range(max(1, int(read_count))):
                v_meas, i_meas = self._read_measurement_pair(smu)
                records.append(
                    _record(
                        timestamp=time.perf_counter() - t0,
                        i_cmd=current,
                        v_meas=v_meas,
                        i_meas=i_meas,
                        cycle_number=float(index),
                    )
                )

            smu.write(":OUTP OFF")
            return records
        finally:
            self._close_temp(smu, temporary)

    @command
    def source_voltage_measure_current(
        self,
        voltages: list[float],
        current_compliance: float,
        delay_s: float = 0.0,
        current_range: float | None = None,
        voltage_range: float | None = None,
        reset: bool = True,
        adr: str | None = None,
        nplc: float | None = None,
        use_auto_current_range: bool = False,
        sweep_range_mode: str = "BEST",
    ) -> list[dict[str, float | None]]:
        """Run a native 2450 voltage-list sweep and read the trace buffer."""
        voltage_values = [float(value) for value in voltages]
        if not voltage_values:
            return []

        delay_value = max(0.0, float(delay_s))
        # Native list timing can exceed commanded dwell substantially on very-high-HRS
        # paths because current autoranging adds per-point overhead. Keep a 300 s
        # margin so long slow sweeps complete before the VISA query timeout.
        timeout_ms = max(600000, int((delay_value * len(voltage_values) + 300.0) * 1000))
        buffer_name = "defbuffer1"
        range_mode = str(sweep_range_mode).strip().upper()
        if range_mode not in {"AUTO", "BEST", "FIXED", "MANUAL"}:
            raise ValueError("sweep_range_mode must be AUTO, BEST, FIXED, or MANUAL.")

        smu, temporary = self._get_session(adr=adr, timeout=timeout_ms)
        try:
            if reset:
                smu.write("*RST")
                smu.write("*CLS")
            else:
                smu.write("*CLS")
            smu.write(":ROUT:TERM REAR")
            smu.write(":SOUR:FUNC VOLT")
            smu.write(":SOUR:VOLT:READ:BACK ON")
            smu.write(':SENS:FUNC "CURR"')
            smu.write(f":SOUR:VOLT:ILIM {float(current_compliance):.17g}")

            if voltage_range is not None:
                smu.write(":SOUR:VOLT:RANG:AUTO OFF")
                smu.write(f":SOUR:VOLT:RANG {float(voltage_range):.12g}")
            else:
                smu.write(":SOUR:VOLT:RANG:AUTO ON")

            if use_auto_current_range or range_mode == "AUTO":
                smu.write(":SENS:CURR:RANG:AUTO ON")
            elif current_range is not None:
                smu.write(":SENS:CURR:RANG:AUTO OFF")
                smu.write(f":SENS:CURR:RANG {float(current_range):.12g}")
            else:
                fixed_range = abs(float(current_compliance))
                if fixed_range <= 0:
                    raise ValueError("current_compliance must be non-zero for fixed range.")
                smu.write(":SENS:CURR:RANG:AUTO OFF")
                smu.write(f":SENS:CURR:RANG {fixed_range:.12g}")

            if nplc is not None:
                smu.write(f":SENS:CURR:NPLC {float(nplc):.12g}")

            smu.write(f':TRAC:CLE "{buffer_name}"')
            # The 2450 enforces a minimum trace-buffer capacity of 10 even
            # when a valid native source list contains fewer points. Buffer
            # capacity is independent of the requested/returned point count.
            smu.write(f':TRAC:POIN {max(10, len(voltage_values))}, "{buffer_name}"')
            smu.write(":FORM:DATA ASC")
            list_proof = self._verify_native_voltage_list_output_off(smu, voltage_values, expected_ilimit=current_compliance)
            smu.write(
                f':SOUR:SWE:VOLT:LIST 1, {delay_value:.12g}, 1, OFF, "{buffer_name}"'
            )
            smu.write(":OUTP ON")
            smu.write(":INIT")
            smu.query("*OPC?").strip()
            smu.write(":OUTP OFF")
            return self._read_trace_records(
                smu=smu,
                voltages=voltage_values,
                delay_s=delay_value,
                buffer_name=buffer_name,
            )
        finally:
            try:
                smu.write(":OUTP OFF")
            except Exception:
                pass
            self._close_temp(smu, temporary)

    @command
    def source_current_measure_voltage(
        self,
        currents: list[float],
        voltage_compliance: float,
        delay_s: float = 0.0,
        current_range: float | None = None,
        voltage_range: float | None = None,
        reset: bool = True,
        adr: str | None = None,
        nplc: float | None = None,
    ) -> list[dict[str, float | None]]:
        """Step through a current list and measure voltage at each point."""
        smu, temporary = self._get_session(adr=adr, timeout=120000)
        try:
            if reset:
                smu.write("*RST")
                smu.write("*CLS")
            smu.write(":ROUT:TERM REAR")
            smu.write(":SOUR:FUNC CURR")
            smu.write(':SENS:FUNC "VOLT"')
            smu.write(f":SENS:VOLT:PROT {float(voltage_compliance):.12g}")
            smu.write(f":SOUR:CURR:VLIM {float(voltage_compliance):.12g}")

            if current_range is not None:
                smu.write(":SOUR:CURR:RANG:AUTO OFF")
                smu.write(f":SOUR:CURR:RANG {float(current_range):.12g}")
            else:
                smu.write(":SOUR:CURR:RANG:AUTO ON")

            if voltage_range is not None:
                smu.write(":SENS:VOLT:RANG:AUTO OFF")
                smu.write(f":SENS:VOLT:RANG {float(voltage_range):.12g}")
            else:
                smu.write(":SENS:VOLT:RANG:AUTO ON")

            if nplc is not None:
                smu.write(f":SENS:VOLT:NPLC {float(nplc):.12g}")

            smu.write(":FORM:ELEM VOLT,CURR")
            smu.write(":OUTP ON")

            t0 = time.perf_counter()
            records: list[dict[str, float | None]] = []
            for index, current in enumerate(float(i) for i in currents):
                smu.write(f":SOUR:CURR:LEV {current:.12g}")
                if delay_s > 0:
                    time.sleep(delay_s)
                v_meas, i_meas = self._read_measurement_pair(smu)
                records.append(
                    _record(
                        timestamp=time.perf_counter() - t0,
                        i_cmd=current,
                        v_meas=v_meas,
                        i_meas=i_meas,
                        cycle_number=float(index),
                    )
                )

            smu.write(":OUTP OFF")
            return records
        finally:
            self._close_temp(smu, temporary)

    @command
    def run_voltage_pulse_train(
        self,
        voltages: list[float],
        current_compliance: float,
        pulse_width_s: float,
        acquire_delay_s: float | None = None,
        current_range: float | None = None,
        reset: bool = True,
        adr: str | None = None,
        current_autorange: bool = False,
    ) -> list[dict[str, float | None]]:
        """Approximate a pulse train using the 2450 native list-sweep model.

        The 2450 does not expose a dedicated fast pulse mode like the Keysight
        B2900 series. This method therefore constructs a source list and executes
        it with the internal list-sweep engine and reading buffer.
        """
        _ = acquire_delay_s
        return self.source_voltage_measure_current(
            voltages=voltages,
            current_compliance=current_compliance,
            delay_s=pulse_width_s,
            current_range=current_range,
            reset=reset,
            adr=adr,
            use_auto_current_range=current_autorange,
        )

    # Internal utility methods

    def _open_resource(self, adr: str | None = None, timeout: int = 10000) -> Any:
        """Open a VISA resource and apply common session settings."""
        target = self.address if adr is None else adr
        smu = self.rm.open_resource(target)
        smu.read_termination = "\n"
        smu.write_termination = "\n"
        smu.timeout = timeout
        return smu

    def _get_session(self, adr: str | None = None, timeout: int = 10000) -> tuple[Any, bool]:
        """Return the main session or open a short-lived one for another address."""
        target = self.address if adr is None else adr
        if target == self.address:
            self.smu.timeout = timeout
            return self.smu, False
        return self._open_resource(target, timeout=timeout), True

    def _close_temp(self, smu, temporary: bool) -> None:
        """Close a temporary VISA session."""
        if temporary and smu is not None:
            smu.close()

    def _normalize_function(self, function: str) -> str:
        """Normalize function tokens such as ``VOLT`` and ``CURR``."""
        text = str(function).strip().upper()
        if text.startswith("V"):
            return "VOLT"
        if text.startswith("I") or text.startswith("C"):
            return "CURR"
        raise ValueError(f"Unsupported function '{function}'.")

    def _read_measurement_pair(self, smu) -> tuple[float | None, float | None]:
        """Read one voltage/current pair using the active configuration."""
        response = smu.query(":READ?").strip()
        parts = [part.strip() for part in response.split(",") if part.strip()]
        if len(parts) >= 2:
            return float(parts[0]), float(parts[1])
        if len(parts) == 1:
            return None, float(parts[0])
        return None, None

    @command
    def verify_native_voltage_list_output_off(self, voltages: list[float],
                                             voltage_range: float | None = None,
                                             current_compliance: float | None = None,
                                             current_range: float | None = None) -> dict[str, Any]:
        """OFF-only proof with the same VOLT/AUTO/compliance/measure-range setup as a native sweep."""
        smu = self.smu
        if smu is None:
            raise RuntimeError('SMU session unavailable')
        if smu.query(':OUTP?').strip().upper() not in {'0', 'OFF'}:
            smu.write(':OUTP OFF')
            raise NativeIntegrityError('Verifier requires output OFF', {'verified': False})
        if voltage_range is not None and (not math.isfinite(float(voltage_range)) or float(voltage_range) <= 0):
            raise ValueError('voltage_range must be finite and positive')
        if current_range is not None and (not math.isfinite(float(current_range)) or float(current_range) <= 0):
            raise ValueError('current_range must be finite and positive')
        smu.write(':SOUR:FUNC VOLT')
        smu.write(':SOUR:VOLT:READ:BACK ON')
        smu.write(':SOUR:VOLT:RANG:AUTO ' + ('ON' if voltage_range is None else 'OFF'))
        if voltage_range is not None:
            smu.write(f':SOUR:VOLT:RANG {float(voltage_range):.12g}')
        if current_range is not None:
            smu.write(':SENS:CURR:RANG:AUTO OFF')
            smu.write(f':SENS:CURR:RANG {float(current_range):.12g}')
        if current_compliance is not None:
            if not math.isfinite(float(current_compliance)) or float(current_compliance) <= 0:
                raise ValueError('current_compliance must be finite and positive')
            smu.write(f':SOUR:VOLT:ILIM {float(current_compliance):.17g}')
        return self._verify_native_voltage_list_output_off(smu, voltages, expected_ilimit=current_compliance)

    def _native_source_snapshot(self, smu):
        return {key: smu.query(cmd).strip() for key, cmd in (
            ('function', ':SOUR:FUNC?'), ('range', ':SOUR:VOLT:RANG?'),
            ('auto', ':SOUR:VOLT:RANG:AUTO?'), ('level', ':SOUR:VOLT:LEV?'),
            ('ilimit', ':SOUR:VOLT:ILIM?'), ('readback', ':SOUR:VOLT:READ:BACK?'))}

    def _parse_native_source_config(self, raw):
        """Parse assignments, never execute returned TSP; AUTO range may be 'not used'."""
        import re
        from decimal import Decimal
        fields = {}
        for part in raw.split(';'):
            m = re.fullmatch(r'\s*smu\.source\.([a-z.]+)\s*=\s*(.*?)\s*', part)
            if m:
                if m[1] in fields:
                    raise ValueError('Duplicate stored source setting')
                fields[m[1]] = m[2]
        if fields.get('func') != 'smu.FUNC_DC_VOLTAGE':
            raise ValueError('Stored source function is not voltage')
        for key in ('level', 'ilimit.level'):
            value = Decimal(fields[key])
            if not value.is_finite():
                raise ValueError('Nonfinite stored source configuration')
        if fields.get('autorange') not in {'smu.ON', 'smu.OFF'}:
            raise ValueError('Missing/unknown stored source autorange')
        return fields

    def _prove_native_source_indices(self, smu, values, actual, proof, expected_ilimit=None):
        from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
        import json
        # Manufacturer 2450 datasheet p8, SOURCE resolution, not accuracy tolerance.
        grids = {Decimal('0.02'): Decimal('0.0000005'), Decimal('0.2'): Decimal('0.000005'),
                 Decimal('2'): Decimal('0.00005'), Decimal('20'): Decimal('0.0005'),
                 Decimal('200'): Decimal('0.005')}
        def six(value):
            value = Decimal(value)
            if value == 0:
                return Decimal(0)
            quantum = Decimal(1).scaleb(value.copy_abs().adjusted() - 5)
            return value.quantize(quantum, rounding=ROUND_HALF_UP)
        def config_encodings(value):
            # Captured TSP settings can expose binary32 storage before seven-digit ASCII.
            # This is a discrete encoding check, never a widened voltage tolerance.
            import struct
            binary32 = struct.unpack('!f', struct.pack('!f', float(value)))[0]
            return {Decimal(format(float(value), '.7g')), Decimal(format(binary32, '.7g'))}

        before = proof['source_config_before']
        proof['stored_configs'] = []
        try:
            for index, (requested, returned) in enumerate(zip(values, actual), 1):
                if smu.query(':OUTP?').strip().upper() not in {'0', 'OFF'}:
                    raise ValueError('Output not OFF before configuration recall')
                raw = smu.query(f':SOUR:CONF:LIST:QUER? "VoltCustomSweepList",{index},SEM').strip()
                row = {'index': index, 'raw_config': raw}
                proof['stored_configs'].append(row)
                fields = self._parse_native_source_config(raw)
                smu.write(f':SOUR:CONF:LIST:REC "VoltCustomSweepList",{index}')
                row['range_V'] = smu.query(':SOUR:VOLT:RANG?').strip()
                row['recalled_level_V'] = smu.query(':SOUR:VOLT:LEV?').strip()
                r, level = Decimal(row['range_V']), Decimal(fields['level'])
                recalled = Decimal(row['recalled_level_V'])
                if not r.is_finite() or r not in grids or not recalled.is_finite():
                    raise ValueError('Unknown/nonfinite recalled range or level')
                if fields['autorange'] != ('smu.ON' if before['auto'] in {'1', 'ON'} else 'smu.OFF'):
                    raise ValueError('Stored AUTO differs from sweep setup')
                if expected_ilimit is None:
                    if six(Decimal(fields['ilimit.level'])) != six(Decimal(before['ilimit'])):
                        raise ValueError('Stored source compliance changed')
                    row['compliance_representation'] = 'queried_six_significant'
                else:
                    requested_ilimit = Decimal(format(float(expected_ilimit), '.17g'))
                    if (six(Decimal(before['ilimit'])) != six(requested_ilimit)
                            or Decimal(fields['ilimit.level']) not in config_encodings(requested_ilimit)):
                        raise ValueError('Stored source compliance changed')
                    row['compliance_representation'] = 'requested_or_binary32_seven_significant'
                if before['auto'] in {'0', 'OFF'} and r != Decimal(before['range']):
                    raise ValueError('Stored fixed range differs from sweep setup')
                if 'range' in fields and Decimal(fields['range']) != r:
                    raise ValueError('Stored range differs from recalled range')
                if six(recalled) != Decimal(str(returned)):
                    raise ValueError('Stored/recalled level does not corroborate list readback')
                request = Decimal(format(requested, '.17g'))
                # List readback/recalled level agreement was checked above at
                # the instrument's query precision. Independently require the
                # stored seven-significant TSP level (or binary32 encoding) to
                # match this exact requested index. The 2450's six-digit query
                # rendering is not a single host-reproducible tie rule.
                if level in config_encodings(request):
                    model = request
                    row['representation'] = 'stored_seven_with_matching_recalled_readback'
                else:
                    quantum = grids[r]
                    quotient = request / quantum
                    lower = quotient.to_integral_value(rounding=ROUND_FLOOR)
                    fraction = quotient - lower
                    if fraction == Decimal('0.5'):
                        raise ValueError('Ambiguous nearest source-grid tie')
                    nearest = (lower + (1 if fraction > Decimal('0.5') else 0)) * quantum
                    if six(nearest) != Decimal(str(returned)):
                        raise ValueError('Same-index documented source-grid mismatch')
                    row['representation'] = 'nearest_source_grid'
                    row['resolution_V'] = str(quantum)
                    model = nearest
                # TSP settings render seven significant digits; never double-round 7 -> 6.
                if level not in config_encodings(model):
                    raise ValueError('Stored seven-significant level does not corroborate representation')
        finally:
            # No output enable: restore final zero list configuration when present.
            if values[-1] == 0:
                smu.write(f':SOUR:CONF:LIST:REC "VoltCustomSweepList",{len(values)}')
            else:
                smu.write(':SOUR:VOLT:LEV ' + before['level'])
            proof['source_config_after'] = self._native_source_snapshot(smu)
            after = proof['source_config_after']
            if any(before[k] != after[k] for k in ('function', 'auto', 'ilimit', 'readback')):
                raise ValueError('Source configuration not preserved after recall proof')
            if Decimal(after['level']) != (Decimal(0) if values[-1] == 0 else Decimal(before['level'])):
                raise ValueError('Source level restoration failed')
        if len(json.dumps(proof).encode()) > 700000:
            raise ValueError('Native proof exceeds bounded metadata budget')

    def _verify_native_voltage_list_output_off(self, smu, voltages: Sequence[float], expected_ilimit=None) -> dict[str, Any]:
        import hashlib
        from pathlib import Path
        proof: dict[str, Any] = {'verified': False, 'readback_significant_digits': 6,
            'deployment': {'driver_path': str(Path(__file__).resolve()),
                           'driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'integrity_revision': 'native-list-stored-range-proof-v2',
                           'physical_qualified': False}}
        self._last_native_list_evidence = proof
        original_timeout = getattr(smu, 'timeout', None)
        if original_timeout is not None:
            smu.timeout = max(original_timeout, 90000)
        try:
            proof['output_before'] = smu.query(':OUTP?').strip()
            if proof['output_before'].upper() not in {'0', 'OFF'}:
                raise ValueError('Native voltage list verification requires output OFF')
            values = [float(v) for v in voltages]
            proof['expected_count'] = len(values)
            if not values or len(values) > 2500 or not all(math.isfinite(v) and abs(v) <= 210 for v in values):
                raise ValueError('Native voltage list requires 1..2500 finite values')
            proof['source_config_before'] = self._native_source_snapshot(smu)
            if proof['source_config_before']['function'].strip('"').upper() != 'VOLT':
                raise ValueError('Source function must be VOLT')
            if proof['source_config_before']['auto'].upper() not in {'0', '1', 'OFF', 'ON'}:
                raise ValueError('Unknown source AUTO state')
            if proof['source_config_before']['readback'].upper() not in {'1', 'ON'}:
                raise ValueError('Native sweep requires source readback ON')
            self._write_voltage_source_list(smu, values)
            proof['uploads'] = self._last_native_list_evidence['uploads']
            self._last_native_list_evidence = proof
            proof['raw_count'] = smu.query(':SOUR:LIST:VOLT:POIN?').strip()
            proof['raw_readback'] = smu.query(':SOUR:LIST:VOLT?').strip()
            proof['raw_error'] = smu.query(':SYST:ERR?').strip()
            count = float(proof['raw_count'])
            actual = [float(v.strip()) for v in proof['raw_readback'].split(',')]
            # Returned values are proved against recalled same-index configuration.
            if (count != len(values) or len(actual) != len(values)
                    or not all(math.isfinite(v) for v in actual)
                    or int(proof['raw_error'].split(',', 1)[0]) != 0):
                raise ValueError('Native voltage list count/ordered six-significant readback mismatch')
            self._prove_native_source_indices(smu, values, actual, proof, expected_ilimit=expected_ilimit)
            proof['raw_config_error'] = smu.query(':SYST:ERR?').strip()
            if int(proof['raw_config_error'].split(',', 1)[0]) != 0:
                raise ValueError('Native configuration recall/query error')
            proof['actual_count'] = int(count)
            proof['verified'] = True
        except Exception as exc:
            proof['failure'] = str(exc)
            if isinstance(exc, NativeIntegrityError):
                proof['upload_failure'] = exc.evidence
            raise NativeIntegrityError('Native voltage list verification failed', proof) from exc
        finally:
            if original_timeout is not None:
                smu.timeout = original_timeout
            self._last_native_list_evidence = proof
            try:
                smu.write(':OUTP OFF')
                proof['output_after'] = smu.query(':OUTP?').strip()
                if proof['output_after'].upper() not in {'0', 'OFF'}:
                    raise ValueError('Output OFF readback mismatch')
            except Exception as exc:
                proof['cleanup_failure'] = str(exc)
                proof['verified'] = False
                raise NativeIntegrityError('Native voltage list OFF cleanup failed', proof) from exc
        return proof

    def _write_voltage_source_list(self, smu, voltages: Sequence[float]) -> None:
        """Write a 2450 voltage source list, chunking around SCPI list limits."""
        if len(voltages) > 2500:
            raise ValueError("The Keithley 2450 source-list limit is 2500 points.")

        tokens = [format(float(value), '.17g') for value in voltages]
        termination = getattr(smu, 'write_termination', None) or '\n'
        start = 0
        evidence = {'expected_count': len(tokens), 'uploads': []}
        self._last_native_list_evidence = evidence
        while start < len(tokens):
            header = ':SOUR:LIST:VOLT' if start == 0 else ':SOUR:LIST:VOLT:APP'
            chunk = []
            for token in tokens[start:start + 100]:
                candidate = header + ' ' + ','.join(chunk + [token])
                if len((candidate + termination).encode('ascii')) > 256:
                    break
                chunk.append(token)
            if not chunk:
                raise RuntimeError('Native voltage list token exceeds byte bound')
            text = header + ' ' + ','.join(chunk)
            smu.write(text)
            start += len(chunk)
            raw_count = smu.query(':SOUR:LIST:VOLT:POIN?').strip()
            raw_error = smu.query(':SYST:ERR?').strip()
            evidence['uploads'].append({'command': text, 'bytes_with_termination':
                len((text + termination).encode('ascii')), 'expected_count': start,
                'raw_count': raw_count, 'raw_error': raw_error})
            try:
                valid = float(raw_count) == start and int(raw_error.split(',', 1)[0]) == 0
            except (ValueError, OverflowError):
                valid = False
            if not valid:
                raise NativeIntegrityError('Native voltage list upload count/error mismatch', evidence)

    def _read_trace_records(
        self,
        smu,
        voltages: Sequence[float],
        delay_s: float,
        buffer_name: str = "defbuffer1",
    ) -> list[dict[str, float | None]]:
        """Require exact native count and finite ordered V/I/REL triples; no synthesis."""
        evidence: dict[str, Any] = {'expected_count': len(voltages),
            'list_proof': getattr(self, '_last_native_list_evidence', None)}
        self._last_native_trace_evidence = evidence
        try:
            evidence['raw_count'] = smu.query(f':TRAC:ACT? "{buffer_name}"').strip()
            count = float(evidence['raw_count'])
            if not math.isfinite(count) or count != len(voltages) or count <= 0:
                raise ValueError('Native trace count differs from expected list count')
            point_count = int(count)
            # One giant USB/native reply was truncated despite ACT=553 and
            # interrupted the query (-410). Read contiguous bounded windows,
            # never retry a failed/truncated query or infer missing samples.
            evidence['trace_window_record_limit'] = 100
            evidence['trace_windows'] = []
            evidence['raw_trace'] = ''
            values = []
            raw_windows = []
            for start in range(1, point_count + 1, 100):
                end = min(point_count, start + 99)
                command = f':TRAC:DATA? {start}, {end}, "{buffer_name}", SOUR, READ, REL'
                window = {'start': start, 'end': end, 'command': command}
                evidence['trace_windows'].append(window)
                try:
                    window['raw_trace'] = smu.query(command).strip()
                except Exception as query_exc:
                    window['query_failure'] = str(query_exc)
                    raise
                raw_windows.append(window['raw_trace'])
                evidence['raw_trace'] = ','.join(raw_windows)
                parts = window['raw_trace'].split(',')
                if len(parts) != 3 * (end - start + 1) or any(not part.strip() for part in parts):
                    raise ValueError('Native trace window requires exactly expected V/I/time triples')
                chunk = [float(part.strip()) for part in parts]
                if not all(math.isfinite(v) for v in chunk):
                    raise ValueError('Native trace window has nonfinite V/I/time')
                # Validate inside each window AND across the window boundary.
                times = ([values[-1]] if values else []) + chunk[2::3]
                if any(t < 0 for t in times) or any(b <= a for a, b in zip(times, times[1:])):
                    raise ValueError('Native trace relative timestamps are not strictly monotonic')
                values.extend(chunk)
                window['validated_records'] = end - start + 1
            if len(values) != 3 * point_count:
                raise ValueError('Native trace requires exactly expected complete V/I/time triples')
            evidence['raw_error'] = smu.query(':SYST:ERR?').strip()
            if int(evidence['raw_error'].split(',', 1)[0]) != 0:
                raise ValueError('Native trace instrument error')
            evidence['actual_count'] = point_count
            evidence['time_provenance'] = 'native_buffer_REL'
            records = []
            for index in range(point_count):
                v_meas, i_meas, timestamp = values[3 * index:3 * index + 3]
                record = _record(timestamp=timestamp, v_cmd=voltages[index],
                    v_meas=v_meas, i_meas=i_meas, cycle_number=float(index))
                record['native_integrity'] = evidence if index == 0 else {'evidence_row_index': 0}
                records.append(record)
            return records
        except Exception as exc:
            evidence['failure'] = str(exc)
            if 'raw_error' not in evidence:
                try:
                    evidence['raw_error'] = smu.query(':SYST:ERR?').strip()
                except Exception as diagnostic_exc:
                    evidence['diagnostic_failure'] = str(diagnostic_exc)
            raise NativeIntegrityError('Native trace integrity failure', evidence) from exc

    def _write(self, command: str, adr: str | None = None) -> None:
        """Send one SCPI command."""
        smu, temporary = self._get_session(adr=adr, timeout=10000)
        try:
            smu.write(command)
        finally:
            self._close_temp(smu, temporary)

    def _query(self, command: str, adr: str | None = None) -> str:
        """Send one SCPI query and return its stripped response."""
        smu, temporary = self._get_session(adr=adr, timeout=10000)
        try:
            return smu.query(command).strip()
        finally:
            self._close_temp(smu, temporary)

    def _connect(
        self,
        address: str | None = None,
        device_no: int = 0,
    ) -> "Driver":
        """Open or reopen the persistent Keithley VISA session."""
        if address is not None:
            self.address = address
        elif self.smu is None:
            addresses = list(self.rm.list_resources())
            self.address = addresses[device_no]

        if self.smu is None:
            self.smu = self._open_resource(self.address, timeout=10000)
        return self

    def _prepare_for_route_change(self) -> None:
        """Best-effort safety step before switch-routing changes."""
        try:
            self.abort_measurement()
            return
        except Exception:
            pass
        try:
            self.stop_output()
        except Exception:
            pass

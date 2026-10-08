"""Pure PyVISA + native SCPI wrapper for the Keithley 2450 SourceMeter."""

from __future__ import annotations

from typing import Any, Sequence
import time

import pyvisa
from puda import command


def _record(
    timestamp: float,
    v_cmd: float | None = None,
    i_cmd: float | None = None,
    v_meas: float | None = None,
    i_meas: float | None = None,
    cycle_number: float | None = None,
) -> dict[str, float | None]:
    """Build one normalized measurement record."""
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
            self._write(f":SENS:CURR:PROT {numeric:.12g}")
            self._write(f":SOUR:VOLT:ILIM {numeric:.12g}")
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
        try:
            if reset:
                smu.write("*RST")
                smu.write("*CLS")
            smu.write(":ROUT:TERM REAR")
            smu.write(":SOUR:FUNC VOLT")
            smu.write(':SENS:FUNC "CURR"')
            smu.write(f":SENS:CURR:PROT {float(current_compliance):.12g}")
            smu.write(f":SOUR:VOLT:ILIM {float(current_compliance):.12g}")

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

            smu.write(":FORM:ELEM VOLT,CURR")
            smu.write(f":SOUR:VOLT:LEV {float(voltage):.12g}")
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
                        v_cmd=voltage,
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
            smu.write(f":SENS:CURR:PROT {float(current_compliance):.12g}")
            smu.write(f":SOUR:VOLT:ILIM {float(current_compliance):.12g}")

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
            smu.write(f':TRAC:POIN {len(voltage_values)}, "{buffer_name}"')
            smu.write(":FORM:DATA ASC")
            self._write_voltage_source_list(smu, voltage_values)
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

    def _write_voltage_source_list(self, smu, voltages: Sequence[float]) -> None:
        """Write a 2450 voltage source list, chunking around SCPI list limits."""
        if len(voltages) > 2500:
            raise ValueError("The Keithley 2450 source-list limit is 2500 points.")

        # Keep each SCPI command comfortably below the 2450 parser/input-buffer
        # limit. Negative values add one character each; 100-point chunks can
        # silently reject the initial list command while a shorter :APP command
        # succeeds, causing only the tail of a sweep to execute.
        chunk_size = 50
        for start in range(0, len(voltages), chunk_size):
            chunk = voltages[start:start + chunk_size]
            payload = ",".join(f"{float(value):.12g}" for value in chunk)
            command = ":SOUR:LIST:VOLT" if start == 0 else ":SOUR:LIST:VOLT:APP"
            smu.write(f"{command} {payload}")

    def _read_trace_records(
        self,
        smu,
        voltages: Sequence[float],
        delay_s: float,
        buffer_name: str = "defbuffer1",
    ) -> list[dict[str, float | None]]:
        """Read source/current/time triples from a 2450 trace buffer."""
        try:
            raw_count = smu.query(f':TRAC:ACT? "{buffer_name}"').strip()
            point_count = int(float(raw_count))
        except Exception:
            point_count = len(voltages)

        point_count = max(0, min(point_count, len(voltages)))
        if point_count <= 0:
            point_count = len(voltages)

        raw = smu.query(
            f':TRAC:DATA? 1, {point_count}, "{buffer_name}", SOUR, READ, REL'
        ).strip()
        values = [part.strip() for part in raw.split(",") if part.strip()]
        records: list[dict[str, float | None]] = []

        for index in range(0, len(values), 3):
            group = values[index:index + 3]
            if len(group) < 3:
                continue
            try:
                v_meas = float(group[0])
                i_meas = float(group[1])
                timestamp = float(group[2])
            except ValueError:
                continue
            voltage_index = len(records)
            v_cmd = voltages[voltage_index] if voltage_index < len(voltages) else v_meas
            records.append(
                _record(
                    timestamp=timestamp,
                    v_cmd=v_cmd,
                    v_meas=v_meas,
                    i_meas=i_meas,
                    cycle_number=float(voltage_index),
                )
            )

        if records:
            return records

        return [
            _record(
                timestamp=float(index) * delay_s,
                v_cmd=float(voltage),
                i_meas=None,
                cycle_number=float(index),
            )
            for index, voltage in enumerate(voltages)
        ]

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

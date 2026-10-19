# Keithley 707B USB disconnect / stale PyVISA session recovery (2026-07-31)

## Trigger

A ViPSA low-bias resistance check failed when `keithley-707b.connect_keithley_smu()` attempted to route the DUT to the Keithley SMU.

The 707B edge was alive and received PUDA commands, but the underlying VISA/USB session had gone stale/disconnected.

## Observed traceback

PUDA command path:

```text
connect_keithley_smu()
→ connect_named_route("keithley")
→ open_all()
→ _send_switch_command('channel.open("allslots")')
→ self._open_device().write(command)
```

Relevant driver lines in `/home/amdm/workspace/ViPSA/keithley-707b/driver.py`:

```python
def open_all(self) -> None:
    """Open all channels in all slots."""
    self._send_switch_command('channel.open("allslots")')


def connect_named_route(self, route_name: str, slot: int | None = None) -> list[str]:
    channels = self._get_route_channels(route_name, slot=slot)
    self.open_all()
    self.close_channel(channels)
    return channels


def connect_keithley_smu(self, slot: int | None = None) -> list[str]:
    return self.connect_named_route("keithley", slot=slot)


def _send_switch_command(self, command: str) -> None:
    try:
        self._open_device().write(command)
    except pyvisa.errors.VisaIOError:
        self._close_device()
        self._open_device().write(command)
```

Underlying error:

```text
usb.core.USBError: [Errno 19] No such device (it may have been disconnected)
ValueError: [Errno 19] No such device (it may have been disconnected)
```

The retry did **not** execute because pyvisa-py surfaced the USB error as `ValueError`, not `pyvisa.errors.VisaIOError`.

## Diagnosis

- `keithley-2450` was not the blocker; it successfully ran `set_output(enabled=false)` and returned idle/null.
- `keithley-707b` accepted START but failed on the first hardware write.
- Final 707B state may become `error` with non-null `run_id` after the failed cleanup attempt.
- This is a 707B USB/VISA/session problem, not an electrical measurement result.

## Recovery checklist

1. Do **not** rerun the electrical measurement until 707B route control is recovered.
2. Try to clear PUDA state:
   ```bash
   NATS='nats://bears:4222,nats://bears:4223,nats://bears:4224'
   puda --nats-servers "$NATS" machine reset keithley-707b || true
   timeout 8 puda --nats-servers "$NATS" machine state keithley-707b
   ```
3. Restart only the 707B edge so the driver constructs a fresh VISA session.
   - Do not kill only the parent login-shell wrapper: `uv run main.py` may survive as a child and remain subscribed, creating duplicate-edge START/run-state failures.
   - Identify every candidate by `/proc/<pid>/cwd == /home/amdm/workspace/ViPSA/keithley-707b`, then stop both wrapper and child processes. Confirm no 707B edge remains before starting exactly one replacement.
   - If startup fails while PyVISA enumerates resources with `OSError: [Errno 24] Too many open files`, relaunch the one edge with a larger per-process descriptor limit, for example `ulimit -n 4096; exec uv run main.py`. This is a restart technique, not evidence that the instrument is absent.
   - Check the replacement edge log/process output for successful NATS queue and immediate subscriptions before issuing commands.
4. Verify with a harmless route-state command before any DUT routing/stress:
   ```bash
   RUN_ID=$(python3 - <<'PY'
   import uuid
   print(uuid.uuid4())
   PY
   )
   puda --nats-servers "$NATS" machine start keithley-707b --run-id "$RUN_ID"
   puda --nats-servers "$NATS" machine run keithley-707b get_closed_channels '{}' --run-id "$RUN_ID"
   puda --nats-servers "$NATS" machine complete keithley-707b --run-id "$RUN_ID"
   ```
   Expected safe result: `nil`. If this lifecycle probe says `Send START command to start a run before sending commands`, re-check for a surviving duplicate edge before retrying; do not treat it as a switch-state result.
5. If the 707B still raises `[Errno 19]`, check VISA visibility from the ViPSA venv:
   ```bash
   cd /home/amdm/workspace/ViPSA
   .venv/bin/python - <<'PY'
   import pyvisa
   rm = pyvisa.ResourceManager('@py')
   print(rm.list_resources())
   PY
   ```
   Expected resource: `USB0::1510::28795::04015087::0::INSTR`.
6. If the VISA resource is absent or still fails after edge restart, physical recovery is required: replug/power-cycle the 707B USB/instrument, restart the 707B edge, then verify `get_closed_channels == nil` before rerunning measurement.

## Durable driver patch idea

Improve `_send_switch_command()` and query helpers to close/reopen the VISA session on pyvisa-py USB/session failures, not only `VisaIOError`:

```python
def _send_switch_command(self, command: str) -> None:
    try:
        self._open_device().write(command)
    except (pyvisa.errors.VisaIOError, ValueError, OSError):
        self._close_device()
        self._open_device().write(command)
```

This helps stale-session cases but cannot fix a physically absent USB device; if the OS no longer sees the instrument, the retry still fails until the USB/instrument is restored.

## Reporting standard

Keep the report concise: “707B edge is alive but VISA/USB write failed in `_send_switch_command()`; Keithley 2450 cleanup succeeded; route state is unverified until 707B is recovered and `get_closed_channels` returns `nil`.”

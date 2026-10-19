# Stage edge vs direct driver motion debug (2026-07-29)

## Trigger

Use this when ViPSA `stage.move_z_by` through PUDA/edge reports success but the user visually observes no physical stage motion, especially after raw serial G-code or a direct Python `Stage` call moves the stage correctly.

## Durable findings

- Do **not** conclude that PUDA stage success or `get_current_position()` proves physical motion. The current stage driver can track position internally.
- PUDA must not write G-code directly. The intended path is:

```text
puda machine run stage move_z_by {...}
→ stage edge EdgeRunner
→ driver.Stage.move_z_by(...)
→ Stage class writes GRBL/G-code to /dev/openflexture
```

- If raw serial such as `G91 G0 Z50` moves the stage, and direct Python importing `Stage` from `stage/driver.py` also moves the stage, but PUDA edge motion does not, narrow the bug to the **edge runtime path / long-lived serial state / EdgeRunner dispatch context**, not the motor, Arduino, or Stage class in isolation.

## Minimal direct-driver verification script

Create a script under `/home/amdm/workspace/ViPSA/stage/` so `from driver import Stage` imports the local driver file:

```python
#!/usr/bin/env python3
from driver import Stage

PORT = "/dev/openflexture"
BAUDRATE = 115200
MULTIPLIER = 1.0
Z_STEPS = -35
FEEDRATE = 450

stage = Stage(port=PORT, baudrate=BAUDRATE, multiplier=MULTIPLIER)
try:
    if stage.ser is None or not stage.ser.is_open:
        raise RuntimeError(f"Failed to open stage serial port: {PORT}")
    print(f"Connected to stage on {PORT}")
    print(f"Commanding Z move: {Z_STEPS} steps at feedrate {FEEDRATE}")
    stage.move_z_by(height=Z_STEPS, feedrate=FEEDRATE)
    print("Command returned from stage.move_z_by")
    print(f"Driver-tracked position after command: {stage.get_current_position()}")
finally:
    if stage.ser is not None and stage.ser.is_open:
        stage.ser.close()
        print("Serial port closed")
```

Stop the stage edge before running this so `/dev/openflexture`/`/dev/ttyACM0` is released. Ask/ensure the user has visually verified the stage area is safe before executing motion.

## Edge serial debug instrumentation

To inspect what the edge sees, temporarily instrument `Stage.move_z_by` in `stage/driver.py`:

```python
logger.info(
    "VERBOSE_Z_MOVE_BEGIN height=%s distance=%s feedrate=%s port=%s open=%s in_waiting_before=%s gcode=%r",
    height, distance, feedrate, getattr(self.ser, "port", None), self.ser.is_open, self.ser.in_waiting, gcode,
)
self.ser.write(gcode.encode())
self.ser.flush()
logger.info("VERBOSE_Z_MOVE_AFTER_WRITE out_waiting=%s in_waiting=%s", self.ser.out_waiting, self.ser.in_waiting)

# after settling and status query
logger.info("VERBOSE_Z_MOVE_STATUS status=%r in_waiting_after_status=%s", status, self.ser.in_waiting)
remaining = [line.decode("utf-8", errors="replace").strip() for line in self.ser.readlines()]
logger.info("VERBOSE_Z_MOVE_GRBL_REMAINING %r", remaining)
```

Then restart the stage edge and execute a small PUDA move, e.g. `puda machine run stage move_z_by '{"height":-20,"feedrate":450}'` within a normal start/run/complete lifecycle.

## What to report

For user-facing reports, separate three kinds of evidence:

1. **PUDA lifecycle:** start/run/complete success and final machine state.
2. **Edge logs:** EdgeRunner command receipt and driver log lines.
3. **GRBL serial output:** `ok`, `error:...`, status lines such as `<Idle|MPos:...>`, or reset banners.

Example finding from the session:

```text
VERBOSE_Z_MOVE_BEGIN ... in_waiting_before=28 gcode='G91\nG1 Z-20.0 F450\nG90\n'
VERBOSE_Z_MOVE_STATUS status='' in_waiting_after_status=103
VERBOSE_Z_MOVE_GRBL_REMAINING ["Grbl 1.1h ['$' for help]", 'ok', 'ok', 'ok', '<Idle|MPos:0.000,0.000,-20.000|FS:0,0|WCO:0.000,0.000,-400.000>']
```

Important interpretation: `Grbl 1.1h ['$' for help]` in the remaining lines means a GRBL reset/banner was still in the input buffer. A clean driver should clear/handle stale input before motion and parse `ok`/`error` per command rather than counting internal position updates as proof.

## Follow-up fix direction

Patch the Stage driver to:

- clear stale input before sending motion when safe,
- send GRBL lines deliberately,
- wait for `ok`/raise on `error:` per line,
- poll `?` until `<Idle...>`,
- log actual GRBL status and response lines,
- avoid marking driver/PUDA success if serial handshake fails,
- treat `get_current_position()` as untrusted unless it queries GRBL `MPos` or is explicitly labeled software-tracked.

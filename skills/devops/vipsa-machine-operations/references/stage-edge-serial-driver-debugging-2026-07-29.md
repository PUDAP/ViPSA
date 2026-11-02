# Stage edge serial/driver debugging — 2026-07-29

## Trigger

Use this when PUDA `stage.move_z_by` reports success but the user says the OpenFlexure/Arduino Z stage did not visibly move, or when approach appears to fail because Stage Z is not physically advancing.

## Confirmed command-path facts

- PUDA must not write raw G-code itself. The intended path is:
  `puda machine run stage move_z_by ... -> stage edge EdgeRunner -> driver.Stage.move_z_by(...) -> driver writes GRBL serial to /dev/openflexture`.
- `/dev/openflexture` resolved to `/dev/ttyACM0` for the stage Arduino in this session.
- Raw GRBL direct serial `G91 G0 Z50` physically moved the stage.
- A direct Python script importing `Stage` from `/home/amdm/workspace/ViPSA/stage/driver.py` and calling `stage.move_z_by(height=-35, feedrate=450)` physically moved the stage.
- After restarting the stage edge and instrumenting `Stage.move_z_by`, PUDA edge moves also physically moved again.

## Key debugging pattern

1. Do not trust PUDA command success or `get_current_position()` alone as physical motion proof.
2. Check whether the stage edge is holding the serial port:
   - identify stage edge processes by cwd `/home/amdm/workspace/ViPSA/stage`.
   - the Python child may hold `/dev/ttyACM0`.
3. If direct serial testing is explicitly authorized, stop the stage edge first, then reopen `/dev/openflexture` from Python/pyserial or the stage driver script.
4. Restart only the stage edge after direct serial work.
5. Instrument `Stage.move_z_by` before concluding where the fault is.

## Useful temporary `move_z_by` instrumentation

Log at method entry:

```python
logger.info(
    "VERBOSE_Z_MOVE_BEGIN height=%s distance=%s feedrate=%s port=%s open=%s in_waiting_before=%s gcode=%r",
    height, distance, feedrate, getattr(self.ser, "port", None), self.ser.is_open, self.ser.in_waiting, gcode,
)
```

Immediately after write/flush:

```python
self.ser.write(gcode.encode())
self.ser.flush()
logger.info("VERBOSE_Z_MOVE_AFTER_WRITE out_waiting=%s in_waiting=%s", self.ser.out_waiting, self.ser.in_waiting)
```

After the wait/status:

```python
status = self._is_busy()
logger.info("VERBOSE_Z_MOVE_STATUS status=%r in_waiting_after_status=%s", status, self.ser.in_waiting)
remaining = [line.decode("utf-8", errors="replace").strip() for line in self.ser.readlines()]
logger.info("VERBOSE_Z_MOVE_GRBL_REMAINING %r", remaining)
```

## Important observation from the successful verbose PUDA move

A `stage.move_z_by({"height": -20, "feedrate": 450})` produced:

```text
VERBOSE_Z_MOVE_BEGIN height=-20 distance=-20.0 ... in_waiting_before=28 gcode='G91\nG1 Z-20.0 F450\nG90\n'
VERBOSE_Z_MOVE_AFTER_WRITE out_waiting=0 in_waiting=28
VERBOSE_Z_MOVE_STATUS status='' in_waiting_after_status=103
VERBOSE_Z_MOVE_GRBL_REMAINING ["Grbl 1.1h ['$' for help]", 'ok', 'ok', 'ok', '<Idle|MPos:0.000,0.000,-20.000|FS:0,0|WCO:0.000,0.000,-400.000>']
```

The `Grbl 1.1h` banner and nonzero `in_waiting_before` showed stale serial input after Arduino reset/edge startup. Future robust fixes should clear/drain serial input after startup and before motion, then parse per-line `ok`/`error:` and final `<Idle|MPos:...>` status.

## Driver caveats to preserve

- `get_current_position()` currently returns internal counters, not a hardware query.
- `serial.flush()` only drains outgoing bytes; it does not prove GRBL executed the move and does not clear incoming stale lines.
- The driver should raise on serial/GRBL failure rather than logging and returning `None`, otherwise PUDA may publish success for a failed physical operation.
- `abort_motion()` contains `G90 G1 Z0 F100`; do not describe it as a pure hold-clear without verifying/understanding the physical effect.

## User-facing reporting standard

When asked to test movement through the edge, report both:

- PUDA command result and final machine state.
- Edge/driver/GRBL serial evidence, especially `VERBOSE_Z_MOVE_*` and `MPos`, while still asking/accepting visual confirmation as the physical truth.

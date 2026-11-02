# Stage edge serial-state and motion-verification pitfall (2026-07-29)

## What happened

During ViPSA contact approach/debugging, the PUDA `stage.move_z_by(...)` command repeatedly reported success and advanced the driver's tracked Z, but the user visually observed no physical stage motion. Two non-PUDA paths did physically move the same stage hardware:

- Raw serial G-code on `/dev/openflexture`: `G91 G0 Z50`
- Direct Python script importing `Stage` from `/home/amdm/workspace/ViPSA/stage/driver.py` and calling `Stage.move_z_by(height=-35, feedrate=450)`

After stopping/restarting the stage edge and adding temporary verbose serial logging inside `Stage.move_z_by`, PUDA edge motion worked again. The verbose log showed stale GRBL startup/status data in the serial input buffer before a move (`in_waiting_before=28`, including `Grbl 1.1h ['$' for help]`).

## Durable lesson

For ViPSA stage Z operations, a PUDA command success and `get_current_position()` readback are not proof of physical motion. The driver's position is software-tracked, and stale serial input/buffer state in a long-lived edge process can cause misleading success reports.

## Future workflow

When stage motion is questioned or approach current does not change as expected:

1. Stop further approach loops; do not keep stepping Z based only on tracked readback.
2. Ask for/obtain visual confirmation of physical motion for one small test jog.
3. Inspect/restart only the stage edge to release/reopen `/dev/openflexture`.
4. If needed, add temporary logging inside `Stage.move_z_by` for:
   - requested `height`, computed `distance`, `feedrate`
   - port/open state and `in_waiting_before`
   - exact G-code representation written by the driver
   - GRBL `ok`/`error`/`<Idle|MPos...>` responses after write
5. Treat `MPos`/visual observation as stronger evidence than the driver's internal `get_current_position()` value.
6. Remove or quiet verbose logging after debugging; user prefers concise ViPSA updates unless explicitly asking for verbose output.

## Session addendum: restart edge then verify MPos after requested Z jog (2026-08-03)

When the user explicitly asks to `restart the edge and move z stage up by 15`, do the restart first, then execute the requested PUDA `stage.move_z_by` through the freshly started edge. Do not report only the software-tracked `get_current_position()` value; inspect the stage edge log/process output for the `VERBOSE_Z_MOVE_*` lines and quote the GRBL evidence.

Observed good evidence after a fresh edge restart:

```text
VERBOSE_Z_MOVE_BEGIN height=15 distance=15.0 feedrate=450 port=/dev/openflexture open=True in_waiting_before=28 gcode='G91\nG1 Z15.0 F450\nG90\n'
VERBOSE_Z_MOVE_AFTER_WRITE out_waiting=0 in_waiting=28
VERBOSE_Z_MOVE_STATUS status='' in_waiting_after_status=102
VERBOSE_Z_MOVE_GRBL_REMAINING ["Grbl 1.1h ['$' for help]", 'ok', 'ok', 'ok', '<Idle|MPos:0.000,0.000,15.000|FS:0,0|WCO:0.000,0.000,-400.000>']
```

Interpretation: stale startup text in the serial buffer is still a pitfall, but the decisive evidence is the per-line `ok` responses plus `<Idle|MPos:...15.000...>`. In the concise user report, say the edge was restarted, the PUDA move was sent, GRBL returned `MPos`, and the machine state is idle/null. Avoid claiming physical motion from readback alone if the log lacks `MPos` or the user says they saw no movement.

## Fix direction

A robust stage driver should clear stale input before movement, send G-code lines with per-line `ok/error` checks, poll GRBL until Idle, and make `get_current_position()` query GRBL status/position rather than only returning internal counters.
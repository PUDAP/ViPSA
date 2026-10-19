# Stage-Z false-success recovery after PUDA reports motion but user sees no movement (2026-07-31)

## Trigger
Use when a Stage-Z PUDA/protocol move reports success and `get_current_position()` changes, but the user says the physical stage did not move. Treat this as the known stale serial / duplicate edge / software-tracked readback class.

## Key lesson
Do **not** report PUDA `move_z_by` success + tracked readback as physical motion confirmation when the user visually contradicts it. Stop further PUDA stage motion until the edge/serial state is recovered and motion is verified by GRBL `MPos` and/or visual observation.

## Recovery procedure used
1. Stop/verify no active grid/approach runners are still commanding Stage-Z.
2. Inspect stage edge processes and `/dev/openflexture` ownership. In this case there were duplicate long-lived stage edge `uv run main.py` processes.
3. Terminate duplicate/stale stage edge process groups so `/dev/openflexture` is released.
4. Run a **direct driver** recovery script from `/home/amdm/workspace/ViPSA/stage` importing `Stage` from `driver.py` (not raw G-code):
   - open `/dev/openflexture` at `115200`
   - record and drain stale serial input
   - call `Stage.move_z_by(height=<requested>, feedrate=450)`
   - query GRBL with `?` and save returned `<Idle|MPos:...>`
   - close serial
5. Restart exactly one stage edge (`cd /home/amdm/workspace/ViPSA/stage && uv run main.py`).
6. Verify a read-only PUDA stage command succeeds and final state is `idle/run_id:null`.

## Evidence pattern
The recovery direct-driver move for a requested `+15` showed stale serial input before motion:

```text
in_waiting_before_clear: 28
stale_lines_before_move: ["", "Grbl 1.1h ['$' for help]"]
```

Then the direct `Stage.move_z_by(height=15, feedrate=450)` produced GRBL/driver evidence:

```text
VERBOSE_Z_MOVE_BEGIN ... gcode='G91\nG1 Z15.0 F450\nG90\n'
VERBOSE_Z_MOVE_STATUS status='ok'
VERBOSE_Z_MOVE_GRBL_REMAINING ['ok', 'ok', '<Idle|MPos:0.000,0.000,15.000|FS:0,0|WCO:0.000,0.000,-400.000>']
grbl_status_after_move: ['<Idle|MPos:0.000,0.000,15.000|FS:0,0|Ov:100,100,100>', 'ok']
```

## Reporting rule
When this happens, say explicitly that the earlier PUDA readback was software-tracked/untrusted and that the real recovery move was performed through the direct `Stage` driver path. Report GRBL `MPos`/visual evidence separately from PUDA lifecycle state.

## Safety notes
- Do not use `stage.disconnect()`; it moves to zero.
- Do not write raw G-code as the normal fix; use `Stage` driver methods unless the user explicitly authorizes raw serial debugging.
- Remove/quiet verbose logging after debugging because the user prefers concise ViPSA updates unless verbose logs are requested.

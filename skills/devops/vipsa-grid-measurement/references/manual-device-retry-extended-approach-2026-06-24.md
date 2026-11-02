# Manual grid-device retry with raised lower threshold and extended approach

## Trigger

Use this pattern when a long ViPSA grid run is paused so a previous/current device can be revisited manually, the approach lower threshold is changed, and the user asks to continue beyond the normal max approach range.

Concrete session pattern: device 22 in an 8x8 batch/substrate grid was revisited after the continuation runner had advanced to later devices. The requested approach window changed from `1e-10–1e-8 A` to `1e-9–1e-8 A` at `0.1 V`, and the user asked to attempt the normal 60-step approach plus 50 additional forward steps if no contact was reached.

## Procedure

1. Stop/pause the active grid runner first; do not treat later SIGTERM notifications from the old process as active failures.
2. Force safe electrical cleanup before travel:
   - Keithley output off
   - Keysight output off
   - 707B `open_all`
   - verify `get_closed_channels == nil`
   - lights off unless explicitly needed
3. Move back to the target device explicitly and separately from the continuation runner:
   - safe stage-Z retract (e.g. `-60` if that is the active run setting)
   - Zaber absolute `move_x_to`/`move_y_to` to the device's recorded `x,y`
   - stage-Z pre-approach (e.g. `+30` if that is the active run setting)
4. Run a standalone approach artifact for the retry, recording the altered parameters:
   - `test_voltage_v`
   - `lower_a`
   - `upper_a`
   - `read_compliance_a`
   - primary max steps
   - extra steps after primary max
   - final stage position and cleanup state
5. If the primary max is reached and the user explicitly authorized extra steps, continue without reclassifying it as failed until the extra-step budget is exhausted.
6. Patch the continuation runner constants and run summary metadata to match the new threshold before any later resume.
7. Leave the grid paused unless the user explicitly asks to resume.

## Pitfalls and recovery

- If a long per-command approach loop stalls around a stage move, do not leave the system ambiguous. Kill the wrapper only if necessary, then issue `stage.abort_motion()`, read stage position, force SMU outputs off, `open_all`, and verify all machines return to `idle`/`run_id: null`.
- A stale `complete` for a stage run may return `RUN_ID_MISMATCH` / `not active`; that is not itself proof of motion failure. Follow with `abort_motion()` and `get_current_position()` to recover a verified safe state.
- If a killed or interrupted retry leaves Keysight `active` with a stale run id even though the retry did not intentionally use Keysight for approach, explicitly complete the stale run id or send a fresh `set_output(false)` and verify Keysight `idle`/`run_id: null` before reporting cleanup complete.
- When a retry remains below the new lower threshold after the full `primary + extra` range, report `no_contact_after_<primary>_plus_<extra>` honestly with final current and final Z; do not call it successful merely because the old lower threshold would have accepted it.

## Reporting standard

Concise report fields:

- grid runner paused / remains paused
- threshold patch applied to continuation runner
- target device and Zaber coordinates
- approach window, voltage, read compliance
- primary max and extra steps attempted
- final current and classification
- final stage position
- cleanup verification: Keithley/Keysight outputs off, 707B `nil`, all six ViPSA machines idle/null

# Manual S1 7x7 device-6 overwrite continuation (2026-07-14)

## Trigger

Use this pattern when the user manually positions the rig at a target grid device, then asks to approach and continue a previous grid measurement from that device while overwriting prior data from that device onward.

Concrete session: user moved to S1 7x7 run device 6 using the old run's recorded aligned Zaber coordinate, then said: turn off the light, approach, continue grid measurement from this device, and override previous run data as testing proceeds.

## Durable workflow

1. **Resolve the current positioned target from artifacts.** For S1 7x7 device 6, the old run had:
   - grid target: `x=49383`, `y=494373`
   - prior alignment correction: `x +521`, `y -48`
   - aligned Zaber coordinate: `x=49904`, `y=494325`
2. **Move/revisit separately before restarting the run.** If the user has not already positioned the rig, move Zaber to the aligned absolute native coordinate and verify readback. Keep the stage at the explicit safe-down Z if already retracted; do not silently pre-approach until the user asks.
3. **Before electrical approach/measurement:**
   - turn the light off and verify `light` returns idle/null;
   - force Keithley and Keysight outputs off;
   - run `keithley-707b.open_all()` and verify `get_closed_channels() == "nil"`;
   - verify machines are idle/null when possible.
4. **Archive old data at and after the explicit restart boundary.** For an overwrite from device 6, move active `device_06`, any `device_06.*` partials, and all later `device_##` folders into a timestamped archive directory such as `archive_before_device6_overwrite_<UTC>`. Preserve devices 1–5.
5. **Prune run summaries at the same boundary.** Edit `summary.partial.json` and `summary.json` to keep only device entries before device 6, and append a `resume_events` entry with the archive path and boundary.
6. **Patch/generate the continuation runner:**
   - set `START_AT_DEVICE=6`;
   - compute serpentine traversal order and slice from the explicit boundary device, rather than filtering by existing `DONE.json`;
   - record `explicit_device6_overwrite_boundary` in `resume_events`;
   - for the first device only, treat it as a **manual handoff**: do not move Zaber, move stage, or realign before the requested approach;
   - turn light off again inside the first-device handoff path;
   - run the normal bounded approach in place, save `approach.json`, then run the configured DCIV and randomized pulse workflow;
   - after device 6, resume normal travel/alignment/approach/device-measurement flow for subsequent serpentine devices.
7. **Launch as a tracked background process** with `notify_on_complete=true`, then verify fresh artifacts for `device_06` rather than just relying on a live PID.

## Verification fields to report

For the first overwritten device, report compactly:

- archive path and that old device 6+ data was moved out of the active path;
- approach status, final approach current, net Z, and final stage Z;
- DCIV max `|I|`, SET/RESET detection flags;
- pulse trains collected and early-stop reason;
- current runner state / next device started;
- current machine states if checked.

Session outcome example for device 6 after overwrite:

- approach: `in_window_after_retract`
- final approach current: `6.84 nA`
- net approach Z: `+42.5` steps; final stage Z readback `+7.5`
- DCIV max `|I|`: `~1e-4 A`
- SET detected: true; RESET detected: false
- randomized pulse: 25 trains collected, stopped at `read_current_near_pulse_compliance`
- runner continued to device 7.

## Pitfalls

- **Do not use `DONE.json` filtering for explicit overwrite boundaries.** Existing `DONE.json` files are exactly what must be bypassed/archived; using them to choose remaining devices can skip the requested redo.
- **Do not re-align before the requested first-device approach** when the user has just positioned the rig at a known aligned coordinate and explicitly says approach/continue from this device. Alignment can occur for later devices.
- **Do not leave light on for electrical approach/measurement.** Turn it off before approach and inside the first-device handoff path.
- **Do not capture this as a new one-off skill.** It belongs under the grid-measurement/manual-handoff/overwrite-continuation class.
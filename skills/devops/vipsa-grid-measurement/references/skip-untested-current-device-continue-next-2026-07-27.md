# Skip untested current grid device and continue from next serpentine device

Use this when a grid continuation is running or paused on the current boundary device, and the user says to skip it *if it has not been tested yet* and move on.

## Trigger

- User asks to skip the current device only if it has not been electrically tested.
- Current run folder has a `device_N/summary.json` in `started`/approach state, but no `dciv.csv`, no `dciv.json`, no randomized pulse CSV/summary, and no valid completed measurement status.
- The next device must be chosen by the run's serpentine traversal order, not by numeric `N+1` unless those match.

## Workflow

1. Verify the live runner/process and active `OUT` folder; do not use stale background notifications alone.
2. Inspect `device_N` artifacts:
   - If DCIV or randomized pulse artifacts exist, report that the device has already been tested/partially tested and ask before discarding or skipping.
   - If only approach/alignment artifacts exist, it is safe to mark the device as skipped when the user asked for this condition.
3. Stop/kill the active runner and verify no matching process remains.
4. Run the full ViPSA cleanup:
   - `stage.abort_motion()` if approach/stage motion may have been active.
   - Keithley output off.
   - Keysight output off.
   - `keithley-707b.open_all()` and `get_closed_channels()`; expected result `nil`.
   - Light off.
   - Verify all six machines idle with `run_id: null`.
5. Mark the old device summary explicitly, preserving artifacts:
   - `status: skipped_untested_by_user`
   - `skip_reason: no DCIV/randomized pulse artifacts; user requested skip`
   - `next_device: <next traversal device>`
6. Patch or generate a fresh continuation runner with:
   - `START_DEVICE=<next_serpentine_device>`.
   - A new output folder name documenting the skip boundary.
   - `skipped_devices` metadata in run summary.
   - First device handled as a normal grid travel/alignment device unless the live position is already that next device. Do **not** accidentally reuse current-device handoff logic meant for the skipped device.
7. Compile the runner, launch it as a tracked background process with `notify_on_complete=true`, and verify the first output line is `device_start` for the next device.

## Concrete 2026-07-27 pattern

- Device 8 had approach attempts but no `dciv.csv` / randomized pulse artifacts.
- The previous runner was killed and cleanup verified.
- Device 8 was marked `skipped_untested_by_user`.
- Serpentine order after 8 was device 15, not 9.
- The new runner started at `START_DEVICE=15`; first-device current-handoff logic was disabled for device 15, so it performed normal safe Z retract, Zaber travel, alignment, approach, one DCIV, and randomized pulses.

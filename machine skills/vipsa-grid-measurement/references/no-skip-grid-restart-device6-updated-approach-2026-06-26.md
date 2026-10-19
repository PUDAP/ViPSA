# No-skip grid restart from device 6 with updated approach parameters (2026-06-26)

Use this pattern when a ViPSA grid continuation is active and the user asks to return to a specific device, rerun approach with new parameters, and continue the grid while preserving an explicit no-skip DCIV/pulse override.

## Trigger

- Active S3/8x8-style grid runner is in progress or partially started.
- User asks to move back to a device already started/partially measured, e.g. device 6.
- User provides updated approach parameters, e.g. `step size 0.5`, `final trim 0.25`, `max attempts 120`.
- User still expects DCIV and randomized pulses to run; do not silently reintroduce skip gates.

## Procedure

1. Identify and stop the current active runner before changing approach parameters.
   - Poll the known Hermes process/session and confirm which script is active.
   - Kill only the active grid runner; ignore older killed-process notifications if they refer to a stale session.
2. Immediately perform electrical cleanup and verify safe state.
   - Force Keithley output off.
   - Force Keysight output off.
   - Open all 707B routes and verify `get_closed_channels == nil`.
   - Turn lights off before electrical approach/measurements unless explicitly told otherwise.
3. Verify all ViPSA machines are idle/null before restart.
   - If `stage` is `idle` but carries a stale non-null `run_id`, clear it using the same per-command start→command→complete/direct cleanup pattern used by the runner, or a harmless read-only position command if appropriate.
4. Archive stale folders from the requested restart device onward.
   - Move `device_06` (and any later stale `device_XX` folders) to an `archive_*_before_<reason>_<timestamp>` directory.
   - Prune `summary.partial.json` so it keeps only devices before the restart boundary.
   - Add a resume event recording the user approach parameters and archive names.
5. Patch/regenerate the continuation runner.
   - Set/confirm `START_AT_DEVICE=<requested device>`.
   - Ensure the `approach()` function uses the user parameters, e.g. forward step `0.5`, trim/fine step `0.25`, max attempts `120`.
   - Record the same approach parameters in run summary metadata and per-device `approach.json`.
   - Preserve any explicit user override such as `do not skip running DCIV/Pulses`: contact/safety gates should be recorded as flags only, and DCIV plus randomized pulse should still be attempted.
6. Compile/validate the patched runner before starting.
   - `python3 -m py_compile <runner.py>` should pass.
   - Search/inspect for the approach parameters and no-skip markers.
7. Start the new runner as a tracked background process with notify-on-complete.
8. Verify restart actually began.
   - Read `device_06/summary.json` and confirm a fresh `started_utc`/`status: started`.
   - Check that new alignment/approach files begin appearing in the fresh `device_06` folder.
   - Probe machine states: Zaber should become idle after XY move; stage/Keithley may be busy during approach.

## Reporting standard

Keep the Telegram report concise:

- State the old runner stopped and cleanup verified.
- List archived stale folders.
- State the new runner session/PID and script path.
- List the new approach parameters.
- State whether device summary/artifacts show the restart began.
- Explicitly say DCIV and randomized pulses remain forced if the user previously requested no-skip behavior.

## Pitfalls

- Do not leave stale `DONE.json` or old `device_06` artifacts in place; the runner may skip the device or mix old skipped data with the restart.
- Do not change only code constants; also update summary metadata/per-device `approach.json` so later analysis knows which approach parameters were actually used.
- Do not treat an old background completion with exit code `-15` as the new run failing; verify against the current session ID/PID.
- Do not report physical motion solely from a successful PUDA response if there is contradictory visual evidence; otherwise report command/readback verification only.

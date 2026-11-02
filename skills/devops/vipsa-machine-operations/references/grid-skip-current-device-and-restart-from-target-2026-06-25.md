# Grid run: skip current device and restart from a target device

Use this when the user changes an active ViPSA grid campaign mid-run with wording like “skip measuring device N, move to M and start the grid from there.”

## Pattern

1. Stop all automation that could conflict:
   - Kill any watcher/helper process waiting on the old current device.
   - Kill the active grid runner process.
   - Treat the resulting background-process completion notifications (`exit code 143` / `-15`, `tcsetattr` noise) as expected if they correspond to the processes intentionally killed.
2. Preserve the skipped device record:
   - Do not delete its folder.
   - Update `device_##/summary.json` with `status: skipped`, `skipped_utc`, and a concise `skip_reason`.
   - Write a small `SKIPPED.json` marker with the same reason.
3. Start the requested target device cleanly:
   - Archive any existing `device_##` folder for the target device before remeasurement, e.g. `device_30_archive_before_start_from30_<UTC>`.
   - Generate a continuation runner with `START_AT_DEVICE=<target>`.
   - Disable any special first-device handoff logic that only applied to the previous manual handoff device (for example, guard `if idx == 0 ... START_AT_DEVICE == 24` so a new `START_AT_DEVICE=30` uses the normal safe retract → Zaber travel → pre-approach → align → approach path).
   - Keep the current approach parameter overrides, including `max_attempts`, thresholds, and no-recording settings.
4. Launch the new runner as a tracked background process with `notify_on_complete=True`.
5. Verify the new runner is alive. If the target folder does not appear immediately, report that it is in startup/cleanup rather than claiming measurement has started.

## Reporting

Keep the update concise:

- “Stopped old runner/watcher.”
- “Marked device N skipped.”
- “Archived old device M folder.”
- “Started new runner from device M onward: session/process/script.”
- Mention that old killed-process notifications are expected only if their process IDs match the stopped runner/watcher.

## Pitfalls

- Do not let an older watcher continue after the user changes the plan; it may stop or restart the wrong device sequence.
- Do not continue a partially measured current device when the user explicitly says to skip it.
- Do not leave stale `DONE.json`/old `device_##` data in place for a device the user wants remeasured; archive it first.
- Do not accidentally reuse manual current-position handoff logic for a different restart target. Normal restart-from-target should travel to the target device and perform alignment/approach normally.

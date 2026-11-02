# Overwrite restart from a device boundary in an active ViPSA grid run

Use this when the user says to move/restart from a specific device and **overwrite existing data** from that point onward.

## Pattern

1. Stop the active tracked grid runner first. Treat later `-15`/SIGTERM notifications from the killed process as expected, not as a new failure.
2. Immediately run electrical cleanup before file edits or travel:
   - `keithley-2450.set_output(false)`
   - `keysight-b2902b.set_output(false)`
   - abort SMU measurements if available
   - `keithley-707b.open_all()`
   - verify `get_closed_channels() == "nil"`
   - turn lights off unless the user requested otherwise
3. Verify no stale grid runner remains.
4. For an **overwrite** request, remove `device_N`, `device_(N+1)`, ... folders in the active run directory rather than archiving them. Preserve folders before `N`.
5. Prune `summary.partial.json` to keep only device summaries before the restart boundary. For serpentine traversal, this usually means “devices already completed before the requested boundary,” not numeric `device_number < N` unless that is the same set.
6. Patch/generate a continuation runner:
   - `START_AT_DEVICE = N`
   - completed/preserved set contains only devices before the boundary
   - restart slicing uses the serpentine traversal index of `START_AT_DEVICE`
   - old `DONE.json` files cannot skip devices at or after the boundary because their folders were removed
   - preserve current approach/electrical parameters and no-skip overrides unless the user changed them
7. If approach thresholds are constants (`APPROACH_LOWER_A`, `APPROACH_UPPER_A`), ensure downstream gate code uses those constants, not stale hard-coded values from a previous window.
8. Compile the runner before launching.
9. Start it as a tracked background process with completion notification.
10. Verify the first restarted device has a fresh `device_N/summary.json` with `status: started` and new artifacts such as alignment images before reporting success.

## Reporting

Keep the report concise:

- stopped old runner
- cleanup/switch state verified
- exact folders removed or boundary removed from
- summary preserved devices
- new runner session id/PID/script
- first restarted device verification
- key retained parameters, especially contact thresholds and skip/no-skip policy

## Pitfalls

- Do not leave the old runner alive while deleting folders; it can recreate or continue writing stale device data.
- Do not prune by numeric device number when the active traversal is serpentine unless that matches the physical traversal boundary.
- Do not archive folders when the user explicitly says overwrite; deleting the restart range is the intended data semantics.
- Do not report a stage `idle` state with stale non-null `run_id` as fully clean if it matters for next motion; a harmless readback/start-complete or reset/recovery may be needed before motion.

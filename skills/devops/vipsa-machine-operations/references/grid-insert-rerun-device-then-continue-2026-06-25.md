# Grid mid-run inserted device remeasure then continuation

Use this when a long ViPSA grid runner is active and the user wants to remeasure a previously completed/poor-contact device after the current device finishes, then continue the remaining traversal.

## Pattern

1. Identify the active grid runner process/session and the current in-progress device from the run folder (`device_##/summary.json` with `status: started` and no `finished_utc`).
2. Create a watcher process instead of interrupting the current device immediately:
   - Poll the current device summary until `finished_utc` is present.
   - Terminate the old grid runner before it starts the next traversal device.
   - Archive the stale target device folder before rerun, e.g. `device_30_archive_before_user_remeasure_<timestamp>`.
   - Rerun the requested device using the current grid target coordinates and the updated contact parameters.
   - After the inserted rerun finishes, start a continuation runner from the next normal traversal device.
3. If the user later corrects “continue automatically,” update the watcher so it launches the continuation runner after the inserted rerun. Do not leave the run paused unless the user explicitly asks to pause.

## Implementation notes

- Prefer a dedicated watcher script under `runs/` plus a tracked background terminal process with `notify_on_complete=true`.
- Record watcher logs under `runs/` so the handoff is auditable.
- Patch or generate a continuation runner with a new `START_AT_DEVICE` for the next normal traversal device. Guard any special first-device handoff logic so it does not accidentally reuse a manual handoff when `START_AT_DEVICE` is no longer that handoff device.
- Preserve the user-requested contact parameter change both in runner constants and in per-device `approach.json` metadata. For this case, `max_attempts=120` should be explicitly recorded along with forward/fine Z step sizes.
- Archive old per-device folders before rerun so stale `DONE.json`, `summary.json`, DCIV, or pulse artifacts do not cause a skip or contaminate the new measurement.
- If stopping the old runner is necessary after the current device, send SIGTERM first and only SIGKILL if it remains alive after a bounded wait.

## Reporting

Report concisely:

- current device being watched,
- inserted remeasure device,
- updated contact max attempts / relevant approach parameters,
- watcher process session/log path,
- whether continuation will resume automatically and from which device.

Avoid saying the grid will pause if the user has asked to continue automatically after the inserted rerun.
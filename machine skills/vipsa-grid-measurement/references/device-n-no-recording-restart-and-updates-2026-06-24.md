# Device-N no-recording grid restart + per-device updates — 2026-06-24

Use this reference when restarting a ViPSA 8×8 batch/substrate grid continuation from a specific device and the user requests no video recording plus updates after each device.

## Operational pattern

1. Distinguish measurement from monitoring:
   - `cronjob` per-device reporters are only watchers; they are not active electrical tests.
   - To answer “is any test running?”, check Hermes tracked processes and OS processes for grid/resume/Python/PUDA runners; also inspect the next device folder.
2. If no measurement runner is active and the user says “start with device N; no video recording”:
   - Patch/regenerate the continuation runner with `START_AT_DEVICE=N`.
   - Ensure the runner uses a no-op recorder (`recording_started=False`, no `Recorder.start()`, no camera threads, no `camera*_resume_*.mp4` paths).
   - Preserve completed devices before N; prune/archive summary records or stale folders for device N+ according to the user’s overwrite boundary.
   - Verify the Python file compiles before launch.
3. Start the runner as a tracked background process with `notify_on_complete=true`.
4. Verify early progress with real artifacts:
   - process PID/session is running;
   - `device_N/summary.json` exists with `status: started` and correct target row/col/x/y;
   - no newly-created `camera*_resume_*.mp4` files appeared after launch.
5. Keep a per-device monitor active if requested:
   - initialize its state file to existing completed `device_*/DONE.json` names so it does not spam old device reports;
   - every tick stays silent unless a new DONE appears;
   - when a new device finishes, send a concise text summary plus `MEDIA:<device_plot.png>` if present.

## Reporting standard

For the restart confirmation, be terse and include:

- “Started device N continuation with no video recording.”
- tracked process session and PID;
- `device_N/summary.json` target and `status: started`;
- explicit “no new camera resume videos created” verification;
- note that per-device updates will arrive when each DONE file appears.

## Pitfalls

- Do not mistake a paused/active monitor cron for a running measurement.
- Do not restart from the prior hard-coded boundary (for example device 6) after the user asks for a new device boundary (for example device 7).
- Do not create new video artifacts when “no video recording” is specified, even if previous run folders contain old camera videos.

# Grid resume after stale-run data and duplicate subscriber / run-id mismatch

Use this when a long ViPSA grid run is interrupted and the user asks to reset machines, delete stale data, and restart from a specific device.

## Pattern

1. **Stop any old run process first.**
   - Check tracked/background process status when available.
   - If you intentionally kill an old process, report later SIGTERM / exit `-15` notifications as expected cleanup, not a new failure.
   - Camera recorder stderr such as H.264 decode warnings from a killed process should be classified as recorder/camera noise unless electrical artifacts or PUDA state show a measurement failure.

2. **Reset/clear machines before deleting/restarting.**
   - Complete any visible stale run IDs if present.
   - Force conservative electrical cleanup: SMU outputs off, 707B `open_all`, verify `get_closed_channels == nil` when command path is responsive.
   - Verify all six ViPSA machines return `idle` with `run_id: null` before restart.

3. **Delete stale run data by device boundary.**
   - Preserve completed devices before the requested restart point.
   - Remove incomplete/stale `device_XX` folders from the restart device onward.
   - Clean `summary.partial.json` so it only contains preserved completed device records and records a compact `resume_cleanup_events` entry.
   - Avoid keeping a confusing backup folder inside the active run directory unless the user asked for backup; stale backup folders can be reinterpreted as live data later.

4. **Patch the resume runner for per-command robustness when run-state is unreliable.**
   - A long shared run ID across all machines can fail after outages: edges may accept `START` and then a queued command can hit a stale/duplicate subscriber that reports `RUN_ID_MISMATCH` or `expected active run`.
   - Use fresh `start -> single command -> complete` transactions for resumed direct-NATS control.
   - On `cannot start, <old-run-id> is currently running`, publish `complete` for the old run ID, then retry with a fresh run ID.
   - Retry the entire `start -> command -> complete` transaction with fresh run IDs on `RUN_ID_MISMATCH`/`expected active run`.
   - Bound per-attempt timeouts for stage/light/zaber/707B commands so a duplicate stale subscriber does not stall the whole grid loop for minutes while machines are actually idle.
   - Always attempt `complete` even after a command failure, then run cleanup.

5. **Verify restart progress with artifacts and machine state.**
   - Confirm only devices before the restart point have `DONE.json` before launching.
   - After launch, verify the restarted device creates expected artifacts (`summary.json`, alignment images, `approach.json`, etc.).
   - If the process is still running but machines are idle and the restarted device is not advancing for longer than the bounded command timeout, treat it as a hung runner: kill the process, cleanup, delete partial restart-device data, patch timeout/retry logic, and restart again.

## Reporting standard

Keep the Telegram report concise:

- Old killed process notifications: `expected SIGTERM from cleanup`.
- H.264 warnings: `camera recorder warning, not electrical failure` unless evidence says otherwise.
- Current active process ID.
- Preserved completed device range and restart device.
- Machine safety verification: outputs off / 707B nil / idle-null states.
- Current restarted-device status and whether it is still running or blocked.

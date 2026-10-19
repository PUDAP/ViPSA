# Live grid restart after SMU busy check + travel-Z update (2026-06-24)

Use this when a long ViPSA grid continuation appears stalled and the user asks to check whether the SMUs are busy, then continue with changed inter-device Z travel settings.

## Trigger

- Active/resume grid runner exists but current device remains `started` with no progress.
- `puda machine state ...` may hang or return no useful state snapshots.
- User asks to check SMUs and restart/continue if not busy.
- User changes safe travel Z values, e.g. safe retract before next-device travel and pre-approach after align/device move.

## Verified pattern

1. Distinguish the measurement process from monitor/reporting jobs.
   - Use the active runner PID/script path, not cron monitor notifications.
   - A killed stale runner can later report exit `-15`; do not treat that as the newly restarted run failing.

2. If `puda machine state` hangs, use a short direct PUDA/NATS busy probe for the electrical machines:
   - For `keithley-2450` and `keysight-b2902b`: fresh `start` → `set_output(enabled=false)` → `complete`.
   - For `keithley-707b`: fresh `start` → `open_all()` → optional `get_closed_channels()` → `complete`.
   - Interpret fresh `START success` as **not busy** for restart purposes.
   - If a follow-up 707B `get_closed_channels` or `complete` returns `RUN_ID_MISMATCH` after `open_all()` succeeded, report that `open_all` succeeded but do not rely on the readback; this is a control-path state loss, not evidence of closed channels.

3. Patch the continuation runner before restart:
   - Update all hard-coded inter-device safe retract/pre-approach moves, including the first restarted device branch and the normal `idx>0` branch.
   - Update summary metadata after loading any previous `summary.partial.json`, because `SUMMARY.update(_prev)` can overwrite the new default params. Re-apply e.g.:
     ```python
     SUMMARY.setdefault('params', {})['safe_retract_z'] = -60
     SUMMARY.setdefault('params', {})['pre_approach_z'] = 30
     ```
   - Update status/print text and per-device `manual_start_move` metadata so the folder records the actual commanded Z values.
   - Preserve prior patches such as no-video recording and no-contact alignment recheck / higher-voltage diagnostic.

4. Stop the stale active runner cleanly, then archive the partial current-device folder if it has no `DONE.json`:
   - Example archive suffix: `device_16_pre_restart_safe60_<utc>`.
   - Do this before launching the patched runner so stale `summary.json` does not mask the restart.

5. Restart as a tracked background process with completion notification.
   - Verify new PID is running.
   - Verify the current `device_##/summary.json` is recreated.
   - Check for early progress artifacts such as `align_frame.jpg`, `align_annotated.jpg`, and `align_detection.json`.
   - Verify no new `camera*_resume_*.mp4` files if recording is disabled.

## Reporting

Keep Telegram report concise:

- SMU status: not busy / output forced off / 707B open-all success.
- Runner action: stale PID stopped, partial device archived, patched values applied.
- Restart handle: session ID, PID, current device.
- Verification: recreated summary, early artifact(s), no video files if no-recording remains requested.

Avoid claiming the device is already measuring electrically unless per-device files or stdout confirm that phase.
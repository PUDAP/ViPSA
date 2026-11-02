# Grid run no-recording stop/resume pattern (2026-06-24)

Use when a ViPSA grid/resume runner is active and the user says variants of **"do not record"**, **"stop recording"**, or asks to continue without videos.

## Meaning

Treat this as an immediate operational correction, not a documentation request:

- Stop any active grid/resume process that is creating camera/video artifacts.
- Disable embedded `Recorder` / camera-video creation in the continuation runner before restart.
- Do not leave the user with new `camera*_resume_*.mp4` artifacts from the stopped attempt unless they explicitly asked to keep them.

## Safe sequence

1. Identify and stop the tracked active grid/resume Python process.
2. Run normal hardware cleanup before claiming success:
   - Keithley output off.
   - Keysight output off.
   - 707B `open_all()` and verify `get_closed_channels()` is `nil`/none.
   - Light off unless the user asked otherwise.
   - Verify relevant machines are `idle` with `run_id: null`; reset/clear stale run ids if needed.
3. Remove the just-created recording artifacts from the current run folder if they came from the aborted recording attempt.
4. Patch or regenerate the continuation runner so camera recording is disabled entirely:
   - remove/guard `Recorder(...)` construction;
   - remove/guard `recorder.start()` / `recorder.stop()` calls;
   - avoid creating `camera1_resume_*.mp4` / `camera2_resume_*.mp4` paths.
5. Restart the grid/resume process only after verifying the no-recording patch.
6. Verify no new `camera*_resume_*.mp4` files are created after restart and report the tracked process id/session.

## Reporting standard

Keep the Telegram reply concise:

- Say recording was stopped/disabled.
- List deleted video files only if useful.
- Confirm hardware cleanup and no-new-video verification.
- Include the restarted process/session handle if it is still running.

Do not summarize unrelated experiment details, PR-style history, or stale run IDs.
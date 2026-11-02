# Pause an active ViPSA grid job safely

Session-derived operational pattern for pausing an in-progress ViPSA grid/protocol run.

## Trigger

Use when the user asks to pause/stop the current ViPSA job, grid run, or active device batch.

## Procedure

1. Identify and stop the tracked active background process for the run, if one exists.
2. Pause any recurring reporter/watchdog cron job associated with the same run so it does not continue posting stale progress.
3. Perform electrical/mechanical cleanup through PUDA machines:
   - `keithley-2450`: turn output off, abort measurement.
   - `keysight-b2902b`: turn output off, abort measurement.
   - `keithley-707b`: `open_all`, then verify `get_closed_channels` is `nil` or otherwise empty.
   - `light`: turn off unless the user explicitly asked to leave illumination on.
4. If `run_id_mismatch` appears during cleanup, reset the affected machine and retry the cleanup command.
5. Verify machine state after cleanup: all involved ViPSA machines should be `idle` with `run_id: null`.
6. Report concise state, including:
   - stopped process/session id if known,
   - paused cron job id/name if any,
   - cleanup verification results,
   - last completed device and any device left in `started`/partial state.

## Pitfalls

- Do not only kill the process; the instruments and switch matrix must be made safe and verified.
- Do not leave the reporter cron enabled after pausing a run; it can continue to deliver misleading progress messages.
- A `run_id_mismatch` is usually cleanup state drift, not a reason to stop cleanup. Reset the affected machine and retry.

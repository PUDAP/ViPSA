# Explicit redo boundary and pause with unverified cleanup

Session-derived corrections for long ViPSA grid continuations.

## Trigger

Use when the user says wording like:

- `do not skip measurements`
- `re-do the measurements from device N`
- `redo from N`
- `pause` during an active grid run

## Explicit redo boundary rule

If the user names a redo/restart device number, that device number is authoritative. Do **not** reinterpret the request as “start from the first device without `DONE.json`” or let the runner's existing `DONE.json` filter choose an earlier/later device.

Required pattern:

1. Stop any active runner/watcher if needed and clean up/verify machines before patching the restart.
2. Compute traversal order and find the user-specified boundary device in that order.
3. Archive or delete all device folders at and after that traversal boundary that could contain `DONE.json` or stale artifacts.
4. Prune `summary.partial.json` at the same traversal boundary.
5. Patch the continuation runner so `START_AT_DEVICE=<user device>` and any `DONE.json` skip filter cannot skip the requested device.
6. Compile/validate the runner.
7. Launch as a tracked background process and verify the first log line and `device_N/summary.json` show the requested device actually started.

If a different unfinished device exists before the requested boundary, preserve it as partial/unfinished unless the user explicitly asks to backfill it now. Do not silently choose it over the user's redo boundary.

## No-skip override semantics

For an explicit no-skip request, contact/health gates should become record-only metadata unless there is a hard instrument/control fault or an immediately dangerous condition that cannot be bounded. DCIV and pulses should still be attempted for each requested device, and the summary should record warnings such as open-like, weak-contact, over-current, short-like, compliance-limited, or recovery attempts.

## Pause during grid run

When the user says `pause`:

1. Kill/stop the tracked grid process immediately.
2. Pause the matching reporter cron job so stale progress messages stop.
3. Inspect logs and artifacts to report the last completed device and any partial `started` device.
4. Run electrical cleanup: Keithley output off/abort, Keysight output off/abort, 707B `open_all` + `get_closed_channels`, light off unless requested otherwise.
5. Verify all six ViPSA machines idle/null if control-plane responses work.

If PUDA/NATS state/control responses time out during cleanup, report cleanup as **unverified** rather than safe/complete. Still report what is known from artifacts, e.g. whether the partial device had only alignment files/log events and no approach/DCIV/pulse artifacts. Do not claim SMU outputs off, 707B open/nil, or lights off without a live response or other direct verification.
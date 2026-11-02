# Grid measurement pause and cleanup (2026-06-22)

Reusable pattern from pausing a long 8x8 ViPSA grid measurement mid-run.

## When to use

Use when the user says to pause/stop a running grid or long measurement script, especially if it is a tracked background Python process coordinating Zaber/stage/light/Keithley/707B/Keysight.

## Procedure

1. Stop the active grid process, not just the current PUDA command. If it was launched as a tracked background process, poll/kill the tracked process; otherwise identify the Python script PID and terminate it.
2. Run electrical cleanup immediately:
   - Keithley output off / abort/reset if applicable.
   - Keysight output off / abort/reset if applicable.
   - Keithley 707B `open_all()` then `get_closed_channels()`.
3. Verify final machine states for all six ViPSA machines:
   - `keithley-2450`
   - `keithley-707b`
   - `keysight-b2902b`
   - `light`
   - `stage`
   - `zaber`
4. For `keysight-b2902b`, a reset request can time out while still clearing the edge back to `idle` with `run_id: null`; verify by reading state after the reset attempt before declaring it blocked.
5. Verify the switch matrix is safe independently of state: `get_closed_channels()` should report `nil` / no closed channels.
6. Inspect the run directory summaries to report where the run stopped:
   - completed devices
   - error devices
   - current/started device at pause time
   - run folder path

## Reporting standard

Keep the report concise and safety-oriented:

- say the measurement was paused/stopped;
- list the stopped process if known;
- list final idle/`run_id: null` verification for the six-machine set;
- explicitly report 707B closed channels as `nil` / none;
- report the last completed device and any device that was `started` when paused;
- do not include transient run IDs unless needed to debug a mismatch.

## Pitfalls

- Do not report “paused” before verifying outputs/routes are safe; stopping the Python process alone is insufficient.
- Do not assume a reset timeout means cleanup failed. Re-read the machine state and route state.
- Do not spam approach-loop details while pausing/resuming grid runs; users want device-level progress and final safety state.
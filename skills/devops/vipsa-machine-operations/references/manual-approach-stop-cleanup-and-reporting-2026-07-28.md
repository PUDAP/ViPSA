# Stop during manual approach: cleanup and reporting

Use when the user sends a terse `stop` while a standalone ViPSA approach or approach-like process is running.

## Procedure

1. Kill the tracked approach process and verify no `vipsa_approach.py`, grid, or current-device runner remains.
2. Do not stop at `Operation interrupted.` Immediately run a cleanup protocol:
   - `keithley-2450.set_output(false)` and `abort_measurement()`
   - `keysight-b2902b.set_output(false)` and `abort_measurement()`
   - `keithley-707b.open_all()` then `get_closed_channels()`; expected `nil`
   - `light.turn_off()` unless explicitly told to leave on
   - `stage.abort_motion()` and `stage.get_current_position()`
3. Verify all six ViPSA machines are `idle` with `run_id: null`.
4. Report concisely: process stopped, cleanup verified/unverified, 707B channel result, final stage readback, and any remaining runner processes.

## Reporting pitfall

A terse `stop` is a safety-critical operation, not just a process-interrupt request. The final user response must include cleanup verification. If cleanup cannot be verified, explicitly say `cleanup unverified` and name the blocker.

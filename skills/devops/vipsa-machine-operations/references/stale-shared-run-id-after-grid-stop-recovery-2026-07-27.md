# Stale shared run ID after stopped grid/direct-runner operations (2026-07-27)

## Trigger

Use this when a ViPSA grid/direct runner has been killed or stopped and later normal PUDA protocol operations fail at START with a message like:

```text
START command failed for machine light: cannot start, <old-run-id> is currently running
```

In the observed case, `light`, `stage`, and `zaber` all reported `state: idle` but retained the same stale non-null `run_id` from an earlier grid/direct runner. This blocked an unrelated Keithley/707B protocol precheck because the protocol also included `light.turn_off`.

## Recovery pattern

1. Do **not** assume the requested electrical/physical operation ran if START failed.
2. Check state for `light`, `stage`, and `zaber`; treat `idle + run_id != null` as stale and requiring cleanup.
3. `puda machine reset <machine>` may clear the stale run id but leave the machine in `error` with `Unknown or restricted command: reset`. Re-read state after reset rather than trusting the reset command exit code.
4. Recover each affected machine with a harmless full-metadata PUDA protocol:
   - `light`: `initialize(startup_command="off")` then `turn_off()`
   - `stage`: `get_current_position()` only
   - `zaber`: `get_current_position(units=null)` only
5. Verify each affected machine returns `idle` with `run_id: null`.
6. Retry the originally requested operation only after the stale states are cleared.

## Reporting

Report the blocked first attempt separately from the successful retry. Say explicitly that no DCIV/stress/motion occurred during the START-blocked attempt, then report the recovery and retry artifacts.

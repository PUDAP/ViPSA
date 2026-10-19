# Keysight edge restart restored multi-command protocol handling (2026-06-24)

## Context
A `keysight-b2902b` + `keithley-707b` low-bias resistance workflow previously failed when more than one Keysight command was sent in a single PUDA protocol/run. The first Keysight command succeeded, then a later Keysight command returned:

```text
Send START command to start a run before sending commands
```

Splitting Keysight operations into one-command protocols worked around the issue.

## Verified recovery pattern
After the user restarted the Keysight edge, rerun the full combined protocol instead of assuming the split-protocol workaround is still required:

1. Verify `keysight-b2902b` and `keithley-707b` are idle with `run_id: null`.
2. Run a combined protocol with:
   - `keysight-b2902b.set_output(false)`
   - `keithley-707b.connect_keysight_smu()`
   - `keysight-b2902b.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=1, reset=True)`
   - `keysight-b2902b.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`
3. Parse `V_meas (V)` and `I_meas (A)`, compute `R = abs(V/I)`.
4. Verify cleanup: Keysight output off, 707B closed channels `nil`, both machines idle/null run id.

## Evidence from the session
The post-restart combined protocol completed all 6 commands successfully. Measurement at 10 mV returned about `3.2e-11 A` (`~312.5 MΩ`), 707B closed channels were `nil`, and both machines were idle with `run_id: null` afterward.

## Durable lesson
When the Keysight multi-command START-state pitfall appears, a restarted edge can clear stale/bad subscriber/run-state. After restart, explicitly retest the combined protocol and only keep using split protocols if the same error persists.
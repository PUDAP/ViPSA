# Keysight 10 mV resistance read: split-protocol workaround for START-state loss

Session lesson from a live ViPSA Keysight B2902B resistance check.

## Symptom

A full metadata PUDA protocol that coordinated `keysight-b2902b` and `keithley-707b` validated successfully and began executing:

1. `keysight-b2902b.set_output(enabled=false)` succeeded.
2. `keithley-707b.connect_keysight_smu()` succeeded and returned route channels `1A02`, `1B04`.
3. The next `keysight-b2902b.hold_voltage_measure_current(...)` failed with:

```text
Send START command to start a run before sending commands
```

The same issue could also appear on a cleanup protocol containing multiple Keysight commands: the first Keysight command succeeded, then the second Keysight command failed with the same START-state error. `puda machine state` could still show `idle` / `run_id: null` afterwards.

This is a PUDA control-path/run-state issue, not a valid electrical measurement failure.

## Working workaround

For Keysight low-bias resistance checks during this failure mode, split the operation into short protocols so each Keysight command gets its own fresh START/COMPLETE lifecycle:

1. Verify `keysight-b2902b` and `keithley-707b` idle.
2. Run a route/setup protocol:
   - `keysight-b2902b.set_output(enabled=false)`
   - `keithley-707b.connect_keysight_smu()`
3. If a combined read fails with START-state loss, do not keep retrying the same multi-machine protocol.
4. Run a **Keysight-only** read protocol:
   - `keysight-b2902b.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=1, reset=true)`
5. Run a **Keysight-only** output-off protocol:
   - `keysight-b2902b.set_output(enabled=false)`
6. Run a **707B-only** cleanup/verify protocol:
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`; expected result `nil`
7. Verify final machine states are `idle` with `run_id: null`.

## Parsing/reporting

For Keysight `hold_voltage_measure_current`, parse current from `response.data.result[0]["I_meas (A)"]` or `"Current (A)"`; parse measured voltage from `"V_meas (V)"` if present. Compute resistance from measured values when available:

```text
R = V_meas / I_meas
```

In the live example, `V_meas=0.0099989 V`, `I_meas=1.34e-10 A`, so `R≈7.46e7 Ω` (`74.6 MΩ`). Do not store this one-off value as a reusable constant; it only demonstrates the calculation and output shape.

## Safety note

If the cleanup command in a multi-command Keysight protocol fails with the START-state error, force output off in a separate one-command Keysight protocol before reporting success, then open/verify 707B separately.
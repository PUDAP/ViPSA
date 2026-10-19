# Pulse reset followed by compliance-limited resistance check (2026-06-10)

## Context

After a DCIV/reset-compliance search and a quick Keysight pulse screen, the DUT appeared very high-R / weak-HRS under non-stressing Keithley reads, but the first mild pulse screen (`±1.2 V`, `1 ms`, `10 µA` compliance) drove both read-after-SET and read-after-RESET to the Keysight `10 µA` compliance limit with no separation.

The user then requested: apply a single `-2 V` reset pulse and check resistance.

## Procedure that worked

1. Force both SMU outputs off before route changes:
   - `keysight-b2902b.set_output(false)`
   - `keithley-2450.set_output(false)`
2. Route DUT to Keysight via 707B:
   - `keithley-707b.connect_keysight_smu()`
3. Apply one reset pulse with bounded stress:
   - `keysight-b2902b.run_voltage_pulse_train(voltages=[-2.0], current_compliance=10e-6, pulse_width_s=0.001, reset=True, current_autorange=False)`
4. Force Keysight output off before switching routes.
5. Route DUT to Keithley:
   - `keithley-707b.connect_keithley_smu()`
6. Check resistance with paired low-bias reads, not just one naive `R=V/I` point:
   - `0 V`, `±10 mV`, `±50 mV`, `±100 mV`
   - Keithley read compliance: `1 µA`
   - Use several reads per bias and report medians.
7. Cleanup:
   - both SMU outputs off
   - `keithley-707b.open_all()`
   - verify `get_closed_channels == nil`
   - verify idle states when possible.

## Result pattern

The `-2 V`, `1 ms`, `10 µA` reset pulse itself hit compliance (`~9.999 µA`).

Afterward, Keithley low-bias reads also pinned at the `1 µA` read compliance for `±10 mV`, `±50 mV`, and `±100 mV`:

- `+10 mV`: `~+1.000 µA` → naive apparent `~10 kΩ`
- `-10 mV`: `~-1.000 µA`
- `±10 mV` differential resistance: `~10 kΩ`
- `±50 mV` and `±100 mV` differential values scaled as compliance-limited artifacts (`~50 kΩ`, `~100 kΩ`) because current remained clamped near `1 µA`.

## Interpretation rule

When a reset pulse and the follow-up resistance check both hit compliance, do **not** report the apparent resistance as a clean ohmic value. Report it as compliance-limited / short-like, e.g.:

> `+10 mV` read reached `1 µA` compliance, so the apparent resistance is `≤10 kΩ` at this read limit, not a trustworthy linear resistance.

If all paired low-bias reads clamp to the same current limit, the resistance is bounded by the lowest-voltage read compliance rather than extracted from the larger-bias pair slopes.

## Reporting style

For the user, keep the report terse:

- Pulse settings and whether pulse hit compliance.
- Resistance/read settings and whether reads hit compliance.
- Apparent low-bias bound (`≤10 kΩ at 10 mV with 1 µA read compliance`).
- Cleanup verification: outputs off, 707B open/all channels nil, machines idle/idle stream.

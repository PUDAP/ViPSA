# Keysight SET/RESET endurance: 500-cycle pulse train and read-compliance drift (2026-06-29)

## Context

Live ViPSA pulse measurement on the current contacted PEA-based memristor device after a successful `+1.0 V` SET compliance ladder. The user requested a pulsed measurement with:

- SET pulse: `+1.0 V`
- RESET pulse: `-1.0 V`
- Read pulse: `+0.05 V`
- Pulse width: `50 ms`
- Cycles: `500`
- Standard plot: `read_after_set` and `read_after_reset` vs cycle

The run used the currently effective high SET compliance condition, `1e-4 A`, because the immediately preceding compliance ladder showed strongest positive retained read current at that compliance.

## Direct-NATS execution pattern

Use the Keysight + 707B direct-NATS pattern when the normal CLI/protocol path is unreliable:

1. Start a coordinated run on `keysight-b2902b` and `keithley-707b`.
2. Force Keysight output off before routing.
3. Route the DUT through the 707B using `connect_keysight_smu`.
4. Build one long voltage list in cycle order:

```text
[SET, READ_AFTER_SET, RESET, READ_AFTER_RESET] * cycles
```

For the 2026-06-29 run this was:

```text
[+1.0, +0.05, -1.0, +0.05] * 500
```

5. Execute with `keysight-b2902b.run_voltage_pulse_train` using:

```json
{
  "voltages": [...],
  "current_compliance": 1e-4,
  "pulse_width_s": 0.05,
  "reset": true
}
```

6. Expect `4 * cycles` returned current values. For 500 cycles, expected count is `2000`. Before submitting long native lists, ensure the driver VISA timeout exceeds the empirically observed total acquisition time with margin. A Keysight `*OPC?` timeout can occur after an unknown partial/full stress sequence; the driver's `finally` may turn output off but return no records. If subsequent trace-buffer recovery yields only invalid `9.91e37` sentinels, treat the physical pulse count as unrecoverable and do not automatically repeat the train without explicit authorization for possible duplicate stress.
7. Parse by pulse index into phases:
   - `set`
   - `read_after_set`
   - `reset`
   - `read_after_reset`
8. Save CSV with cycle, phase, commanded voltage, signed current, absolute current, read resistance estimate, compliance, and estimated elapsed time.
9. Plot:
   - log-scale `|read_after_set|` and `|read_after_reset|` vs cycle
   - optional log-scale ratio `|I_read_after_set| / |I_read_after_reset|` vs cycle
   - optional histogram of read-current distributions
10. Cleanup and verify:
   - Keysight output off
   - 707B `open_all`
   - 707B `get_closed_channels == nil`
   - complete both machine runs

## Concrete observed outcome

The 2026-06-29 run completed successfully:

- Returned points: `2000 / 2000`
- Runtime: about `111 s`
- `read_after_set` median `|I|`: `1.694425e-5 A`
- `read_after_reset` median `|I|`: `9.4745e-7 A`
- Median ratio: `1.37x`
- Cycles with ratio `>= 2`: `160 / 500`
- Cycles with ratio `>= 5`: `100 / 500`
- Cycles with ratio `>= 10`: `79 / 500`

Important drift/safety observation:

- Both read states drifted upward during cycling.
- Some `+0.05 V` read pulses reached the `100 µA` compliance.
- This should be reported as the device becoming very conductive / short-like during endurance, not as clean durable SET/RESET switching.
- RESET at `-1 V` did not consistently restore a clean HRS.

## Reporting guidance

For future similar requests:

- Do not call the condition optimized or robust just because `read_after_set` is high.
- Explicitly report if either read state approaches or hits read/stress compliance, even if the pulse train technically completes.
- Emphasize separation metrics and drift:
  - median read-after-SET current
  - median read-after-RESET current
  - median and max ratio
  - counts above ratio thresholds (`>=2`, `>=5`, `>=10`)
  - whether read currents trend toward compliance
- If low-voltage reads hit compliance during endurance, interpret as over-conductive/short-like behavior and recommend lowering compliance, lowering SET amplitude, increasing RESET strength cautiously, or using shorter screening batches before another long run.

## Artifact naming pattern

Recommended run folder:

```text
runs/keysight_pulsed_set_reset_<set>v_<cycles>cycles_<timestamp>/
```

Recommended files:

```text
keysight_set1_resetm1_read0p05_500cycles.csv
keysight_pulsed_set_reset_1v_500cycles_reads.png
keysight_pulsed_set_reset_1v_500cycles_hist.png
summary.json
responses.jsonl
```

# Integrated dual-SMU electrical calibration (2026-09-23)

## Scope

Validated the assembled ViPSA DC path, not just instrument specifications:

`SMU -> Keithley 707B -> probe/clip fixture -> return`

Both SMUs were routed sequentially with output-off, `open_all`, and `get_closed_channels == nil` between routes.

## Calibration order

1. Matrix-open baseline.
2. Routed probe/clip open baseline.
3. Repeated routed-open baseline in reverse instrument order.
4. Routed short.
5. 100 kOhm, 1 MOhm, and 100 MOhm standards.
6. Final routed-open closure after fixture handling.

Use paired positive/negative measurements to suppress current offset. For high resistance, subtract the reproducible routed-open conductance, not only the zero-bias current.

## Open-path protocol

- Biases: `0, +/-10 mV, +/-50 mV`.
- 100 samples per bias.
- NPLC 1, 0.5 s settling, fixed 1 uA range/compliance.
- Repeat with reversed SMU order to test order/settling effects.

Observed routed-open conductance was reproducible within 1.05% (Keithley) and 3.55% (Keysight). Matrix-open leakage was much lower, proving the downstream cable/probe/clip path dominated.

A post-calibration closure initially showed nA-to-hundreds-of-nA transients and was rejected. After physical stabilization/discharge, closure recovered pA-scale behavior; fitted leakage slopes changed by -5.45% and -3.41% relative to pre-calibration means. Preserve rejected closure runs as audit evidence.

## Short-path protocol and driver pitfalls

A direct crocodile-to-crocodile short across probe HI and LO was measured with paired polarities.

- Keithley scalar `hold_current_measure_voltage` returned `V_meas=None` and anomalous current; do not use that primitive for short resistance until the driver is fixed.
- Keithley native voltage-list requests above about 512 points returned only 513 records. Split acquisition into <=100-point batches.
- Keysight native voltage-list mode timed out on 100 repeated points. Use bounded `hold_voltage_measure_current` batches (for example 5 x 20 reads per level).
- Use measured voltage and measured current at compliance to calculate paired differential resistance.

Final routed short medians:

- Keithley 2450: 1.840 Ohm.
- Keysight B2902B: 1.656 Ohm.

## Reference-resistor protocol

For each resistor, use 100 reads per bias in bounded 20-read batches at `0, +/-10, +/-50, +/-100, +/-500 mV, +/-1 V`. Use current range/compliance appropriate to the resistor. Compute

`Rdiff = (V+ - V-) / (I+ - I-)`.

For the 100 MOhm standard, correct conductance as

`Gdevice = Gmeasured - Grouted_open`, then `Rdevice = 1/Gdevice`.

Corrected medians:

| Standard | Keithley 2450 | Keysight B2902B |
|---|---:|---:|
| 100 kOhm | 99.996 kOhm | 100.012 kOhm |
| 1 MOhm | 1.000339 MOhm | 1.000477 MOhm |
| 100 MOhm | 100.060 MOhm | 99.882 MOhm |

The raw 100 MOhm values were 94.462 MOhm and 88.840 MOhm, demonstrating that routed-open correction is essential at high resistance but negligible near 100 kOhm to 1 MOhm.

## Acceptance and reporting

- Separate functional integrated-system validation from accredited traceable calibration.
- Preserve raw, rejected, and corrected datasets.
- Require a final routed-open closure within a predefined slope-change threshold (10% was used here) and no >1 nA transient excursions.
- Always verify both outputs off, 707B channels `nil`, light off, and idle/null machine states.

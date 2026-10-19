# Integrated electrical-path calibration: open, short, and dual-SMU baselines

## Scope

Use this workflow to calibrate the complete ViPSA electrical path—including SMUs, 707B routes, cables, probe connection, crocodile-return lead, and fixture—before testing precision resistors or devices. Preserve raw records and distinguish matrix-open, routed-open, and routed-short configurations.

## Required order

1. **Matrix open:** both SMU outputs off, `707B.open_all()`, verify closed channels `nil`.
2. **Routed open:** close one SMU route at a time while probe and crocodile return remain electrically separated.
3. **Routed-open replicate in reverse SMU order:** separates reproducible downstream leakage from time/order effects.
4. **Routed short:** probe/HI and crocodile/LO contact the same clean copper or gold conductor; do not clamp directly onto the probe tip.
5. Only after open and short baselines pass, connect the resistor ladder (typically 1 MΩ first, then 100 kΩ and 100 MΩ).

Never route both SMUs simultaneously. Turn lights off, avoid stage motion, and verify output-off/open-all cleanup between instruments and at the end.

## Open-circuit acquisition

A validated matched protocol is:

- biases: `0, +10 mV, -10 mV, +50 mV, -50 mV`;
- 100 readings per bias per SMU;
- 0.5 s initial settling;
- NPLC 1 where supported;
- fixed 1 µA current range and compliance;
- save measured current, timestamps, mean, median, SD, RMS, peak-to-peak, and drift.

Treat apparent open-path resistance as a leakage-slope metric, not as a real resistor measurement. A routed-open reference includes downstream cables/probes/clip/fixture; a matrix-open reference characterizes only the upstream instrument/matrix-input path.

Session result: routed-open leakage was reproducible under reversed SMU order (Keithley slope changed about -1.05%; Keysight about +3.55%). Routed zero offsets repeated within roughly 4–4.5 pA. Matrix-open apparent leakage was much smaller than routed open, isolating a stable downstream contribution.

## Short fixture

Use a clean conductive coupon:

```text
SMU HI -> 707B -> probe tip -> clean copper/gold conductor -> crocodile clip -> SMU LO
```

Do not clip directly onto the tip. The short must include the actual probe, clip, cables, and route.

### Validated short-measurement method

Prefer paired bipolar measurements and compute:

`Rdiff = (Vmeas+ - Vmeas-) / (Imeas+ - Imeas-)`

A working conservative method for both instruments is voltage sourcing at `0, ±1 mV, ±5 mV, ±10 mV` with 100 µA compliance and measured voltage/current retained at each point.

- For Keithley native list acquisition, use independent 100-point batches per level rather than one very long list; this avoids trace-buffer truncation and leaves auditable per-level raw files.
- For Keysight, bounded scalar hold-voltage batches (for example 5 batches × 20 readings per level) are a reliable fallback when long native-list execution times out. Preserve measured voltage and current so compliance-limited points still yield differential resistance.
- If a current-source primitive omits measured voltage, do not infer resistance from commanded current alone; switch to a validated method that returns both measured quantities.

Session result: the assembled short path measured about 1.840 Ω on the Keithley and 1.656 Ω on the Keysight, stable across ±1, ±5, and ±10 mV pairs. The absolute difference was about 0.184 Ω. This passed a provisional <100 Ω continuity criterion while retaining the instrument difference as calibration evidence.

## Precision-resistor setup

Connect each resistor between probe/HI and crocodile/LO on a clean insulating fixture. Use 1 MΩ first because its expected signals (10 nA at 10 mV, 50 nA at 50 mV, 100 nA at 100 mV) are comfortably above the routed-open pA baseline. For 100 MΩ, avoid breadboards and finger contamination; use PTFE/high-insulation support and shielding because fixture leakage can be a material fraction of the signal.

## Data and exclusions

- Keep raw failed/partial runs, but mark them invalid or partial; do not merge them into calibration fits.
- Parser or buffer failures are not electrical evidence.
- A successful command is not a valid calibration point unless the expected record count and measured fields are present.
- Preserve instrument-specific settings when capabilities differ; label unsupported NPLC or integration settings instead of pretending the protocols are identical.

## Final verification

Require:

- both SMU outputs explicitly off;
- 707B `open_all` and closed channels `nil`;
- light off;
- all relevant machines idle with null run IDs;
- plots/CSV/JSON regenerated from saved raw data without rerunning hardware.
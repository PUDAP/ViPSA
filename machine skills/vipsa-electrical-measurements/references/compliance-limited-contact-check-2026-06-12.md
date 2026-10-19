# Compliance-limited contact check after over-contact or Z retract

## Context

After an approach/alignment chain and subsequent Z movement, the user asked whether the device was in contact. A non-destructive Keithley check at `10 mV` with `1 µA` read compliance returned repeated readings near `9.9999e-7 A`, i.e. right at the read compliance limit. Cleanup (`set_output(false)`, `keithley-707b.open_all`, `get_closed_channels`) succeeded and the stage/SMU/switch were idle.

## Durable interpretation

A 10 mV contact check that hits the configured read compliance is strong evidence of electrical contact, but it should be reported as **short-like / over-contacted**, not as a precise ohmic resistance.

Recommended wording:

```text
Device is in contact, but very strong / short-like.
10 mV read hit 1 µA compliance, so apparent resistance is ≤ ~10 kΩ rather than a precise 10 kΩ value.
```

Do not proceed to forming DCIV or Keysight pulses from this state unless the user explicitly asks to stress a short-like contact. A safer next action is to retract Z by a deliberate amount, then re-check low-bias resistance.

## Recommended protocol shape

Use a single PUDA protocol for the read and cleanup:

1. `keithley-2450.set_output(enabled=false)`
2. `keithley-707b.connect_keithley_smu()`
3. `keithley-2450.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=3, reset=true)`
4. `keithley-2450.set_output(enabled=false)`
5. `keithley-707b.open_all()`
6. `keithley-707b.get_closed_channels()`

Then verify `keithley-2450`, `keithley-707b`, and `stage` are idle. Preserve the distinction between:

- **Contact present**: current clearly above nA thresholds.
- **Short-like/over-contacted**: low-bias read reaches compliance.
- **Open/high-HRS**: pA/sub-nA reads with weak or no voltage scaling.

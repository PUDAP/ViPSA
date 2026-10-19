# Post-DCIV low-bias health and 100 mV resistance check — 2026-06-15

Use this when a device has just undergone aggressive/override DCIV and the user asks whether it is shorted/perma-SET or asks for resistance at a higher non-stressing probe voltage.

## Pattern

1. Route DUT to Keithley with output off first and use a guarded read compliance, typically `1e-6 A` unless the user specifies otherwise.
2. For short/perma-SET screening, read multiple low biases rather than relying on a single point:
   - `0 V`
   - `±10 mV`
   - `±50 mV`
   - optionally `±100 mV` if requested or needed.
3. Classify short/perma-SET only when low-voltage current is high or compliance-limited. pA/sub-nA readings at these biases are **not** shorted; report as high-resistance / weak-contact-like / not retained.
4. If the user asks for resistance at `100 mV`, include `0 V`, `+100 mV`, and `-100 mV` reads and compute:
   - naive `R+ = 0.1 / |I(+100 mV)|`
   - naive `R- = 0.1 / |I(-100 mV)|`
   - offset-corrected one-sided estimates: `0.1 / |I(+100)-I(0)|` and `0.1 / |I(-100)-I(0)|`
   - paired differential estimate: `0.2 / |I(+100)-I(-100)|`
5. Prefer the paired differential estimate when zero-bias offset is comparable to the measured current.
6. Always cleanup: `set_output(false)`, `keithley-707b.open_all()`, `get_closed_channels() == nil`, then verify machines are idle.

## Reporting language

- If all readings are pA/sub-nA and far from compliance: "not shorted / not perma-SET right now".
- If naive positive and negative resistances disagree strongly because one polarity is near the offset/noise floor, call that out and report the paired differential resistance as the best estimate.
- For compliance-limited reads, report resistance as a bound, not a precise ohmic value.

## Concrete observed example

After an override negative-first 10-cycle DCIV that had ended compliance-limited at low read voltage, a later low-bias health check relaxed back to pA/sub-nA and was not shorted. A requested `100 mV` check measured roughly:

```text
I(0 V)       ≈ 7.71e-11 A
I(+100 mV)  ≈ 1.50e-10 A
I(-100 mV)  ≈ -2.98e-12 A
```

Naive resistances were polarity-asymmetric (`~665 MΩ` vs `~33.6 GΩ`), but offset-corrected and paired differential estimates clustered around `~1.3 GΩ`. Report this as very high resistance / weak-contact-like, not shorted.

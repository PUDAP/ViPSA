# Alive vs shorted low-bias Keithley check — 2026-06-09

## Trigger

Use when the user asks whether the current ViPSA DUT is still alive, open, or shorted after DCIV/pulse stress, and a full stress sweep is unnecessary or potentially harmful.

## Non-stressing check pattern

1. Use Keithley 2450 for low-bias voltage-hold/current reads.
2. Start with `0 V` using `reset: true` to capture zero-bias offset.
3. Measure paired small biases with low compliance, e.g.:
   - `+0.01 V`, `-0.01 V`
   - `+0.05 V`, `-0.05 V`
   - `+0.10 V`, `-0.10 V` if safe/useful
4. Use a low compliance such as `1e-6 A` unless the user specifies otherwise.
5. Take multiple reads per bias and report medians.
6. Compute differential conductance from paired medians:

```text
G_pair = (I(+V) - I(-V)) / (2V)
R_pair = 1 / G_pair
```

This is more meaningful than naive `R = V/I` when zero-bias offset is tens of pA and comparable to the biased current.

## Interpretation pattern

- **Hard short / low resistance**: high current at small bias, current near compliance, or resistance in low-ohm/kΩ range depending on context.
- **Not shorted, high resistance / open-like**: sub-nA low-bias currents, no compliance hits, paired differential resistance in MΩ–GΩ+ range.
- **Open/poor contact vs true HRS**: if current is at the pA noise floor and voltage scaling is weak, phrase as `very high resistance / open-like`; do not claim the device is physically open without contact/Z evidence.

## Concrete session outcome

A post-DCIV alive/short check used `0 V`, `±10 mV`, `±50 mV`, and `±100 mV` at `1 µA` compliance with 3 reads per bias. The max low-bias median current was about `1.17e-10 A`, no read approached compliance, and paired differential resistance was about:

- `±10 mV`: `~1.38 GΩ`
- `±50 mV`: `~1.45 GΩ`
- `±100 mV`: `~1.45 GΩ`

Recommended wording: `not hard-shorted; currently very high resistance / open-like`.

## Cleanup and report requirements

Always cleanup and verify:

- Keithley output off (`set_output(false)` or equivalent)
- 707B `open_all`
- `get_closed_channels` returns nil/empty
- include raw JSON/CSV path in the final concise report

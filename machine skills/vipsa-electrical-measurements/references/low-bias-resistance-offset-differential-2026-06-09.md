# Low-bias resistance check with pA zero-bias offset

Session pattern: user asked for a terse `check resistance` on the current ViPSA DUT.

## Safe measurement sequence

Use Keithley 2450 + 707B with low stress:

1. Verify `keithley-2450` and `keithley-707b` are idle.
2. `keithley-2450.set_output(enabled=false)`.
3. `keithley-707b.connect_keithley_smu()`.
4. Run a quick read, e.g. `hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=3, reset=true)`.
5. Cleanup in the same protocol when possible: `set_output(false)`, `open_all()`, `get_closed_channels()`.
6. Verify final idle state and `get_closed_channels == "nil"`.

Use the single-server NATS override (`--nats-servers nats://100.109.131.12:4222`) if the multi-server route hangs or stale cluster routes are suspected.

## Interpretation pitfall

At pA/sub-nA current levels, a simple `R = V/I` from a single low-voltage read can be misleading because the Keithley/DUT path may show a nonzero offset current at `0 V`.

If the 10 mV read is only tens of pA or otherwise close to the zero-bias offset, immediately run a non-stressing multi-bias diagnostic before reporting contact quality as a hard conclusion:

- `0 V`
- `+10 mV`, `-10 mV`
- `+50 mV`, `-50 mV`
- low compliance such as `1e-6 A` unless the user specified otherwise
- 3 reads per bias is sufficient for a quick check

Report both:

- naive single-bias `R = V/I`, clearly labeled as naive
- differential resistance from paired biases: `R_diff = (V_pos - V_neg) / (I_pos - I_neg)`

## User-facing wording

Keep it concise. Example:

```text
Resistance check done.

- 10 mV read: I ≈ <value>
- Naive R = V/I: ≈ <value>
- Multi-bias showed ~<value> zero-bias offset, so differential resistance is more meaningful:
  - ±10 mV differential: ≈ <value>
  - ±50 mV differential: ≈ <value>

Interpretation: very high resistance / weak-contact-or-high-HRS-like, not shorted.

Cleanup verified: Keithley output off, 707B open_all, closed channels nil, machines idle.
```

Avoid overclaiming open circuit from this alone. Stable voltage-scaled current suggests high-HRS; pA noise floor with little voltage dependence suggests open/poor contact or HRS beyond measurement sensitivity.
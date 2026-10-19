# Bounded DCIV forming when the device is weakly coupled / high-HRS

Session pattern from 2026-06-10: user asked to “run the best set of DCIV to properly form the filament” after a prior reset-compliance escalation found only weak contact/high-HRS behavior and no clean RESET.

## Safe forming strategy used

- Treat this as a bounded forming screen, not an unlimited escalation.
- Keep Keithley + 707B cleanup around every attempt:
  - `keithley-2450.set_output(false)` before routing.
  - `keithley-707b.connect_keithley_smu()`.
  - low-bias pre-read.
  - DCIV branch sequence.
  - low-bias post-read probes.
  - `keithley-2450.set_output(false)`.
  - `keithley-707b.open_all()`.
  - `keithley-707b.get_closed_channels()`.
- Use low-bias read probes as deciding evidence, not only compliance hits.

Concrete candidate sequence used:

1. Candidate 1:
   - SET compliance: `300 nA`
   - RESET compliance: `30 µA`
   - Sweep path: `0 → +1.2 → 0 → -2.0 → 0 V`
2. Candidate 2, only if candidate 1 is safe but not formed:
   - SET compliance: `1 µA`
   - RESET compliance: `100 µA`
   - Same sweep path.

## Stop condition learned

If the device current remains only pA–nA throughout the sweep and never approaches SET or RESET compliance, do **not** keep escalating voltage/current blindly. In this session:

- Pre/post `+10 mV` reads stayed near `55–65 pA`.
- Max sweep current stayed only `~1.3 nA`.
- No SET compliance hits.
- No RESET compliance hits.
- Post/pre low-bias ratio stayed near `1.1×`.

Interpretation: the device/contact was too weakly coupled or still very high-HRS; a larger stress would be blind stress rather than controlled forming. Stop, cleanup, and recommend a small contact improvement such as `+0.25 Z` followed by a low-bias check before another forming attempt.

## Reporting wording

Good concise wording:

> Ran bounded forming candidates at SET `300 nA → 1 µA` and RESET `30 µA → 100 µA`. The device did not form: current stayed pA–nA, max sweep current was only ~nA, and read probes changed by only ~1.1×. Cleanup verified. Recommend a small contact improvement before further stress.

Avoid saying the device is permanently dead or that forming failed because of material quality; the evidence only supports weak/open-like coupling or very high-HRS at the current contact.

## Plot/data handling

If measurement succeeded but plotting fails because system Python lacks `matplotlib`, do not rerun hardware. Regenerate plots from saved CSV/JSON using a local venv or any available plotting-capable environment, then attach the regenerated plot.

# Post-approach resistance check and requested split-compliance DCIV — 2026-06-06

## Context

After a Keithley-guided +Z contact approach, the user asked to check resistance at `0.01 V` and comment on whether contact looked proper, then requested a one-cycle split-compliance DCIV sweep with explicit path/point count/route/compliance.

## Resistance/contact read pattern

Command pattern used:

1. Ensure Keithley output off.
2. Route DUT to Keithley through 707B (`connect_keithley_smu`, observed channels `1A01`, `1B03`).
3. Run `hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=1, reset=True)`.
4. Compute `R = V / I`.
5. Cleanup: `set_output(false)`, `open_all`, verify `get_closed_channels() == nil`, final states idle.

Observed read:

- `V = 0.01 V`
- `I = 1.235446e-7 A`
- `R ≈ 80.9 kΩ`
- Not near `1 µA` compliance.

Interpretation language: this is electrically real/proper contact, not pA noise-floor/open. Because the current is slightly above the previous approach target window (`1e-8`–`1e-7 A` at 10 mV), describe it as slightly strong/low-resistance contact, but not hard-shorted or compliance-limited.

## User-requested split DCIV recipe

Requested parameters:

- Path: `0 → +1 → 0 → -2 → 0 V`
- Cycles: `1`
- Step: `0.05 V`
- Requested delay: `0.001 s`
- Points: `121` when vertices are not duplicated between segments
- Route: Keithley via 707B `1A01`, `1B03`
- Compliance:
  - PF `0 → +1`: `1e-6 A`
  - PB `+1 → 0`: `1e-6 A`
  - NF `0 → -2`: `1e-4 A`
  - NB `-2 → 0`: `1e-6 A`

Inclusive segment construction that yields 121 points without duplicate vertices:

```python
PF = seq(0.0, 1.0, +0.05)      # 21 points
PB = seq(0.95, 0.0, -0.05)     # 20 points, skip duplicate +1.0
NF = seq(-0.05, -2.0, -0.05)   # 40 points, skip duplicate 0.0
NB = seq(-1.95, 0.0, +0.05)    # 40 points, skip duplicate -2.0
```

Use one protocol per segment with `source_voltage_measure_current`, preserving row order and adding `segment`, `segment_index`, `point_index`, and `compliance_A` columns. Use `reset=True` only on the first segment unless the user asks otherwise.

## Plot recovery pitfall

If system Python completes the measurement and writes CSV/JSON but fails while importing `matplotlib`, do not rerun the electrical sweep. Regenerate plots from the saved JSON/CSV using a plotting-capable venv, then verify file sizes and row count.

When post-processing updates summary sanity fields, update both top-level `summary.valid_measurement` and `summary.flags.valid_measurement`; otherwise the JSON can contain a stale false flag even though 121 rows were collected.

## Example outcome and report wording

Observed result for this run:

- Points collected: `121`
- PF compliance hits: `4`
- PB compliance hits: `9`
- NF did not hit `0.1 mA`; max `~1.60e-9 A`
- NB did not hit `1 µA`; max `~1.57e-7 A`
- SET-like jump near `+0.60 V`, `4.21e-10 A → 1.19e-7 A`, about `2.45 decades`
- No clear RESET on the negative branch
- Approx PB/PF ON/OFF at `+0.1 V`: `~21×`

Report cleanup verification alongside artifacts: Keithley output off, 707B open all, closed channels `nil`, relevant machines idle. Attach log-scale DCIV plot, segment-colored plot, raw CSV, and summary JSON.

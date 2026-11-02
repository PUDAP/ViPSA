# Adaptive forming DCIV to randomized 5000-train pulse handoff (2026-06-23)

Use this reference for probabilistic-computing substrates where each device needs a forming DCIV, then a randomized pulse train for sigmoid extraction.

## DCIV/forming gate

Requested forming path:

```text
0 → +1.0 → +1.5 → 0 → reset-side voltage → 0
```

Starting compliance:

```text
SET/positive side:   1e-6 A
RESET/negative side: 1e-5 A
```

Adaptive branches:

- If a low-bias precheck indicates the device is already shorted or SET/LRS, run a truncated lower-voltage RESET sweep first with one order of magnitude higher reset compliance.
- If the negative-forward/reset side shows a sudden **upward** current jump, record the event and lower the reset-side voltage magnitude for subsequent devices.
- If no RESET is detected (no sudden downward current jump or no post-reset HRS recovery), run a reset-side recovery sweep with higher reset compliance.
- If the device appears permanently HRS/no meaningful current, first check contact mechanically with only a single `+0.5` Z step before escalating compliance.

## Vset extraction for pulse generation

Extract `Vset` from the DCIV using a conservative positive-branch log-current jump heuristic:

- Use ordered sweep rows; do not sort by voltage.
- Prefer the strongest positive `dlog10(|I|)` jump on the positive/forming branch.
- Treat `Vset` as unavailable if no clear jump is present; use a conservative fallback range only if the user has authorized continuing.

## Randomized pulse protocol

After successful DCIV:

- Switch the DUT to Keysight.
- If the DCIV likely left the device in SET/LRS, send 5 RESET pulses first.
- Generate randomized trains of:

```text
SET pulse → read pulse → RESET pulse → read pulse
```

- SET voltage range: `0.2 V` to `Vset + 0.2 V` in `0.05 V` increments.
- Pulse duration: `10 ms`.
- Initial pulse compliance: `10e-5 A` (`1e-4 A`).
- Continue until at least `5000` trains are completed or the device becomes permanently stuck in SET.
- If stuck in SET, wait `10 s` and apply 5 consecutive RESET pulses; stop only if recovery attempts fail or the device remains permanently SET.

## Permanent HRS behavior during pulses

If the pulse reads remain permanently HRS/no meaningful current:

1. Ensure contact is proper by moving stage Z forward/up by only a single `+0.5` step.
2. If behavior persists, increase pulse compliance rather than changing the randomized voltage ladder or reducing pulse count.

## Data products

Save these per device:

- `dciv.csv` and `dciv.json` with branch labels, compliance values, Vset/reset events, and adaptive next-reset-voltage recommendation.
- `randomized_pulse_plan.csv` containing the generated randomized pulse sequence.
- `randomized_pulse_results.csv` with every pulse/read current and compliance flag.
- `switching_probability.csv` and `randomized_pulse_summary.json` with threshold, probability table, and sigmoid fit.

Do not fabricate probabilities or fits if Keysight execution fails or returns too few currents; save partial raw data and report the hardware/control blocker.

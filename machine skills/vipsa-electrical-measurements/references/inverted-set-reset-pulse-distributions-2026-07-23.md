# Inverted SET/RESET pulse-read distributions

Use this when a `SET → read → RESET → read` experiment reports lower read current after nominal SET than after nominal RESET.

## First verify the comparison

- Compare the two reads only when they use the same read voltage, width, compliance, and timing.
- Inspect **signed** current as well as `|I|`; do not let an absolute-current plot hide a polarity or offset issue.
- Summarize paired medians and `median(I_after_RESET) / median(I_after_SET)` globally and at each SET-voltage level.
- Check whether the inversion is systematic across voltage levels or only caused by drift/outliers.

## Physical interpretation

For the usual convention, SET should produce LRS and therefore a larger same-bias read current than RESET. If the ordering is consistently reversed, the command labels are not verified physical states. Likely explanations include:

1. The nominal RESET polarity is potentiating/strengthening the filament for that electrode orientation.
2. The nominal SET pulse is too weak, has opposite effective polarity, or partially dissolves the filament.
3. The state is volatile and relaxes before the read.
4. The stronger reset amplitude causes transient ionic/capacitive current in the immediately following read.
5. Contact drift or asymmetric interfaces alter the polarity response.

Use DCIV as corroboration: `reset_detected=false` supports the conclusion that the nominal RESET operation did not produce HRS.

## Analysis pitfall: degenerate `P(switch)=1`

A one-direction ROC/Youden classifier that assumes `I_after_SET > I_after_RESET` can fail when the distributions are reversed. It may choose a threshold below both distributions, yielding:

- `P(switch) = 1`
- `reset_high_fraction = 1`

That is **not** 100% switching; it means both classes were marked high and there is no valid directional separation under the assumed labels.

Before computing switching probability:

1. Compute the median or location difference between the two read distributions.
2. Require the expected direction (`median_after_SET > median_after_RESET`) and positive separation quality (e.g. Youden > 0 by a declared minimum).
3. If reversed, mark `state_order = inverted` and `switching_probability_valid = false` under the original polarity convention.
4. Do not fit/report a SET-voltage sigmoid from a degenerate or inverted threshold.
5. Optionally evaluate the swapped physical-state hypothesis, but label it explicitly as `polarity_swapped_candidate`; never silently relabel commands.
6. Plot the two read distributions and annotate medians, ratio, direction, and validity.

## Reporting language

Preferred concise conclusion:

> The nominal RESET pulse produced the more conductive read state. The pulse labels describe command order, not verified HRS/LRS transitions. Because the distributions are inverted, the displayed 100% switching probability is invalid under the SET-high assumption.

## Session example

A device used `+0.20…+0.60 V` nominal SET pulses, `−1.2 V` nominal RESET pulses, and identical `+0.1 V` reads. Median read current was about `7.5 nA` after SET and `10.1 nA` after RESET (roughly `1.35×` higher after RESET), with the inversion present at every SET-voltage level. DCIV had `set_detected=true` and `reset_detected=false`. The appropriate classification was inverted/no valid SET–RESET separation, not `P(switch)=1`.

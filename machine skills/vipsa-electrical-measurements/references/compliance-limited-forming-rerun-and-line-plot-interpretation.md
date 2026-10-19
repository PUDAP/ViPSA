# Compliance-limited forming reruns and connected-line interpretation

## Trigger

Use this reference when a single-device forming/SET/RESET DCIV trace looks “weird,” especially when:

- the programmed endpoint is much larger than the maximum measured DUT voltage;
- a connected line jumps backward in measured voltage while current rises to compliance;
- the same device has already been formed or cycled;
- the test uses zero commanded dwell.

## Interpretation sequence

1. **Verify execution before interpreting physics.**
   - Returned record count must equal the planned list length.
   - Confirm the first/last measured/source points are near zero.
   - Confirm the intended extrema were represented unless current compliance legitimately prevented delivery.
   - For long negative lists, apply the 50-point SCPI chunk rule in `single-device-yield-form-set-reset-slow-sweep.md`; a truncated tail is an execution fault, not device behavior.

2. **Compare commanded and measured voltage separately.**
   - Before compliance, measured voltage should track commanded voltage.
   - At a SET/forming transition, DUT resistance can collapse and current can demand more than the limit.
   - The SMU then leaves voltage regulation and lowers actual DUT voltage to hold the current limit. The command may continue toward `Vmax` while measured DUT voltage stays far below it.
   - Report both the requested endpoint and maximum measured voltage; never say the DUT received the commanded endpoint after compliance engaged.

3. **Treat connected diagonals as sampled-state bridges.**
   - A line joining `(high measured V, pre-switch current)` to `(low measured V, compliance current)` connects two consecutive samples.
   - It does not prove the DUT continuously traversed every intermediate point.
   - Zero-dwell acquisition can undersample a fast transition, making the bridge especially long.

4. **Separate forward and return branches.**
   - Use connected lines with no dot markers for single-device DCIV/forming plots, preserving acquisition order.
   - Plot forward and return branches independently when diagnosing transitions so the endpoint turn does not create misleading bridges.
   - If the return branch remains compliance-limited down to low commanded voltage, report retained/highly conductive LRS-like behavior rather than a normal HRS return.

5. **Do not call a rerun virgin forming.**
   - After any earlier forming/SET/RESET stress, `forming_positive` is a programmed cycle label, not proof of first electroforming.
   - Compare prior and rerun pre-transition currents and compliance-onset command. Higher current or a lower onset on rerun indicates history-dependent modification, partial filament retention, or degradation.

6. **Keep contact instability as a labeled alternative.**
   - If the pre-test low-bias approach remained open-like or unstable, field-assisted contact changes can mimic forming.
   - Electrical evidence alone may not distinguish filament formation from probe/contact evolution. Say so explicitly rather than choosing one mechanism with certainty.

## Preferred plots

Default user-facing DCIV figure:

- connected lines, no point markers;
- signed current on a linear panel;
- `|I|` on a log panel;
- one trace per operation/cycle, in acquisition order.

When forming needs explanation, add a three-panel diagnostic:

1. commanded voltage vs `|I|`, with compliance line;
2. measured DUT voltage vs `|I|`, with forward/return separated;
3. commanded and measured voltage vs acquisition index, marking compliance onset.

## Reporting language

Prefer:

> At the transition, current reached compliance and the SMU reduced actual DUT voltage. The long connected segment joins two sampled states and is partly a visualization of an abrupt, undersampled transition. Because this device had already been stressed, this branch is a repeat positive-forming/SET-like cycle rather than virgin forming.

Avoid:

> The device was swept all the way to the commanded endpoint.

when measured voltage was compliance-clamped well below that endpoint.

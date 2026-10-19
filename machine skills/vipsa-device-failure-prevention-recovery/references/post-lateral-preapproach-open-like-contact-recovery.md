# Post-lateral pre-approach open-like contact recovery

## Trigger

Use after a safe lateral device move where Z was first retracted and only partially restored (a **pre-approach**), followed by a low-bias resistance check that is pA-scale/GΩ/open-like.

## Durable interpretation

A pre-approach is clearance recovery, not proof of probe contact. If the final Z remains retracted relative to the prior contacted position, a pA/GΩ check should be classified as **contact not yet established / very-high-resistance-like**, not immediately as a damaged DUT.

## Workflow

1. Confirm no prior approach, grid, or pulse runner is active.
2. Verify stage, Keithley 2450, and 707B are idle with cleared run IDs.
3. Preserve the low-bias resistance artifact and note the commanded/readback Z and lateral coordinates.
4. Turn illumination off unless the user explicitly latched it on.
5. Route the DUT to the Keithley and run a bounded live approach at `+10 mV`, `1 µA` compliance.
6. For the current ViPSA grid workflow, target **50–500 nA** before DCIV or pulse work. Use coarse `+0.5 Z` steps while clearly open-like, then minimum `0.25 Z` trimming at the contact edge.
7. If current exceeds the upper gate, retract in `-0.25 Z` increments and re-read. If it falls below the lower gate, allow bounded `+0.25 Z` recovery rather than oscillating indefinitely.
8. Stop at the configured maximum approach travel/attempt count if contact is not established. Do not form or pulse an open-like trace.
9. Always force Keithley output off, call 707B `open_all`, verify closed channels are `nil`, and report final stage position/current.

## Reporting

During a long bounded approach, provide compact progress only when useful: target window, latest current, cumulative Z motion, and whether the run is still below/in/above the gate. Final reporting must distinguish commanded motion from verified stage readback.

## Pitfalls

- Do not infer that the adjacent DUT itself is open merely because a check was made before completing contact approach.
- Do not use the older `10–100 nA` gate when the active ViPSA grid policy requires `50–500 nA`.
- Do not start a second approach runner when the first is still active.
- Do not report approach completion from script start or intended motion; require final current, stage readback, and cleanup evidence.

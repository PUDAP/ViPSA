# Adaptive forming-as-contact in C-pad memristor grids

This is a session-derived pattern for constrained multi-objective memristor optimization when a user explicitly authorizes forming sweeps as the contact detector.

## Geometry and alignment

- Match the vision model to pad geometry. Do not apply a complete-square detector to a C-shaped-pad grid.
- Infer a probe-occluded target from repeated C-pad centers and the actual visible probe tip.
- Convert pixel residuals with established axis-specific calibration; make bounded corrections and recapture.
- After one verified site, carry its aligned encoder offset by the user-confirmed pitch/directions, while retaining nominal coordinates separately and saving a fresh illuminated alignment frame per device.

## Low-stress forming-as-contact

1. Begin after verified cleanup, safe retraction, absolute X/Y travel, optical verification, and bounded pre-approach.
2. Use only the lowest forming tier during weak coupling. One prospective campaign used `0 → +4 V → 0`, `10 µA`, 50 mV steps.
3. Do not freeze Z merely because pA/nA current scales with voltage. If peak current is below the predefined meaningful-coupling gate, cleanup and advance the bounded Z increment.
4. A useful discovery gate is `peak |I| >= 100 nA` plus polarity-consistent response. Unlock a higher forming tier only after that gate and only if clean forming has not occurred.
5. Stop at the first clean event: three consecutive forward points at >=90% compliance, no low-voltage short flag, and no pre-transition >10× downward-current jump.
6. Never repeat a completed successful forming sweep.

Prospective examples formed only after deeper contact: one at Z `+30` on `+4 V/10 µA`; two at Z `+35` to `+40` after unlocking `+6 V/25 µA`. These observations motivate the policy but are not universal constants.

## Conditioning feasibility gate

- Fixed low-bias reads after every SET and RESET.
- Three consecutive directionally correct ON/OFF ratios >=5.
- Maximum/minimum ratio spread across the same three pairs <=2.5×.
- Do not round borderline failures into feasibility; `2.64×` remains outside a `2.5×` gate.
- Large conditioning ratios are not endurance or retention evidence.

## Runner correctness invariants

- An unmet forming gate must exit unconditionally before post-forming RESET or conditioning. Avoid compact one-line nested control flow where a `raise` is accidentally scoped to only one branch.
- Preserve every completed operation and resume from the first missing operation; uncertain stress is recorded and never silently replayed.
- Constant-bias records may have valid `I_meas` and `V_meas=None`; for read rows only, use commanded hold voltage with explicit provenance. Continue requiring measured voltage for sweep interpretation.
- Update the experiment knowledge record after every device: recipe, aligned position, forming/contact history, conditioning, objectives, failures, artifacts, learning, and exact next-device change.

## Reporting

For this user's long optimization campaigns, report in chat only after successful or scientifically interesting results, with a focused plot and cautious explanation. Keep routine negative attempts in raw artifacts and the wiki without repetitive progress prose.

A focused activation figure should show:

1. forming peak current versus Z and tier;
2. successful forming sweep with compliance/onset markers;
3. after-SET and after-RESET read currents by conditioning pair;
4. ON/OFF by pair with feasibility thresholds.

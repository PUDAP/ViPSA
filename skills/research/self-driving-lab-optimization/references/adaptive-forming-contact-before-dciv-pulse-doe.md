# Adaptive forming/contact before DC-IV and pulse DOE

Use this reference for constrained multi-objective RRAM optimization where forming and conditioning are irreversible preconditions and the same grid must support DC-IV and pulse campaigns.

## Separate experimental roles

Allocate devices before testing: activation/forming pilots, DC-IV DOE, pulse DOE, Pareto confirmation, and long endurance/retention reserve. Keep cycles nested within devices; never treat cycles as independent recipes.

## Forming/contact gate

- If forming is explicitly used as the contact detector, begin with the lowest stress tier at each bounded mechanical position.
- While peak response remains below a predefined meaningful-coupling gate, advance the bounded mechanical variable rather than sweeping all higher voltage/compliance tiers at every position.
- Unlock higher forming tiers only after meaningful coupling without a clean forming transition.
- Accept forming only with sustained compliance across consecutive forward points, correct polarity, complete records, and no large pre-compliance current collapse.
- Compliance attainment with repeated current collapse is an infeasible/unstable outcome, not success.
- Preserve failed/open/non-forming devices in the dataset; do not silently replace them.

## Conditioning feasibility

Use post-SET and post-RESET low-bias reads after every pair. Define convergence prospectively, for example:

- three consecutive directionally correct ratios;
- ratio above a minimum useful threshold; and
- bounded max/min spread across the accepted window.

Do not round borderline failures into feasibility. Large ON/OFF values with inverted early pairs or order-of-magnitude HRS drift are informative but not stable endurance evidence.

## DC-IV and pulse handoff

Only feasible activation outcomes enter assigned DOE recipes. For DC-IV, start with a short characterization block before endurance. For pulses, respect any single-compliance/single-width hardware coupling and treat it as a known input constraint. Long endurance and retention are conditional resource expenditures, not default steps for every candidate.

## Per-device learning loop

After every device:

1. Preserve raw data, metadata, cleanup evidence, and failure class.
2. Recompute focused metrics and generate a legible focused plot.
3. Append the device record to the campaign wiki/logbook.
4. Modify the next-device policy only at a safe boundary and only within approved constraints.
5. Continue automatically if the user authorized unattended optimization; report successful or scientifically interesting results with plots and explanations, while routine failures remain in the ledger.

## Runner correctness

- Unmet-gate branches must return/raise unconditionally before downstream stress.
- A restart resumes from the next untested mechanical/electrical phase without replaying completed stress.
- Constant-bias measurements can contain valid measured current with absent measured voltage; retain commanded-voltage provenance rather than rejecting valid current-only records.

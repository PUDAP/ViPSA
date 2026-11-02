# Per-device BO: exploratory evidence versus deployment

## Lessons from a bounded live-device experiment

Actual acquisition-selected RESET trials can find temporarily credible baselines without establishing a deployable RESET/SET recipe. A later SET can destroy feasibility. A hard read-current stop is an unsafe outcome, not a large useful response or an optimum.

- On an informed explicit request for exploratory BO after initialization failures, fit a real surrogate and use acquisition; do not rename initialization or a grid sweep as BO.
- Keep soft drift/initialization failures as constraint observations. Withhold SET on each invalid baseline. Preserve unconditional electrical/control stops.
- Separate initialization probability, baseline drift, between-trial consistency, and electrical danger. Batch means can conceal failed individual trials.
- RESET-only consistency does not demonstrate recovery after SET. Test recovery within the eventual operating sequence.
- Broad uncertainty is not permission for a jump from the lowest SET amplitude to the upper bound after one observation. Use bounded local exploration and explicit safety qualification.
- An unconditioned response prior is not a measured-response GP. Label it separately; never create fictitious response observations.

## Evidence and implementation audit

Save every candidate, partial trial, constraint failure, uncertainty, acquisition value, pulse count, and raw response. Keep command intent and returned execution counts separate, including uncertain partial stress after communication failure.

Deep-copy training data into each pre-decision model record before appending new observations. Referencing a mutable observation list can make an old summary entry appear to contain future data. Immutable per-decision JSON/model files are the authoritative audit records.

Host checks after a returned voltage list cannot abort at an earlier sample within that list. Report this latency honestly. Instrument-side interlocks or segmented acquisition need validation before deployment; changing segmentation can change the physical protocol.

Track finite runners and preserve cleanup in error/signal paths. No replay of uncertain stress. A process exit code alone does not verify experiment success or hardware cleanup.

## Plot delivery preference

Provide readable plots with the result, not only raw/model files:
1. Actual RESET/SET applications across trials, with candidate boundaries.
2. Paired baseline drift and explicit invalid-trial marks.
3. Paired read currents and hard safety thresholds; label commanded versus measured voltage collapse.
4. Pre-decision acquisition scores, predicted feasibility, and posterior uncertainty.

Use scatter-only measurement markers, PNG previews, and editable SVG. Exclude setup reads from trial comparisons but retain them in raw data and pulse accounting. Predicted joint drift/consistency feasibility and observed baseline-valid fraction are different events; label them rather than suggesting calibration from their agreement. Show prior-only SET decisions explicitly. Inspect rendered figures for clipped labels and overlapping footnotes.

## Proposed deployment specification — not yet validated

QUALIFY → CHARACTERIZE → RESET_BO → SET_BO → FREEZE → VERIFY → ACCEPT/REJECT → CLEANUP.

Use low-stress paired-bias/repeated reads for contact. Repeated full DCIV during mechanical approach can condition/form the device and confound contact with induced switching. After stable contact, a bounded DCIV can supply weak amplitude priors, with explicit sweep fidelity and post-sweep state checks; do not pool sweep currents as pulse outcomes.

Reserve fresh verification trials before BO. Freeze the recipe, classifier, timing and compliance. Independently test randomized-voltage switching probabilities with intervals, actual state distributions, early/middle/late stability, serial dependence, RESET recovery, and application-relevant persistence/endurance. Do not force a sigmoid for deterministic, unimodal, inverted, or compliance-limited data. Permit 'no feasible recipe found.'

Require fault-injection tests and held-out-device validation before claiming unattended deployment. The experimental run established real exploratory BO and a safety stop, not a validated deployment pipeline.

## Motion authorization boundary

A session explicitly clarified 'down 100, up 85, approach 5' as Stage +100 → lateral travel → −85 → −5 increments. This illustrates why contradictory prose direction conventions must be resolved to signed commands before motion. Do not generalize that session's distances into a universal default. A proposed three-increment approach cap was not accepted or executed; do not represent it as approved policy.

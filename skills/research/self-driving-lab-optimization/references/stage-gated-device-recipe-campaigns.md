# Stage-gated device/recipe campaigns

Use this pattern when a recipe can be tested only after a device passes contact, forming, and state-conditioning gates.

## Outcome hierarchy

Record each device at the first terminal stage:

1. `activation_failed_open_or_weak`
2. `activation_failed_unstable_forming`
3. `formed_conditioning_failed`
4. `formed_conditioning_read_clamped`
5. `recipe_characterization_failed`
6. `recipe_characterization_passed_endurance_failed`
7. `recipe_endurance_passed_retention_failed`
8. `fully_qualified`

A recipe is **unevaluated**, not failed, when the device does not reach the recipe stage. Preserve `assigned_recipe_id`, but never include that assignment as a negative recipe observation.

## Sequential gates

- Forming: require sustained compliance/current transition, correct polarity, complete data, no low-voltage short, and no unrecovered pre-compliance collapse.
- Conditioning: require three consecutive directionally correct ON/OFF ratios above the declared floor and within the declared spread limit. Large isolated ratios do not substitute for convergence.
- State reads: a compliance-clamped read is invalid/censored. Stop or review the read-compliance tier; do not treat it as a valid LRS/HRS value and do not increase compliance automatically.
- Characterization: require every planned screening cycle to pass before endurance.
- Endurance/retention: run only after characterization passes. A completed cycle count alone is not evidence of working endurance.

## Optimization implications

Model at least two processes separately:

- Eligibility/yield model: probability of reaching recipe execution.
- Conditional recipe-performance model: outcome given eligibility.

Do not optimize recipe parameters from assigned-but-unexecuted rows. Report stagewise denominators, e.g. `formed / attempted`, `conditioned / formed`, `recipe-evaluated / conditioned`, and `qualified / evaluated`.

If many devices form but conditioning repeatedly fails, pause recipe-space interpretation: the dominant uncertainty is activation/conditioning reproducibility. Use exact anchor replicates and targeted conditioning DOE before spending more devices on broad recipe exploration.

## Evidence and reporting

For each device preserve raw data, stage status, stop reason, cleanup state, and the exact gate metrics. In user-facing summaries distinguish:

- best activation/conditioning protocol,
- best recipe among actually evaluated recipes,
- best fully qualified protocol.

If no recipe reaches endurance/retention, explicitly state that there is no validated optimum.
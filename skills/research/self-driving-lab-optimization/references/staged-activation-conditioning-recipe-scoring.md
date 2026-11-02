# Staged activation, conditioning, and recipe scoring

Use this pattern for device-grid optimization where each site must pass prerequisite electrical stages before its assigned DC-IV or pulse recipe is meaningful.

## Outcome hierarchy

Treat these as separate outcomes:

1. **Activation yield** — clean forming/contact gate passes.
2. **Conditioning yield** — repeated SET/read/RESET/read pairs converge directionally and in spread.
3. **Recipe feasibility** — the assigned DC-IV or pulse recipe is actually executed after stages 1–2.
4. **Characterization stability** — every short characterization cycle meets the state-separation and validity gates.
5. **Endurance/retention** — only evaluated after stable characterization.

A recipe is **unevaluated/withheld**, not failed, when activation or conditioning blocks execution. A run status such as `completed_*_doe` means the runner completed its control flow; it does not by itself mean the recipe passed characterization.

## Conditioning gate

A robust screen requires at least three consecutive directionally correct ON/OFF ratios above the acceptance floor and within the declared spread limit. Large ratios alone are insufficient: inversion, extreme pair-to-pair spread, or a compliance-clamped state read invalidates convergence.

When a post-SET or post-RESET **read** reaches compliance:

- stop the conditioning sequence;
- preserve all earlier valid pairs;
- classify the event as state-read compliance saturation;
- do not use the clamped current to compute or approve state separation;
- do not automatically raise read compliance; review compliance tiers first; and
- leave the downstream recipe unevaluated.

## Campaign interpretation

Maintain separate counts for activation failures, unstable forming, conditioning non-convergence, read-compliance saturation, recipes actually executed, characterization passes, endurance passes, and retention passes. Do not divide recipe success by all allocated devices; report both stage-conditional and unconditional yield.

Use anchor replicates to diagnose the dominant bottleneck. If independent anchors repeatedly form but fail conditioning before recipe execution, pause broad recipe ranking: the evidence supports an activation/conditioning reproducibility problem, not a conclusion about the recipe space.

## Autonomous continuation

For unattended grid work:

- cleanup and verify both SMUs off, matrix open/`nil`, light off, and safe retraction before lateral motion;
- write raw/partial data and the stage-specific classification before moving on;
- update the experiment ledger after every device;
- continue to the next independent allocation without escalating compliance unless explicitly authorized; and
- report interesting successes or new failure classes, avoiding repetitive step-by-step chatter.

## Minimum ledger fields

Record device/site, assigned recipe, whether forming passed, whether conditioning passed, whether the recipe executed, characterization ratios/validity, endurance/retention counts, exact stop reason, cleanup state, and artifact path.

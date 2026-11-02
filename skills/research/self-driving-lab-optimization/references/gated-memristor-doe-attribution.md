# Gated Memristor DOE: Activation, Conditioning, and Recipe Attribution

Use this reference for grid campaigns in which each fresh device must pass forming/contact and conditioning before its assigned DC-IV or pulse recipe is executed.

## Stage-separated outcome model

Treat each device as moving through ordered gates:

1. **Activation/forming** — valid transition, correct polarity, no low-voltage short, no severe pre-compliance collapse.
2. **Conditioning** — sequential directionally correct ON/OFF ratios meeting the declared minimum and spread criterion.
3. **Recipe characterization** — repeated valid cycles under the assigned DC-IV or pulse recipe.
4. **Endurance** — bounded repeated cycles with explicit invalid-cycle stop rules.
5. **Retention** — independent retained-state reads, not inferred from sweep branches.

Never attribute a failure to a later recipe when an earlier gate failed. Report the recipe as **withheld/unevaluated**, not failed.

## Distinct failure classes

Keep these labels separate in the dataset and optimization model:

- `activation_no_transition`: bounded search remains noise-floor/open-like.
- `activation_unstable_forming`: coupling/compliance appears, but collapse or other validity checks reject forming.
- `activation_low_voltage_short_like`: high low-bias current or very early compliance; stop before conditioning.
- `conditioning_nonconverged`: valid forming, but no qualifying run of sequential state ratios.
- `conditioning_read_compliance`: a post-SET or post-RESET read is clamped; the state value and derived ratio are invalid.
- `recipe_characterization_failed`: activation and conditioning pass, but assigned recipe cycles fail validity.
- `recipe_characterization_passed`: all declared characterization cycles pass; only then unlock endurance.

A read-compliance event is not evidence of a strong LRS. Preserve prior valid pairs, stop safely, and review the read-compliance tier before any explicit retest. Do not silently raise compliance.

## Sequential conditioning criterion

Use a predeclared criterion based on consecutive pairs, not isolated large ratios. A practical campaign gate is:

- three consecutive directionally correct ON/OFF ratios,
- each ratio at least the declared minimum (for example 5),
- max/min spread no greater than the declared limit (for example 2.5×),
- no read compliance hits.

Huge ratios can coexist with poor reproducibility. Inversions, alternating ratios, and extreme spread are conditioning failures even if some individual ratios are excellent.

## Anchor replicates and bottleneck diagnosis

Include exact anchor replicates among discovery recipes. If independent anchors repeatedly fail before recipe execution, conclude that activation/conditioning reproducibility is the current bottleneck. Do not compare or optimize later recipe parameters from withheld runs.

If one recipe reaches characterization but degrades after early cycles, classify it as initial switching with unstable state separation—not endurance-capable. Do not infer durability from one or two valid cycles.

## Optimization table schema

Store one row per device with at least:

- device/grid/traversal identifiers,
- assigned recipe and role (`discovery`, `anchor_replicate`),
- forming outcome and onset evidence,
- conditioning ratios, stability flag, and failure reason,
- whether the recipe was actually executed,
- characterization validity vector,
- endurance/retention eligibility,
- cleanup verification and artifact path.

For surrogate training, model activation yield and conditioning feasibility separately from recipe performance. Recipe parameters are not explanatory variables for outcomes observed before recipe execution.

## Safe autonomous continuation

After every device:

1. Save raw/partial data and summary.
2. Force all relevant SMU outputs off.
3. Open and verify the matrix (`closed_channels` empty/`nil`).
4. Retract to verified safe Z before lateral motion.
5. Record the outcome in the campaign wiki and failure log.
6. Continue in declared traversal order only after live encoder/readback verification.

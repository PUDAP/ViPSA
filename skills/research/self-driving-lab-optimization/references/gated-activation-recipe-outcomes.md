# Gated activation and recipe-performance optimization

Use this pattern when a physical-device campaign has prerequisite stages before the assigned recipe can be evaluated.

## Multi-stage outcome model

Treat each device as moving through explicit gates:

1. **Activation/forming:** bounded low-stress search; clean success requires sustained response with no short flag or unrecovered pre-compliance collapse. Compliance attainment alone is not success.
2. **Conditioning:** require repeated directionally correct state separation. A strict practical gate is three consecutive ON/OFF ratios `≥5` with max/min spread `≤2.5×`.
3. **Recipe characterization:** run a short fixed block only after conditioning passes. Every characterization cycle must satisfy the declared validity floor, polarity, and unclamped-read rules before endurance begins.
4. **Endurance:** count valid cycles separately from completed cycles; stop after a declared sequence of invalid cycles.
5. **Retention:** run only after valid endurance, preserving the exact initialization/read sequence.

## Censoring and labels

Use mutually exclusive outcomes:

- activation-yield failure;
- unstable forming;
- conditioning non-convergence;
- state-read compliance saturation;
- recipe evaluated but characterization failed;
- recipe passed characterization/endurance/retention.

If a device fails before the recipe stage, the recipe is **unevaluated**, not unsuccessful. Preserve the assigned recipe and failure stage, but exclude it from recipe-response regression.

Estimate separate probabilities where data permit:

- `P(form)`;
- `P(condition | form)`;
- `P(recipe success | conditioned)`.

This prevents activation yield from being mistaken for recipe performance.

## Safety/validity rules

- A compliance-clamped state read is invalid evidence; preserve partials and do not increase compliance automatically.
- Direction inversion (ON/OFF `≤1`) fails the intended-state gate even if absolute separation is large.
- One or two valid characterization cycles do not establish durability.
- Anchor replicates that fail activation still inform yield, but do not replicate recipe performance.

## Ranking language

Rank protocols by achieved evidence tier:

1. retention-qualified;
2. endurance-qualified;
3. fully characterized;
4. best-tested candidate with explicit failure point;
5. untested mechanistic recommendation.

Do not call a protocol optimal when no candidate has passed endurance and retention.
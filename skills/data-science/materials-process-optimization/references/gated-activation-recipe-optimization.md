# Gated optimization when activation and recipe performance are confounded

Use this reference for materials/device campaigns in which an upstream activation or contact step determines whether a downstream recipe was truly evaluated.

## Core rule

Separate **activation yield** from **recipe efficacy**. If activation, conditioning, contact integrity, or measurement validity fails, mark the assigned recipe *withheld/unevaluated*. Do not score it as a failed recipe.

## Validated gated sequence

1. Run a bounded, low-stress activation/contact search.
2. Require a clean activation trace; threshold/compliance attainment alone is insufficient when the trace contains large preceding collapses or other instability.
3. Require replicated state conditioning before DOE entry. A useful strict gate is three consecutive directionally correct state ratios above the feasibility floor with bounded spread.
4. Treat compliance-limited or clamped state reads as invalid observations. Preserve partials and do not increase compliance automatically.
5. Run a short prospective characterization block before endurance. Every characterization cycle must pass directionality, unclamped-read, and state-separation gates.
6. Withhold endurance and retention when characterization fails; one or two valid cycles do not establish durability.
7. Track failure classes separately: activation yield, unstable activation, conditioning non-convergence, invalid/clamped measurement, recipe characterization failure, endurance failure, and retention failure.
8. Update the experiment ledger after every device. Continue autonomously within approved bounds; report only successful or scientifically interesting results with focused plots and cautious interpretation.

## Optimization implications

- Feasibility gates precede scalar scoring, Pareto ranking, Bayesian optimization, or adaptive acquisition.
- Unevaluated recipes remain candidates for later replicated assignment; they are not negative objective observations.
- Do not select an optimum from one device or from transient first-cycle separation.
- When a recipe initially separates states and then collapses, inspect which state drifts before proposing the next candidate; label the proposal as untested.

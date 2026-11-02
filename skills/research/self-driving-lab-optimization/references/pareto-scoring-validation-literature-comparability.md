# Pareto scoring, validation claims and literature comparability

## Output-space audit

A completed candidate run is not automatically a scored optimization observation. Before Pareto ranking, require explicit objective definitions, directions, candidate-level aggregation, feasibility rules, and a frozen data cutoff. Match nonsuperseded completed candidates to measured vectors; deduplicate by candidate identity, not copies of summaries. Keep preparation, health telemetry and legacy metric namespaces separate. Missing values and UNKNOWN exposures are not zeros. If no eligible vectors exist, produce an explicitly labeled empty-front/coverage plot, counts and an audit manifest identifying the scoring gap. Do not fabricate a front or silently inherit directions from an older contract. Verify delegated PNG/CSV/manifest artifacts before claiming delivery or completion.

## Directional switching and censoring

Report SET contrast |I_PB/I_PF| and RESET contrast |I_NF/I_NB| separately at declared matched measured voltages, with validity flags and valid/attempted counts. Arithmetic averages across directions can hide failed RESET or extreme outliers. Prefer directional medians/lower tails for robust summaries; retain invalid comparisons in the denominator of valid-cycle yield. These are within-sweep metrics, not independent retained-state ON/OFF. Independent memory-window comparisons require identical read bias and timing after SET and RESET, unclipped current, verified voltage delivery, qualified contact and controlled read disturbance.

Survival at a cycle cap is a lower bound/right-censored lifetime, not an exact failure count. Do not turn censored or unknown outcomes into fabricated scores.

## Validation language

'Validated optimum' means a confirmed feasible/nondominated recipe within a declared tested domain, with held-out device/substrate replication and uncertainty. It does not establish global optimality. Numerical thresholds proposed in discussion are not automatically approved execution gates. Clearly distinguish exploratory candidates, confirmed recipes, and externally competitive performance.

## Retrieved literature benchmarks

These are examples, not an exhaustive or permanently current SOTA survey. Different stacks and architectures are not matched controls.

- John et al., Nature Communications (2022), Reconfigurable halide perovskite nanocrystal memristors for neuromorphic computing: https://www.nature.com/articles/s41467-022-29727-1 . CsPbBr3 nanocrystal devices reported nonvolatile endurance 5,655 cycles, retention 10^5 s, and 1 mA SET compliance. Nonvolatile ON/OFF was extracted at the same 0.1 V read pulse. The separate 2-million-cycle result is volatile endurance and must not be represented as nonvolatile memory performance.
- Poddar et al., Nature Communications (2026), Ultra-high density perovskite nanowire array memristor-based multi-layer perceptron: https://www.nature.com/articles/s41467-026-71372-5 . MAPbBr3 nanowire arrays reported dynamic range 200, 139 distinguishable conductance states, retention >10^6 s, and extended endurance >4x10^5 programming pulses. Use the body/methods pulse definition rather than treating the abstract's cycle terminology as automatically equivalent to complete DCIV SET/RESET pairs. A 64x64 array and analog variability metrics are different evidence from a small device pilot.
- Kim et al., Nature Nanotechnology (2025), Linearly programmable two-dimensional halide perovskite memristor arrays for neuromorphic computing: https://www.nature.com/articles/s41565-024-01790-3 . Accessible abstract reports a 7x7 array, low variation, retained multilevel states and moisture stability over seven months. Environmental shelf stability is not state retention; do not invent unavailable quantitative yields or lifetimes.

When comparing campaign criteria, explicitly separate full cycles vs pulses, volatile vs nonvolatile endurance, analog dynamic range vs binary memory window, and elapsed retention vs shelf/environmental stability. Large sweep contrast alone cannot establish SOTA memory performance.

## Reporting discipline

For short campaign summaries, give verified results, dominant limitation and next discriminating test. Do not invent an autonomy percentage: define whether the denominator is active work time, actions or tasks, then audit user intervention and restart records. Agent-executed work differs from unprompted end-to-end continuation.

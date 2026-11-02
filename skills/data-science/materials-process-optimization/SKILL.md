---
name: materials-process-optimization
description: "Use when optimizing materials from historical data."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [materials, process-optimization, bayesian-optimization, experimental-design, multi-objective, multi-fidelity]
    related_skills: [jupyter-live-kernel, grounded-citations]
---

# Materials Process Optimization

Use this class-level skill to turn historical fabrication and characterization data into defensible multi-objective batch experiments. It applies to thin films, devices, formulations, coatings, deposition recipes, and other nested materials datasets.

## Core principle

Historical characterization is often useful as a **warm start**, but its measurements may be lower fidelity than the real downstream objective. Preserve that distinction:

$$
y_{\mathrm{high}}(x)=\rho y_{\mathrm{low}}(x)+\delta(x).
$$

If prospective experiments show weak transfer, shrink $\rho$ toward zero rather than continuing to trust the historical ranking.

## Workflow

1. **Define the experimental unit.** Separate batch, substrate/specimen, device/region, cycle, and measurement point. Never treat repeated cycles as independent recipes.
2. **Audit provenance and integrity.** Inventory raw files, input tables, metadata, hashes, unmatched records, missing conditions, and duplicated recipes.
3. **Recompute questionable metrics.** When compiled fields are nonphysical or undocumented, derive responses from raw ordered measurements and retain extraction definitions.
4. **Separate controls from nuisance variables.** Process settings belong in $x$; batch, environment, location, age, and measurement order belong in telemetry/random effects unless deliberately controlled.
5. **Define individual objectives and hard gates.** Keep yield, performance, stability, safety, energy, and failure modes separate until a Pareto analysis is available.
6. **Fit modest hierarchical surrogates.** For tens of recipes, prefer Gaussian processes, generalized linear mixed models, beta-binomial models, or regularized tree ensembles—not deep neural networks.
7. **Select a batch for both performance and learning.** Include anchor replicates, exploitation, local contrasts, and feasible exploration. Randomize physical placement and measurement order.
8. **Run a prospective transfer test.** Use new high-fidelity results to update or reject the historical proxy.
9. **Report uncertainty honestly.** A selected batch is an information-efficient experiment, not proof that a recipe is optimal.

## Objective design

Typical objective groups are:

- maximize usable yield;
- maximize balanced forward/reverse or activation/recovery performance;
- maximize target response quality;
- maximize endurance and calibration stability;
- minimize operating stress, energy, defects, and compliance/safety events; and
- cover a deliberate target distribution rather than maximizing uncontrolled variance.

Use a Pareto front when practical. If a scalar acquisition score is necessary, publish its weights and perform sensitivity analysis.

## Derived-feature discipline

Distinguish:

- **pre-experiment features**, which can be model inputs for an unmeasured recipe;
- **post-characterization features**, which are outputs, auxiliary targets, or multi-fidelity observations; and
- **uncontrolled telemetry**, which helps remove nuisance variation but is not a process recommendation.

Do not leak post-measurement outcomes into the feature vector used to select an unmeasured recipe.

Useful pre-experiment features may include normalized variables, logarithms, physically motivated ratios, ramp-time proxies, and a limited number of interactions. With sparse designs, regularize aggressively and avoid combinatorial polynomial expansions.

## Constraints

Represent constraints explicitly:

- process-domain bounds or discrete allowed levels;
- chemical/material compatibility;
- equipment limits;
- safety and compliance limits;
- batch capacity;
- minimum valid sample count;
- metadata completeness;
- fixed downstream measurement protocol during process comparison; and
- probability of feasibility, for example $P(\mathrm{safe}\mid x)\geq0.95$.

A constrained acquisition can take the form

$$
\alpha(x)=\mathrm{EHVI}(x)P(\mathrm{safe}\mid x)P(n_{\mathrm{valid}}\geq n_{\min}\mid x).
$$

## Batch design

For a small production batch, prefer a balanced portfolio:

- repeated high-fidelity anchor(s);
- historical low-fidelity transfer candidate(s);
- one-factor or structured local perturbations around the anchor; and
- uncertainty-driven exploration only in plausibly feasible regions.

When the surrogate is weak or kernel/noise parameters hit bounds, interpretable contrasts and replication are more valuable than unrelated high-uncertainty extremes.

Separate anchor replicates spatially and temporally. Use a seeded assignment for reproducibility, but do not mistake randomization for replication.

## Modeling nested data

Use the true hierarchy in both aggregation and validation:

```text
batch → specimen/substrate → device/region → cycle → point
```

Recommended model families:

- beta-binomial or logistic models for yield;
- Student-t or robust Gaussian processes for continuous responses;
- multinomial models for failure class;
- batch/specimen random effects; and
- multi-output or multi-fidelity models for related responses.

Use specimen- or recipe-level train/test splits. Random point- or cycle-level splits cause leakage and exaggerated performance.

## Reporting standard

Report:

- source counts and hashes;
- reconciled versus excluded records;
- experimental-unit hierarchy;
- objective and constraint definitions;
- raw-to-derived calculation rules;
- historical versus interpolated recipes;
- uncertainty and model warnings;
- exact batch roles and randomized order; and
- the planned decision rule after the batch.

For Markdown deliverables, use `$...$` for inline mathematics and `$$...$$` for display mathematics. Avoid `\(...\)` and `\[...\]` in clients that do not render them.

## Reference

- `references/historical-dciv-warm-start.md` — validated low-fidelity DCIV proxy extraction, p-bit multi-fidelity framing, and eight-sample batch design.

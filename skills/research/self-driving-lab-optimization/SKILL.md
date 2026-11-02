---
name: self-driving-lab-optimization
description: "Use for constrained multi-objective lab optimization."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [self-driving-lab, bayesian-optimization, doe, surrogate, multi-objective, materials]
    related_skills: [research-intelligence, jupyter-live-kernel, grounded-citations]
---

# Self-Driving Lab Optimization

Use this class-level skill for materials/process optimization in which expensive physical experiments, nested replicates, noisy objectives, safety constraints, and batch fabrication must be coordinated.

## Core principle

Separate three questions that are often conflated:

1. **Is the data valid and comparable?**
2. **Does the surrogate predict held-out experiments?**
3. **Does the acquisition policy choose useful next experiments?**

An acquisition function does not have a statistical “fit.” Diagnose the surrogate with held-out prediction, and diagnose the acquisition policy with retrospective replay or prospective regret/hypervolume—not training $R^2$.

## 1. Identify the true experimental hierarchy

Write the hierarchy before modeling, for example:

```text
solution preparation / fabrication batch
└── substrate
    └── device
        └── cycle
            └── measurement point
```

The independently controlled fabrication unit—not the number of devices or cycles—is the effective sample size for process optimization. Devices and cycles estimate within-substrate variability and uncertainty; treating them as independent recipes creates pseudoreplication and overconfident models.

Always preserve batch, substrate, device, cycle, spatial coordinate, protocol version, and measurement order.

## 2. Separate historical and prospective evidence

Historical data are useful for defining domains, safety limits, failure modes, candidate anchors, feature engineering, and low-fidelity priors. Do not pool heterogeneous historical measurements with fresh prospective measurements as though they share one protocol.

When protocol, contact gating, extraction logic, or batch conditions changed, use a multi-fidelity relationship such as:

$$
y_{\mathrm{fresh}}(x)=\rho y_{\mathrm{old}}(x)+\delta(x).
$$

Estimate transfer from fresh overlap points. If $\rho$ is near zero or historical inclusion worsens held-out prediction, remove the old data from acquisition decisions while retaining it for context.

## 3. Re-extract physical features from raw data

Do not train on compiled metrics known to contain nonphysical values. Recompute responses from ordered raw measurements while preserving sweep direction and signed values.

For source-measure sweeps, distinguish commanded voltage, measured/applied voltage, current, compliance state, branch/acquisition order, and programmed dwell versus actual point spacing.

For compliance-limited sweeps, use **commanded voltage** as the primary x-axis when the plot is intended to show the programmed sweep shape. Retain measured voltage in the data and provide a companion diagnostic when voltage collapse matters physically. Never let a measured-voltage foldback plot make a correctly commanded SET sweep appear malformed.

A source-code edit does not hot-reload into an already running experiment. Do not interrupt active electrical testing merely to change visualization. Regenerate requested plots from saved partial data, patch future runs, and state whether the current process will retain its in-memory plotting function.

Report dwell precisely: “commanded dwell” is the explicit delay parameter; “effective seconds per point” includes integration, autoranging, communication, and software overhead and should be calculated from timestamps or elapsed time.

## 4. Define objectives without hiding failure modes

Prefer a Pareto objective vector over one arbitrary scalar. Typical materials/device objectives include usable-device yield, balanced directional switching, state/property separation, controllability, endurance, drift stability, process reproducibility, and energy/voltage/time/material cost.

For two essential directional yields, use a harmonic mean so one-sided success cannot dominate:

$$
H=\frac{2Y_1Y_2}{Y_1+Y_2+\epsilon}.
$$

Keep failure labels explicit. A smooth aggregate score must not hide open, short, compliance-limited, stuck-state, invalid-contact, or missing-data outcomes.

## 5. Separate inputs, covariates, responses, and telemetry

- **Controllable inputs:** variables deliberately set before fabrication or testing.
- **Input-derived covariates:** transformations and interactions available before an experiment.
- **Measured responses:** outcomes used as objectives or constraints.
- **Telemetry/uncontrolled variables:** batch, environment, age, position, tool identity, operator intervention, and actual timing.

Do not feed post-measurement outcomes into a recipe-selection surrogate as if they were pre-experiment inputs. Use them as auxiliary targets, constraint models, or diagnostic covariates for retrospective analysis.

## 6. Use fresh space-filling data when transfer is poor

If recipe-level cross-validation is near or below $R^2=0$, or batch-holdout performance collapses, do not try to repair the problem by changing EI to UCB or adding evolutionary selection pressure. The limitation is data/model identifiability.

Use a prospective design with scrambled Sobol, maximin LHS, or discrete maximin coverage; deliberate anchor replicates; one-factor local contrasts where mechanistic learning matters; and at least two independent fabrication batches before claiming transfer.

For discrete factors, snapped continuous LHS can duplicate points and distort balance. Optimize a discrete maximin or D-optimal design directly over allowed levels. Pure LHS provides coverage but no replicate-based noise estimate; an augmented design with anchors is usually preferable.

## 7. Respect batch feasibility

Before proposing a batch, determine which inputs vary per sample and which are shared by the whole batch. If one solution preparation feeds every substrate, composition is a batch-level variable even if spin programs vary per substrate.

Never propose an eight-point four-variable design inside one batch until the equipment can actually assign all four variables independently. If not, nest the design across batches and model the hierarchy explicitly.

## 8. Fit and validate the surrogate

With limited physical experiments, start with interpretable probabilistic models: beta-binomial/logistic models for yields, Student-t or Gaussian processes for continuous metrics, classification models for feasibility, and batch/substrate random effects.

Report both in-sample and held-out diagnostics, but treat training fit as descriptive only. At minimum report held-out $R^2$, RMSE, MAE, rank correlation, predictive-interval coverage, leave-one-substrate-out performance, and leave-one-batch-out performance when the design permits it.

Kernel-bound warnings, constant targets, high fitted noise, and poor interval coverage are model findings, not cosmetic warnings. A constant constraint target is not learnable and contributes no ranking information.

## 9. Choose acquisition functions only after validation

For noisy constrained multi-objective batches, use constrained `qLogNEHVI`/`qNEHVI` as a baseline after prospective validation. Compare with `qNParEGO` and a model-independent space-filling baseline.

Evolution-guided Bayesian optimization can combine a qNEHVI candidate pool with U-NSGA-III or another evolutionary pool, then rank the union by constrained hypervolume improvement. This can improve Pareto convergence but may overexploit noise or crowd constraint boundaries when the surrogate is weak.

Handle constraints by type:

- **Known input constraints:** pre-repair, reject, or parameterize candidates so they are feasible before ranking.
- **Unknown output constraints:** model probabilistically from measured outcomes.

Do not use post-repair blindly: projecting infeasible candidates after acquisition optimization can concentrate samples on a narrow boundary and bias the experiment.

## 10. Benchmark acquisition policies correctly

Retrospective checks can compare posterior mean, lower/upper confidence bounds, EI, uncertainty sampling, qNEHVI, or evolutionary hybrids on a closed observed set. Report top-$k$ overlap and realized utility/hypervolume, but label this as a closed-world replay—not proof of performance on unmeasured recipes.

If EI, UCB, and LCB select nearly identical candidates while uncertainty sampling selects a disjoint region, changing acquisition functions is unlikely to fix the surrogate. Prefer prospective information collection.

Prospectively compare policies using hypervolume improvement, Pareto-front non-uniformity, infeasible-sample fraction, constraint-violation magnitude, valid outcomes per batch, regret, and information gained per unit time/material.

## 11. Transition from DOE to autonomous optimization

Do not activate autonomous acquisition merely because a GP can be fit. Require positive held-out performance on priority objectives, useful rank correlation, calibrated predictive intervals, replicated batch transfer, enough positive/negative constraint examples, and a prospective result better than a space-filling/random baseline.

Until then, use replicated DOE and describe the model as a weak warm-start/ranking aid.

## Markdown output convention

For user-facing Markdown, use `$...$` for inline mathematics and `$$...$$` for display mathematics. Verify that `\(...\)` and `\[...\]` do not remain unless the target renderer explicitly supports them.

## Verification checklist

- [ ] True fabrication unit and hierarchy documented.
- [ ] Historical and fresh fidelities separated.
- [ ] Raw ordered measurements used for response extraction.
- [ ] Commanded versus measured values and dwell semantics distinguished.
- [ ] Objectives, constraints, failures, and telemetry separated.
- [ ] Proposed design is physically executable by the batch tool.
- [ ] Exact recipe replication included where noise/transfer matter.
- [ ] Surrogate judged by held-out—not training—fit.
- [ ] Acquisition judged by policy outcome—not “fit.”
- [ ] Known input constraints handled before experimental evaluation.
- [ ] Autonomous BO gated on prospective validation.

## References

- See `references/vipsa-warmstart-egbo-and-live-plotting.md` for an applied session reference covering raw DCIV warm starts, GP diagnostics, LHS/Sobol design trade-offs, EGBO/qNEHVI lessons, and compliance-limited live plotting.

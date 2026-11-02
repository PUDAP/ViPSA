# PEA2PbBr4 simulated-annealing substrate optimization by Bayesian DOE (2026-07-31)

## Context

Application: on-chip simulated annealing using PEA2PbBr4 memristor arrays. The desired substrate is a **population** of calibrated stochastic p-bits, not just one high-ON/OFF device.

Fabrication is one-step and currently constrained:

```text
PEABr + PbBr2 dissolved in DMF/DMSO
→ spincoat
→ anneal at 100 °C baseline 10 min
→ PMMA topcoat
→ thermally evaporated Ag top electrodes
```

No antisolvent quenching. Annealing temperature is not varied within a batch.

Available knobs:

```text
DMF:DMSO ratio: 1:3, 1:2, 1:1, 2:1, 3:1
perovskite concentration: 0.2 M, 0.4 M, 0.6 M, 0.8 M
spin speed
spin acceleration
annealing time
```

## Scientific framing

A device’s p-bit transfer can be fit as:

```text
P(state=1 | V) = 1 / (1 + exp[-k(V - V0)])
```

`k` acts like inverse effective temperature:

```text
T_eff ∝ 1/k
```

Device selection can therefore provide **hardware-discrete effective-temperature bins** if slope differences are reproducible:

```text
shallow k  → high effective T / exploration
medium k   → intermediate T
steep k    → low effective T / exploitation
```

For publication, frame this as device-selection-based effective-temperature binning, ideally with electrical knobs such as pulse amplitude/width/read threshold for finer dynamic tuning.

## Why simultaneous optimization is preferred

Do not assume solvent ratio, concentration, spin speed, acceleration, and anneal time are independent. Sequential one-variable-at-a-time optimization can miss interactions such as:

```text
DMF:DMSO × spin speed        → drying rate / pinholes / thickness
concentration × spin speed   → open/short balance
acceleration × solvent ratio → nucleation / film uniformity
anneal time × thickness      → drift / crystallinity / stochasticity
```

Preferred design: mixed-variable space-filling DOE followed by batch Bayesian optimization.

## Initial DOE

Use an initial space-filling sample over all five variables rather than fixing a risky baseline spin condition.

Good options:

```text
Sobol / Latin-hypercube / stratified random initial design
N ≈ 16–40 substrates depending on fabrication budget
```

Encode variables as:

```text
solvent_ratio: categorical/ordinal {1:3, 1:2, 1:1, 2:1, 3:1}
concentration: discrete numeric {0.2, 0.4, 0.6, 0.8}
spin_speed: bounded numeric
spin_acceleration: bounded numeric
anneal_time: bounded numeric/discrete
```

Include controls/replicates in every batch:

```text
known prior best recipe if available
balanced midpoint recipe
thin/short-prone sentinel
thick/open-prone sentinel
duplicate recipe for process noise
```

## ViPSA phenotype per substrate

Use multi-fidelity screening.

### Fidelity 1 — fast substrate triage

Measure many devices per substrate:

```text
optical / pad usability
alignment success
approach success
quick low-bias resistance: 0 V, ±10 mV, ±50 mV
classification: open / weak / usable / short-like / compliance-limited
```

Metrics:

```text
usable_yield
short_fraction
open_fraction
median_low_bias_R
spatial clustering of failures
candidate_fraction
```

### Fidelity 2 — p-bit candidate characterization

On selected devices:

```text
safe DCIV / forming precheck
randomized SET-read-RESET-read pulse train
read-after-write current distributions
binary thresholding
sigmoid fit
entropy analysis
```

Fit/extract:

```text
k, V0, fit quality
H_binary(V) = -p log2 p - (1-p) log2(1-p)
H_disc(I|V) from binned analog current distributions
Hmax and voltage of Hmax
slope-bin membership
read-compliance / stress-compliance hit fraction
```

### Fidelity 3 — validation

For top recipes only:

```text
longer endurance
drift: Δk/k0, ΔV0
retention/relaxation
replicate substrates
small annealing/Ising demonstration or measured-device emulator
```

## Objective functions

Keep individual metrics, but a scalar score for BO can be:

```text
score =
  + usable_yield
  + sigmoid_success_rate
  + slope_temperature_coverage
  + entropy_quality
  + endurance_stability
  + reproducibility
  - short_fraction
  - open_fraction
  - drift_penalty
  - compliance_hit_fraction
```

For multi-objective BO, track Pareto fronts over:

```text
maximize usable_yield
maximize sigmoid_success_rate
maximize slope coverage/diversity
maximize entropy quality
maximize endurance stability
minimize short/open/compliance/drift penalties
```

Important: a broad `k` distribution is useful only if the sigmoids are stable/calibratable and enough devices populate each bin. Do not reward single outliers.

## Bayesian optimization loop

Recommended loop:

```text
Batch 0: 16–40 space-filling recipes
→ ViPSA fast + medium phenotype
→ fit surrogate model
→ propose next 8–12 recipes using qEI/qUCB/qNEHVI
→ include 1–2 best-recipe replicates and 1–2 high-uncertainty exploratory recipes
→ repeat for 2–3 BO rounds
→ confirm best 2–5 recipes with replicate substrates and full validation
```

Resource-light version:

```text
Initial 16 recipes
2 BO rounds × 8 recipes
2 best recipes × 3 replicate substrates
≈ 38 substrates
```

Stronger version:

```text
Initial 30 recipes
3 BO rounds × 10 recipes
3 best recipes × 3 replicate substrates
≈ 69 substrates
```

## Publication-ready outputs

Generate:

```text
process-variable table
substrate/device classification maps
resistance distributions
representative stochastic pulse scatter plots
P(state=1) vs V_SET sigmoid fits
k / T_eff distribution across devices and substrates
entropy vs bias
endurance/drift of k and V0
Pareto front / substrate ranking
annealing demonstration using selected slope bins
```

## Reporting rule

Keep protocol advice concise unless the user explicitly asks for detailed rationale. For active ViPSA operations, report verified results, blockers, paths, and cleanup state; avoid per-step spam.

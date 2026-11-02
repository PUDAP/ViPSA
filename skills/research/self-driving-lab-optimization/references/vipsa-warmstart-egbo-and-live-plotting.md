# ViPSA warm start, EGBO, and live plotting reference

## Historical archive and hierarchy

The applied archive contained 1,473 raw sweep files, 14,730 repeated cycles, and 1,470 devices reconciled to the fabrication-input table. These mapped to 59 substrate/slot observations and 57 unique process recipes. The process inputs were concentration, solvent/DMSO fraction, spin speed, and spin acceleration.

The correct hierarchy was:

```text
fabrication batch → substrate/slot → device → cycle → point
```

Do not promote device or cycle count to fabrication sample size.

## Conservative raw DCIV proxy extraction

Known-invalid compiled resistance/ON-OFF fields were not used. Four signed low-bias observations were extracted from each repeated cycle:

1. $+0.1$ V before positive stress;
2. $+0.1$ V after positive stress;
3. $-0.1$ V before RESET;
4. $-0.1$ V after RESET.

A strict bidirectional proxy required correct current polarity, at least twofold directional changes on SET and RESET sides, paired HRS/LRS agreement within a factor of ten across bias signs, and no compliance at those read points. This is a DCIV proxy, not a measured p-bit switching probability.

## Exploratory GP and fit

Independent Gaussian-process regressors used min-max-scaled process inputs and a constant-times-Matérn-$5/2$ ARD kernel plus white noise. Recipe-level means were the training rows.

Training $R^2$ values were 0.82–0.90, but five-fold recipe-level results were poor:

| Objective | CV $R^2$ | Spearman $\rho$ |
|---|---:|---:|
| Robust-device proxy yield | -0.105 | 0.287 |
| Bidirectional-cycle fraction | -0.016 | 0.410 |
| SET/RESET harmonic mean | 0.079 | 0.525 |
| Coherent paired-read fraction | -0.020 | 0.193 |

Nominal 95% interval coverage was only about 84–88%. Batch holdout was worse and confounded by different recipe coverage. Several kernel parameters hit bounds. The low-bias compliance target was constant, so it was not learnable.

Conclusion: use the model as a weak ranking aid only. Start the authoritative optimization model from fresh, frozen-protocol data and test historical transfer through $y_{fresh}=\rho y_{old}+\delta$.

## Acquisition comparison

On the closed finite candidate set, posterior mean and conservative LCB had 8/8 top-candidate overlap; mean versus UCB and EI each had 7/8 overlap. Pure uncertainty sampling had 0/8 overlap. EI values were tiny. This showed that changing EI/UCB/LCB could not repair the weak surrogate.

Use replicated space-filling data first. After prospective validation, benchmark constrained qLogNEHVI against qNParEGO and a model-independent baseline.

## LHS/Sobol design lesson

A local anchor-heavy design had normalized minimum unique-point distance 0.160 and mean pairwise distance 0.469. An augmented discrete maximin design improved these to 0.865 and 1.067, respectively, but had lower weak-model proxy utility.

Prefer two anchor replicates plus six discrete maximin/Sobol points when learning is the priority. Check first whether composition and spin settings can vary per substrate; otherwise nest composition across fabrication batches.

## EGBO paper translation

Low et al. used Sobol initialization, separate SingleTaskGP models in ModelListGP, qNEHVI, and an EGBO hybrid that pooled qNEHVI candidates with U-NSGA-III evolutionary candidates and ranked the union by qNEHVI. They distinguished known input constraints from measured output constraints and found pre-repair preferable to naïve post-repair.

For ViPSA-like work, use EGBO only after prospective surrogate validation. Evolutionary selection pressure can amplify noise when held-out predictive fit is poor.

## Compliance-limited plotting correction

When compliance makes measured voltage collapse, plotting current versus measured voltage can fold or compress the SET branch and make the programmed sweep look malformed. For the user-facing protocol plot:

- x-axis: commanded voltage;
- y-axis: signed current and/or log $|I|$;
- preserve measured voltage in raw data;
- optionally add a companion commanded-versus-measured diagnostic;
- preserve acquisition order and phase/branch labels.

If a run is active, editing its source file does not update functions already loaded in the Python process. Do not interrupt electrical testing solely for plotting. Regenerate plots from saved partial CSV/JSON, patch future runs, and disclose that already-running notifications may retain the old view.

## Dwell reporting

A commanded 1.0 s dwell can produce a larger effective per-point interval due to integration, autoranging, instrument, network, and software overhead. Report both values when available, and never relabel total elapsed-per-point as programmed dwell.

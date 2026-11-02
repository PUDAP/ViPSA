# Retained-switching protocol optimization with constrained MOBO

Use this reference when optimizing SET/RESET/read conditions for retained resistive switching on one substrate. It captures a key correction: a bounded low-stress screen with fixed SET compliance is **not** a true optimization of the switching protocol.

## Scientific target

Optimize a protocol recipe, not the appearance of a compliance-limited sweep. A suitable decision vector is

$$
x=[V_{SET},\log_{10}I_{SET},t_{SET},|V_{RESET}|,\log_{10}I_{RESET},t_{RESET},V_{read}].
$$

SET voltage and SET compliance are primary interacting variables. Voltage controls threshold crossing; compliance controls filament strength/cross-section. Holding compliance fixed can systematically produce transient high-field conduction while excluding stable-filament conditions.

Retention sampling times should normally be frozen audit conditions (for example 0.5, 1, 5, and 20 s), not optimized variables. Otherwise the optimizer can improve its score merely by reading earlier.

## Multi-objective formulation

For device $d$ and cycle $c$, define delayed state separation

$$
r_{dc}=\log_{10}\frac{|I_{SET,dc}(20s)|+\epsilon}{|I_{RESET,dc}(20s)|+\epsilon}.
$$

Maximize a Pareto vector such as:

1. lower-tail or lower-credible-bound delayed separation, e.g. $Q_{0.10}(r_{dc})$;
2. lower-confidence usable-device/endurance yield at a frozen cycle target;
3. negative drift and cycle spread, e.g. $-\mathrm{median}(|\beta_d|+\lambda\,\mathrm{IQR}_c(r_{dc}))$;
4. negative log measured energy per valid SET/RESET/read cycle.

Do not use maximum ON/OFF ratio as the primary objective. It rewards outliers and contact artifacts.

## Constraints

### Known input constraints

Pre-repair or generate only physically executable candidates:

- preserve SET positive and RESET negative signs;
- enforce voltage/current/dwell bounds and instrument list limits;
- enforce per-branch and cumulative-device energy budgets;
- keep each operation as a complete zero-return cycle;
- exclude high-risk reserve tiers from the routine search domain unless separately authorized.

### Hard runtime constraints

Stop the device test on:

- read compliance;
- persistent high conductance after RESET;
- invalid measured-voltage delivery or excessive voltage collapse;
- current above the declared compliance tolerance;
- branch energy above budget;
- unidentified contact, route uncertainty, control failure, or unverified cleanup.

Save these as constraint observations; do not silently replace them with objective zeros.

### Probabilistic output constraints

Model recipe feasibility explicitly, for example:

$$
P(\text{retained ratio}\ge R_{min})\ge p_{ret},
$$
$$
P(|I_{SET}|>|I_{RESET}|)\ge p_{dir},
$$
$$
P(\text{valid RESET})\ge p_{reset},
$$
$$
P(\text{read clamp}),P(\text{persistent short}),P(\text{invalid voltage delivery})\le p_{fail}.
$$

Freeze $R_{min}$ and probability thresholds before execution.

Contact failure, activation failure, recipe execution, characterization pass, and endurance pass are separate stages. Contact-invalid or activation-blocked trials are censored/withheld recipe evaluations, not ordinary recipe failures. Report both conditional recipe performance and unconditional substrate yield.

## Sampling strategy

1. Treat heterogeneous historical data as a separate fidelity. Use overlap anchors to estimate transfer; remove historical data from acquisition decisions if it worsens held-out prediction.
2. Start with replicated discrete maximin/Sobol sampling, not BO. Include:
   - multiple replicates of a historical working anchor;
   - overlap replicates of the current conservative recipe;
   - space-filling points across SET voltage/compliance and RESET settings.
3. Randomize and spatially stratify recipe assignments across the substrate. Include device X/Y as nuisance covariates or random effects.
4. Use one assigned recipe per fresh device; repeated cycles estimate within-device variance but are not independent recipes.
5. Stage cost and stress:

```text
contact/activation
→ 3 conditioning pairs
→ 6 conditioning pairs
→ short characterization
→ 30-cycle endurance
→ longer retention/endurance only after passing
```

Record why later stages were withheld. Never convert withheld endurance into zero endurance.

## qNEHVI / qLogNEHVI

qNEHVI is appropriate after surrogate validation because it jointly selects a noisy batch by expected feasible hypervolume improvement while integrating uncertainty in the latent Pareto frontier. Use separate probabilistic models for objectives and output constraints. For discrete hardware-safe domains, enumerate/pre-repair the feasible candidate table and evaluate acquisition on that table instead of relying only on unconstrained continuous optimization.

Prefer qLogNEHVI where supported for numerically small acquisition values. A practical batch may contain acquisition-selected candidates plus one forced anchor replicate for drift monitoring.

Do not activate autonomous qNEHVI merely because a GP fits. Require positive held-out ranking/prediction, calibrated uncertainty, replicated anchors, positive and negative feasibility examples, and prospective performance better than a space-filling baseline.

## EGBO

Evolution-Guided Bayesian Optimization (EGBO) combines qNEHVI candidates with an evolutionary pool such as U-NSGA-III, then ranks the union with constrained qNEHVI. The evolutionary arm can improve Pareto-front coverage; it is not a remedy for a weak surrogate.

Recommended flow:

```text
fit objective + constraint models
├─ qLogNEHVI candidate pool
└─ U-NSGA-III candidate pool
   ↓
pre-repair known input constraints
remove duplicates
rank union by constrained qLogNEHVI
select final batch
```

Use EGBO only after qNEHVI has a validated surrogate and shows inadequate Pareto coverage. Evolutionary pressure can amplify noise or crowd constraint boundaries when the model is weak.

## Retention-debugging lesson before optimization

A high return-branch current or sustained compliance event is not retained switching. Require separate labels:

- `within_sweep_transition_detected`;
- `retained_postforming_state_confirmed`.

If immediate post-SET current repeatedly decays before RESET, do not escalate RESET first. First isolate:

1. time-resolved decay with the route held fixed;
2. the same timing with matrix open/reconnect;
3. weak versus historical stronger SET conditions on independent sacrificial devices;
4. a read range capable of observing the known LRS without clipping.

Matrix-open cleanup can be electrically safe while changing the scientific protocol. Log exact cross-operation wall-clock timing and measured read voltage so physical decay can be separated from route/reconnection effects.

## External references

- Daulton, Balandat, and Bakshy, *Parallel Bayesian Optimization of Multiple Noisy Objectives with Expected Hypervolume Improvement*: https://arxiv.org/abs/2105.08195
- Low et al., *Evolution-guided Bayesian optimization for constrained multi-objective optimization in self-driving labs*: https://www.nature.com/articles/s41524-024-01274-x
- BoTorch constrained MOBO tutorial: https://github.com/meta-pytorch/botorch/tree/main/tutorials/constrained_multi_objective_bo

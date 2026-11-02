# Prospective yield campaign after weak historical transfer

Use when historical device data provide a weak warm start but held-out recipe or batch prediction is poor, and the next task is to launch a fresh fabrication/device-yield campaign.

## Data roles

- Keep historical data for domains, safety limits, failure modes, feature engineering, and weak low-fidelity priors.
- Train the authoritative acquisition surrogate on prospectively controlled data first.
- Do not pool a prior pilot with fresh devices without a protocol-fidelity label.

If an origin device has already been stressed or used a mixed dwell and the user explicitly chooses to count it in yield, preserve that choice in the displayed denominator but also report fresh-protocol yield separately. The mixed-fidelity pilot must not masquerade as a fresh replicate in the surrogate likelihood.

## Prospective campaign contract

Before launch, freeze and machine-check:

1. fabrication/measurement inputs and units;
2. grid geometry and traversal order;
3. the yield denominator and failure taxonomy;
4. contact-validity rules;
5. the complete electrical operation plan;
6. commanded dwell and actual timing telemetry;
7. illumination/environment policy;
8. batch/substrate/device/cycle hierarchy;
9. cleanup and resumability checkpoints.

Use a dry-run that enumerates every grid coordinate and exact operation count. Unit-test exact signed motion constants and protocol parameters. Do not claim a background runner started from PID existence alone; require advancing machine-state timestamps or created alignment/measurement artifacts.

## Yield accounting

Report at least three denominators:

$$
Y_{\mathrm{navigation}}=\frac{n_{\mathrm{target\ reached}}}{n_{\mathrm{planned}}},
$$

$$
Y_{\mathrm{contact}}=\frac{n_{\mathrm{verified\ electrical\ contact}}}{n_{\mathrm{target\ reached}}},
$$

$$
Y_{\mathrm{device}}=\frac{n_{\mathrm{protocol\ passing}}}{n_{\mathrm{verified\ electrical\ contact}}}.
$$

Also give end-to-end yield relative to all planned devices. Keep alignment failure, contact failure, open-like, short-like, compliance-limited, SET-only, RESET failure, drift failure, interrupted, and completed-pass outcomes distinct.

## Transition back to BO

After at least two prospectively controlled batches, compare fresh-only and multi-fidelity models under substrate/batch holdout. Historical data may enter acquisition decisions only if it improves held-out ranking/calibration. Until then, continue anchor-replicated Sobol/maximin DOE rather than trying to rescue a weak surrogate with a more aggressive acquisition function.

# Incumbent-baseline optimization for electrical device protocols

Use this reference when optimizing SET/RESET/read recipes after a historical protocol has already produced working DC-IV or matched-read behavior.

## 1. Treat the working protocol as an incumbent, not automatically as a ceiling

Separate three concepts:

- **Incumbent:** best currently demonstrated recipe.
- **Search boundary:** parameter range authorized for exploration.
- **Hard safety limit:** value that cannot be exceeded without new approval.

A historical recipe can be the incumbent while some of its parameters remain hard limits. Do not bias the complete search below the incumbent merely because it was previously the highest-stress recipe; this can remove the only region where stable switching was observed.

Define improvement relative to the incumbent $x_0$:

$$
\Delta f_k(x)=f_k(x)-f_k(x_0).
$$

Use non-inferiority constraints for retained separation, endurance, drift, and failure risk. Select the lowest-stress recipe that is non-inferior, unless higher stress produces a justified gain.

## 2. Establish protocol comparability before warm-starting

Historical sweep hysteresis is not automatically a retention baseline. Before pooling data, compare:

- stress endpoints, compliance, step size, dwell, and NPLC;
- commanded versus measured voltage and actual current;
- matrix routing/output-off sequence between stress and read;
- read bias, range/compliance, settle time, and read count;
- immediate versus delayed read times;
- conditioning and endurance definitions.

Run fresh overlap replicates of the incumbent under the frozen new measurement protocol. Model historical transfer as a separate fidelity, e.g. $y_{fresh}=\rho y_{old}+\delta$. If transfer is weak, retain historical results as context but exclude them from acquisition decisions.

## 3. Verify executed protocol from source and artifacts

Do not trust summary prose alone. Resolve discrepancies using, in order:

1. per-operation CSV/raw response and commanded fields;
2. executed runner source;
3. run summary metadata;
4. narrative plans.

Configured compliance is not delivered current. Report both. A protocol variant (for example a higher RESET compliance on a subset of devices) must be shown separately, not silently pooled into the canonical baseline.

## 4. Qualification logic for nonvolatile switching

A compliance event during a sweep proves high-field conduction, not retained forming. Keep separate labels:

- within-sweep transition detected;
- post-forming state retained;
- correct SET-high/RESET-low direction;
- delayed retention validated;
- endurance qualified.

RESET cannot explain ON-state loss measured before RESET. When strong return-branch current collapses before the delayed read, isolate volatility from routing effects using fixed-route time-resolved reads before changing RESET.

Read compliance must be capable of observing the incumbent LRS. If it clips the known working range, classify the result as censored rather than failed or successful.

## 5. Sampling strategy

For a fresh substrate/device population:

1. Spatially stratify recipe assignments.
2. Reserve held-out devices before testing.
3. Include repeated incumbent anchors across the substrate.
4. Use local perturbations around the incumbent before broad global exploration.
5. Assign one recipe per fresh device when stress history would confound later recipes.
6. Use staged fidelity: activation → conditioning → characterization → endurance.
7. Record withheld downstream stages as unevaluated, not zero performance.

Use constrained qLogNEHVI only after held-out surrogate prediction and feasibility calibration are useful. EGBO can pool qNEHVI and U-NSGA-III candidates for broader Pareto coverage, but it is not a remedy for weak surrogates. Apply known input constraints before acquisition ranking; model unknown output constraints probabilistically.

## 6. Parameter-coverage visualization

For campaign review, generate a four-part figure:

1. SET/forming endpoint magnitude versus compliance on a log-compliance axis.
2. RESET endpoint magnitude versus compliance on a log-compliance axis.
3. Protocol table covering voltage step, dwell, read settings, retention timing, and endurance.
4. Spatial candidate map showing electrically used versus fresh sites.

Overlay incumbent protocol points with distinct symbols. Label campaign markers by **unique sites**, not repeated sweeps. Export PNG, editable SVG, and the underlying coverage CSV.

Extract executed combinations from saved per-operation artifacts and summaries. Deduplicate by endpoint/compliance and aggregate site IDs. Plans and candidate-grid status fields become stale; determine fresh-device count from actual electrical/stress artifacts and state the provenance.

## 7. Autonomous-run prerequisites

Before an unattended campaign:

- all required edges must have fresh heartbeats;
- stale run IDs must be reset only after confirming no live runner;
- electrical cleanup and position readbacks must be fresh;
- substrate/holder identity and the safe travel route must be confirmed;
- the device allocation, parameter envelope, energy limits, and hard stops must be frozen;
- irreversible stress requires one explicit campaign GO.

If fewer fresh devices remain than needed for replicated anchors, held-out validation, and exploration, reduce the claim to a bounded baseline challenge/local DOE. Do not call a six-device local comparison a validated global BO optimum.

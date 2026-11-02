# Historical DCIV warm starts for probabilistic-device optimization

## Valid use

Use historical quasi-static DCIV data as a **low-fidelity fabrication prior**, not as direct evidence of pulse-induced switching probability, entropy, pulse endurance, update energy, or solver success.

Model fresh randomized-pulse data as high fidelity:

$$
y_{\mathrm{pbit}}(x)=\rho y_{\mathrm{DCIV}}(x)+\delta(x).
$$

If prospective results do not correlate with the DCIV proxy, shrink $\rho$ toward zero.

## Preserve hierarchy

Use:

```text
batch → substrate/slot → device → cycle → measurement point
```

Do not treat devices or cycles as independent process recipes. Aggregate uncertainty at substrate/recipe level or use a hierarchical likelihood. Split validation sets by substrate or recipe, never randomly by cycle.

## Audit and extraction

1. Inventory raw sweeps, resistance files, process-input rows, metadata, unmatched slots, and repeated recipes.
2. Reconcile measured slots to process recipes; flag or exclude unmatched records.
3. Preserve row order because hysteresis depends on voltage trajectory.
4. Inspect the actual trajectory before using branch indices or fixed offsets.
5. Regenerate responses from signed raw voltage/current when compiled resistance, ON/OFF, or threshold fields are nonphysical or undocumented.
6. Hash source tables and retain extraction-code provenance.

For repeated bipolar sweeps, compare safe low-bias readings at four states:

1. positive read before SET;
2. positive read after SET;
3. negative read before RESET; and
4. negative read after RESET.

A conservative bidirectional proxy should require:

- current polarity following applied bias;
- declared SET- and RESET-side change thresholds;
- reasonable HRS/LRS agreement across opposite bias signs;
- no read-compliance event; and
- no inference of open contact from pA/GΩ magnitude alone.

For high-HRS contact, use bias-dependent slope, polarity, $\Delta I$ scaling, resistance consistency across safe bias pairs, and a lifted-tip/open-route baseline when available.

Label all such outputs `DCIV proxy`; they are not p-bit probabilities.

## Low-fidelity responses

Estimate per substrate/recipe:

- electrical-valid fraction;
- SET and RESET yields;
- their harmonic mean;
- direction-aware state separation;
- strict bidirectional-cycle fraction;
- stuck-SET/stuck-RESET fractions;
- compliance fraction;
- threshold/read-current drift; and
- cycle survival.

Do not reward SET yield without RESET.

## Sparse-surrogate guidance

For tens of unique recipes:

- use beta-binomial/logistic models for yields;
- use robust or Student-t Gaussian processes for continuous metrics;
- model failure class separately where useful;
- include batch as a block/random effect;
- retain predictive uncertainty; and
- avoid deep neural networks.

If kernel length scales or noise terms hit bounds, treat the model as weak. Prefer replication and interpretable contrasts over blindly selecting high predicted means or unrelated high-uncertainty extremes.

## Eight-sample batch pattern

A defensible small batch combines:

- two separated repeats of the strongest high-fidelity anchor;
- one or two prospective transfers of strong historical proxies;
- one-factor or structured local perturbations around the anchor; and
- uncertainty-driven exploration only where feasibility remains credible.

Randomize physical assignment and independently randomize measurement order. Separate anchor repeats spatially and temporally. Freeze non-listed fabrication variables and the downstream electrical protocol.

## Reporting

Report:

- source and reconciled-record counts;
- experimental hierarchy;
- proxy definitions and thresholds;
- historical versus interpolated recipes;
- anchor evidence level;
- surrogate warnings;
- exact batch roles and randomized order; and
- the planned decision rule after the batch.

State explicitly that the batch is an information-efficient experiment, not proof of an optimum.

# All-unit descriptive ON/OFF plots

Use this pattern when the user requests a simple response-versus-input visualization rather than a model-ready Bayesian objective.

## Response definition

For each physical unit, within the requested cycle window:

1. Collect every saved finite positive- and negative-direction ON/OFF ratio.
2. Skip ratios that are null or undefined; do not invent or interpolate them.
3. Compute the requested arithmetic mean from the available ratios.
4. Retain the physical unit even when fewer than the maximum number of ratios contribute.
5. Save `ratios_used` and `ratios_possible` with the mean.

A partial analysis window is not incomplete acquisition. Keep those concepts separate in labels and explanations.

## Plot contract

- One point per physical unit for every requested input parameter.
- Annotate device/unit ID when legible.
- Use a log response axis when ratios span orders of magnitude.
- Encode the contributing-ratio count by color or marker and publish it in the CSV.
- State the exact cycle window and arithmetic-mean definition in the caption.
- Verify the plotted point count equals the requested physical-unit count.
- Preserve stricter paired-window or feasibility analysis as a separate diagnostic; do not let it silently exclude units from this descriptive product.

## Provenance

Prefer curated per-cycle contrast tables. If generations differ, reconcile by unit and cycle, use explicit saved finite ratios, record each source path, and reject ambiguous duplicate histories rather than blending them silently.

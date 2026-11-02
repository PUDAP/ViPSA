# Consolidating scientific figures and delivering editable diagrams

Use this reference when a platform manuscript has many standalone figures and the author asks for a smaller set of composite figures before changing the manuscript.

## Narrative-first figure selection

Choose one main figure for each principal claim in the paper. A reliable five-figure sequence for an instrument/platform paper is:

1. platform design and physical implementation;
2. component and integrated calibration;
3. closed-loop performance and stability;
4. experimental workflow and control architecture;
5. campaign-scale scientific demonstration.

Avoid combining panels merely because they share a file type. Each composite needs one sentence that states its scientific message. Move full CAD plates, wiring detail, anomaly histories, and secondary validation plots to supplementary figures rather than shrinking them until unreadable.

## Planning gate

If the author asks for a plan first, inspect the source figures and manuscript references but do not edit the manuscript. Produce a panel map that states:

- source image or dataset;
- main claim supported;
- proposed panel letter;
- transformation or crop;
- main-text or supplementary destination;
- required sample size, exclusions, and scope language;
- missing input, if any.

Wait for approval before replacing LaTeX figure environments.

## Data and placeholder policy

Regenerate plots from authoritative raw data when available. Cropping an existing PNG is acceptable for a layout draft, but not the preferred publication source. If an authentic image, run-level distribution, or trustworthy analysis is unavailable, insert a conspicuous placeholder box that names the required evidence. Never fill a missing panel with invented data or an unrelated illustrative image.

For campaign figures, distinguish verified totals from unavailable distributions. Do not plot yield, resistance, ON/OFF, or thresholds from legacy derived fields known to be non-physical; regenerate them from ordered raw measurements with explicit quality gates.

## Editable SVG delivery

For requested editable flowcharts, create native SVG objects (`rect`, `text`, `path`, markers, and groups). Do not embed a PNG inside an SVG wrapper. Deliver both individual diagrams and one combined composite when useful. Verify:

- XML parses successfully;
- rendered previews have no clipping or overlap;
- every label remains legible at journal width;
- connector direction and safety boundaries are correct;
- the SVG contains zero embedded `<image>` elements unless the author explicitly requested a mixed photo/vector figure.

Package the individual SVGs in a ZIP for convenient handoff while also exposing the separate files.

## Figure design checks

- Use consistent panel labels, typography, SI units, colors, and line weights.
- Prefer 8–9 pt final printed text and vector plots/diagrams.
- Keep embedded panel titles out of source plots; use one composite caption instead.
- Preserve acquisition order in hysteretic electrical plots.
- Show setup-transient exclusions explicitly rather than silently removing them.
- Do not let workflow diagrams imply an agentic demonstration that has not been measured.
- Render and inspect every composite before manuscript insertion.

## Manuscript integration

After figure approval, update figure environments, captions, labels, cross-references, and supplementary references together. Compile from a clean output directory. Use float barriers or controlled page breaks so validation figures do not drift beyond conclusions or references. Inspect the full PDF as a contact sheet and then review dense tables and composite figures at full resolution.

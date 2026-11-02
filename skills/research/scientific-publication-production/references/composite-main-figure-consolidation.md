# Consolidating a manuscript into 4–5 main figures

Use this workflow when an author asks to reduce many standalone manuscript figures into a small narrative set, especially when some desired panels lack source data.

## 1. Plan before editing

If the author asks for a plan first, do not touch the manuscript. Inspect the current figure files and the sections/claims they support, then propose 4–5 figures organized by the paper's argument rather than by file availability. A useful platform-paper sequence is:

1. platform and modular construction;
2. component/integrated calibration;
3. closed-loop performance and stability;
4. experimental workflow and constrained control;
5. campaign-scale scientific demonstration.

For every proposed panel, state its source, principal claim, and whether it stays in the main text or moves to supplementary information.

## 2. Keep draft production separate

After approval to produce drafts, create a separate `figure_drafts/` directory and a reproducible build script. Do not overwrite source plots and do not edit LaTeX until the author approves the composites.

Create explicit placeholder boxes where evidence is unavailable. Each placeholder should say what is missing and what provenance/selection rule is required, for example:

- authentic instrument/sample image with verified provenance;
- raw ordered sweeps selected by predeclared criteria;
- run-level timing records needed for a distribution.

Never fill a missing panel with synthetic scientific data or a decorative image that could be mistaken for evidence.

## 3. Consolidate by evidentiary strength

When old and new calibration plots overlap, keep the dataset with the stronger design (more repeats, direction-specific fits, visible anomalies) in the main figure. Move legacy aggregate plots and detailed diagnostics to supplementary figures.

Preserve unsuccessful or anomalous observations when they materially justify safeguards. Examples include wrong-sign motion, stalls after reversal, setup transients, and return error. Do not hide them merely to simplify the layout.

## 4. Composite layout rules

- Use consistent panel lettering, typography, units, colors, and thresholds.
- Prefer vector regeneration from raw data; crop existing raster plots only as a documented fallback.
- Remove embedded plot titles before adding composite panel titles, otherwise headings overlap.
- When splitting a two-panel raster, avoid exact midpoint crops that cut y-axis labels or leave a stray strip. If clean separation is not possible, retain the original pair as one composite panel.
- Do not embed a full four-panel CAD plate unchanged inside another four-panel figure. Select the views needed for the main claim and move the full plate to supplementary information.
- Tight-crop CAD views around geometry, excluding inherited titles, captions, and unrelated panel labels.
- Keep workflow boxes inside axes bounds and verify first/last boxes and arrowheads are not clipped.
- Avoid dual-axis bar charts unless each axis is clearly colored and every bar is directly labeled.

## 5. Scientific scope rules

- A motion-controller readback is not independent evidence of physical displacement.
- A fixed-coordinate vision pilot is not a holder-wide pad-to-probe benchmark.
- Lateral image shift during Z commands is not absolute Z calibration.
- Architecture diagrams may show implemented interfaces and deterministic guards, but must not depict autonomous recovery as completed unless prospective evidence exists.
- Campaign figures must distinguish verified totals from missing distributions or invalid legacy derived fields.

## 6. Visual QA loop

Render every composite at final or higher resolution and inspect it directly. Check:

- panel-title overlap and duplicate embedded titles;
- clipped axes, labels, workflow boxes, arrows, and legends;
- tiny text after two-column reduction;
- stray crop strips from source multipanel images;
- ambiguous placeholders;
- panel order matching the manuscript narrative;
- actual metrics visually distinct from planned/missing evidence.

Revise and inspect again. File generation alone is not verification.

## 7. Manuscript integration

Only after author approval:

1. map each composite to the section and claim it supports;
2. replace redundant figure environments;
3. update labels, references, and captions;
4. move detailed panels to supplementary figures;
5. compile and inspect every affected page;
6. verify all figures appear before conclusions/references and all displayed numbers match authoritative data.

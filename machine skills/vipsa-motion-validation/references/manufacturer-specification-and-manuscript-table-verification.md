# Manufacturer specifications and manuscript-table verification

Use this note when filling manufacturer-specification rows alongside measured ViPSA motion results.

## Source hierarchy

1. Confirm the exact installed part number, not only the series name.
2. Prefer the manufacturer's current series datasheet and official product API/page over reseller summaries.
3. Record the access date and direct URL in the manuscript.
4. Keep manufacturer specifications separate from installed-system measurements.

For Zaber product pages, the official JSON endpoint can expose structured part specifications even when the rendered HTML omits the table:

`https://www.zaber.com/api/my-series/url/X-LSQ`

Find `base_parts[]` where `base_part == "X-LSQ150A"`, then read `base_part_specs[]` by `definition.spec`. Verify the same values against the official series datasheet:

`https://www.zaber.com/fs/datasheets/X-LSQ-Datasheet.pdf`

## X-LSQ150A values verified in 2026-09

Both ViPSA coarse axes use X-LSQ150A:

- travel range: 150 mm;
- default microstep size: 0.09921875 µm;
- unidirectional accuracy: 45 µm;
- repeatability: <2 µm;
- backlash: <15 µm;
- maximum speed: 53 mm/s.

The generated part-specific PDF reported a tighter backlash value (<9 µm), while the series datasheet and product API agreed on <15 µm. Use the conservative <15 µm value and document the chosen source when official outputs disagree.

## Reporting rules

- Do not present manufacturer accuracy, repeatability, or backlash as measured installed-system performance.
- Preserve separate rows for manufacturer specification, workflow/software nominal conversion, controller readback, and optically measured integrated calibration.
- If a workflow assumes 0.1 µm/native unit while the official default microstep is 0.09921875 µm, label 0.1 explicitly as the workflow or software nominal rather than silently calling it the manufacturer value.
- After editing a LaTeX table, compile, extract PDF text, render the affected page, and visually check column alignment, clipping, unit rendering, and status labels.
- Use ragged-right paragraph columns for narrow prose/status columns to avoid stretched interword spacing.

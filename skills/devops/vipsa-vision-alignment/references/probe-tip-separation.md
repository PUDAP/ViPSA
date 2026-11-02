# Probe-tip separation / annotation

Session-derived note for one-off microscope images where the user asks to separate or identify the probe tip.

## Trigger

Use this when the task is image-only: "separate where the probe tip is in this photo", "mark the probe tip", "where is the probe tip", etc. This is not necessarily a physical alignment or move request.

## Practical workflow

1. Inspect the image visually/with vision first.
   - Probe body/taper: typically brown/metal, elongated, triangular or tapered, entering from a side of the image.
   - Contact pad: dark square/rectangular feature, should not be labeled as the probe tip.
2. Estimate the full-image tip coordinate at the terminal point of the taper nearest the pad.
3. Generate an annotated output image:
   - orange/yellow overlay following the visible probe taper/body
   - red dot/circle at the estimated tip
   - optional text label `probe tip`
4. Return concise result:
   - approximate full-image pixel coordinate `(x, y)`
   - note that the pad is separate from the tip if ambiguity matters
   - attach the annotated image with `MEDIA:/absolute/path`

## Implementation note

For OpenCV annotation scripts, use:

```bash
/home/vipsa/.venvs/align-cv2/bin/python /tmp/annotate_probe_tip.py
```

The default Hermes Python may not have `cv2`; do not stop at `ModuleNotFoundError`. Use the dedicated `align-cv2` venv from the parent skill's Environment setup, or create it if absent.

## Overlay convention

- Probe taper/body: orange/yellow line, contour, or semi-transparent mask.
- Estimated tip: red dot and/or red circle.
- Keep labels minimal so the microscope content remains visible.

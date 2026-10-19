# Image-selected pad relocation with adaptive verification

Use when a user marks a target pad in an older camera image and asks to move to it.

## Workflow

1. Establish safety: SMU output off, switch channels open, machines idle.
2. Read current stage and Zaber positions.
3. If lateral motion is requested while approached, retract stage Z by a known bounded amount and verify the signed readback delta.
4. In the user image, distinguish annotations (arrow/markup) from the target pad. Estimate:
   - visible probe-tip coordinate;
   - marked pad centroid;
   - image resolution.
5. Convert the pixel offset to the live-stream resolution before applying calibration. Never use coordinates from a downscaled Telegram image directly against a full-resolution steps/pixel calibration.
6. Make one bounded Zaber correction using the established axis signs and nominal axis-specific steps/pixel.
7. Capture a fresh frame and verify the same target by surrounding grid geometry, pad size, defects/marks, and neighborhood—not nearest-centroid alone.
8. Derive observed axis scales only from a plausible same-target response:
   `M_axis = abs(commanded_steps / (offset_after - offset_before))`.
9. Apply at most a bounded adaptive refinement, recapture, and report residual to the **actual visible probe tip**, not frame center.
10. Keep the stage retracted unless the user separately asks to approach/contact. Geometric alignment is not electrical contact.
11. Finish with lights off by default, outputs off, switch open, and controller states verified idle.

## Reporting

Report the verified final Zaber position, stage Z/retracted state, visual residual, and a clear statement that electrical contact has not been established.
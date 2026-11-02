# User-annotated arbitrary-pad alignment

Use when the user marks a specific pad in an uploaded Camera-1 image (arrow, circle, or “move here”). This is **not** the standard nearest-pad/frame-center procedure.

## Safe workflow

1. Verify the annotated image’s pixel dimensions. Identify separately:
   - the annotation geometry (arrow/mark),
   - the center of the physical target pad indicated by it,
   - the actual visible probe-tip coordinate.
   Never use the arrow tip itself as the motion target unless it coincides with the pad center.
2. Confirm the requested target is a real, distinctive pad by its size and neighborhood. Preserve those surrounding features as the identity check after motion; do not silently substitute a nearer pad.
3. Before any lateral Zaber move, retract stage Z to the known safe tracked retracted position with SMU output off and 707B open. Verify the signed Z change and readback. Geometric alignment while retracted does not establish electrical contact.
4. Convert uploaded-image coordinates to the live Camera-1 resolution explicitly. For example, a 960×540 supplied frame mapped to a 1920×1080 stream uses a ×2 coordinate scale. Compute target-minus-probe offset in the same coordinate frame.
5. Use axis-specific calibrated response rather than a single isotropic scale when available. Apply one bounded first-pass X/Y move, then capture a fresh live frame.
6. In the fresh frame, locate the **same distinctive target pad** and actual probe tip. Compute residual `(pad_center - probe_tip)`; do not assess residual against frame center.
7. If residual is significant, estimate observed axis response from commanded native steps and measured before/after pixel offsets, then make a bounded empirical correction. Recapture after every correction. Stop at tolerance or when improvement stalls.
8. Final report must include final Zaber readback, residual pixels, an attached verification image, retracted/contact status, output-off/707B-open state, light cleanup, and idle states. Say “geometrically aligned” rather than “in contact.”

## Coordinate/response example

For an uploaded half-resolution image, an offset of `(369, -195) px` becomes `(738, -390) px` at full resolution. After a first move, derive each scale from the observed response:

```text
steps_per_px_x = abs(move_x_steps / (offset_after_x - offset_before_x))
steps_per_px_y = abs(move_y_steps / (offset_after_y - offset_before_y))
```

Use the live observed signs and clamp the correction; camera/Zaber sign conventions must be verified from the first move rather than assumed blindly.

## Historical-height follow-up

If the user later asks for the Z used on a nearby device shown in an image, do not infer Z from pixels or “above/below” alone. Correlate the exact target with run timestamp, Zaber position, image neighborhood, and saved stage metadata, then follow the stage coordinate-frame reconstruction reference in `vipsa-machine-operations`.

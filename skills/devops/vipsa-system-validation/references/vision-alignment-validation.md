# Vision-alignment validation pitfalls

Use when validating Camera-1 probe-to-pad alignment as part of a ViPSA release/publication benchmark.

- Distinguish return-to-fixed-image-coordinate repeatability from actual pad-to-probe alignment. The latter requires a confirmed physical apex target.
- Target the sharp visible probe apex, not image centre, pad centre, or probe-body centroid.
- A fixed-ROI detector can be repeatable without being generally accurate; one manual annotation is not a multi-annotator absolute-accuracy benchmark.
- Dark probe and pad silhouettes can merge at overlap. Never let a connected-component detector redefine the apex from a merged component. Preserve the last clean apex coordinate; infer an obscured pad centre from a verified regular grid only when necessary, and label the residual as inferred.
- Before lateral motion, verify probe clearance and preserve the authorized Z sign. Check the live Stage schema: Z uses `move_z_by(height, feedrate=...)`; X/Y use `move_x_by(steps)` and `move_y_by(steps)`.
- Fresh optical response overrides controller tracking. Stop blind accumulation if movement is wrong-sign, magnitude-inconsistent, or stalled; use bounded camera-verified coarse correction while retracted when appropriate.
- Current illumination is one coiled addressable RGBA strip. Firmware modes are white-max on, off, red, green, and rainbow; do not claim unavailable left/right, intensity, or spatial controls.
- Report direct vs inferred coordinates, axis-specific pixel scales, commands and optical responses, residual components/radial residual, clearance, illumination mode, and final run cleanup.

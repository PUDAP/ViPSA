# ViPSA camera-ruler motion calibration

Verified workflow for calibrating coarse Zaber and fine OpenFlexure X/Y motion against Camera 1.

## Method

1. Use a traceable ruler/grid with known pitch. Calibrate Camera 1 independently for X and Y by rotating the scale 90°; do not assume square pixels.
2. Fit detected tick positions against integer division index and retain µm/pixel plus fit residual.
3. Verify probe retraction, travel clearance, live machine identity/state, and the user's requested light state.
4. Hold the non-tested stage fixed. For every magnitude, sign, and repeat, save `before`, `after`, and `return` images.
5. Move only through PUDA driver methods. For Zaber physical calibration, native commands avoid unit-serialization ambiguity.
6. Split long acquisition by command magnitude and append each completed excursion to CSV so partial progress survives timeouts.
7. Measure optical shift, convert with the axis-specific pixel scale, fit signed displacement through the origin, and fit positive/negative directions separately.
8. Report scale, direction asymmetry, repeatability, reversal/return error, wrong-sign events, and final optical-anchor residual.
9. Verify fresh readbacks and final `idle`, `run_id: null`. `stage.set_zero()` resets tracking only; `[0,0,0]` is not an absolute physical origin.

## Recovery and interpretation

- Track signed net movement. After interruption, inspect the exact live run and edge response: COMPLETE the live run ID; undo only moves confirmed as executed; then verify the optical anchor.
- Zaber can have excellent scale linearity but material reversal error. Use consistent-direction final approach or camera-verified compensation.
- OpenFlexure geared motion can depend on preload/direction. Begin with a bounded sensitivity trial, characterize reversal deadband, and reject/flag wrong-sign responses.
- Do not interpret perpendicular image displacement as mechanical cross-axis coupling until camera/ruler rotation is removed.

## Video evidence

Record both RTSP streams to separate MKV files with stream copy, remux to MP4 after controlled stop, and create a side-by-side accelerated copy for chat. Verify sampled start/middle/end frames.

## Session-specific observations

Do not reuse these constants after optical/mechanical changes: Camera X 1.822287 µm/px, Camera Y 1.824598 µm/px; Zaber X 0.0991555 µm/native, Zaber Y 0.0994266 µm/native. OpenFlexure exhibited direction dependence, X reversal deadband around five command steps, and one Y wrong-sign event; these justify optical closure rather than permanent universal constants.

# Probe-tip-targeted ViPSA camera-1 alignment (2026-08-08)

## Why this reference exists

A legacy alignment runner ranked pads by distance to the centered ROI and moved the selected pad to the frame center. In the current 1920×1080 camera-1 microscope view, the physical probe tip was visibly far from frame center. Blindly using the frame center would therefore align the pad to the wrong point.

## Validated workflow

1. Retract stage Z enough for lateral Zaber motion; force Keithley output off, open all 707B channels, and keep illumination temporary.
2. Probe the camera stream before turning on the light, then capture a fresh camera-1 frame.
3. Determine the **actual probe-tip target in full-image pixels** from the current image/calibration. For this session it was approximately `(640, 528)` in a 1920×1080 frame. Treat this as session-specific and revalidate after camera/optics/resolution changes.
4. Detect plausible square pads near that target. The current substrate showed bright pads on a dark background, so a bright-response mask (`gray - blurred_background`) worked; other illumination may require the established dark-response mask. Apply square/area/extent filters and inspect the annotated preflight before motion.
5. Let `offset = pad_centroid - probe_tip_target`. Under the verified ViPSA sign convention, command `zaber_axis_steps = round(offset_axis × steps_per_pixel_axis)`.
6. Use a bounded first correction with the nominal calibration, recapture, and require the same physical pad/geometry. Derive observed axis-specific scale from the verified response when plausible: `M_axis = abs(step_axis / (offset_after - offset_before))`.
7. Apply at most a bounded adaptive second correction, recapture, and stop inside tolerance. If the feature changes, response sign is implausible, or motion barely changes the offset, stop and roll back rather than adapting.
8. Produce a final overlay showing probe target, selected square pad, centroid, and residual. Turn the light off and verify Zaber/stage/light idle, Keithley output off, and 707B open.

## Session result

- Initial nominal multiplier: `21.5 native steps/px`.
- Pass 1: X `+702`, Y `−1458`.
- Observed post-move scales used for refinement: X `31.94`, Y `19.02 native steps/px`.
- Pass 2: X `+341`, Y `+168`.
- Final residual: X `−4.1 px`, Y `−1.1 px`, distance `4.2 px`.
- The final overlay visually confirmed a plausible square contact pad under the marked probe tip. This verifies geometry only, not electrical contact.

## Durable lesson

Alignment means pad-to-**probe-tip**, not pad-to-frame-center. A centered ROI is only a search window unless the physical tip has independently been calibrated to its center. Pad polarity (bright versus dark) must also be selected from the current frame rather than hard-coded.

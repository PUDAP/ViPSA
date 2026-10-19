# Resolution-aware ViPSA pad alignment calibration (2026-07-20)

## Trigger

Use when a valid camera-1 contact-pad frame is available, the standard first correction uses the usual native-steps-per-pixel multiplier, but the verified residual shows axis-specific over/undershoot after a camera resolution, crop, or optical-scale change.

## Safe workflow

1. Capture and visually inspect a preflight frame before motion. Confirm a sharp, illuminated contact-pad grid and probe view—not a motor/stage assembly—and confirm the selected contour is a plausible square pad.
2. Detect the nearest valid dark-square contour in the centered `900x900` ROI and record its signed offset `o0 = pad - ROI_center`.
3. Apply the standard first correction using the current nominal multiplier.
4. Recapture, verify the detector selected the **same physical pad**, and record `o1`.
5. Derive per-axis observed scale only where response is nontrivial and plausible:
   - `M_axis = abs(step_axis / (o1_axis - o0_axis))`
   - next correction: `step_axis = round(o1_axis * M_axis)`
6. Recapture after every correction. Stop within the requested tolerance; a bounded micro-correction may be used if the final residual is just outside tolerance.
7. If the offset barely changes after a large move, changes with an implausible sign, or the selected contour jumps to a different pad/feature, stop and rollback rather than adapting the calibration.
8. Turn lights off after final verification unless the user requested them left on. Verify `zaber`, `light`, and `stage` return to `idle`, `run_id: null`, and attach the final overlay.

## Worked session

A `1920x1080` frame had initial offset `(11.805, 125.446) px`. The nominal `25 steps/px` first move was `(X +295, Y +3136)`, producing residual `(0.430, -45.579) px`. This showed different observed scales by axis:

- `Mx = 25.93 native steps/px`
- `My = 18.34 native steps/px`

An adaptive second move `(X +11, Y -836)` reduced the residual to `(-1.189, -6.440) px`. A bounded micro-correction `(X -31, Y -118)` produced final residual `(0.533, 0.242) px`, distance `0.586 px`.

Total correction was `(X +275, Y +2182)` native steps. Final overlay and machine-state verification were produced; lights were turned off.

## Durable lesson

Do not assume one historical steps-per-pixel constant remains exact across camera resolutions or both axes. Use the nominal multiplier for the first bounded correction, then let verified before/after image response calibrate each axis independently—without relaxing pad-identity and rollback guards.

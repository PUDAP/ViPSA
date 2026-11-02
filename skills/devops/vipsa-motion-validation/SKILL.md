---
name: vipsa-motion-validation
description: Use when calibrating or validating integrated ViPSA motion.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vipsa, puda, calibration, motion, drift, repeatability, opencv]
    related_skills: [vipsa-machine-operations, vipsa-image-capture, vipsa-vision-alignment, puda-operations]
---

# ViPSA Motion Validation

## Scope

Use this skill for integrated X/Y stage calibration, return-to-position tests, backlash/reversal characterization, repeatability, settling, stationary drift, cross-axis coupling, and manuscript-ready motion validation. It covers both the Zaber coarse stages and OpenFlexure fine stage.

Load the companion machine-operation and image-capture skills before physical side effects. Preserve the exact authorized axis/sign, retract the probe before coarse lateral motion, hold the non-tested stage fixed, and verify PUDA cleanup after interrupted or completed runs.

## Core principle

Validate the installed camera–stage–holder system optically. Manufacturer specifications and controller readbacks are useful metadata but are not substitutes for measured integrated displacement.

Calibrate Zaber and OpenFlexure separately. Never attribute observed motion to one actuator if both moved during the trial.

## Reference artifact

- `references/integrated-motion-and-drift-calibration-2026-08.md` contains the verified Camera 1 scale, installed X/Y Zaber and OpenFlexure results, one-hour drift result, and the session-specific manuscript interpretation.

## Standard X/Y calibration workflow

1. **Preflight**
   - Verify Camera 1 stream and ruler/fiducial visibility.
   - Verify `stage`, `zaber`, and `light` are idle with `run_id: null`.
   - Confirm the probe is retracted before any Zaber lateral movement.
   - Fix focus, exposure, gain, illumination, and camera mount.
2. **Pixel scale**
   - Image a traceable or documented scale in the sample plane.
   - Fit multiple marks rather than measuring one interval.
   - Calibrate X and Y independently; rotate the same scale by 90° when needed.
   - Save tick coordinates, fitted spacing, residual RMS, overlay, and physical units/pixel.
3. **Actuator isolation**
   - Hold OpenFlexure fixed during Zaber calibration.
   - Hold Zaber fixed during OpenFlexure calibration.
4. **Excursion matrix**
   - Use multiple short/medium/long commands, both directions, repeated trials, and return images.
   - For publication-quality claims, target at least 10 repeats per condition and multiple holder locations where practical.
   - Save command, axis, sign, repeat, before/after/return images, timestamps, controller readback, and environmental/lighting state.
5. **Optical measurement**
   - Register before→after for displacement and before→return for return error.
   - Convert pixels with the axis-specific camera scale.
   - Fit direction-specific slopes through the origin only when physically justified; also inspect residuals and direction asymmetry.
6. **Reversal and small-step checks**
   - Explicitly test reversal deadband and same-direction preload.
   - Do not assume geared OpenFlexure commands are symmetric or reliable at the smallest step size.
   - Reject a move whose observed image response has the wrong sign; recover with bounded corrections and recapture.
7. **Cleanup and verification**
   - Return the physical target near its optical anchor, not merely controller zero.
   - Use `set_zero` only as a tracked reference; do not describe it as an independently measured absolute origin.
   - Complete/reset any retained run ID and verify final machine states.
   - Preserve the requested final illumination state.

## Axis conversion rule

Never reuse a stale global steps/pixel multiplier after a new calibration. Compute per axis from verified values:

`native_units_per_pixel = camera_axis_um_per_px / stage_axis_um_per_native_unit`

Use a calculation tool, preserve signs explicitly, and retain both the raw calibrated values and resulting conversion in the run artifacts. Direction-specific OpenFlexure conversions should remain separate when asymmetry is material.

## Image-registration quality gate

A small reported displacement is not trustworthy by itself.

- Always record the registration response/correlation.
- Full-frame phase correlation can be weak on low-texture scenes even when its displacement looks plausible.
- If confidence is weak, select a stable high-contrast ROI and rerun with OpenCV ECC translation registration or another independently validated method.
- Validate sign conventions using a known synthetic or physical shift.
- Report the ROI, preprocessing, model, confidence range, and any excluded frames.
- Preserve the original analysis rather than silently overwriting it.

A verified drift analysis should report net drift, peak-to-peak excursion, standard deviation, fitted slope, duration, frame count, registration confidence, and the fact that integrated drift combines camera, optics, thermal, and mechanical effects.

## Interpretation and tolerance

Define tolerance from the workflow and pad geometry before declaring pass/fail.

- Coarse-stage accuracy may pass if it keeps the target inside the camera field and fine-stage capture range; this does not prove blind pad landing.
- Fine-stage performance may pass under camera-verified correction even when open-loop direction asymmetry is significant.
- Keep anomalous wrong-sign or failed moves visible in the dataset and manuscript.
- Do not claim absolute Z displacement from an unsuitable webcam. Defer metric Z calibration until an appropriate external reference is available.
- Do not interpret apparent image motion on the orthogonal axis as mechanical cross-axis coupling until ruler/camera rotation is separated from true motion.

## Manuscript-ready outputs

Produce:

- raw acquisition CSV and machine logs;
- calibrated per-axis result CSV;
- commanded-versus-measured plots;
- return-error/repeatability plots;
- scale-detection and representative motion overlays;
- drift plot and summary;
- concise Markdown report with methods, results, limitations, and final state.

Place concise measured values in the hardware tables, full methods/results in `System Validation and Benchmarking → Motion Calibration`, workflow implications in Discussion, and reversal/small-step/cross-axis/Z limitations in Limitations. Put raw images, scripts, logs, videos, and complete reports in supplementary data or the repository.

## Reporting style

Report verified values concisely. Distinguish nominal, tracked, optically measured, and physically inferred states. Never overclaim motion, return-to-zero, cross-axis coupling, or tolerance from controller status alone.
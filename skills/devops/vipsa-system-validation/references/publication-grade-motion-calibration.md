# Publication-grade ViPSA motion calibration

## Evidence rule

Controller coordinates are telemetry, not independent displacement evidence. After a Stage edge/driver restart, tracked OpenFlexure position may restart at `[0,0,0]`; record it as a run-local software origin, never as a verified physical origin.

Independent metrology:

- Zaber X/Y and OpenFlexure X/Y: Camera 1 plus a stage micrometer or traceable calibration grid.
- OpenFlexure Z: dial indicator, laser displacement sensor, or calibrated side-view imaging. A top-down camera can measure lateral cross-axis shift, focus change, image return, and drift, but normally cannot prove absolute vertical µm/step.

## Preflight

1. Inspect live `stage`, `zaber`, and `light` state/signatures.
2. Verify the probe is physically retracted and authorized travel is clear before lateral motion.
3. Read Stage and Zaber positions, keeping tracked Stage coordinates distinct from Zaber hardware telemetry.
4. Confirm exactly one edge owns each device. Detect duplicate `main.py` processes by process CWD because wrappers may appear only as `uv run main.py`.
5. To recover a stale Stage edge, stop its wrapper and child, launch exactly one replacement, wait for subscriptions, then run a harmless START → `get_current_position` → COMPLETE transaction. Verify `idle`, `run_id:null` before motion.
6. Do not use `puda machine reset stage` as normal recovery when reset is not exposed; restart one edge and validate read-only.
7. Record target ID, camera resolution, optics/focus, illumination, units, speed/acceleration, temperature, and timestamps.

## Camera scale

1. Mount the micrometer/grid flat and focus Camera 1.
2. Estimate X and Y scale from several known intervals.
3. Repeat near field centre and corners to quantify distortion.
4. Save raw/annotated images and fit residuals.

## Zaber X/Y

For each axis, use several safe distances spanning local and long-range motion (for example 0.5, 1, 5, and 10 mm):

- at least 10 unidirectional repeats per distance;
- matched positive/negative moves;
- reversal tests for backlash;
- move-away-and-return trials.

Measure from registered images. Report scale error, positioning error, repeatability, reversal error, and return error, including median/95th percentile/max.

## OpenFlexure X/Y

Use several signed command sizes (for example 1, 2, 5, 10, 25, and 50 Stage steps when safe), repeated both ways. Measure µm/step, repeatability, hysteresis, return error, and cross-axis displacement.

All motion must pass through the Python `Stage` driver/PUDA layer. Never use raw G-code, and never move Stage X/Y without explicit authorization.

## OpenFlexure Z

With independent vertical metrology, test multiple signed increments/reversals, including the installed minimum command when relevant. Report vertical µm/step, repeatability, hysteresis, return error, and induced X/Y shift. Preserve `Z Up=+`, `Z Down=-` exactly.

Without vertical metrology, restrict claims to tracked response, lateral coupling, focus/visual change, and image-return repeatability. Do not claim calibrated absolute Z.

## Drift and settling

Track a fixed feature after representative motion. Capture periodically for about one hour or the intended experiment duration. Report initial settling, X/Y drift versus time, and drift rate; include Z when independently measured.

## Data contract

Save CSV/JSON fields for axis, command, units, direction, repeat, start/end readbacks, independently measured displacement, image paths, timestamps, environment, and validity/exclusion reason. Preserve PUDA logs and raw images. Generate scatter-only plots for commanded-versus-measured displacement, residuals, reversal/return error, coupling, and drift.

Always report commanded motion, controller readback, independent displacement, optical evidence, and assumptions separately.
# Alignment with lights intentionally left on — 2026-06-12

## Trigger

Use this when the user asks to perform ViPSA camera alignment and explicitly requests that the lights remain on afterward.

## Workflow note

The normal alignment cleanup may turn lights off, but when the user says to leave lights on:

1. Turn lights on before capture.
2. Perform camera1 pad-centering alignment using the existing dark-pad detector / ROI workflow.
3. Run one or two Zaber XY correction passes as needed.
4. Capture and annotate a final verification image.
5. In the `finally` / cleanup block, call `light.turn_on()` rather than `turn_off()`.
6. Verify `light`, `zaber`, and `stage` return `idle`, `run_id: null`.

## Observed calibration from session

A two-pass alignment using multiplier `25 native Zaber steps / pixel` moved:

- Pass 1: X `-176`, Y `-1106` for offset about `(-7.0, -44.2) px`.
- Pass 2: X `+30`, Y `+409` for offset about `(1.2, 16.4) px`.
- Final offset: about `(0.54, 0.10) px`, distance `0.55 px`.

This supports the existing 25 steps/px correction factor for this setup, but still verify with a final image every time.

## Reporting

Return the final offset, the Zaber moves, final machine states, and the final annotated image. State explicitly that the final `light.turn_on()` succeeded if lights are meant to stay on.

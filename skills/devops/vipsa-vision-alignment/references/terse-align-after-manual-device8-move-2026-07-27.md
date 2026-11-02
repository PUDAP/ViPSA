# Terse/current-device align after manual S9 device-8 moves (2026-07-27)

## Trigger
Use when the user says only `align` after a manual grid move / stage-Z clearance, or says `restart the grid measurement; start with aligning the current device`. They expect the standard live camera-1 pad-centering action first, not a plan.

## Verified command shape
Run the canonical editable align script with explicit live endpoints when needed:

```bash
/home/amdm/.venvs/align-cv2/bin/python \
  /home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/align.py \
  --execute \
  --nats-servers nats://100.109.131.12:4224 \
  --rtsp rtsp://100.74.20.98:8554/camera1 \
  --final-light on
```

This preserves the script's standard settings: `900x900` ROI, `21.5` native Zaber steps/pixel, `5 px` tolerance, up to two correction passes, and final light left on.

## Restart-grid alignment handoff

When alignment is the first step of restarting a grid measurement:

1. Verify there is no old active grid runner and that stage/Zaber/light are idle/null before aligning.
2. Run the standalone align script and verify the final residual is inside tolerance.
3. Record the final Zaber readback and annotated image path.
4. Launch the grid continuation in a fresh output folder after alignment.
5. Mark the first grid device as externally/currently aligned so the runner does not immediately redo first-device vision alignment or snap back to nominal grid X/Y. It should still turn lights off and run electrical approach before DCIV/pulses.

## Example result patterns

Earlier manual device-8 align:
- Pass 1 near-pad offset about `(13 px, 47 px)` -> native Zaber correction around `(x=+285, y=+1003)`.
- Pass 2 residual about `(-1.3 px, -8.2 px)` -> correction around `(x=-28, y=-176)`.
- Final residual about `(0.06 px, -4.51 px)`, distance `4.51 px`, within the `5 px` tolerance.

Restart-grid align:
- Pass 1 offset about `(10.9 px, -0.5 px)` -> native Zaber correction around `(x=+234, y=-11)` using the active sign convention.
- Final residual about `(-1.6 px, -0.44 px)`, distance `1.67 px`, within tolerance.

## Reporting shape

Report concisely:
- 🎯 aligned / residual distance and tolerance result.
- Native Zaber correction(s) and final Zaber readback.
- Stage unchanged unless it was moved.
- Final light state.
- `MEDIA:` final annotated image.
- If this was a grid restart, include the new runner process id and run folder separately after launch.

## Pitfall
Do not stop at the first post-move image when residual is just above tolerance; let the canonical two-pass script run its bounded second correction. Conversely, when the final residual is inside tolerance, stop and report alignment rather than adding extra unrequested correction passes.

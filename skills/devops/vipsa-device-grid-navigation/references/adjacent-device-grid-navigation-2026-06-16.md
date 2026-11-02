# Adjacent-device grid navigation run note — 2026-06-16

## Durable workflow learned

When the user asks to move to an adjacent ViPSA device and then align/approach, treat the grid travel as a multi-phase operation with resumable checkpoints:

1. Safe clearance move on microscope stage Z: `stage.move_z_by(height=-35, feedrate=450)`.
2. Zaber native grid move using the direction mapping:
   - right: `move_x_by(+5000, units=None)`
   - left: `move_x_by(-5000, units=None)`
   - below: `move_y_by(+5000, units=None)`
   - above: `move_y_by(-5000, units=None)`
3. Camera-based pad alignment, with lights on only for imaging.
4. Turn lights off before electrical approach unless explicitly told otherwise.
5. Keithley-guided contact approach, with cleanup and state verification.

## Resumability pitfall

If the grid pre-move succeeds but a later phase fails (for example image capture/alignment), do **not** repeat the `-35` stage clearance and `5000` Zaber grid pitch on retry. Resume from the completed checkpoint and continue with alignment/approach only. In scripts, support a flag such as `SKIP_PREMOVE=1` or equivalent checkpoint detection.

## Camera capture robustness

For alignment capture, use the standard camera-1 RTSP image path. If a preferred capture executable fails in the current runtime, retry with OpenCV `cv2.VideoCapture(RTSP, cv2.CAP_FFMPEG)` and write a local JPG artifact, rather than abandoning the hardware sequence after the movement already completed.

## Reporting detail

Report:

- the signed pre-move commands and readbacks;
- final Zaber position;
- final alignment residual and annotated image;
- approach current and whether it landed in target range;
- if final current is below target after guard retract, explicitly say the device was left in the safer weak/open-contact state rather than over-current;
- cleanup state: Keithley output off, 707B open/closed channels nil, relevant machines idle.

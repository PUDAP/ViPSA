# ViPSA terse align + overlay photo request (2026-06-25)

Trigger: user asks tersely for alignment plus an overlay image, e.g. `align and send a photo with overlay`.

Validated workflow:

1. Treat as a complete ViPSA camera-1 contact-pad alignment task, not just image capture.
2. Use PUDA protocol-first light/Zaber control from `/home/vipsa/vipsa-puda-project`.
3. Current reusable runner: `/home/vipsa/vipsa-puda-project/runs/run_alignment_now_turn_off.py`.
   - Uses camera 1 RTSP (`rtsp://100.67.251.110:8554/camera1`).
   - Uses OpenCV dark-pad detection in centered 900x900 ROI.
   - Uses 25 native Zaber steps per pixel.
   - Runs up to two correction passes, stopping if residual distance is <= 5 px.
   - Performs a final verification capture and writes `final_annotated.jpg`.
   - Turns lights off afterward by default.
4. After the script finishes, verify the final annotated image exists and is non-empty before sending `MEDIA:`.
5. Concise report fields:
   - 🎯 aligned status
   - Zaber move(s) applied in native steps
   - final offset x/y/dist in px
   - final `zaber`, `light`, and `stage` state (`idle`, `run_id: null` when verified)
   - attach only the final overlay unless the user asks for raw/mask images.

Example successful result format:

```text
🎯 Aligned.

- Move applied: Zaber X +253, Y +306 native steps
- Final offset: x=-2.35 px, y=-3.59 px, distance 4.29 px
- Final state: zaber, light, stage all idle, run_id: null
- Lights turned off after capture

Overlay photo:
MEDIA:/home/vipsa/vipsa-puda-project/runs/<run>/final_annotated.jpg
```

Pitfall: do not leave the turn after merely turning lights on or capturing a raw photo. The user asked for alignment, so execute the full align/correct/verify path and send the overlay artifact.
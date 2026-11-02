# Stage Z motion video capture — 2026-06-24

Reusable pattern for requests like: “move Z stage down by 25 steps and send a video of it.”

## When to use

Use this for a visual record of a manual stage-Z jog, especially when the user asks for a video rather than just a still image.

## Confirmed workflow

1. Use PUDA protocol-first control for the actual motion.
2. Interpret user direction with the current ViPSA convention:
   - `up` -> positive `stage.move_z_by(height=+N, feedrate=450)`
   - `down` -> negative `stage.move_z_by(height=-N, feedrate=450)`
3. Verify active env and pre-motion stage state with bounded checks:
   - `puda env current`
   - `timeout 5 puda machine state stage`
4. Turn the light on before recording unless the user explicitly says not to illuminate.
5. Start an OpenCV RTSP recorder thread before sending the motion protocol:
   - default stream for a single “send a video” request can be `camera1`, unless the user asks for camera 2 or both cameras.
   - known RTSP URLs in this setup:
     - `rtsp://100.67.251.110:8554/camera1`
     - `rtsp://100.67.251.110:8554/camera2`
   - use `cv2.VideoCapture(url, cv2.CAP_FFMPEG)` and `cv2.VideoWriter(..., fourcc='mp4v', fps≈10)`.
   - include a short pre-roll (~1–2 s), keep recording through the move, then include a short post-roll (~2 s).
6. Execute a one-command full-metadata PUDA protocol:
   - `stage.move_z_by(height=<signed_steps>, feedrate=450)`
7. Stop the recorder, verify the MP4 exists, has non-zero size, and record the frame count if available.
8. Run a separate position readback protocol:
   - `stage.get_current_position()`
   - report returned `response.data.result` exactly/compactly.
9. Turn the light off in a cleanup/finally path, then verify:
   - `timeout 5 puda machine state light`
   - `timeout 5 puda machine state stage`
10. Reply tersely with signed motion, final Z readback, stage/light idle verification, and attach the video via `MEDIA:/absolute/path.mp4`.

## Notes and pitfalls

- Do not use one combined protocol for `move_z_by` + `get_current_position`; use a separate position-read protocol after the move to avoid run-state/readback mismatch.
- If recording fails but the motion succeeded, still perform light-off and state verification, then report the motion separately from the missing video rather than implying a video was captured.
- Use OpenCV RTSP recording instead of direct physical camera capture when livestream/MediaMTX already owns the camera devices.
- Store session artifacts under `/home/vipsa/vipsa-puda-project/runs/videos/` with descriptive filenames, e.g. `camera1_z_down25_<timestamp>.mp4`, plus a JSON sidecar for verification output.

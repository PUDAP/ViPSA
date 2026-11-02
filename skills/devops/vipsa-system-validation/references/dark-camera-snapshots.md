# Dark ViPSA Camera Snapshots

Use this procedure when a camera still must be captured without ViPSA illumination.

## Validated sequence

1. Send `light.turn_off` through a one-command PUDA protocol using `nats://bears:4222,nats://bears:4223,nats://bears:4224`.
2. Require the command response to show `status: success` and `result: true`. The light machine being `idle` does not prove LED state.
3. Inspect any existing convenience capture script before running it. Do not use scripts that wrap acquisition in `turn_on`/`turn_off` when a dark frame was requested.
4. Resolve the live RTSP endpoint rather than relying on an archived IP. Probe port 8554 and verify `/camera2` with `ffprobe` over RTSP/TCP. If MediaMTX is local, prefer `rtsp://127.0.0.1:8554/camera2`.
5. Capture one frame with a bounded timeout:
   ```bash
   timeout 30 ffmpeg -hide_banner -loglevel warning -y \
     -rtsp_transport tcp -i rtsp://127.0.0.1:8554/camera2 \
     -frames:v 1 -update 1 -q:v 2 camera2_dark.jpg
   ```
6. Verify format, byte size, dimensions, and visual integrity. Confirm that the top-mounted light ring is not emitting; ambient room light may still make the frame bright.
7. Send the verified file directly with a `MEDIA:` absolute path.

## Interpretation

Camera 2 is a context webcam. Use it for qualitative inspection and its environmental gauge, not micrometre Z calibration. The installed illumination is one coiled addressable RGBA strip mounted at the top.

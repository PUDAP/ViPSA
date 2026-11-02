# Local V4L2 fallback for both-camera ViPSA snapshots (2026-07-13)

Trigger: user asks for still captures from both ViPSA cameras and RTSP/MediaMTX paths are unavailable, stale, or return no frames/404.

Validated fallback:

1. Keep the normal light workflow: turn `light.turn_on()`, capture, then `light.turn_off()` in a cleanup/finally path and verify `light` state is `idle`, `run_id: null`.
2. If RTSP URLs such as `rtsp://127.0.0.1:8554/camera1` / `camera2` fail, check local devices. In this environment the usable direct devices were:
   - camera 1: `/dev/video0`
   - camera 2: `/dev/video2`
   - `/dev/video1` and `/dev/video3` were non-capturing companion nodes.
3. Use OpenCV V4L2 capture, not the RTSP backend:

```python
cap = cv2.VideoCapture(dev_index, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# read several frames, keep the latest real frame, then cv2.imwrite(...)
```

4. Save verified JPEGs and return both as `MEDIA:` attachments.
5. Report camera source explicitly, for example `Camera 1: /dev/video0`, `Camera 2: /dev/video2`, plus final light state.

Pitfall: a failed RTSP capture script may turn the light back off before producing images. If the user asked for captures and RTSP fails, do not stop there; try the local V4L2 fallback before reporting failure. Do not generalize this as RTSP being permanently broken — treat it as a fallback when streams are not currently published.
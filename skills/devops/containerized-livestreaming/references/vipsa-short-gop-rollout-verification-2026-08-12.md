# ViPSA short-GOP rollout and verification

Use this note after diagnosing healthy RTSP transport but delayed WebRTC/HLS startup caused by a long x264 GOP on a low-FPS camera.

## Publisher correction

Apply explicit GOP controls to the V4L2/libx264 publisher branch:

```bash
-g 10 -keyint_min 10 -sc_threshold 0 \
-x264-params repeat-headers=1
```

At 30 fps this targets about 0.33 s between keyframes; at 5 fps, about 2 s. Short GOPs improve join latency at some bitrate cost.

## Safe rollout

1. Run `docker compose config --quiet` and `git diff --check`.
2. Recreate only the FFmpeg publisher: `docker compose up -d --force-recreate ffmpeg`. Avoid restarting MediaMTX unnecessarily.
3. Require MediaMTX logs to show every expected stream path online again.
4. Probe each RTSP path for codec, resolution, and FPS.
5. Measure packet keyframe timestamps concurrently over a bounded interval; calculate adjacent timestamp gaps.
6. Verify HLS manifests and WebRTC viewer pages return HTTP 200.

## Acceptance evidence from ViPSA

After applying GOP 10, both streams remained H.264 at 1920×1080. Measured keyframe spacing changed to approximately:

- Camera 1, 30 fps: 0.333 s
- Camera 2, 5 fps: 2.04 s

Camera 2's HLS manifest then appeared in about 3 seconds instead of timing out.

An HTTP 200 from a viewer page is not sufficient proof of working video. Media proof requires online-path logs plus valid RTSP metadata/packets and bounded keyframe spacing. A disabled MediaMTX status API is a separate reporting issue and must not be confused with transport failure.

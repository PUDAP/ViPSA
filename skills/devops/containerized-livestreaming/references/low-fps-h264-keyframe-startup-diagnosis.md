# Diagnosing Low-FPS H.264 Streams That Appear Offline

Use this when RTSP probes succeed but WebRTC/HLS viewers remain in buffering or show an error.

## Failure pattern

- MediaMTX and publisher containers are running.
- `ffprobe` reports valid H.264 metadata and RTSP can read packets.
- WebRTC signaling/ICE may establish successfully, yet the browser video remains at `readyState=0`.
- HLS master-manifest creation can time out while waiting for usable video.
- The problem is often a long GOP rather than a dead camera.

## Root cause

The default x264 GOP is commonly 250 frames. Startup delay therefore depends on source frame rate:

```text
keyframe interval in seconds = GOP frames / source FPS
```

At 5 fps, a 250-frame GOP is about 50 seconds. A viewer joining just after a keyframe can look broken until the next IDR frame arrives.

## Verification

First establish that the transport and path are healthy:

```bash
timeout 12 ffprobe -v error -rtsp_transport tcp \
  -show_entries stream=codec_name,width,height,avg_frame_rate \
  -of csv=p=0 rtsp://127.0.0.1:8554/camera2
```

Then measure keyframe timestamps over a window long enough to catch at least two:

```bash
timeout 70 ffprobe -v error -rtsp_transport tcp \
  -read_intervals '%+60' -select_streams v:0 \
  -show_entries packet=pts_time,flags -of csv=p=0 \
  rtsp://127.0.0.1:8554/camera2
```

Rows whose flags contain `K` are keyframes. Subtract adjacent timestamps to obtain the GOP duration. Run low-FPS and normal-FPS streams in parallel when possible so the comparison does not double the wait.

Also distinguish these layers:

1. RTSP packet/frame availability.
2. WebRTC session establishment in MediaMTX logs.
3. Browser decode state (`readyState`, dimensions, media error).
4. HLS manifest/segment production with redirects followed.
5. Status API availability; a missing API can mislabel a healthy stream but does not itself break video.

## Production fix

For low-latency x264 publishers, force regular IDR frames and repeat headers:

```bash
-c:v libx264 -preset ultrafast -tune zerolatency \
-g 10 -keyint_min 10 -sc_threshold 0 \
-x264-params repeat-headers=1
```

Choose the GOP from the desired time interval and the lowest expected frame rate. For example, `-g 10` gives approximately 2-second keyframes at 5 fps and 0.33-second keyframes at 30 fps. Shorter GOPs improve join time but increase bitrate; avoid prescribing one value without considering that trade-off.

After editing, validate Compose, recreate only the publisher if possible, then verify:

- both RTSP paths still publish at the expected resolution/FPS;
- keyframe spacing is now bounded;
- WebRTC reaches playable browser state;
- HLS manifests and media segments appear promptly;
- MediaMTX logs show no new publisher or decoder errors.

## ViPSA observation, 2026-08-11

The ViPSA stack had healthy 1080p RTSP streams, but the 5 fps camera produced about one keyframe every 50 seconds because the publisher had no explicit GOP settings. Camera 1 at 30 fps produced keyframes every 8.33 seconds. This explained why Camera 2 established WebRTC yet appeared stuck/erroring and why HLS startup timed out. MediaMTX API port 9997 was also disabled, a separate status-reporting issue rather than the transport failure.
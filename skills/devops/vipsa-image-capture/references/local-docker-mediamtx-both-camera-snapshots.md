# Local Docker MediaMTX both-camera snapshots

Use when both ViPSA publishers are running in Docker and host-side MediaMTX RTSP is available.

## Discovery

Check the publisher processes before assuming physical-device-to-stream labels. A working deployment exposed:

- `/dev/video2` publisher → `rtmp://mediamtx:1935/camera1`
- `/dev/video0` publisher → `rtmp://mediamtx:1935/camera2`

Treat those mappings as discovered session state, not a permanent camera identity. Attach/report the MediaMTX path labels (`camera1`, `camera2`) unless the physical mapping has been freshly verified.

Confirm MediaMTX publishes host port `8554`, then use:

```bash
ffprobe -v error -rtsp_transport tcp -timeout 5000000 \
  -show_entries stream=codec_name,width,height,avg_frame_rate -of json \
  rtsp://127.0.0.1:8554/camera2
```

## Preflight source resolution before illumination

Resolve a working RTSP source **before** turning the capture light on. OpenCV/FFmpeg can block for about 30 seconds while opening a dead endpoint, so discovering the source after illumination unnecessarily leaves the sample lit and delays cleanup.

1. Probe likely endpoints for both paths with bounded `ffprobe`, preferably in parallel: local `rtsp://127.0.0.1:8554/cameraN`, the currently verified Tailscale host, then any remembered LAN/WSL host.
2. Inspect active MediaMTX/publisher processes only to discover mappings; do not assume `/dev/videoN` identities are permanent.
3. Require stream metadata for **both** requested paths before issuing `light.turn_on`.
4. Turn on the light, capture both frames from the verified endpoint, and turn the light off in `finally`.
5. If a capture fails after light-on, still run/verify light-off before trying another source.

A validated retry found a stale LAN RTSP endpoint while both `127.0.0.1:8554/camera1` and `/camera2` were healthy 1920×1080 H.264 streams. The durable rule is endpoint preflight, not the particular stale address.

## Capture pattern

```bash
ffmpeg -hide_banner -loglevel error -y -rtsp_transport tcp \
  -i rtsp://127.0.0.1:8554/camera1 \
  -frames:v 1 -update 1 -q:v 2 camera1.jpg
```

Repeat for `camera2`.

## Long-GOP pitfall

A low-frame-rate stream can be healthy and probe successfully yet take tens of seconds to emit the first decodable keyframe. In one deployment, `camera2` was H.264 1920×1080 at 5 fps and a 25-second one-shot capture timed out; retrying with an 80-second bound produced a valid JPEG. Therefore:

1. Probe the stream with `ffprobe` before declaring it down.
2. If metadata is present but no frame arrives, retry once with a 75–80 second timeout.
3. Verify the output file is non-zero and visually nonblank before attaching.
4. Do not reuse a stale snapshot just because the new capture is slow.

Keep the normal light workflow around the capture. If light control fails, still satisfy an explicit camera request with fresh frames when possible, but clearly report final lamp state as unverified.
# Containerized media pipeline debugging notes

Use when debugging Docker Compose camera/livestream stacks such as FFmpeg -> RTMP -> MediaMTX -> RTSP/HLS/WebRTC.

## Durable debugging pattern

1. Separate listener availability from stream availability.
   - Open ports or HTTP player pages (`200 OK`) only prove the server is running.
   - Verify actual published streams via server logs and media manifests.
   - For MediaMTX HLS, fetch the playlist (`/<path>/index.m3u8`) and look for a real `#EXT-X-STREAM-INF` entry; JSON like `no stream is available on path ...` means no publisher is active.

2. Check current Compose state, not just config.
   - `docker compose config --quiet` validates YAML/env interpolation only.
   - `docker compose ps -a` shows whether old containers are still running or new services exited.
   - `docker compose logs --tail=... <server> <publishers...>` shows whether publishers connected and what path they publish to.
   - After renaming services, use `docker compose up -d --remove-orphans` so stale containers do not keep devices or publish old paths.

3. For USB camera publishers, validate the camera outside the full stack.
   - Test each capture device with a short FFmpeg probe before assuming MediaMTX is at fault.
   - Specify `-input_format`, `-video_size`, and often `-framerate`; camera defaults can choose a mode that opens but never produces frames.
   - Linux V4L devices commonly expose paired nodes; only nodes with `ID_V4L_CAPABILITIES=:capture:` are usable capture devices.

4. Verify end-to-end after restart.
   - Logs should show `stream is available and online` and `is publishing to path '<path>'`.
   - HLS playlists should include resolution/codecs, e.g. `RESOLUTION=640x480`.
   - RTSP can be verified with an FFmpeg/ffprobe client against `rtsp://127.0.0.1:8554/<path>`.

## Pitfalls

- A browser player URL can return HTML even when no stream exists; always probe the manifest or server logs.
- A `Device or resource busy` error may be caused by a stale/orphan FFmpeg container, not another visible host process.
- A higher camera resolution can hang under USB bridges even when the device advertises it. Test smaller explicit MJPEG modes before changing architecture.

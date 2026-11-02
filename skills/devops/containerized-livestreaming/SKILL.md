---
name: containerized-livestreaming
description: Build, modify, and verify containerized livestream stacks using Docker Compose, MediaMTX, FFmpeg, V4L2 USB cameras, RTSP/RTMP/HLS/WebRTC, and related camera device mapping.
---

# Containerized Livestreaming

Use this skill when the user asks to create, edit, debug, or verify a livestreaming repo/stack, especially Docker Compose services that ingest cameras with FFmpeg and publish through MediaMTX, RTSP, RTMP, HLS, or WebRTC.

## Workflow

0. **Classify the failure layer before changing config.**
   - Check whether MediaMTX is listening, whether a stream path is published, and whether the viewer page is merely served.
   - A WebRTC page returning HTML only proves MediaMTX HTTP is up; also verify a real stream frame through RTSP/ffprobe or MediaMTX logs showing `stream is available and online`.
   - In WSL + Docker Desktop setups, if `/dev/video*` is absent, do not keep restarting container FFmpeg publishers that map Linux video devices. Use a host-side Windows DirectShow publisher into MediaMTX as a recovery path; see `references/wsl-windows-directshow-mediamtx.md`.

1. **Locate the actual repo before editing.**
   - If the user gives a path that is missing, search nearby likely locations instead of stopping immediately.
   - Report the actual path edited in the final response.

2. **Inspect the stack and current stream topology.**
   - Read `compose.yml`, `.env.example`, README/docs, and non-secret config files.
   - Avoid reading secret-bearing `.env` with file tools; if live `.env` edits are required, preserve existing keys and only update the necessary non-secret variables.

3. **Discover camera devices when streaming from USB/V4L2.**
   - List `/dev/video*`.
   - Prefer capture-capable nodes, not metadata/control-only sibling nodes.
   - Useful probes:
     - `for d in /dev/video*; do b=$(basename "$d"); echo "$d: $(cat /sys/class/video4linux/$b/name 2>/dev/null)"; done`
     - `udevadm info --query=property --name=/dev/videoN | grep -E 'ID_V4L|ID_MODEL|ID_SERIAL|ID_PATH'`
     - `v4l2-ctl --list-devices` when installed.

4. **For multiple USB cameras, create one ingest service per camera.**
   - Map each device explicitly with Docker Compose `devices:`.
   - Give each FFmpeg container a unique service and `container_name`.
   - Publish each stream to a distinct MediaMTX path, e.g. `camera1`, `camera2`.
   - If no audio device is configured, use `-an`; do not invent AAC audio input from video-only V4L2 devices.

5. **Keep examples and live config aligned.**
   - Update `.env.example` with any new variables.
   - Update README with stream names and viewer URLs.
   - If safe and necessary, update the live `.env` while preserving unrelated values.

6. **Verify before finalizing.**
   - Always run `docker compose config --quiet` from the repo root after Compose edits.
   - Run `git diff --check` to catch whitespace and newline problems.
   - If containers are started, verify service health/logs and test at least one published URL or MediaMTX path.
   - For resolution/format changes, verify the stream actually publishes at the requested resolution (for example HLS manifest `RESOLUTION=...` or `ffprobe`/MediaMTX logs), not just that the container is running. If a requested setting causes FFmpeg to hang or MediaMTX to lose the path, restore the last known-good settings unless the user explicitly wants the broken experimental state left in place.

## Pitfalls

- Do not confuse a served MediaMTX viewer page with a working stream. A `GET /camera1/` HTML response can still coexist with RTSP 404 / `no stream is available on path`; verify by extracting a frame or inspecting MediaMTX publisher logs.
- When RTSP is healthy and WebRTC signaling connects but a low-FPS camera remains at browser `readyState=0` or HLS startup times out, measure H.264 keyframe spacing before restarting services. The default x264 GOP of 250 frames becomes a 50-second join delay at 5 fps. Force an explicit bounded GOP (`-g`, `-keyint_min`, `-sc_threshold 0`, repeated headers), balance startup latency against bitrate, and verify packet keyframes plus browser/HLS playback afterward. Keep status-API failure separate from media-path failure. See `references/low-fps-h264-keyframe-startup-diagnosis.md`.
- In WSL, absence of `/dev/video*` is a camera-ingest problem, not a MediaMTX problem. Keep MediaMTX running and publish from Windows FFmpeg/DirectShow into RTMP when Windows can see the cameras.
- DirectShow device names can be visually similar and exact, including spaces (`USB_Camera`, `USB CAMERA `, `Logi Webcam C920e`). If a camera stream goes offline after a device swap, first enumerate current DirectShow names, then update both the live publisher command and any startup launcher/script that hard-codes the old name. If a retry says the device is in use, clear stale Windows `ffmpeg.exe` processes before restarting publishers, and consider starting the more finicky camera first.
- In Windows PowerShell launchers, `Start-Process -ArgumentList` can strip quotes around a DirectShow input and turn `-i "video=USB CAMERA "` into `video=USB`. For device names with spaces/trailing spaces, use a generated `.cmd` launcher (or another process API that preserves argv exactly) so FFmpeg receives `-i "video=USB CAMERA "` intact. Avoid multiline `+` continuations when constructing launcher text; PowerShell can parse a line ending in `+` as `ExpectedValueExpression`. Prefer an array of fragments with parenthesized function calls and `-join ''`. If the user still reports the old parser error after a patch, verify/copy the exact Windows-local script or create a new fixed launcher name to avoid stale-path confusion. See `references/powershell-directshow-launcher-quoting.md`.
- USB cameras often expose pairs such as `/dev/video0` and `/dev/video1`; only one may have `ID_V4L_CAPABILITIES=:capture:`. Pick the capture-capable node.
- Do not assume the user’s stated path is exact. In WSL or migrated workspaces, the repo may be in `~/repo` instead of `~/workspace/repo`.
- In WSL with Docker Desktop, Linux `docker` can fail on `/var/run/docker.sock` permissions even while containers are manageable through Windows Docker. If that happens, try the Docker Desktop CLI at `/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe` from the repo root before asking the user to fix groups/sudo.
- MediaMTX stream paths are created by the publisher URL. Changing from `livestream` to `camera1`/`camera2` changes viewer URLs; document that.
- For WebRTC over Tailscale/VPN, stale `MTX_WEBRTCADDITIONALHOSTS` breaks remote viewers even when RTSP/HLS and local playback work. Compare `tailscale ip -4`/`hostname -I` against the live container env (`docker inspect mediamtx`) and update/recreate the container if the advertised host is old.
- Container names must be unique; duplicating a single `ffmpeg` service will collide unless renamed.
- Some USB/DirectShow cameras list high resolutions or alternate aspect ratios that do not actually open. Treat `-list_options true`/`-list_formats all` as a capability hint, not proof; test a frame or live publish and be ready to revert to a known-good resolution. For the ViPSA Logitech C920e camera2, `2304x1536` and `2304x1296` YUYV 2 fps were listed but failed with `Could not set video options`; the verified production mode is `1920x1080` MJPEG at up to 30 fps. See `references/logitech-c920e-camera2-highres-and-fov-2026-06-13.md`.
- When exposing MJPEG/HTTP ports from WSL to Windows clients, Windows Firewall may need an inbound allow rule for the chosen ports (for example 8080-8081). After the user creates the rule, verify both layers: (1) the Windows rule is enabled/OK, and (2) a service is actually listening on the ports from WSL (`ss -ltnp`, `curl -I http://127.0.0.1:<port>/`). A good firewall rule alone does not prove the stream service is running.

## References

- `references/dual-usb-mediamtx.md` — concrete pattern for converting a one-camera MediaMTX/FFmpeg Compose stack into two USB camera streams.
- `references/wsl-usb-camera-resolution.md` — validation and rollback pattern for WSL USB camera resolution changes that list as supported but hang at capture time.
- `references/windows-directshow-mediamtx-startup.md` — Windows DirectShow publisher fallback for WSL/Docker Desktop setups, including swapped camera mappings, 1080p verification, and per-user startup launchers.
- `references/powershell-directshow-launcher-quoting.md` — PowerShell/DirectShow FFmpeg launcher quoting pattern for camera names with spaces/trailing spaces, safe `.cmd` generation, and stale-script checks.
- `references/logitech-c920e-camera2-highres-and-fov-2026-06-13.md` — ViPSA camera2 Logitech C920e notes: no separate wide-angle DirectShow mode, failed 2304px YUYV high-res attempts, quoting requirements for device names with spaces, and restoring/verifying the known-good 1920x1080 MJPEG stream.
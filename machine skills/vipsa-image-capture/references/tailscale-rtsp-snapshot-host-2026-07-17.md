# Tailscale RTSP snapshot host and verification (2026-07-17)

## Context

During a request for camera livestream addresses and screenshots, the historically used ViPSA RTSP host `100.67.251.110` / `vipsapc` was present in older scripts but did not respond to RTSP/API probes. The active local machine reported Tailscale IP `100.74.20.98` (`vipsa-ubuntu`) and MediaMTX listened on `0.0.0.0:8554` / `0.0.0.0:8889`.

## Verified stream URLs for that session

```text
rtsp://100.74.20.98:8554/camera1
rtsp://100.74.20.98:8554/camera2
```

`ffprobe` confirmed:

```text
camera1: h264, 1920x1080, ~30 fps
camera2: h264, 1920x1080, ~5 fps
```

LAN fallback from the same host also worked at:

```text
rtsp://10.42.0.86:8554/camera1
rtsp://10.42.0.86:8554/camera2
```

Treat these as live-discovered values, not immutable constants. Always verify current Tailscale IP and RTSP frame availability before reporting current URLs.

## Screenshot capture pattern

For a user request like “send me a screenshot of camera1 and camera2”, a direct RTSP ffmpeg capture was reliable and faster than the heavier light-control/capture script:

```bash
OUT=/home/amdm/vipsa_captures/$(date +%Y%m%d_%H%M%S_rtsp)
mkdir -p "$OUT"
for cam in camera1 camera2; do
  ffmpeg -hide_banner -loglevel error -y -rtsp_transport tcp \
    -i "rtsp://100.74.20.98:8554/$cam" \
    -frames:v 1 -update 1 -q:v 2 "$OUT/$cam.jpg"
  stat -c "$cam %s bytes" "$OUT/$cam.jpg"
done
```

Return both JPEGs with `MEDIA:` only after confirming nonzero file sizes.

## Light-control reporting pitfall

A later PUDA `light.turn_off` cleanup attempt timed out at START while `puda machine state light` returned a stale/old idle snapshot. In that case, do **not** claim a verified light-state change. Report the screenshots as captured and state that light cleanup verification was blocked/unverified.

## URL reporting pitfall

Do not simply repeat old script URLs. When asked for livestream IPs, verify:

1. `tailscale ip -4` / `tailscale status` for candidate hosts.
2. TCP/listening ports (`8554`, optionally `8889`).
3. A real stream with `ffprobe` or frame capture, not only a served MediaMTX page.

If HTTP/WebRTC endpoints return 404 while RTSP works, provide RTSP URLs as the verified working endpoints and avoid claiming WebRTC is available.

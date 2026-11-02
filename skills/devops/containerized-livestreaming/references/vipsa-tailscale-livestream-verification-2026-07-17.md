# ViPSA Tailscale livestream endpoint verification (2026-07-17)

## What happened

The user asked for the Tailscale IP address of camera 1 and camera 2 livestreams. Older scripts still referenced `100.67.251.110` and `172.30.111.161`, but live checks showed those endpoints timed out from the current host. The active livestream server was on the current machine's Tailscale IP `100.74.20.98` (`vipsa-ubuntu`), with MediaMTX listening on `8554` and `8889`.

## Verification sequence

Use this sequence for future “what is the camera livestream IP/URL?” requests:

```bash
tailscale ip -4
tailscale status | grep -Ei 'vipsa|camera|<candidate-ip>'
ss -ltnp | grep -E ':(8554|8889|9997)\b'
for path in camera1 camera2; do
  timeout 15 ffprobe -v error -rtsp_transport tcp \
    -show_entries stream=index,codec_type,width,height \
    -of compact=p=0:nk=1 \
    "rtsp://<tailscale-ip>:8554/$path"
done
```

Do not rely on script constants or Tailscale hostnames alone. A host can remain in `tailscale status` while being stale/offline for the stream.

## Result in this session

Verified RTSP URLs:

```text
rtsp://100.74.20.98:8554/camera1
rtsp://100.74.20.98:8554/camera2
```

Observed stream metadata:

```text
camera1: h264 1920x1080 ~30 fps
camera2: h264 1920x1080 ~5 fps
```

A LAN fallback also worked locally:

```text
rtsp://10.42.0.86:8554/camera1
rtsp://10.42.0.86:8554/camera2
```

## Pitfalls

- `100.67.251.110` appeared in many old scripts but timed out in this session. Treat old constants as candidates only.
- HTTP/WebRTC URLs on port `8889` returned 404 even while RTSP worked. A served HTTP page or open TCP port is not enough; verify the actual stream via `ffprobe` or frame extraction.
- Camera mappings can be counterintuitive at the publisher layer: observed processes published `/dev/video2` to `camera1` and `/dev/video0` to `camera2`. Report stream path names (`camera1`, `camera2`) rather than assuming physical `/dev/videoN` names unless needed.

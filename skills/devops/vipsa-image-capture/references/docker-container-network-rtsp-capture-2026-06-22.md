# Docker container-network RTSP capture fallback

## When this applies

Use this when ViPSA camera streams are published inside the `mediamtx` Docker container, but the RTSP port is not exposed to WSL/host (`rtsp://127.0.0.1:8554/...` and host IPs return connection refused) while MediaMTX logs still show `camera1` / `camera2` paths are online.

This is a stream-access topology issue, not necessarily a camera failure.

## Working pattern

Capture from the MediaMTX container network namespace with a disposable FFmpeg container:

```bash
OUT=/home/vipsa/vipsa-puda-project/runs/tmp_capture
mkdir -p "$OUT"

docker run --rm --network container:mediamtx \
  -v "$OUT":/out \
  linuxserver/ffmpeg:latest \
  -hide_banner -y -rtsp_transport tcp \
  -i rtsp://127.0.0.1:8554/camera1 \
  -frames:v 1 -update 1 -q:v 2 \
  /out/camera1.jpg
```

For camera 2, use `rtsp://127.0.0.1:8554/camera2` and a different output filename.

Verify the image exists and is non-empty before proceeding:

```bash
file "$OUT/camera1.jpg"
ls -lh "$OUT/camera1.jpg"
```

The file may be root-owned because it was written by Docker. That does not block read/attach, but if later processing needs write access in the same directory, write derived artifacts as the WSL user or adjust ownership when permitted.

## Alignment integration

For align runs, this Docker RTSP capture can replace OpenCV host RTSP capture while preserving the same downstream OpenCV detection pipeline:

1. Turn light on via PUDA protocol.
2. Capture `camera1.jpg` through `docker run --network container:mediamtx ... rtsp://127.0.0.1:8554/camera1`.
3. Run the standard 900x900 ROI dark-pad detector.
4. Apply Zaber native-unit correction via PUDA protocol.
5. Recapture and verify residual.

## Pitfall

A browser/WebRTC viewer or MediaMTX logs can show streams online while the host-side RTSP port is not published. Do not conclude the camera stream is down until checking the container-network capture path.
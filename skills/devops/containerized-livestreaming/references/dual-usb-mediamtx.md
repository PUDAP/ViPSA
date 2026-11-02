# Dual USB cameras with MediaMTX + FFmpeg Compose

Session-derived pattern for a repo that originally had one `ffmpeg` service publishing one V4L2 device to `rtmp://mediamtx:1935/livestream`.

## Device discovery

In WSL/Linux, USB cameras may expose multiple `/dev/video*` nodes per physical camera. Check capabilities before choosing inputs:

```bash
for d in /dev/video*; do
  b=$(basename "$d")
  printf '%s: ' "$d"
  cat "/sys/class/video4linux/$b/name" 2>/dev/null || echo unknown
  udevadm info --query=property --name="$d" 2>/dev/null | grep -E 'ID_V4L_CAPABILITIES|ID_MODEL|ID_SERIAL|ID_PATH'
done
```

Example result:

- `/dev/video0`: `ID_V4L_CAPABILITIES=:capture:` for first USB camera.
- `/dev/video1`: sibling node without capture capability.
- `/dev/video2`: `ID_V4L_CAPABILITIES=:capture:` for second USB camera.
- `/dev/video3`: sibling node without capture capability.

Use `/dev/video0` and `/dev/video2`, not `/dev/video1`/`3`, for FFmpeg inputs.

## Compose transformation

Replace one ingest service with one service per camera:

```yaml
  ffmpeg-camera1:
    image: linuxserver/ffmpeg:latest
    container_name: ffmpeg-camera1
    depends_on:
      - mediamtx
    devices:
      - ${VIDEO_DEVICE_1}:${VIDEO_DEVICE_1}
    group_add:
      - video
    command: >
      -loglevel error
      -f v4l2 -i ${VIDEO_DEVICE_1}
      -c:v libx264 -preset ultrafast -tune zerolatency
      -an -f flv rtmp://mediamtx:1935/camera1
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    restart: unless-stopped

  ffmpeg-camera2:
    image: linuxserver/ffmpeg:latest
    container_name: ffmpeg-camera2
    depends_on:
      - mediamtx
    devices:
      - ${VIDEO_DEVICE_2}:${VIDEO_DEVICE_2}
    group_add:
      - video
    command: >
      -loglevel error
      -f v4l2 -i ${VIDEO_DEVICE_2}
      -c:v libx264 -preset ultrafast -tune zerolatency
      -an -f flv rtmp://mediamtx:1935/camera2
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    restart: unless-stopped
```

Update environment examples:

```dotenv
VIDEO_DEVICE_1=/dev/video0
VIDEO_DEVICE_2=/dev/video2
TAILSCALE_IP=...
```

Update README/viewer docs:

- RTSP: `rtsp://<host>:8554/camera1`, `rtsp://<host>:8554/camera2`
- HLS: `http://<host>:8888/camera1/`, `http://<host>:8888/camera2/`
- WebRTC: `http://<host>:8889/camera1/`, `http://<host>:8889/camera2/`

## Verification

Run from repo root. In WSL with Docker Desktop socket/group issues, substitute the Windows Docker CLI path while staying in the Linux repo directory:

```bash
docker compose config --quiet && echo 'compose config ok'
"/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" compose config --quiet && echo 'compose config ok'
git diff --check
```

If starting the stack, use:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=100 mediamtx ffmpeg-camera1 ffmpeg-camera2
```

Then test at least one stream URL or MediaMTX path.
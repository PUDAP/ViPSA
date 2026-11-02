# WSL USB camera resolution validation

Session-derived pattern for Docker Compose + MediaMTX + FFmpeg stacks running under WSL with USB cameras bridged from Windows.

## Durable lesson

A V4L2 device may list a high resolution/format but still hang when FFmpeg tries to capture frames through the WSL USB camera bridge. Do not treat a running FFmpeg container as proof that the stream is publishing.

## Validation sequence

1. Render the effective Compose command:

```bash
docker compose config --quiet
docker compose config | sed -n '/ffmpeg-camera2:/,/^[^ ]/p'
```

2. Recreate only the affected camera service:

```bash
docker compose up -d --force-recreate ffmpeg-camera2
```

3. Verify the publisher, not just container status:

```bash
docker compose ps
docker logs --since 30s mediamtx | grep -i 'camera2\|error\|warn'
curl -fsSL --max-time 15 http://127.0.0.1:8888/camera2/index.m3u8
```

Look for MediaMTX log lines like `stream is available and online` and an HLS manifest containing the requested `RESOLUTION=`.

4. If the stream disappears or HLS returns 404, test direct frame capture outside the long-running service:

```bash
timeout 20 docker run --rm --device /dev/video2:/dev/video2 \
  linuxserver/ffmpeg:latest \
  -loglevel info -f v4l2 -input_format mjpeg -video_size 1280x720 \
  -i /dev/video2 -frames:v 1 -f null -
```

If this times out, FFmpeg is hanging at that mode. Restore the last known-good format/resolution unless the user explicitly wants the experimental broken state.

## Docker Desktop from WSL

If Linux `docker` cannot access `/var/run/docker.sock` due to permissions, invoke Docker Desktop directly:

```bash
'/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' compose ps
'/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' compose up -d --force-recreate ffmpeg-camera2
```

## Example finding from this session

For `~/livestream`, `camera2` (`/dev/video2`) listed `1280x720` for MJPEG and YUYV, but FFmpeg timed out at `1280x720`; `320x240` MJPEG published successfully and produced an HLS manifest with `RESOLUTION=320x240`.

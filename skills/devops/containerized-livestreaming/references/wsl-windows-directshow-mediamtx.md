# WSL + Windows DirectShow fallback for MediaMTX camera streams

Use this when a MediaMTX Docker stack is reachable but FFmpeg ingest containers cannot access USB cameras because WSL has no `/dev/video*` devices, while Windows DirectShow can capture the cameras.

## Symptom pattern

- WebRTC URLs such as `http://<tailscale-ip>:8889/camera1/` do not load or return MediaMTX pages with no playable stream.
- `ss`/curl initially shows MediaMTX ports not listening if Docker Desktop is stopped.
- After MediaMTX starts, logs show `no stream is available on path 'camera1'` / `camera2`.
- Docker Compose camera services fail with device errors such as `error gathering device information while adding custom device "/dev/video0": no such file or directory`.
- `/dev/video*` is absent in WSL, but Windows FFmpeg DirectShow can list/capture `video=...` devices.

## Recovery sequence

1. Start Docker Desktop if the Linux engine is unreachable, then wait for it:

```bash
powershell.exe -NoProfile -Command "if (-not (Get-Process 'Docker Desktop' -ErrorAction SilentlyContinue)) { Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe' }"
for i in $(seq 1 30); do '/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' version && break; sleep 3; done
```

2. Start MediaMTX only / tolerate FFmpeg container failures if `/dev/video*` is unavailable:

```bash
'/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' compose up -d mediamtx
'/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' compose ps
```

3. Use Windows FFmpeg DirectShow as host-side publishers into MediaMTX RTMP. First list DirectShow options to get exact device names and working formats:

```bash
FF='/mnt/c/Users/amdm/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'
"$FF" -hide_banner -f dshow -list_options true -i video='USB_Camera'
"$FF" -hide_banner -f dshow -list_options true -i video='USB CAMERA '
```

4. Clear stale Windows FFmpeg processes if a DirectShow device reports `device already in use`:

```bash
powershell.exe -NoProfile -Command "Get-Process ffmpeg -ErrorAction SilentlyContinue | Stop-Process -Force"
```

5. Start publishers. Starting camera2 first can avoid device contention when device names are similar:

```bash
FF='/mnt/c/Users/amdm/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'
"$FF" -hide_banner -loglevel warning -f dshow -video_size 640x480 -vcodec mjpeg -i video='USB CAMERA ' \
  -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -an -f flv rtmp://127.0.0.1:1935/camera2 &
sleep 2
"$FF" -hide_banner -loglevel warning -f dshow -video_size 640x480 -vcodec mjpeg -i video='USB_Camera' \
  -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -an -f flv rtmp://127.0.0.1:1935/camera1 &
```

## Verification

Verify all three layers, not just the page:

```bash
# MediaMTX pages served through the target address
curl -sS --max-time 5 http://100.67.251.110:8889/camera1/ | head -c 80
curl -sS --max-time 5 http://100.67.251.110:8889/camera2/ | head -c 80

# Actual stream frames through RTSP
FF='/mnt/c/Users/amdm/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe'
"$FF" -hide_banner -loglevel error -rtsp_transport tcp -i rtsp://100.67.251.110:8554/camera1 -frames:v 1 -y /tmp/camera1_tailscale_probe.jpg
"$FF" -hide_banner -loglevel error -rtsp_transport tcp -i rtsp://100.67.251.110:8554/camera2 -frames:v 1 -y /tmp/camera2_tailscale_probe.jpg
file /tmp/camera1_tailscale_probe.jpg /tmp/camera2_tailscale_probe.jpg
```

MediaMTX logs should show `stream is available and online` for each path and RTMP publishing connections.

## Caveats

- This is a live workaround, not persistent service management. It survives while the Windows FFmpeg processes run, but not necessarily across reboot or process death.
- The exact Windows FFmpeg path and DirectShow device names are host-specific; rediscover them if they change.
- Avoid writing a durable rule that WSL camera devices never work. This fallback applies when `/dev/video*` is currently absent or unusable.

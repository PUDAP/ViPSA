# Camera publisher restart/release and lighted snapshot workflow

## Context

During ViPSA operation, camera 1 had been intentionally released by stopping the Windows DirectShow `ffmpeg.exe` publisher that held `video=USB CAMERA ` and published `camera1` to MediaMTX. Later the user asked to restart camera 1, capture an image with light, and send it in chat.

## Durable workflow

### Release a camera stream

When the user asks to release a camera, stop the long-running Windows `ffmpeg.exe` publisher for that specific MediaMTX path, not a completed one-shot capture process.

1. Query Windows processes from WSL:

```bash
powershell.exe -NoProfile -Command 'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "ffmpeg" -and $_.CommandLine -match "camera1|camera2|USB CAMERA|USB_Camera" } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Depth 3'
```

2. Stop only the PID matching the requested stream/device:

```bash
powershell.exe -NoProfile -Command 'Stop-Process -Id <PID> -Force'
```

3. Verify the target publisher is gone and any other camera publisher requested to remain active is still running.

### Restart camera 1 publisher

If PowerShell `Start-Process` quoting becomes fragile, start the Windows ffmpeg binary directly from WSL as a tracked background process. Example pattern:

```bash
'/mnt/c/Users/amdm/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.exe' \
  -hide_banner -loglevel warning \
  -f dshow -video_size 1920x1080 -vcodec mjpeg \
  -i 'video=USB CAMERA ' \
  -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -an \
  -f flv rtmp://127.0.0.1:1935/camera1
```

Run it with the terminal tool as `background=true`. Then wait a few seconds and verify RTSP by capturing one frame:

```bash
ffmpeg.exe -hide_banner -y -rtsp_transport tcp \
  -i rtsp://100.67.251.110:8554/camera1 \
  -frames:v 1 -update 1 -q:v 3 C:\\Users\\amdm\\AppData\\Local\\Temp\\camera1_probe.jpg
```

Attach the WSL path equivalent after checking non-empty file size.

### Lighted snapshot sequence

For requests like “restart camera 1 stream and capture an image with light”:

1. Restart and verify the camera stream first.
2. Turn the light on via PUDA protocol.
3. Capture the RTSP frame using Windows ffmpeg outputting to a Windows temp path.
4. Turn the light off in cleanup even if capture fails.
5. Verify `light` returns `idle` and attach the captured image.

Do not claim the snapshot has light unless `light.turn_on` succeeded before capture and `turn_off`/idle cleanup succeeded afterward.

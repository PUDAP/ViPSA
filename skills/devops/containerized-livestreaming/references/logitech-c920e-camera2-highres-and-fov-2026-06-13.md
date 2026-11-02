# Logitech C920e camera2 DirectShow high-resolution mode testing — 2026-06-13

## Context

Camera2 was moved from an older unclear camera to Windows DirectShow device:

```text
Logi Webcam C920e
```

The working production stream is:

```text
DirectShow `Logi Webcam C920e` -> FFmpeg -> RTMP camera2 -> MediaMTX -> RTSP/WebRTC
input: 1920x1080 MJPEG
output verified: 1920x1080
```

## Wide/high-resolution findings

DirectShow exposed many modes. Useful highlights:

- `1920x1080` MJPEG up to `30 fps` — working production mode.
- `1280x720`, `1024x576`, `960x720`, `800x600` MJPEG/YUYV variants — lower resolution or more vertical/taller formats, not wider optics.
- `2304x1536` YUYV at `2 fps` — listed but failed to open.
- `2304x1296` YUYV at `2 fps` — listed but failed to open.

Both high-resolution attempts failed with:

```text
Could not set video options
Error opening input file video=Logi Webcam C920e.
Error opening input files: I/O error
```

Conclusion: there is no separate wide-angle/ultrawide mode exposed through DirectShow for this camera. The C920e has a fixed optical field of view; changing resolution can alter crop/aspect/FPS but not true lens width.

## Operational pattern for future experiments

1. Before changing production, capture the active camera2 publisher command and verify current RTSP frame decode.
2. Stop only the camera2 Windows `ffmpeg.exe` publisher matching `rtmp://127.0.0.1:1935/camera2`.
3. Try the experimental DirectShow mode with a short wait.
4. Verify actual RTSP frame decode (`ffmpeg -rtsp_transport tcp -i rtsp://127.0.0.1:8554/camera2 -frames:v 1 ...`) rather than trusting that the FFmpeg process started.
5. If the path 404s or FFmpeg exits, restore the last known-good `1920x1080` MJPEG publisher immediately.
6. Send the user a snapshot from the verified restored/current stream if requested.

## Known-good camera2 publisher command shape

Use a single quoted argument string for DirectShow names with spaces:

```powershell
$cam2Args = '-hide_banner -loglevel warning -f dshow -video_size 1920x1080 -vcodec mjpeg -i "video=Logi Webcam C920e" -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -an -f flv rtmp://127.0.0.1:1935/camera2'
Start-Process -FilePath $Ffmpeg -ArgumentList $cam2Args -RedirectStandardError camera2-ffmpeg.log -RedirectStandardOutput camera2-ffmpeg.out -WindowStyle Hidden
```

Quoting pitfall: if the DirectShow input is passed as an array item without preserving quotes around `video=Logi Webcam C920e`, FFmpeg can see only `video=Logi` and exit.

## Verification example

A restored snapshot from the working stream verified:

```text
JPEG image data, 1920x1080
ffprobe: 1920,1080
```

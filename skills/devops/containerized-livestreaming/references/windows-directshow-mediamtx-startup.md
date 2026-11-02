# Windows DirectShow publishers for MediaMTX from WSL/Docker Desktop

Use this when a MediaMTX Docker container is reachable but Linux/WSL FFmpeg containers cannot access `/dev/video*`, while Windows can capture cameras via DirectShow.

## Pattern

1. Start/reuse MediaMTX in Docker Desktop.
   - From WSL, Windows Docker CLI works:
     ```bash
     '/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe' start mediamtx
     ```
   - If the container does not exist, create it with the MediaMTX ports and WebRTC additional host:
     ```powershell
     docker run -d --name mediamtx --restart unless-stopped `
       -p 8554:8554 -p 1935:1935 -p 8888:8888 -p 8889:8889 `
       -p 8189:8189/udp -p 8189:8189/tcp `
       -e MTX_WEBRTC=yes -e MTX_WEBRTCADDRESS=:8889 `
       -e MTX_WEBRTCLOCALUDPADDRESS=:8189 `
       -e MTX_WEBRTCADDITIONALHOSTS=<tailscale-ip> `
       bluenviron/mediamtx:latest
     ```

2. Publish each Windows DirectShow camera to a MediaMTX RTMP path with Windows FFmpeg.
   - Enumerate devices first when a known path disappears; USB replacements often change the DirectShow name (`USB_Camera` may become `Logi Webcam C920e`).
     ```powershell
     & $Ffmpeg -hide_banner -f dshow -list_devices true -i dummy
     ```
   - Device names with spaces or trailing spaces must be passed as one quoted ffmpeg argument, e.g. `-i "video=USB CAMERA "` or `-i "video=Logi Webcam C920e"`.
   - When using PowerShell `Start-Process`, avoid an array for the DirectShow `-i` argument if the name contains spaces; build a single argument string so quoting survives.
   - When repairing a live stream, update both the currently running publisher and the persistent startup script/launcher that hard-codes camera names.

   Example:
   ```powershell
   $Ffmpeg = 'C:\path\to\ffmpeg.exe'
   $cam1Args = '-hide_banner -loglevel warning -f dshow -video_size 1920x1080 -vcodec mjpeg -i "video=USB CAMERA " -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -an -f flv rtmp://127.0.0.1:1935/camera1'
   Start-Process -FilePath $Ffmpeg -ArgumentList $cam1Args -WindowStyle Hidden
   ```

3. Persistence options.
   - Prefer a normal scheduled task when permissions allow.
   - If `Register-ScheduledTask` returns access denied, use per-user startup:
     - `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\<name>` pointing to a `.cmd` wrapper.
     - Copy the `.cmd` wrapper to the user's Startup folder.
   - The `.cmd` wrapper should detach PowerShell so the caller does not block on long-lived FFmpeg children:
     ```cmd
     @echo off
     start "ViPSA MediaMTX Streams" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\<user>\vipsa-livestream-launcher\start-vipsa-mediamtx-streams.ps1"
     exit /b 0
     ```

4. Stop/restart only the relevant publishers.
   - Do not kill unrelated FFmpeg jobs. Filter command lines for `rtmp://127.0.0.1:1935/camera` or the project-specific stream path.
   ```powershell
   Get-CimInstance Win32_Process -Filter "name = 'ffmpeg.exe'" |
     Where-Object { $_.CommandLine -like '*rtmp://127.0.0.1:1935/camera*' } |
     ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
   ```

## Verification

- Check MediaMTX pages over the same address the user uses:
  ```bash
  curl -sS --max-time 5 http://<host>:8889/camera1/ | head -c 80
  curl -sS --max-time 5 http://<host>:8889/camera2/ | head -c 80
  ```
- Verify the actual video stream and dimensions by extracting a frame over RTSP/TCP, then probing the saved image. This avoids cases where RTSP metadata briefly reports width/height as `0` or UDP probes hang.
  ```bash
  ffmpeg.exe -hide_banner -loglevel error -rtsp_transport tcp -i rtsp://<host>:8554/camera1 -frames:v 1 -y /tmp/camera1_probe.jpg
  ffprobe.exe -v error -show_entries stream=width,height -of csv=p=0 /tmp/camera1_probe.jpg
  ```
- For WebRTC, the HTML page returning is necessary but not sufficient; confirm RTSP or MediaMTX logs show the path online and frames decode.

## Pitfalls

- A 404 from `/cameraN/` can mean MediaMTX is up but no publisher is attached to that path.
- DirectShow device names may differ only by punctuation or trailing spaces (`USB_Camera` vs `USB CAMERA `); preserve exact names.
- Running PowerShell from WSL with inline `$_.CommandLine` often gets mangled by shell expansion. For complex PowerShell, write a `.ps1` file and run it with `powershell.exe -File`.
- A foreground launcher may appear to hang if long-lived FFmpeg child processes inherit handles. Use a detached `.cmd` wrapper (`start ... powershell.exe ...`) for startup entries.

# Absorbed skill: wsl-windows-camera-streaming

Original package: `media/wsl-windows-camera-streaming` archived after consolidation into `media-workflows`.

Support files copied: ['references/ -> references/wsl-windows-camera-streaming/'].

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: wsl-windows-camera-streaming
description: "Troubleshoot and set up webcam/livestream paths between Windows and WSL, including Windows FFmpeg MJPEG/WebRTC streams, WSL v4l2 devices, USB/IP ownership, MediaMTX, and verification from WSL."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wsl, windows, webcam, ffmpeg, livestream, mjpeg, webrtc, rtmp, mediamtx, usbip, v4l2]
    created_by: agent
---

# WSL / Windows Camera Streaming

Use this skill when the user wants to stream a webcam between Windows and WSL, expose a camera as MJPEG/HTTP, debug `ffmpeg` camera capture, or verify livestream access from WSL/browser.

## Recommended approach: Windows FFmpeg MJPEG stream to WSL

When the camera is owned by Windows and visible to DirectShow:

1. Confirm Windows FFmpeg exists:
   ```bash
   powershell.exe -NoProfile -Command 'Get-Command ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source'
   ```
2. If needed, install it from Windows PowerShell:
   ```powershell
   winget install Gyan.FFmpeg
   ```
3. List DirectShow camera names:
   ```bash
   powershell.exe -NoProfile -Command 'ffmpeg.exe -hide_banner -f dshow -list_devices true -i dummy' 2>&1
   ```
4. Start MJPEG HTTP stream from Windows:
   ```powershell
   ffmpeg.exe -f dshow -i video="USB Camera" -f mjpeg -listen 1 http://0.0.0.0:8080/stream.mjpg
   ```
5. From WSL, find the Windows host IP:
   ```bash
   ip route | awk '/default/ {print $3; exit}'
   ```
6. Verify from WSL:
   ```bash
   curl -m 5 -v http://<windows-host-ip>:8080/stream.mjpg -o /tmp/stream-test.mjpg
   ```

`localhost` may work in some WSL networking modes, but the default gateway IP is usually more reliable.

## Quoting PowerShell from WSL

When invoking PowerShell from bash, wrap PowerShell scripts in single quotes so `$_` is not expanded by bash:

```bash
powershell.exe -NoProfile -Command 'Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" }'
```

Avoid double-quoted bash strings containing `$_`; bash can turn `$_` into the previous command argument/path and produce confusing errors like `/home/user.IPAddress` inside PowerShell.

## USB/IP ownership pitfall

If Windows FFmpeg reports:

```text
Could not enumerate video devices (or none found).
```

but WSL has `/dev/video*` devices, the camera may be attached to WSL via USB/IP. In that state, Windows may see only `USBIP Shared Device` or generic USB entries and DirectShow cannot use the camera.

Diagnostic commands:

```bash
# WSL video devices
for d in /dev/video*; do [ -e "$d" ] && printf '%s\n' "$d"; done

# Windows PnP indicators; single-quote the PowerShell script so bash does not expand $_
powershell.exe -NoProfile -Command 'Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match "USBIP|USB Composite|Camera|Video|Webcam|UVC" } | Select-Object Name,PNPClass,Status,DeviceID | Format-List'

# usbipd may not be on PATH from WSL-launched PowerShell; default install path:
powershell.exe -NoProfile -Command '& "C:\Program Files\usbipd-win\usbipd.exe" list'
```

```

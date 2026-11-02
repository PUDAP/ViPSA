# Windows startup automation for WSL MediaMTX WebRTC camera streams

Session-derived recipe for making a WSL MediaMTX WebRTC camera stack restart automatically after Windows login.

## Pattern

Use a Windows-side PowerShell script as the durable entry point:

```powershell
# C:\Users\<user>\vipsa-start-webrtc.ps1
$Distro = 'Ubuntu'
$WslUser = 'vipsa'
$MediaMtxDir = '/home/vipsa/mediamtx-wsl'
$MediaMtxConfig = 'mediamtx-puda.yml'

# start MediaMTX in WSL detached
$cmd = "cd '$MediaMtxDir' && pkill -f '$MediaMtxDir/mediamtx' 2>/dev/null || true; cd '$MediaMtxDir' && nohup ./mediamtx '$MediaMtxConfig' >/tmp/mediamtx-puda.log 2>&1 &"
& wsl.exe -d $Distro -u $WslUser -- bash -lc $cmd | Out-Null

# discover WSL IP dynamically each run
$raw = (& wsl.exe -d $Distro -u $WslUser -- hostname -I) -join ' '
$wslIp = ($raw -split '\s+' | Where-Object { $_ -match '^\d+\.\d+\.\d+\.\d+$' } | Select-Object -First 1)
```

Then start Windows `ffmpeg.exe` publishers to `rtmp://$wslIp:1935/<path>`.

## ViPSA two-camera details from this session

- `camera1`: DirectShow input name has a trailing space: `video=USB CAMERA `.
- `camera2`: DirectShow input name: `video=USB_Camera`.
- `camera2` can be requested at 1280x720 via `-video_size 1280x720`; verified output was H264 1280x720 at about 8 fps.
- WebRTC browser URLs: `http://localhost:8889/camera1/` and `http://localhost:8889/camera2/`.

## PowerShell pitfalls

1. Do not let logging functions write to the success output stream if their caller captures command output.
   - Bad in helper functions that feed values into variables: `Write-Output $line`.
   - Better for logs: `Write-Host $line` plus `Add-Content` to a log file.
   - In this session, `Write-Output` from `Log` polluted the captured WSL IP, producing malformed RTMP URLs like `rtmp://2026-... WSL IP is ... 172.x.x.x:1935/camera1`.

2. Be careful with `Start-Process -RedirectStandardOutput/-RedirectStandardError` for long-lived `ffmpeg.exe` launched from WSL or Task Scheduler.
   - Redirected child pipe handles can keep the parent `powershell.exe` session alive or appear hung.
   - For startup automation, prefer `Start-Process ... -WindowStyle Hidden -PassThru` without redirection, and log only parent startup actions.

3. Preserve quoting of DirectShow device names.
   - `camera1` must be one argument including the trailing space: `-i "video=USB CAMERA "`.
   - Use a carefully constructed argument string when spaces/trailing spaces matter.

## Autostart options

### Preferred if permissions allow: Task Scheduler

A non-admin session may fail to register or modify tasks with errors like `Access is denied` or task result `0x800710e0`. If this happens, do not spend time looping on quoting; check permissions and either ask the user to run an admin helper or use the Startup-folder fallback.

Example admin helper:

```cmd
schtasks /Create /TN "ViPSA WebRTC Stream" /SC ONLOGON /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\amdm\vipsa-start-webrtc.ps1\"" /F
```

### No-admin fallback: Windows Startup folder

Create a `.cmd` file in:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ViPSA-WebRTC-Stream.cmd
```

Contents:

```cmd
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\amdm\vipsa-start-webrtc.ps1"
```

This runs at interactive Windows logon for that user. It is not exactly boot-time before login, but is reliable without elevation.

## Verification checklist

After installing startup automation, run the PowerShell startup script manually once and verify:

```bash
curl -sS http://localhost:9997/v3/paths/get/camera1
curl -sS http://localhost:9997/v3/paths/get/camera2
curl -i http://localhost:8889/camera1/
curl -i http://localhost:8889/camera2/
```

Expected: both paths `ready=true`, tracks include `H264`, and WebRTC page GETs return HTTP 200.

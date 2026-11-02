# Option A: Windows FFmpeg MJPEG stream to WSL

Session-derived diagnostic notes for attempting to expose a Windows webcam as MJPEG/HTTP for WSL access.

## Baseline commands

Check Windows FFmpeg and winget from WSL:

```bash
powershell.exe -NoProfile -Command 'Get-Command ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source'
powershell.exe -NoProfile -Command 'Get-Command winget.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source'
```

List DirectShow devices:

```bash
powershell.exe -NoProfile -Command 'ffmpeg.exe -hide_banner -f dshow -list_devices true -i dummy' 2>&1
```

Start stream when DirectShow sees the camera:

```powershell
ffmpeg.exe -f dshow -i video="USB Camera" -f mjpeg -listen 1 http://0.0.0.0:8080/stream.mjpg
```

From WSL, default Windows host IP is often:

```bash
ip route | awk '/default/ {print $3; exit}'
```

Verify:

```bash
curl -m 5 -v http://<windows-host-ip>:8080/stream.mjpg -o /tmp/stream-test.mjpg
```

## Observed failure pattern

DirectShow list devices returned:

```text
Could not enumerate video devices (or none found).
Could not enumerate audio only devices (or none found).
Error opening input file dummy.
```

Starting the named stream exited immediately:

```text
Could not enumerate video devices (or none found).
Error opening input file video=USB Camera.
Error opening input files: I/O error
```

The older `vfwcap` path listed `Microsoft WDM Image Capture (Win32)` but failed to connect:

```text
Could not connect to device.
Error opening input file 0.
Error opening input files: No such device
```

No process listened on port 8080, and WSL curl to the Windows host IP timed out.

## Useful ownership diagnostics

WSL video-device check:

```bash
for d in /dev/video*; do [ -e "$d" ] && printf '%s\n' "$d"; done
```

Windows PnP check:

```bash
powershell.exe -NoProfile -Command 'Get-CimInstance Win32_PnPEntity | Where-Object { $_.Name -match "USBIP|USB Composite|Camera|Video|Webcam|UVC" } | Select-Object Name,PNPClass,Status,DeviceID | Format-List'
```

If WSL shows `/dev/video*` and Windows shows `USBIP Shared Device`, the camera is probably attached to WSL/USBIP rather than available to Windows DirectShow. The fix is to detach/return the camera to Windows, then rerun DirectShow enumeration.

## Shell quoting lesson

From WSL bash, do not put PowerShell `$_` inside a double-quoted bash string. Bash may expand it and produce errors like:

```text
/home/vipsa.IPAddress : The term '/home/vipsa.IPAddress' is not recognized...
```

Use single quotes around the PowerShell program:

```bash
powershell.exe -NoProfile -Command 'Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" }'
```

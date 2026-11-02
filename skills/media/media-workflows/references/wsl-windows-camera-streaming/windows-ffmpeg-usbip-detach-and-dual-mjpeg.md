# Windows FFmpeg + USB/IP detach + dual MJPEG streams

Session-derived recipe for switching USB webcams from WSL ownership back to Windows, then exposing them to WSL as Windows-hosted MJPEG HTTP streams.

## 1. Locate `usbipd.exe`

`usbipd.exe` may not be on PATH from PowerShell launched via WSL. Check the default install path first:

```bash
powershell.exe -NoProfile -Command 'Test-Path "C:\Program Files\usbipd-win\usbipd.exe"; & "C:\Program Files\usbipd-win\usbipd.exe" list'
```

## 2. Identify cameras attached to WSL

Example `usbipd list` output when cameras are owned by WSL:

```text
BUSID  VID:PID    DEVICE                         STATE
1-4    0458:708c  USB_Camera, USB2.0 MIC         Attached
3-4    0ac8:3420  USB CAMERA                     Attached
```

In this state, Windows FFmpeg/DirectShow may report no devices or fail to open `video=USB Camera`.

## 3. Detach cameras back to Windows

```bash
powershell.exe -NoProfile -Command '
& "C:\Program Files\usbipd-win\usbipd.exe" detach --busid 1-4
& "C:\Program Files\usbipd-win\usbipd.exe" detach --busid 3-4
& "C:\Program Files\usbipd-win\usbipd.exe" list
'
```

After detach, rerun DirectShow enumeration:

```bash
powershell.exe -NoProfile -Command 'ffmpeg.exe -hide_banner -f dshow -list_devices true -i dummy' 2>&1
```

Observed camera names after detach:

```text
"USB_Camera" (video)
"USB CAMERA " (video)
```

Note the trailing space in `"USB CAMERA "`; preserve it exactly.

## 4. Start Windows-hosted MJPEG streams from WSL

Use separate ports for two cameras. Start them as background Windows processes with separate stdout/stderr log files; `Start-Process` refuses when both redirects point to the same file.

```bash
powershell.exe -NoProfile -Command '
$base = "$env:TEMP"
$out0 = Join-Path $base "ffmpeg-usb-camera-8080.out.log"
$err0 = Join-Path $base "ffmpeg-usb-camera-8080.err.log"
$out1 = Join-Path $base "ffmpeg-usb-camera-8081.out.log"
$err1 = Join-Path $base "ffmpeg-usb-camera-8081.err.log"
Remove-Item $out0,$err0,$out1,$err1 -ErrorAction SilentlyContinue
$args0 = "-hide_banner -loglevel info -f dshow -i `"video=USB CAMERA `" -f mjpeg -listen 1 http://0.0.0.0:8080/stream.mjpg"
$args1 = "-hide_banner -loglevel info -f dshow -i `"video=USB_Camera`" -f mjpeg -listen 1 http://0.0.0.0:8081/stream.mjpg"
$p0 = Start-Process -FilePath ffmpeg.exe -ArgumentList $args0 -RedirectStandardOutput $out0 -RedirectStandardError $err0 -PassThru -WindowStyle Hidden
$p1 = Start-Process -FilePath ffmpeg.exe -ArgumentList $args1 -RedirectStandardOutput $out1 -RedirectStandardError $err1 -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 4
"cam8080 PID=$($p0.Id) HasExited=$($p0.HasExited)"
"cam8081 PID=$($p1.Id) HasExited=$($p1.HasExited)"
netstat -ano | Select-String ":8080|:8081"
'
```

Expected listeners:

```text
0.0.0.0:8080 LISTENING <pid>
0.0.0.0:8081 LISTENING <pid>
```

## 5. Verify access

Windows-local test:

```bash
powershell.exe -NoProfile -Command '
foreach ($port in 8080,8081) {
  $out = "$env:TEMP\cam-$port-test.mjpg"
  Remove-Item $out -ErrorAction SilentlyContinue
  & curl.exe --max-time 4 -sS "http://127.0.0.1:$port/stream.mjpg" -o $out
  if (Test-Path $out) { "port=$port bytes=$((Get-Item $out).Length)" }
}
'
```

WSL test:

```bash
winip=$(ip route | awk '/default/ {print $3; exit}')
curl --max-time 5 "http://$winip:8080/stream.mjpg" -o /tmp/cam8080.mjpg
curl --max-time 5 "http://$winip:8081/stream.mjpg" -o /tmp/cam8081.mjpg
```

If Windows-local curl succeeds but WSL cannot connect to the Windows host IP, add a Windows Firewall inbound rule from an elevated PowerShell:

```powershell
New-NetFirewallRule `
  -DisplayName "Allow FFmpeg MJPEG 8080-8081 from WSL" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 8080-8081 `
  -Profile Any
```

Non-admin PowerShell may return `Access is denied`; that is setup/privilege state, not evidence that the streaming method is wrong.

## Operational pitfalls

- `ffmpeg -listen 1` serves a client connection; aborting a curl/browser client can produce Windows socket error `-10054` and may end the FFmpeg process depending on timing. Re-check `Get-Process ffmpeg` and `netstat` after tests.
- A raw MJPEG stream can be high-bandwidth. Buffer warnings such as `real-time buffer ... too full ... frame dropped` indicate pressure but do not necessarily mean capture failed.
- Preserve exact DirectShow names, including spaces and case, from `-list_devices true` output.

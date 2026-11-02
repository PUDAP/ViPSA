# Windows FFmpeg -> WSL MediaMTX -> WebRTC

Session-derived recipe for exposing Windows-owned USB cameras as WebRTC pages served from WSL.

## When to use

Use when:

- The user wants WebRTC/browser viewing from WSL.
- Cameras are visible to Windows DirectShow, not Linux `/dev/video*`.
- MJPEG `ffmpeg -listen 1` is too fragile or not a true WebRTC deliverable.
- Docker is unavailable from WSL or WSL Docker integration is not configured; run native MediaMTX instead.

## Architecture

```text
Windows USB camera
  -> Windows ffmpeg.exe -f dshow
  -> RTMP publish to WSL IP:1935/<path>
  -> MediaMTX running in WSL
  -> WebRTC browser page http://localhost:8889/<path>/
```

## Camera ownership and exact names

If Windows FFmpeg says no video devices are available while WSL has `/dev/video*`, inspect USB/IP:

```bash
powershell.exe -NoProfile -Command '& "C:\Program Files\usbipd-win\usbipd.exe" list'
powershell.exe -NoProfile -Command '& "C:\Program Files\usbipd-win\usbipd.exe" detach --busid <BUSID>'
powershell.exe -NoProfile -Command 'ffmpeg.exe -hide_banner -f dshow -list_devices true -i dummy' 2>&1
```

Preserve DirectShow device names exactly. In the session that produced this recipe the names included:

```text
USB_Camera
USB CAMERA 
```

The second name has a trailing space and must be quoted carefully.

## Native MediaMTX in WSL

Download a Linux amd64 MediaMTX release if Docker is not usable:

```bash
mkdir -p ~/mediamtx-wsl
cd ~/mediamtx-wsl
# Example release URL will change; use the latest Linux amd64 tarball from MediaMTX releases.
curl -L -o mediamtx.tar.gz 'https://github.com/bluenviron/mediamtx/releases/download/vX.Y.Z/mediamtx_vX.Y.Z_linux_amd64.tar.gz'
tar -xzf mediamtx.tar.gz
./mediamtx --version
```

Copy the default config for the camera setup and enable the API:

```bash
cp mediamtx.yml mediamtx-puda.yml
# edit mediamtx-puda.yml:
#   api: true
#   logLevel: debug   # useful while debugging; optional later
./mediamtx mediamtx-puda.yml
```

If restart fails with a UDP bind error such as `listen udp :8000: bind: address already in use`, an old MediaMTX instance is still running; stop it before starting a new one.

## Start Windows FFmpeg publishers

Compute the WSL IP from WSL and pass it to a PowerShell helper:

```bash
wsl_ip=$(hostname -I | awk '{print $1}')
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\<WindowsUser>\AppData\Local\Temp\start-cameras-rtmp.ps1' -WslIp "$wsl_ip"
```

PowerShell helper pattern:

```powershell
param([Parameter(Mandatory=$true)][string]$WslIp)

Get-Process ffmpeg -ErrorAction SilentlyContinue | Stop-Process -Force

$ffmpeg = 'ffmpeg.exe'

# Use a single string for arguments when device names contain spaces/trailing spaces.
$cam1Args = '-f dshow -i "video=USB CAMERA " -an -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -f flv rtmp://' + $WslIp + ':1935/camera1'
Start-Process -FilePath $ffmpeg -ArgumentList $cam1Args -WindowStyle Minimized

$cam2Args = '-f dshow -i "video=USB_Camera" -an -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -f flv rtmp://' + $WslIp + ':1935/camera2'
Start-Process -FilePath $ffmpeg -ArgumentList $cam2Args -WindowStyle Minimized
```

Why a single argument string: `Start-Process -ArgumentList` arrays can split DirectShow names like `video=USB CAMERA ` so FFmpeg searches for a device named `USB`.

## Verify readiness

MediaMTX API should show both paths ready, sourced from RTMP, with H264 tracks and `inboundFramesInError: 0`:

```bash
curl -sS http://localhost:9997/v3/paths/list
```

Check browser pages by GET, not HEAD:

```bash
curl -i http://localhost:8889/camera1/ | head
curl -i http://localhost:8889/camera2/ | head
```

Expected: `HTTP/1.1 200 OK` and an HTML response. A `GET /<path>/whep` may return `405 Method Not Allowed`; that only means WHEP expects POST/ICE negotiation, not plain GET.

Windows localhost forwarding can make these work directly in a Windows browser:

```text
http://localhost:8889/camera1/
http://localhost:8889/camera2/
```

For remote LAN browsers, plan explicit firewall/port-forwarding for MediaMTX WebRTC TCP `8889` and UDP `8000/8001` rather than relying on WSL localhost forwarding.

## Pitfalls

- `ffmpeg -f mjpeg -listen 1 http://0.0.0.0:8080/stream.mjpg` is single-listener and can exit when a curl probe connects/disconnects. For durable WebRTC, publish to MediaMTX instead.
- Do not treat missing WSL `ffmpeg` or Docker WSL integration as durable blockers; Windows FFmpeg plus native MediaMTX can bypass both.
- Do not ask for or preserve Windows admin passwords. If firewall/UAC is needed, have the user approve UAC or run a specific admin command locally.
- If PowerShell is launched from a WSL UNC working directory and WSL path translation fails, compute the WSL IP in WSL first and pass it as a normal parameter.

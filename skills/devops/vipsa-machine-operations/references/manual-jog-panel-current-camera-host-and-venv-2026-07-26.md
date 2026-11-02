# Manual jog panel current camera host and venv dependency (2026-07-26)

Use this when restoring or debugging the ViPSA manual jog panel camera viewport.

## Durable lesson

The panel can be operational while the camera viewport is blank if its iframe points at a stale MediaMTX/WebRTC host. Do not assume the camera is down when the user says MTX streams work; verify the iframe URL separately from the panel API.

## Verified workflow

1. Probe likely camera WebRTC/HLS pages before editing the panel:
   ```bash
   python3 - <<'PY'
   import urllib.request
   for u in [
       'http://100.67.251.110:8889/camera1/',
       'http://100.74.20.98:8889/camera1/',
       'http://127.0.0.1:8889/camera1/',
   ]:
       try:
           with urllib.request.urlopen(u, timeout=5) as r:
               print(u, r.status, r.getheader('content-type'))
       except Exception as e:
           print(u, type(e).__name__, e)
   PY
   ```
2. Patch `/home/amdm/vipsa_windows_backup/vipsa-jog-panel/server.py` so `CAMERA1_URL` defaults to the current working host, e.g. `http://100.74.20.98:8889/camera1/` when that is the verified host.
3. Start the panel from its venv so the persistent Python NATS client works:
   ```bash
   cd /home/amdm/vipsa_windows_backup/vipsa-jog-panel
   uv venv .venv  # only if missing
   . .venv/bin/activate
   uv pip install nats-py  # only if missing
   export PUDA_PROJECT_DIR=/home/amdm/vipsa_windows_backup/vipsa-puda-project
   export PUDA_NATS_SERVERS=nats://100.109.131.12:4224
   python server.py
   ```
4. Verify the page, iframe, and console:
   - panel API: `http://127.0.0.1:8765/api/status` returns 200
   - current Tailscale panel API returns 200, e.g. `http://100.74.20.98:8765/api/status`
   - iframe `src` is the verified current camera URL
   - browser accessibility tree shows a video element inside the iframe
   - browser console has no JS errors

## Reporting standard

Report the stale URL and the replacement URL explicitly. State that the MTX stream was working and the panel was fixed by updating the embedded camera host, not by restarting camera publishers.

## Pitfalls

- Do not leave `CAMERA1_URL` hard-coded to an old Tailscale address just because the panel itself loads.
- Do not stop at `/api/status` success; the jog controls and the camera iframe are independent.
- Missing `nats-py` is a setup issue for the panel venv; the fix is to install it into `.venv` and relaunch from that venv, not to disable persistent direct mode.

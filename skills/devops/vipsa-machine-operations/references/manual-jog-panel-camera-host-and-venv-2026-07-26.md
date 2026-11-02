# Manual jog panel camera host and venv restore (2026-07-26)

Use when restoring `/home/amdm/vipsa_windows_backup/vipsa-jog-panel/server.py` or when the manual jogging panel loads but the camera viewport is blank while MediaMTX streams are otherwise working.

## What happened

The panel server restored successfully and the control API worked, but the camera iframe used a stale Tailscale host:

- stale / unavailable: `http://100.67.251.110:8889/camera1/`
- verified current host: `http://100.74.20.98:8889/camera1/`

The current host was verified by HTTP GETs against:

- `http://100.74.20.98:8889/camera1/` → `200 text/html`
- `http://127.0.0.1:8889/camera1/` → `200 text/html`

Then `server.py` was patched so `CAMERA1_URL` defaulted to the current reachable Tailscale URL, and the panel was restarted. Browser verification showed the iframe source was the current URL and contained a video element, with no console errors.

## Durable workflow

1. Do not assume the `CAMERA1_URL` embedded in the panel is current. Probe the live MediaMTX web page before starting/restarting the panel:
   ```bash
   python3 - <<'PY'
   import urllib.request
   for u in ['http://100.74.20.98:8889/camera1/','http://127.0.0.1:8889/camera1/']:
       try:
           with urllib.request.urlopen(u, timeout=5) as r:
               print(u, r.status, r.getheader('content-type'))
       except Exception as e:
           print(u, type(e).__name__, e)
   PY
   ```
2. Patch or export `CAMERA1_URL` to the reachable host before launch. Prefer the externally reachable Tailscale URL in the iframe when the user opens the panel remotely; `127.0.0.1` only works from the machine itself.
3. The restored backup panel imports `nats`. If the runtime Python lacks it, create/use a panel-local venv rather than changing system Python:
   ```bash
   cd /home/amdm/vipsa_windows_backup/vipsa-jog-panel
   uv venv .venv
   . .venv/bin/activate
   uv pip install nats-py
   ```
4. Launch from that venv:
   ```bash
   export PUDA_PROJECT_DIR=/home/amdm/vipsa_windows_backup/vipsa-puda-project
   export PUDA_NATS_SERVERS=nats://100.109.131.12:4224
   export CAMERA1_URL=http://100.74.20.98:8889/camera1/
   . .venv/bin/activate
   python server.py
   ```
5. Verify the control panel and camera together:
   - `http://127.0.0.1:8765/` returns the panel HTML.
   - `/api/status` returns JSON and `active: false` initially.
   - Browser snapshot includes an iframe with a `Video` element.
   - `document.querySelector('iframe')?.src` equals the verified MediaMTX URL.
   - Browser console has no JavaScript errors.

## Safety

Only use the safe lifecycle/read-only verification unless the user explicitly asks for jog/light side effects: `Start -> read stage position -> read Zaber position -> Complete`, then verify `light`, `stage`, and `zaber` are `idle` with `run_id: null`.

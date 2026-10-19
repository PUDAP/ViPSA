# Manual jog panel: quick resistance button and camera iframe repair (2026-07-26)

Use this when restoring or extending the ViPSA manual jog panel and the user wants an electrical health/resistance button in the UI, or reports that the camera viewport is blank while MediaMTX streams themselves are healthy.

## Quick resistance button pattern

Panel location used in this session:

- Restored panel script: `/home/amdm/vipsa_windows_backup/vipsa-jog-panel/server.py`
- Project dir: `/home/amdm/vipsa_windows_backup/vipsa-puda-project`
- Default panel URL: `http://<current-tailscale-host>:8765/`

Add an **Electrical** card with a **Quick resistance check** button that does **not** require pressing Start. The button should call a new endpoint such as `/api/resistance` and write the returned JSON into the panel status box.

Endpoint behavior:

1. Run a one-command PUDA protocol to turn lights off first.
2. Execute the existing canonical quick resistance script:
   ```bash
   python3 /home/amdm/vipsa_windows_backup/vipsa-puda-project/tools/quick_resistance_check.py --nats nats://100.109.131.12:4224
   ```
3. Return parsed JSON to the UI, including classification, estimated resistance, `closed_channels_after_measurement`, cleanup status, and final machine states.
4. Keep the standard electrical cleanup invariant: Keithley output off, 707B `open_all`, `get_closed_channels == nil`.

Implementation details:

- Add `import sys` if the server launches the script using `sys.executable`.
- Use a full-metadata PUDA protocol for the light-off pre-step; do not rely on a manual-run Start session for this button.
- Save protocol JSON/logs under the project run tree (for example `runs/jog_panel_actions/`) so failures are inspectable.
- The button is intentionally outside `.gated`, because it should work without Start and without leaving a persistent manual run active.

Minimal frontend shape:

```html
<div class="card">
  <h2>Electrical</h2>
  <div class="muted">Runs a dark low-bias Keithley/707B resistance check: lights off, 0 V / ±10 mV / ±50 mV, then Keithley output off and 707B open/nil. Does not require Start.</div>
  <button class="warn" id="resistance-btn" onclick="quickResistance()">Quick resistance check</button>
</div>
```

```js
async function quickResistance(){
  const btn = document.getElementById('resistance-btn');
  btn.disabled = true;
  try { await api('/api/resistance', {}); }
  catch(e) { setStatus(String(e)); }
  finally { btn.disabled = false; }
}
```

## Camera viewport blank but MediaMTX works

If the user says the panel camera viewport is unavailable/blank while MTX streams are working, do not debug the cameras first. Inspect the iframe URL in the panel page or `CAMERA1_URL` default/env var, then compare it with a live HTTP/RTSP probe of the current MediaMTX host.

Observed fix pattern:

1. Probe candidate WebRTC pages:
   ```bash
   python3 - <<'PY'
   import urllib.request
   for u in ['http://<old-host>:8889/camera1/','http://<current-host>:8889/camera1/','http://127.0.0.1:8889/camera1/']:
       try:
           with urllib.request.urlopen(u, timeout=5) as r:
               print(u, r.status, r.getheader('content-type'))
       except Exception as e:
           print(u, type(e).__name__, e)
   PY
   ```
2. Patch `CAMERA1_URL` default or restart the panel with `CAMERA1_URL=http://<current-host>:8889/camera1/`.
3. Restart the panel server from its venv.
4. Verify the browser accessibility tree shows a `Video` element inside the iframe, the iframe `src` is the current host, and browser console has no JS errors.

## Dependency fix for restored backup panel

The restored backup panel uses Python `nats` (`nats-py`) for persistent direct control. If Start fails with `ModuleNotFoundError: No module named 'nats'`, fix the panel environment rather than rewriting the control path:

```bash
cd /home/amdm/vipsa_windows_backup/vipsa-jog-panel
uv venv .venv
. .venv/bin/activate
uv pip install nats-py
python server.py
```

Then verify safe lifecycle only (`Start -> read stage -> read zaber -> Complete`) before reporting restored motion controls. Do not test jog moves or light toggles unless the user explicitly requested those side effects.

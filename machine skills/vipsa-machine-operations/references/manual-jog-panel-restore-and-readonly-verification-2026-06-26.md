# Manual jog panel restore and read-only verification (2026-06-26)

Use this when the user says the ViPSA manual jogging panel is broken or asks to restore/fix it.

## Panel location and default server

- Preferred script: `/home/vipsa/vipsa-jog-panel/server.py`
- If that path is missing in the current Hermes/WSL context, a working backup/restore location has been `/home/amdm/vipsa_windows_backup/vipsa-jog-panel/server.py`; run it with `PUDA_PROJECT_DIR=/home/amdm/vipsa_windows_backup/vipsa-puda-project` unless a live project path is available.
- Default bind: `0.0.0.0:8765`
- Useful URLs:
  - Local: `http://127.0.0.1:8765/`
  - Tailscale/current host style: use the host's current `100.x.y.z` address (for example `hostname -I | tr ' ' '\n' | grep '^100\.'`) and report `http://<that-ip>:8765/`; older notes may show `http://100.67.251.110:8765/`.
- Camera iframe default in the script: `http://100.67.251.110:8889/camera1/` unless overridden with `CAMERA1_URL`.

## Restore workflow

1. Locate any existing process:
   ```bash
   ps -ef | grep -Ei 'jog|panel|http.server|ThreadingHTTPServer|manual' | grep -v grep || true
   ss -ltnp | grep ':8765' || true
   ```
2. Syntax-check the server before launching:
   ```bash
   cd <panel-dir>
   python3 -m py_compile server.py
   ```
3. Ensure the Python runtime used to launch the server has `nats-py` available. A durable setup fix is to create/use a venv in the panel directory:
   ```bash
   cd <panel-dir>
   uv venv .venv
   . .venv/bin/activate
   uv pip install nats-py
   ```
4. Start the server as a tracked background process from its directory, with explicit environment overrides when using the backup path:
   ```bash
   cd <panel-dir>
   export PUDA_PROJECT_DIR=<puda-project-dir>
   export PUDA_NATS_SERVERS=nats://100.109.131.12:4224
   export CAMERA1_URL=http://100.67.251.110:8889/camera1/
   . .venv/bin/activate  # if using the panel venv
   python3 server.py
   ```
4. Verify HTTP health without side effects:
   ```bash
   python3 - <<'PY'
   import urllib.request
   for url in ['http://127.0.0.1:8765/', 'http://127.0.0.1:8765/api/status']:
       with urllib.request.urlopen(url, timeout=5) as r:
           print(url, r.status, r.getheader('content-type'))
   PY
   ```
5. Open the page in the browser if available and check:
   - page title is `ViPSA Manual Jog Panel`
   - camera iframe loads
   - controls are disabled before Start
   - no JavaScript console errors

## Safe functional verification

First read `puda machine state light`, `stage`, and `zaber`, **but verify freshness**: on the bears cluster the CLI can read stale `MACHINE_STATE_<machine>` per-machine KV entries while the running edges write current truth to shared `MACHINE_STATE` KV. Compare timestamps and read shared KV via nats-py (`js.key_value('MACHINE_STATE').get(machine)`) before concluding a run is active. If a run is actually active with a run_id not owned by the panel's current `/api/status` session, do not POST `/api/start` or `/api/complete` and do not reset it. A prior panel implementation automatically sent COMPLETE for an active run_id on Start, which could seize deliberate manual control; current server must fail closed on that mismatch and stop before STARTing subsequent machines. Verify only GET `/` and GET `/api/status` and report the conflict to the user. Do not assume matching IDs on two of three machines permit resuming a whole manual session. On this host the live panel path may be `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-jog-panel/server.py` and project path the sibling `vipsa-puda-project`; prefer live discovery over old `/home/vipsa` paths.

Only when all machines are idle is it acceptable to verify the manual-run lifecycle and read-only endpoints; do **not** test real jog motion or light toggles unless the user explicitly asks for that side effect.

Safe verification sequence:

1. POST `/api/start` with `{}` and confirm `ok: true`, `machines: ["light", "stage", "zaber"]`, and controls unlock.
2. POST `/api/position` for `stage`; expected successful payload has `response.data.result` like `[x, y, z]`.
3. POST `/api/position` for `zaber`; expected successful payload has `response.data.x` and `response.data.y`.
4. POST `/api/complete` with `{}` and confirm `ok: true` and controls lock again.
5. Verify final states with timed `puda machine state light`, `stage`, and `zaber`: all should be `idle` with `run_id: null`.

## Implementation details / pitfalls

- The panel uses direct persistent Python NATS for low-latency control after Start. It starts only `light`, `stage`, and `zaber` by default (`MANUAL_RUN_MACHINES`), while reset-all targets the full ViPSA machine set.
- If `/api/start` returns `persistent direct PUDA connect failed: ModuleNotFoundError: No module named 'nats'`, install `nats-py` into the exact environment used to launch `server.py`, restart the server, then rerun the read-only lifecycle verification. Capture this as a setup fix, not as a panel failure.
- Start/Complete are real PUDA run lifecycle commands but not physical motion. Position reads are read-only. Jog buttons and light buttons are side-effecting.
- Stage X/Y buttons are intentionally gated behind an enable checkbox; Stage Z unlocks after Start. Preserve this safety behavior.
- Zaber native units are represented as `units: null`; do not convert to mm unless the user chooses mm.
- For browser verification, do not rely only on the accessibility snapshot after clicking Start; inspect the JS state/status if the snapshot has not refreshed yet.
- If `/api/complete` hangs/times out but the active panel run ID is known from `/api/status`, take back control by publishing direct `complete` immediate commands for that exact run ID to `light`, `stage`, and `zaber` on the active ViPSA NATS servers. Then verify each machine is `idle` with `run_id: null`. If the panel UI/session remains active only in server memory after verified machine cleanup, restart `/home/vipsa/vipsa-jog-panel/server.py` to clear the in-memory session and verify `/api/status` reports `active: false`, `run_id: null`.

# Manual web jog panel pattern (2026-06-08)

Use this when the user asks for a browser/webpage control panel for manual ViPSA motion with a live camera view.

## Proven shape

A small Python stdlib `ThreadingHTTPServer` is sufficient; no Flask install is required. The panel can be hosted from WSL and call PUDA through server-side endpoints that generate one-command protocol JSON files and run:

```bash
puda protocol run --file /tmp/<protocol>.json
```

The web UI used this layout:

- Left: iframe pointed at the existing MediaMTX WebRTC page for `camera1`.
  - If the page is opened only on the WSL/Windows host, `http://localhost:8889/camera1/` works.
  - If the page is opened from another device/phone over Tailscale/LAN, do **not** embed `localhost`; it resolves on the viewer's device and causes “localhost refused to connect.” Use the same reachable host/IP as the camera links, e.g. `http://<tailscale-or-lan-ip>:8889/camera1/`.
- Right: cards for:
  - Zaber XY jog controls
  - Stage XYZ jog controls
  - Lights on/off controls
- Each motion axis has a step-size input and `-` / `+` buttons.
- Include read-position buttons for both motion machines.

## PUDA command mapping

Zaber:

- `move_x_by(distance, units=None)`
- `move_y_by(distance, units=None)`
- `get_current_position(units=None)`

Default Zaber units should be native controller units (`units: null`). Offer `mm` only as an explicit selector.

Stage:

- `move_x_by(steps)`
- `move_y_by(steps)`
- `move_z_by(height)`
- `get_current_position()`

Stage X/Y motion is physically riskier. In the browser UI, keep Stage X/Y buttons disabled behind an explicit enable checkbox. Stage Z can be enabled by default.

Lights:

- Add a small `Lights` card with `Lights ON` and `Lights OFF` buttons when the user wants illumination control in the jog panel.
- Preferred mapping when `puda protocol run` is reliable: server-side endpoints create PUDA one-command protocols:
  - `turn_on()` on machine `light`
  - `turn_off()` on machine `light`
- Pitfall/fallback: the panel can fail with `failed to connect to NATS: dial tcp 192.168.50.6:<port>: i/o timeout` even when `--nats-servers nats://100.109.131.12:4222` is supplied, because the NATS route/cluster advertises stale `192.168.50.6` routes. For light controls, bypass `puda protocol run` and publish through Python `nats` JetStream directly: `start` and `complete` on `puda.light.cmd.immediate`, and `turn_on`/`turn_off` on `puda.light.cmd.queue`; subscribe to `puda.light.cmd.response.*` and wait for the matching `run_id` step-1 success.
- As with jog moves, verify endpoint wiring/UI presence without actually toggling the lights unless the user explicitly asks to test a real toggle.

## Protocol metadata

PUDA requires full protocol metadata, not command-only JSON. Reuse active project metadata from an existing protocol JSON under the current PUDA project and create a fresh `protocol_id`/`created_at` for each command.

Required fields:

- `protocol_id`
- `project_id`
- `user_id`
- `username`
- `description`
- `created_at`
- `commands`

## Low-latency direct-control panel update

If the manual panel feels slow, do **not** send each button click through `puda protocol run` or create a fresh NATS connection per request. Use one persistent Python NATS client in the panel server:

- Keep a single asyncio loop/thread and NATS connection alive for `light`, `stage`, and `zaber`.
- Subscribe once to `puda.*.cmd.response.>` plus the explicit immediate/queue response subjects.
- On Start, publish direct `start` lifecycle commands under one shared manual `run_id`.
- On jog/read/light actions, publish direct queue commands under that active `run_id` (`move_x_by`, `move_y_by`, `move_z_by`, `get_current_position`, `turn_on`, `turn_off`).
- On Complete, publish direct `complete` lifecycle commands and clear the server-side session.
- Prefer NATS `:4222` first for this panel (`4222,4223,4224`). A later test showed `:4224` could accept/publish starts while the panel missed light/stage responses and left stale active state; switching back to `:4222` made Start → read positions → Complete reliable again.
- Add a short post-subscribe delay (~0.3 s) before the first publish; without it, fast edge responses can be missed, leaving machines active while the UI reports a timeout.
- If Start returns `RUN_ID_MISMATCH` with `cannot start, <run_id> is currently running`, publish `complete` for that stale run id and retry Start for that machine. If the stale id equals the **fresh** run id that was just published, treat it as accepted/success for that machine rather than completing your own new run.
- Disable the Start button while a Start request is pending to avoid accidental double-click duplicate STARTs.
- If light is left in stale/error state after direct-panel testing, recover with a normal PUDA protocol containing `initialize(startup_command="off")` then `turn_off()`, then verify `light` is idle / `run_id: null`.

Verified implementation path: `/home/vipsa/vipsa-jog-panel/server.py` with `direct_mode: persistent_python_nats`. Read-only HTTP verification used Start → Zaber position → Stage position → Complete on `nats://100.109.131.12:4222`, with final `light`, `stage`, and `zaber` idle / `run_id: null`. Do not test real jog moves unless explicitly requested.

## Verification standard

Before reporting success:

1. Verify active env and machine idle state for `zaber` and `stage`.
2. Verify MediaMTX has `camera1` ready if using its iframe.
3. Start the server in the background and confirm it listens on the intended port.
4. Load the page in a browser and confirm the camera iframe/control layout renders.
5. Exercise only read-only position endpoints unless the user explicitly approves jog motion.
6. Report the local URL, WSL IP URL, and the verified readbacks.

## Safety notes

- Do not test actual jog moves unless explicitly requested.
- Preserve the established Stage X/Y safety rule: do not move Stage X/Y unless the user specifically enables/requests it.
- Keep Zaber native units as the default; do not silently convert to mm.

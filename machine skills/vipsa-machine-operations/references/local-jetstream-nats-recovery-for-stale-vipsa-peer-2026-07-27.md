# Local JetStream NATS recovery for stale ViPSA NATS peer (2026-07-27)

## Trigger

Use when a ViPSA operation is blocked because the configured NATS endpoint is no longer reachable, and the user asks to resolve the issue rather than only diagnose it.

Observed signals:

- `tailscale ping <old-nats-ip>` reports `no matching peer`.
- MagicDNS name such as `bears` no longer resolves.
- TCP probes to the old NATS ports (`4222`, `4223`, `4224`) fail/timeout.
- Existing local ViPSA edge logs repeat `puda.edge_nats_client` connection errors to the old endpoint.
- The ViPSA edge source tree and `.env` files exist locally, so the edge services can be restarted against another NATS server.

## Recovery pattern

1. Verify the old endpoint is truly stale/unreachable before changing control routing.
2. Install or provide a user-local `nats-server` binary if system install requires sudo and sudo is unavailable. A known-good option was downloading the upstream Linux amd64 release binary to `~/.local/bin/nats-server`.
3. Start a local JetStream NATS:

   ```bash
   ~/.local/bin/nats-server -js -sd ~/.local/share/puda-nats -p 4222
   ```

4. Set PUDA CLI NATS config to localhost:

   ```bash
   puda config set nats_servers nats://127.0.0.1:4222
   ```

5. Patch ViPSA edge `.env` files from the stale cluster to:

   ```text
   NATS_SERVERS=nats://127.0.0.1:4222
   ```

6. Restart the needed edge service(s), or all six ViPSA edges if the user needs the rig generally restored:

   ```bash
   cd /path/to/ViPSA/stage && uv run main.py
   cd /path/to/ViPSA/light && uv run main.py
   cd /path/to/ViPSA/zaber && uv run main.py
   cd /path/to/ViPSA/keithley-707b && uv run main.py
   cd /path/to/ViPSA/keithley-2450 && uv run main.py
   cd /path/to/ViPSA/keysight-b2902b && uv run main.py
   ```

7. Verify with read-only PUDA checks before any physical/electrical side effect:

   ```bash
   puda machine list --json
   puda machine commands stage
   # Prefer a full-metadata read-only protocol for get_current_position before motion.
   ```

8. Only after START/command/COMPLETE works for a read-only protocol, execute the requested motion as a normal PUDA protocol. Verify with a separate readback protocol and final machine state.

## Reporting caveat

This recovery restores local PUDA control-plane semantics and driver readback. If the user has reported that the motor does not visibly move despite PUDA success/readback, do not claim physical motion solely from PUDA readback; report it as PUDA/driver-confirmed and note that remaining failure would be below PUDA at the driver/motor/hardware layer.

## Tailscale notes

- `tailscale ping probot` returning `via 192.168.x.x:41641` indicates a direct local-network Tailscale path.
- `tailscale ping <peer>` returning only `via DERP(...)` with `direct connection not established` means Tailscale reachability exists, but peer-to-peer NAT traversal did not establish.
- Normal ICMP `ping` can fail even when Tailscale connectivity is healthy; prefer `tailscale ping` and actual service/TCP checks for diagnosis.

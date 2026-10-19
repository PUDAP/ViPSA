# ViPSA bears NATS edge restart — 2026-07-28

## Context

The local `nats-server` was stopped and the PUDA controller/CLI config was changed to:

```text
nats://bears:4222,nats://bears:4223,nats://bears:4224
```

However, the already-running ViPSA edge services under `/home/amdm/workspace/ViPSA` were still connected to `nats://127.0.0.1:4222`, as shown by edge logs in `/home/amdm/workspace/ViPSA/logs/edges/*.log`.

## Durable lesson

Changing `puda config nats_servers` is not enough for edges. Edge services read `NATS_SERVERS` from their own `.env` / process environment at startup. To move edges to another NATS cluster, edit each edge `.env` and restart all edge processes.

## Successful fix pattern

For the ViPSA edge set:

```text
zaber
stage
light
keysight-b2902b
keithley-707b
keithley-2450
```

Set each `/home/amdm/workspace/ViPSA/<edge>/.env` to contain:

```text
NATS_SERVERS=nats://bears:4222,nats://bears:4223,nats://bears:4224
```

Then stop old edge processes, restart with:

```bash
cd /home/amdm/workspace/ViPSA
./start_all_edges.sh
```

When using Hermes terminal tools, run the launcher as a tracked background process rather than using shell-level `&`.

## Verification used

1. Confirm old local NATS and old edge processes are gone or replaced:
   ```bash
   ps -ef | grep -E 'workspace/ViPSA|\.venv/bin/python3 main.py|uv run main.py' | grep -v grep || true
   ss -ltnp '( sport = :4222 or sport = :4223 or sport = :4224 )' || true
   ```
2. Confirm each edge log shows:
   ```text
   Connected to NATS servers: ['nats://bears:4222', 'nats://bears:4223', 'nats://bears:4224']
   ```
3. Confirm the controller sees the ViPSA machines via bears:
   ```bash
   puda --nats-servers 'nats://bears:4222,nats://bears:4223,nats://bears:4224' machine list --json
   ```

Expected ViPSA machine IDs: `keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, `zaber`.

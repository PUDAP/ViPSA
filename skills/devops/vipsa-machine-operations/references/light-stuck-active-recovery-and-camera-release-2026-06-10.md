# Light stuck-active recovery and camera publisher release (2026-06-10)

## Context

During camera snapshot/light-control work, `light` was stuck with a stale active `run_id`. New PUDA light protocols failed at START with:

```text
START command failed for machine light: cannot start, <old-run-id> is currently running
```

A direct `puda machine reset light` was accepted by the control layer enough to clear the stale run id, but the driver rejected reset as restricted:

```text
Error: reset failed: Unknown or restricted command: reset
```

After that, the light state became:

```json
{"run_id": null, "state": "error"}
```

## Recovery recipe

Use PUDA protocol-first recovery after the stale run id is cleared:

1. Check state:

```bash
timeout 6 puda --nats-servers nats://100.109.131.12:4224 machine state light
```

2. If `state=active` with a stale run id and protocols cannot START, attempt:

```bash
puda --nats-servers nats://100.109.131.12:4224 machine reset light
```

Do not treat `Unknown or restricted command: reset` as success by itself. It may clear `run_id` but leave `state=error`.

3. Recover with a validated PUDA protocol. In deployments where `initialize` is in the remote-command allowlist, `initialize(startup_command="off")` followed by `turn_off` may work. **Check the actual edge response:** on the 2026-09-30 ViPSA edge, both `reset` and `initialize` returned `Unknown or restricted command`; `turn_off` alone then succeeded and the fresh light-edge log reported `state=idle, run_id=None`. Do not retry a rejected `initialize` as proof of hardware initialization. Use a one-command `turn_off` protocol if that is the supported harmless command.

```json
{
  "commands": [
    {"step_number": 1, "machine_id": "light", "name": "turn_off", "params": {}}
  ]
}
```

4. Verify final state is idle:

```bash
timeout 8 puda --nats-servers nats://100.109.131.12:4224 machine state light
```

Expected final state:

```json
{"run_id": null, "state": "idle"}
```

If `puda machine state` still returns an old timestamp/run ID despite successful fresh protocols (observed with bears 4222–4224 on 2026-09-30), do **not** trust that snapshot as live status and do not repeat a hardware reset. Require a current command response plus the edge's fresh `Updated state in KV store: ... 'state': 'idle', 'run_id': None` log line, and retain the CLI snapshot inconsistency as an unresolved control-plane issue. A heartbeat list may differ by server; check all three approved bears endpoints and aggregate the six live identities. Never restart NATS merely to reconcile this display.

## Camera release pattern

Camera snapshots from RTSP do not hold the physical DirectShow camera after ffmpeg exits. If the user asks to release camera 1, the holder is usually the Windows publisher process that feeds MediaMTX, not the one-shot snapshot command.

Check Windows publishers from WSL:

```bash
powershell.exe -NoProfile -Command 'Get-CimInstance Win32_Process | Where-Object { $_.Name -match "ffmpeg|mediamtx" -or $_.CommandLine -match "camera1|camera2|video" } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Depth 3'
```

For camera 1 in this setup, the publisher command contains both:

- `video=USB CAMERA `
- `rtmp://127.0.0.1:1935/camera1`

Stop only the matching camera 1 `ffmpeg.exe` process, then re-query to verify no camera1 publisher remains and camera2 still runs if it should remain available.

Use file-based PowerShell or single-quoted `-Command` strings from WSL; mixed Bash/PowerShell quoting can otherwise corrupt the command.

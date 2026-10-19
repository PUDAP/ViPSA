# PUDA protocol-first ViPSA operations and NATS-layer debugging (2026-06-10)

## Durable user workflow correction

For ViPSA machine operations, use `puda protocol` by default unless the user explicitly states otherwise. This applies even when direct/raw NATS control is technically available.

Direct/raw NATS control should be limited to:

- read-only diagnostics, or
- clearing a stale run / machine state only when the user explicitly authorizes bypassing PUDA protocol, or
- emergency safety cleanup when protocol control is impossible and the user has approved the fallback.

When a direct fallback is used, gate it on a successful `START` response. Do not treat a queued driver command as executed unless the command response reports success.

## Protocol cleanup pattern

For “clean up connections and ensure idle” on ViPSA, create a full-metadata PUDA protocol, validate it, then run it. Example command list:

```json
[
  {"step_number": 1, "machine_id": "light", "name": "turn_off", "params": {}},
  {"step_number": 2, "machine_id": "stage", "name": "abort_motion", "params": {}},
  {"step_number": 3, "machine_id": "stage", "name": "get_current_position", "params": {}},
  {"step_number": 4, "machine_id": "keithley-2450", "name": "set_output", "params": {"enabled": false}},
  {"step_number": 5, "machine_id": "keysight-b2902b", "name": "set_output", "params": {"enabled": false}},
  {"step_number": 6, "machine_id": "keithley-707b", "name": "open_all", "params": {}},
  {"step_number": 7, "machine_id": "keithley-707b", "name": "get_closed_channels", "params": {}}
]
```

If protocol validation passes but `puda protocol run` times out connecting to NATS, do not claim cleanup ran. Report that the protocol file is ready/validated but not executed.

## Pinpointing “where exactly is blocked”

Use a layered read-only diagnosis before assuming machine failure:

1. PUDA/env:
   ```bash
   command -v puda
   puda --version
   puda env current
   ```
2. TCP port reachability:
   ```bash
   for p in 4222 4223 4224; do
     printf '%s ' "$p"
     timeout 2 bash -c "</dev/tcp/100.109.131.12/$p" && echo open || echo closed
   done
   ```
3. Raw NATS banner test. Healthy NATS sends an `INFO {...}` banner shortly after connect:
   ```python
   import socket, select, time
   for p in [4222, 4223, 4224]:
       try:
           s = socket.create_connection(('100.109.131.12', p), timeout=3)
           s.setblocking(False)
           data = b''
           end = time.time() + 3
           while time.time() < end:
               r, _, _ = select.select([s], [], [], 0.25)
               if r:
                   chunk = s.recv(512)
                   if not chunk:
                       break
                   data += chunk
                   if b'INFO' in data:
                       break
           print(p, 'NATS_INFO_OK' if b'INFO' in data else f'NO_INFO data={data[:120]!r}')
           s.close()
       except Exception as e:
           print(p, type(e).__name__, e)
   ```
4. Read-only PUDA state:
   ```bash
   timeout 12 puda --nats-servers nats://100.109.131.12:4224 machine state stage
   ```
5. All ViPSA machine states:
   ```bash
   for m in light stage keithley-2450 keithley-707b keysight-b2902b zaber; do
     echo "===== $m ====="
     timeout 6 puda --nats-servers nats://100.109.131.12:4224 machine state "$m" || true
   done
   ```

Interpretation:

- TCP closed: network/Tailscale/firewall/NATS listener layer.
- TCP open but no NATS `INFO`: NATS server/proxy/path is accepting sockets but not speaking NATS reliably.
- NATS `INFO` OK but `puda machine state` times out: PUDA client/route/env or server-side account/cluster issue.
- State works but a machine shows `state: active` with an old `run_id`: the machine edge has a stale active run that must be completed/reset before new protocol commands can start.

In the session that produced this note, NATS recovered and the true remaining blocker was the `light` machine stuck active with an old `run_id`, while stage, Keithley, Keysight, 707B, and Zaber were idle.

## Reporting standard

When asked “where exactly is the error?”, answer with the narrowest currently verified layer, for example:

- “NATS layer: TCP open but no NATS INFO banner.”
- “PUDA client layer: NATS INFO is OK but `puda machine state` times out.”
- “Machine state layer: `light` is stuck active with run_id `<id>`; other ViPSA machines are idle.”

Avoid saying simply “NATS is broken” once more specific evidence is available.
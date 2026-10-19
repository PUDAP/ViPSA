# PUDA edge restart NATS advertised-route pitfall

Session lesson: after restarting ViPSA edges, the edges logged `puda.edge_nats_client - ERROR - NATS error :` and none of the ViPSA machines reappeared in `puda machine list`, even though TCP to the configured NATS servers was open.

## Diagnostic pattern

From the PUDA project:

```bash
puda env current
timeout 8 puda machine list --json
for p in 4222 4223 4224; do timeout 3 bash -lc "</dev/tcp/100.109.131.12/$p" && echo open $p || echo blocked $p; done
python3 - <<'PY'
import socket
for port in (4222,4223,4224):
    s=socket.socket(); s.settimeout(3)
    s.connect(('100.109.131.12', port))
    print(port, s.recv(2048).decode(errors='replace'))
    s.close()
PY
```

In the observed case, NATS was reachable at `100.109.131.12:{4222,4223,4224}`, but the server INFO advertised internal cluster URLs:

```text
connect_urls: 192.168.50.6:4222, 192.168.50.6:4223, 192.168.50.6:4224
```

This can make clients that connect through Tailscale/public IP subsequently try unreachable LAN addresses and emit generic NATS errors.

## Interpretation

- `puda machine list` showing only unrelated machines means the ViPSA edges are not successfully registered/heartbeating.
- Stale `puda machine state <machine>` timestamps from previous sessions are not proof the restarted edge is healthy.
- TCP `open` to `100.109.131.12` only proves the route to the NATS listener, not that edge clients can maintain a healthy NATS connection after processing advertised URLs.

## Fix directions to suggest

1. Best fix: configure the NATS cluster/client advertise URLs to use the reachable address for these edge machines, e.g. `100.109.131.12`, rather than `192.168.50.6`.
2. Edge-side workaround: configure each edge with the explicit reachable server list:
   ```text
   nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224
   ```
   and disable discovered/reconnect URLs if the edge client supports it.
3. Client-side workaround for Hermes/WSL operations: if `puda protocol run --nats-servers nats://100.109.131.12:4222` still fails by trying an advertised `192.168.50.6:*` URL, use a bounded direct NATS transaction only for the needed machine command/cleanup. In Python `nats.py`, connect with `allow_reconnect=False` to one reachable Tailscale server, subscribe to the relevant `puda.<machine>.cmd.response.{immediate,queue}` subjects, publish `start` → one queued command → `complete`, and require matching success responses before reporting execution. If `nc.flush()` times out during this advertised-route outage, it may still be possible to publish then wait briefly for matching command responses; do not treat a flush timeout alone as proof the edge command path is dead.
4. If the edge machine is supposed to be on the LAN, fix routing/firewall/VPN access to `192.168.50.6:4222-4224`.

Ask for the full text after `NATS error :` when needed; it usually identifies whether the client is timing out, getting `no route to host`, or failing auth/TLS.

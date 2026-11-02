# NATS connectivity diagnosis without fixing (2026-06-30)

Use when the user asks to locate a PUDA/NATS connectivity issue and explicitly says **do not fix**. Keep the workflow read-only: do not change Tailscale, PUDA config, NATS config, machine state, or edge services.

## Diagnostic pattern

1. Confirm PUDA config and DNS resolution:
   ```bash
   command -v puda && puda --version
   puda config get nats_servers || true
   getent hosts bears || true
   ip route get 100.109.131.12 || true
   ```
2. Check Tailscale health and path quality:
   ```bash
   tailscale status --peers=false || true
   tailscale ping --timeout 3s --c 3 bears || true
   ping -c 3 -W 2 100.109.131.12 || true
   ```
   High packet loss or DERP-only high-latency replies indicate a network path issue even if TCP ports open.
3. Check TCP reachability separately from NATS protocol health:
   ```bash
   for p in 4222 4223 4224; do
     timeout 3 bash -lc "</dev/tcp/100.109.131.12/$p" >/dev/null 2>&1 && echo "$p open" || echo "$p failed"
   done
   ```
4. Check raw NATS INFO/PONG without publishing machine commands:
   ```python
   import socket, time
   for port in (4222, 4223, 4224):
       s = socket.socket(); s.settimeout(4)
       t = time.time()
       try:
           s.connect(("100.109.131.12", port))
           info = s.recv(4096).decode(errors="replace")
           s.sendall(b'CONNECT {"verbose":false}\r\nPING\r\n')
           pong = s.recv(4096).decode(errors="replace")
           print(port, round(time.time()-t, 2), pong.strip(), info[:300])
       except Exception as e:
           print(port, "fail", round(time.time()-t, 2), repr(e))
       finally:
           s.close()
   ```
5. Inspect NATS `INFO` `connect_urls`. If servers advertise internal addresses such as `192.168.50.6:4222/4223/4224`, test them separately:
   ```bash
   for p in 4222 4223 4224; do timeout 3 bash -lc "</dev/tcp/192.168.50.6/$p" >/dev/null 2>&1 && echo "internal $p open" || echo "internal $p failed"; done
   ip route get 192.168.50.6 || true
   ```
6. Confirm PUDA-level read-only health after raw NATS passes:
   ```bash
   for S in nats://100.109.131.12:4224 nats://100.109.131.12:4223 nats://100.109.131.12:4222; do
     timeout 10 puda --nats-servers "$S" machine list --json || true
     timeout 6 puda --nats-servers "$S" machine state stage || true
   done
   ```

## Interpretation rules

- TCP `open` is not enough; raw NATS `PONG` and PUDA `machine list/state` show progressively higher-level health.
- If raw NATS connects but PUDA fails with `dial tcp 192.168.50.6:422x` / `no route to host` / `i/o timeout`, the issue is likely NATS advertising unreachable internal cluster URLs to this host, not the target machine command or protocol file.
- If Tailscale ping shows high loss or high-latency DERP-only routing, classify it as network path instability even when TCP ports intermittently open.
- If raw NATS `PONG` returns quickly on all three ports and `puda machine list --json` works on all three, report NATS connectivity restored. Machine-state timestamps may still be stale; distinguish restored control-plane connectivity from fresh machine telemetry.
- For motion/electrical requests that failed before START due to NATS connection errors, do not claim physical motion/electrical stress occurred unless a later command response/readback verifies execution.

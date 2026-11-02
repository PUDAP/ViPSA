---
name: network-connectivity-diagnostics
description: Diagnose network reachability issues such as ping failures, DNS problems, HTTP access, and service-specific TCP connectivity.
---

## When to use

Use this when a user asks whether a host is reachable, why `ping` fails, whether the internet works, or whether a service endpoint such as `nats://host:4222` is accessible.

## Core rule

Do **not** equate ping failure with internet failure. `ping` uses ICMP echo; many networks, VPNs, routers, firewalls, and hosts drop ICMP while DNS and TCP/HTTPS still work.

## Diagnostic flow

1. **Run the exact user-requested check first**
   - Example: `ping -c 4 google.com` or `ping -c 4 8.8.8.8`.
   - Report packet counts and loss directly.

2. **Separate DNS from transport reachability**
   - DNS: `getent hosts <host>` or a small Python `socket.gethostbyname` check.
   - HTTP(S): `curl -I --max-time 10 https://<host>` for web endpoints.
   - Raw TCP service: `timeout 5 bash -lc '</dev/tcp/<host>/<port>'`.

3. **Compare local gateway vs external host**
   - Get route: `ip route`.
   - Ping default gateway if present.
   - If gateway ping works but external ICMP fails while HTTPS works, explain that ICMP is filtered upstream.

4. **For overlay/VPN names**
   - If a hostname looks like a Tailscale/MagicDNS or LAN alias, check name resolution and inventory where available, e.g. `tailscale status`.
   - Do not assume a short hostname exists just because it is semantically plausible.

5. **For PUDA/NATS endpoints**
   - Set configuration only when requested: `puda config set nats_servers <urls>`.
   - Verify with a real PUDA command such as `puda machine list`.
   - If it fails, distinguish unresolved hostname, TCP port unreachable, and PUDA/NATS protocol failure.

## Reporting style

Be concise and evidence-based. Use a small table for multi-check summaries. Explain likely cause only after showing what was verified.

## References

- `references/ping-vs-internet.md` — session-derived pattern for ICMP blocked while web access works.
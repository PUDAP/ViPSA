# Ping failure with working internet

Session-derived diagnostic pattern:

- `ping google.com` and `ping 8.8.8.8` returned 100% packet loss.
- `curl -I https://www.google.com` and `curl -I https://example.com` returned HTTP 200.
- DNS lookups for public hosts succeeded.
- Ping to the local default gateway succeeded.
- Therefore, the correct conclusion was: internet access works, but ICMP echo is being filtered/dropped beyond the local gateway.

Useful commands:

```bash
ping -c 4 <host>
getent hosts <host>
curl -I --max-time 10 https://<host>
ip route
ping -c 3 <default-gateway>
tracepath -n -m 8 <ip>
timeout 5 bash -lc '</dev/tcp/<host>/<port>' && echo ok || echo failed
```

For service endpoints such as `nats://host:4222`, do not use ping as the final proof. Verify DNS, TCP port 4222, and the service client command itself.
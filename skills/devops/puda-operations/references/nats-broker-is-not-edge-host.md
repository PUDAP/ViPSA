# NATS host versus edge-host discovery

A configured NATS endpoint is a message-bus location, not evidence that PUDA hardware edges run on that host.

Before using SSH to restart an edge:

1. Inspect local `/proc/<pid>/cwd` and command lines for the expected edge directories.
2. Read the edge `.env` only to learn which NATS cluster it connects to; do not infer process location from `NATS_SERVERS`.
3. Observe heartbeats and edge logs to identify the edge identity and freshness.
4. Restart the process on the host where its PID/CWD is actually found.
5. Use SSH only after independent evidence shows the edge is remote and identifies the correct remote account/host.

For ViPSA, `bears` can host the NATS cluster while `light`, `stage`, `zaber`, and instrument edges run locally on ViPSA-Ubuntu. Contacting `bears` over NATS is therefore normal control traffic and does not justify SSH administration of `bears`.

If SSH itself must be restored, keep host verification enabled, verify the presented key through the tailnet or another independent channel, distinguish normal OpenSSH `~/.ssh/known_hosts` from Tailscale SSH's separate trust cache, and identify the correct remote username before changing `authorized_keys`.
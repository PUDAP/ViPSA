# Targeted PUDA edge recovery after remote NATS interruption

Use when remote NATS connectivity returns but selected edges remain stale, absent from discovery, reject fresh START commands, or log broken queue consumers after reconnect.

## Validated recovery pattern

1. Pause measurement supervision and autonomous continuation. Preserve completed artifacts and ledger state.
2. Observe heartbeats for at least 15 seconds; distinguish a short discovery-window omission from a genuinely absent edge.
3. Inspect edge logs for fresh connection/subscription events and reconnect-loop errors. A process can remain alive while its queue consumer is unusable.
4. Map candidate PIDs to edge identity via `/proc/<pid>/cwd` and command line. This prevents killing unrelated ViPSA edges.
5. Restart only affected electrical edges. Do not disturb stage, Zaber, light, or unrelated instruments.
6. If an instrument uses a separately deployed protected driver, restart from that deployed directory rather than the generic workspace edge.
7. Require exactly one replacement process per affected edge, fresh queue/immediate subscriptions, and `idle` with `run_id: null`.
8. Before resuming stress, force output OFF, open the matrix, require output readback `0`, closed-channel readback `nil`/empty, and no instrument errors.
9. Reconcile retained operations before resuming. Never replay a completed batch solely because the supervisor exited nonzero.

## Pitfalls

- Do not restart local NATS when the rig uses the remote `bears` cluster.
- A successful `machine list` can be incomplete because its discovery window is shorter than the heartbeat interval.
- A visible process is not proof its NATS pull consumer is healthy.
- Do not replace a protected deployed SMU driver with a generic workspace copy during recovery.

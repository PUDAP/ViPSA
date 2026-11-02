# Stage edge NATS endpoint alignment and readback

Use this when a ViPSA Stage-Z command is requested after local NATS or edge-service restarts.

## Lesson

The PUDA client endpoint and the stage edge endpoint must match. A local JetStream NATS server can be running and still not receive stage commands if the restarted stage edge connected to its configured `nats_servers` elsewhere (for example `nats://bears:4222,...`).

## Recommended workflow

1. Before a stage move, check stage state against the endpoint you plan to use.
2. If `puda --nats-servers nats://127.0.0.1:4222 ...` times out at protocol START while the stage edge is running, inspect the stage edge log line `Connecting to NATS at ...` / `Connected to NATS servers: ...` and route the PUDA command to the same endpoint.
3. Prefer one-command motion protocols plus a **separate** read-only position protocol when the stage edge shows run-state fragility. A combined `move_z_by -> get_current_position` protocol can execute the move and then fail the readback with `Send START command to start a run before sending commands`.
4. Reporting standard:
   - If `move_z_by` returned success but the separate readback failed, say **command succeeded; numeric readback not verified**.
   - Do not report a new stage coordinate unless a fresh readback protocol succeeds.
   - Still verify final `puda machine state stage` is `idle` / `run_id: null` on the endpoint that handled the command.
5. If the user asks to stop during an approach or move chain, kill the tracked process first, then run cleanup: SMU outputs off, abort measurements, 707B open/nil, light off, stage abort, and final states.

## Concrete pattern

```bash
# State/protocol against the endpoint the stage edge actually joined.
puda --nats-servers nats://bears:4222 machine state stage
puda protocol run --file /tmp/stage_z_up.json --nats-servers nats://bears:4222

# Then read back separately, not as a second command in the same motion protocol.
puda protocol run --file /tmp/stage_get_position.json --nats-servers nats://bears:4222
```

This is not a reason to abandon protocol-first control; it is an endpoint-alignment and verification issue.
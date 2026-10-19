# Live instrument-audit evidence and probe selection

## Evidence hierarchy

Use the strongest available layer and report weaker layers separately:

1. **Direct hardware readback:** identity, output state, routes, error queue, encoder/position, or serial state.
2. **Harmless command response:** proves edge and transport; a structured `UNKNOWN_COMMAND` proves only those layers.
3. **Fresh heartbeat/discovery:** useful inventory evidence, but not authoritative when direct probes disagree.
4. **Cached state/catalog:** historical unless timestamped current.
5. **Process existence:** proves neither transport nor hardware access.

## Partial NATS recovery

A cluster can partially recover while some configured peers still time out or heartbeat discovery omits live edges. Do not declare instruments dead and do not wait indefinitely for every expected machine name.

- Probe only required edges with bounded harmless calls.
- For electrical readiness require output OFF, matrix open, acceptable errors, intended driver/capabilities, and no unresolved UNKNOWN exposure.
- For motion readiness require persisted/live position, no pending move, and a responsive motion edge.
- Continue when the operation-specific direct gate passes even if discovery remains incomplete.
- Do not restart local NATS merely because remote peers or discovery are incomplete.

## Duplicate-edge diagnosis

Count independent parents/CWDs, not Python children. One `uv run main.py` parent plus its Python child is one edge.

Conflicting START replies (`RUN_ID_MISMATCH` plus success for the same run ID) can result from command redelivery after transport recovery. They do not prove duplicate edges. Correlate raw replies by machine, run ID, command, and timestamp, then inspect process topology. If only one edge exists and stale run state persists, restart only that affected edge and repeat the direct safety gate.

## Probe examples

- SMU: identity, output state, terminals, error queue; never source stress for liveness.
- Matrix: `open_all`, then explicit closed-channel readback.
- Motion: encoder/current position or persisted confirmed position with `pending_command=null`.
- Light/auxiliary serial edge: harmless OFF or status call; if status methods are restricted, combine structured response with serial-FD evidence.
- Destructive error queues: preserve the first read, then re-read to decide whether the error persists.

## Reporting classes

Use: `healthy`, `alive-but-degraded`, `edge-alive/hardware-unverified`, `offline`, or `unsafe/UNKNOWN`. State the exact evidence and timestamp; do not compress process, transport, hardware, safety, and exclusivity into one binary claim.

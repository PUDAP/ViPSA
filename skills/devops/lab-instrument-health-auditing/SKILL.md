---
name: lab-instrument-health-auditing
description: "Use when checking whether lab instruments are alive."
version: 1.0.0
metadata:
  hermes:
    tags: [instrumentation, health-check, edge, nats, usb, serial]
    related_skills: [puda-operations, network-connectivity-diagnostics, native-instrument-acquisition-recovery]
---

# Lab Instrument Health Auditing

Use this class-level skill to answer whether an instrument fleet is alive, reachable, safe, and ready. Do not collapse process, edge, transport, and hardware health into one binary claim.

## Health layers

Audit each layer independently:

1. **Process:** expected edge process exists with the intended executable, CWD, parent tree, and start time.
2. **Transport:** the edge answers a bounded live request on the intended broker/endpoint.
3. **Hardware:** the driver returns direct identity/state/readback from the physical instrument.
4. **Safety:** outputs, routes, errors, motion state, and UNKNOWN exposure are acceptable.
5. **Exclusivity:** no duplicate edge instance can race for the same hardware or durable consumer.

## Workflow

1. Identify the expected machine inventory and intended environment/cluster.
2. Query live discovery with the endpoint selected explicitly.
3. Treat cached/offline state as historical until its timestamp is shown current.
4. Issue harmless live probes through the normal command path.
5. Verify USB/serial attachment when direct readback is restricted or ambiguous.
6. Inspect process topology for duplicate independent parents, not just child processes.
7. Recheck destructive error queues after the first read drains them.
8. Report each machine as healthy, alive-but-degraded, edge-alive/hardware-unverified, offline, or unsafe/UNKNOWN.

## Core rules

- A configured machine or cached command catalog is not evidence of liveness.
- Process existence is not hardware proof.
- A prompt structured `UNKNOWN_COMMAND` response proves edge/transport liveness, not device usability.
- Heartbeat discovery can omit an edge that still answers commands; escalate to a harmless live probe before declaring it offline.
- Error queues are often destructive reads. Preserve the first result and perform a second read before deciding whether the condition persists.
- An orchestration parent plus its Python child is one edge instance; two independent parents for one machine are duplicate instances.
- Never use a stress-producing command merely to test liveness.
- Include electrical safety readbacks (`output OFF`, matrix open, acceptable errors) whenever relevant.

## Output

Return a compact machine table with evidence and caveats. Call out stale timestamps, duplicate processes, restricted probes, and unresolved UNKNOWN state explicitly.

See `references/live-audit-evidence-and-probes.md` for probe selection, interpretation, and reporting examples.

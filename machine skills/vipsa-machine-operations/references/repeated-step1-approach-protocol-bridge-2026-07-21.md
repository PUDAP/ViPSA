# Repeated step-size-1 contact approach through the PUDA latency bridge (2026-07-21)

## Context

After camera-pad alignment completed but an earlier combined run was interrupted before electrical approach began, the user requested two consecutive Keithley-guided approaches with `step_size=1`.

Established parameters were retained:

- read voltage: `0.01 V`
- contact window: `1e-8..1e-7 A`
- read compliance: `1e-6 A`
- forward direction: `+Z`
- coarse step: `+1.0 Z`
- bounded budget: 100 moves per request
- final trim minimum: `0.25 Z`

## Reusable execution pattern

1. Start the short-lived PUDA NATS latency bridge and use `nats://127.0.0.1:54222` for both state checks and every one-command protocol:
   ```bash
   python3 ~/.hermes/skills/devops/vipsa-machine-operations/scripts/nats-latency-proxy.py \
     --remote-host 100.109.131.12 --remote-port 4222 --local-port 54222
   ```
2. Inspect `light`, `keithley-2450`, `keithley-707b`, and `stage` before motion. If the electrical machines carry stale non-null run IDs, reset them and then re-read state. A reset may time out while still successfully returning the machine to `idle`, `run_id: null`; trust the fresh state read, not only the reset command exit.
3. Use an outer Python orchestrator that creates full-metadata one-command PUDA protocols. Turn lights off, force Keithley output off, route the 707B to Keithley, then alternate one live current read and one `stage.move_z_by(+1.0)`.
4. Treat a later terse “try approach again, with 1 step” as a new bounded continuation from the verified current Stage-Z position. Do not reset Stage-Z or repeat earlier moves; re-read live current and give the new request its own 100-move budget.
5. Stop honestly as `no_contact_after_max` if all reads stay below threshold. Do not run DCIV or infer contact merely because cumulative tracked Z travel is large.
6. After every bounded attempt, force Keithley output off, call 707B `open_all`, require `get_closed_channels == nil`, verify all involved machines `idle` with `run_id: null`, and stop the latency bridge.

## Observed outcome

- First bounded run: 100 × `+1 Z`, current remained about `12–19 pA`, final tracked stage position `[0, 0, 100]`, no contact.
- Second bounded continuation: another 100 × `+1 Z`, current remained about `12–15 pA`, final tracked stage position `[0, 0, 200]`, no contact.
- Both runs completed cleanup with Keithley output off, 707B channels `nil`, lights off, and all four machines idle with null run IDs.

These values are session-specific. The durable lesson is to preserve cumulative Z readback across retries, bound each user-authorized continuation separately, and report persistent pA current as open/very-high-resistance-like rather than contact.

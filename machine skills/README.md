# ViPSA Machine Skills

This directory contains the operational skill stack used for ViPSA machine control, measurement, recovery, and autonomous campaigns.

## Core ViPSA operations

- `vipsa-machine-operations` — PUDA-connected SMUs, switch matrix, lights, Stage, Zaber, lifecycle, cleanup, and recovery.
- `vipsa-device-grid-navigation` — absolute/relative device navigation with safe clearance and readback.
- `vipsa-grid-measurement` — multi-device traversal, alignment, approach, measurement, and per-device records.
- `vipsa-motion-validation` — integrated motion calibration, bounds, readback, and uncertainty handling.
- `vipsa-image-capture` — Camera 1/2 capture with controlled illumination state.
- `vipsa-vision-alignment` — probe-tip/pad detection, phase correlation, and bounded Zaber corrections.
- `vipsa-electrical-measurements` — DCIV, pulses, resistance checks, forming, endurance, analysis, and plotting.
- `vipsa-device-failure-prevention-recovery` — device failure modes, prevention, recovery, and recurrence records.
- `vipsa-system-validation` — integrated ViPSA benchmarking and release/publication validation.

## Campaign and recovery

- `adaptive-dciv-campaign-operations` — crash-safe adaptive campaigns, ledgers, caps, failure rules, and no-replay recovery.
- `instrument-campaign-resilience` — durable long-running instrument campaigns.
- `lab-instrument-health-auditing` — edge/instrument health and command-readiness checks.
- `lab-instrument-run-recovery` — interrupted-run reconciliation and defensible resume boundaries.
- `native-instrument-acquisition-recovery` — native acquisition, trace-buffer, and post-dispatch recovery.
- `puda-operations` — PUDA CLI, environment, edge, NATS, and machine lifecycle operations.

Each skill is self-contained under its own directory. Start with that directory's `SKILL.md`; supporting material is under `references/`, `scripts/`, `templates/`, or `assets/` where present.

## Safety posture

These skills are intentionally fail-closed. They preserve durable motion/electrical intent, require hardware readback, avoid automatic replay after uncertain exposure, and verify output-OFF plus matrix-open cleanup before progression.

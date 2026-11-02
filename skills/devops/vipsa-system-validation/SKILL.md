---
name: vipsa-system-validation
description: "Use when benchmarking ViPSA for publication or release."
version: 1.0.0
metadata:
  hermes:
    tags: [vipsa, validation, calibration, benchmarking, publication]
    related_skills: [vipsa-machine-operations, vipsa-vision-alignment, vipsa-electrical-measurements, puda-operations]
---

# ViPSA System Validation

Use this class-level skill to design, execute, analyze, and report evidence for ViPSA platform claims. It covers motion calibration, quantitative vision/alignment, contact reliability and damage, electrical integrity/noise, campaign throughput/reliability, environmental characterization, and PUDA agentic demonstrations.

## Required companion skills

Load the operational skill for every subsystem touched. In particular, use `vipsa-machine-operations` and `puda-operations` before hardware side effects, `vipsa-vision-alignment` for camera workflows, and `vipsa-electrical-measurements` for SMU/contact data. Validation does not relax their safety or cleanup rules.

## Evidence hierarchy

Keep these distinct in every dataset and report:

1. commanded operation;
2. driver/controller readback;
3. independent physical measurement;
4. optical or electrical corroboration;
5. unverified assumption.

A successful command is not proof of physical motion, contact, alignment, or calibrated displacement. Use independent references and retain raw artifacts.

## Validation workflow

1. Translate each manuscript/platform claim into a measurable quantity and acceptance criterion.
2. Inventory independent standards, calibration targets, reference devices, sensors, and raw historical logs.
3. Preflight live machine identity/state, physical clearance, safety limits, and data paths.
4. Define repeats, randomized or balanced order, environmental metadata, exclusions, and failure categories before collecting data.
5. Execute through PUDA/validated driver methods, preserving exact axis signs and units.
6. Save raw measurements, images, commands, readbacks, timestamps, validity flags, and cleanup verification.
7. Analyze programmatically; report distributions and failures, not only successful averages.
8. Verify final machine cleanup and manuscript table/figure traceability.

## Validation domains

### Motion

Use independent displacement metrology. Camera 1 plus a stage micrometer/grid supports X/Y; absolute OpenFlexure Z normally needs a dial indicator, displacement sensor, or calibrated side view. After a Stage-edge restart, `[0,0,0]` is a run-local tracked origin, not a verified physical origin. See `references/publication-grade-motion-calibration.md`.

### Vision and alignment

Calibrate object-plane pixel scale, create manually annotated ground truth, and benchmark probe-tip/pad localization plus final residual across pad sizes, holder positions, illumination, glare, occlusion, and missing-device cases. Target the actual visible probe tip, not frame centre. Preserve before/after overlays.

### Contact

Compare conductive references, representative high-resistance devices, and lifted-probe/open baselines. Quantify success, false contact, approach travel, repeatability, damage, and wear. Do not classify pristine HRS devices as open from pA/GΩ magnitude alone; use reproducible bias dependence and baseline comparison.

### Electrical integrity

Measure open, short, reference resistors, route leakage, instrument agreement, shielding, lighting, motion, settling, and noise. Test the assembled path rather than quoting SMU specifications.

### Throughput and reliability

Extract attempted/successful devices, failure categories, interventions, faults, replacements, unattended duration, and per-phase timing from raw campaign artifacts. Declared totals must reconcile programmatically.

### Environment

When enclosure performance is claimed, log sample-adjacent humidity, oxygen, and temperature versus purge time and experiment duration. Describe purgeable systems as purgeable unless hermetic performance is independently established.

### PUDA agentic demonstration

Use a predefined end-to-end task and one or more safe failure cases. Record success, tool calls, time, interventions, recovery, interlock activations, and cleanup. Verify deterministic limits cannot be bypassed.

## Outputs

Prefer auditable CSV/JSON plus raw images/logs. Use scatter-only plots for device-level and calibration-point results unless another representation is explicitly requested. Each manuscript metric must link to its source artifact and analysis code.

## Pitfalls

- Treating manufacturer specifications as integrated-system validation.
- Treating software coordinates as physical ground truth.
- Calibrating absolute Z from a top-down image without a defensible axial model/reference.
- Hiding failed trials or excluding them after seeing results.
- Moving Stage X/Y without explicit authorization.
- Losing units, signs, camera settings, or environmental metadata.
- Reporting cleanup based on intent rather than verified final state.

## Verification checklist

- [ ] Every central claim has a measured metric and acceptance criterion.
- [ ] Independent standards and traceability are documented.
- [ ] Raw data and exclusions are preserved.
- [ ] Commanded, readback, and independently measured values are separated.
- [ ] Counts and totals reconcile programmatically.
- [ ] Final machine state and cleanup are verified.
- [ ] Manuscript tables/figures can be regenerated from saved artifacts.

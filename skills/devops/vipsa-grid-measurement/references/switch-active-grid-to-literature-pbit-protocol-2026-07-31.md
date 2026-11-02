# Switching an active ViPSA grid to the literature p-bit protocol at a subsequent-device boundary (2026-07-31)

## Trigger
Use when the user changes an active/current grid run from a prior electrical protocol to the literature-derived p-bit protocol for **subsequent devices**.

## Procedure
1. Stop the active grid runner and pause its per-device reporter.
2. Verify no child Python/`uv run`/`tee` runner processes remain.
3. Run full cleanup before launching the continuation:
   - Keithley output off
   - Keysight output off
   - 707B `open_all()` and `get_closed_channels == nil`
   - lights off
   - stage abort/readback if interrupted during/after alignment
   - all six ViPSA machines `idle/run_id:null`
4. Inspect the old run log and current device summary to identify the exact restart boundary. In this case, the old runner had completed through device 27 and was interrupted at device 26 **after alignment only**: `summary.json` still had `status: started` and no contact-gate/DCIV/pulse results.
5. Preserve earlier device summaries as previous-protocol records; do not claim they used the new protocol.
6. Create a new continuation run folder and start at the interrupted/subsequent device boundary, reusing the current physical position only when the old runner had already moved/aligned/pre-approached that exact device. Later devices follow normal grid travel: cleanup → `stage.move_z_by(-50)` → absolute Zaber X/Y → vision alignment → `stage.move_z_by(+40)` → approach/contact gate.
7. Create a new reporter for the new run and pause the old one to avoid stale duplicate messages.

## Literature p-bit per-device protocol used
- Dark setup and cleanup.
- Mechanical approach first, then literature contact gate.
- Contact gate: Keithley reads at `0 V, +10 mV, -10 mV, +50 mV, -50 mV`, 3 reads per voltage, `1 µA` compliance, ~0.2 s settle.
- Classify:
  - compliance-limited low-bias -> `short_like_or_overcontact_read_compliance`, skip p-bit train
  - pA/sub-nA/no voltage scaling -> `open_weak_no_voltage_scaling`, skip p-bit train
  - nA-scale or voltage-scaled and not compliance-limited -> candidate
- Candidate DCIV: `0 -> +0.8 -> 0 -> -1.0 -> 0 V`, 50 mV step, `+1 µA` SET-side compliance, `10 µA` reset-side compliance.
- Post-DCIV health check; skip long p-bit train if read-compliance-limited/short-like.
- Pulse train for candidates: `RESET -> READ_RESET -> SET(random V_SET) -> READ_SET`, `V_READ=+0.1 V`, `V_SET=0.20..1.00 V` in 0.05 V steps, 20 attempts/level, `V_RESET=-1.0 V` or `-2.0 V` fallback if DCIV SET without RESET, pulse width 10 ms, compliance 10 µA.
- Analysis: threshold read distributions, compute `P(1|V_SET)`, entropy, sigmoid fit, compliance/stuck flags.

## Artifact/status rule
A killed runner may leave an interrupted device with only `started`, alignment, or pre-approach artifacts. Treat `summary.json` status and measurement keys as authoritative. Do not let `DONE.json`/plots alone cause the continuation to skip a device whose new-protocol contact gate/DCIV/pulses have not actually run.

# 8×8 current-origin grid: align → approach → forming DCIV → randomized sigmoid pulses (2026-06-22)

## Context

User requested a grid-wise ViPSA measurement from the current device:

- Grid shape: `8 × 8` from current Zaber position.
- Native Zaber spacing: `x_step = 5000`, `y_step = 5000`.
- Per-device sequence: optical align → Keithley contact approach → DCIV for forming → randomized pulse measurement to get a sigmoid switching-probability curve.
- Tweakable parameters: approach contact window, DCIV compliance/voltage/points, randomized pulse voltage range.
- Pulse rule: stop after every `100` pulses to analyze whether the device is still in good condition and switching; do **not** run a separate health check during pulsing.

## Durable workflow pattern

1. Preflight `bears` ViPSA machines (`keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, `zaber`) and verify idle/null run IDs before launch.
2. Treat the current Zaber readback as device 1 origin. Generate row-major device numbering but physically traverse serpentine.
3. For an `8×8`, `5000` native-unit grid:
   ```python
   for row in range(8):
       for col in range(8):
           device_number = row * 8 + col + 1
           x = origin_x + col * 5000
           y = origin_y + row * 5000
   ```
4. Use a tracked background process for the full grid run and report the `process` session ID plus run folder immediately, since the run is long.
5. Per device:
   - Cleanup electrical outputs/routes before travel or stress.
   - Safe microscope-stage Z retract before Zaber X/Y travel, then partial pre-approach lower.
   - Camera-1 dark-pad alignment with lights on only during align, then lights off.
   - Keithley contact approach using the established `10–100 nA at 10 mV` window unless user overrides.
   - If weak/open contact in a grid run and not short/over-current: apply the existing `+1 Z` override and continue measurements rather than skipping.
   - Forming DCIV with conservative defaults tuned from recent failures: `0→+1.0→0→-1.5→0 V`, `0.05 V` step, `+1 µA` SET-side compliance, `10 µA` RESET-side compliance.
   - Then run randomized SET-voltage pulse probability measurement.
6. Randomized pulse sigmoid default used for this class of run:
   - SET voltages `0.30..1.10 V` in `0.10 V` steps.
   - `10` randomized repeats per SET voltage.
   - Trial shape: `SET`, `read_after_set`, `RESET`, `read_after_reset`.
   - Read voltage `+0.1 V`, reset `-1.5 V`, pulse width `5 ms`, compliance `10 µA`.
   - Generate `randomized_pulse_plan.csv` before hardware execution.
   - Execute in chunks/checkpoints of `100` pulses.
   - After each checkpoint, analyze read currents already collected: max read current, median read-after-SET/RESET, ROC/Youden threshold, per-voltage probability table. Stop if low-voltage read current approaches compliance (e.g. `>= 9 µA` with `10 µA` compliance), indicating likely short/over-contact.
   - Do not insert a separate Keithley health check between pulse chunks unless the user asks; the pulse read data is the condition check for this workflow.
7. Plot per-device summary with: DCIV log `|I|`, approach reads vs net Z, randomized pulse read currents, and switching probability vs SET voltage.

## Implementation pitfall

When parsing SMU pulse responses, do not double-count aliases such as both `I_meas (A)` and `Current (A)` from the same reading object. Prefer one current field per reading in priority order:

1. `I_meas (A)`
2. `Current (A)`
3. `current_A`
4. `current`
5. `I`

If parsed current count is exactly double the expected pulse-row count, suspect alias double-counting before rerunning hardware.

## Reporting

Initial report should be concise and operational:

- Grid shape/spacing/traversal.
- Per-device sequence and key parameter choices.
- Process session ID.
- Run folder.
- Origin Zaber readback.
- State that machines were preflighted idle before launch.

Do not spam per-approach-step updates; report device-level completion, blockers, and plots/artifacts.
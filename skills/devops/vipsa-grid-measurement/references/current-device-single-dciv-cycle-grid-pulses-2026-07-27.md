# Current-device approach + one DCIV cycle + grid randomized pulses (2026-07-27)

## Trigger

Use this pattern when the user asks to **approach the current device** and then run the same grid measurement electrical sequence, but explicitly limits DCIV to **one cycle** and says not to run extra reset sweeps.

Example wording:

> approach the current device, and run the test protocol of 1 DCIV cycle and then randomized pulses, identical to what is used during the grid measurement. Do not run additional sweeps for reset

## Procedure

1. Treat the **live/current device** as the target. Do not infer a different device from stale folders.
2. Turn lights off before electrical routing.
3. Approach using the current grid contact window and stability rule.
   - For this S9 narrow-window workflow, target `1–10 nA` at `10 mV` with three stable reads.
   - If the first in-window read is not stable because subsequent reads dip just below threshold, continue from current Z with minimum valid `+0.25` steps; do **not** insert a gross retract between retries.
4. When stable contact is confirmed, run **exactly one DCIV cycle** matching the grid’s first cycle:
   - `0 -> +0.6 -> 0 -> -0.75 -> 0 V`
   - `0.05 V` steps
   - SET-side compliance `1e-5 A`
   - RESET-side compliance `1e-4 A`
   - include low-bias read after SET and after the single RESET branch if the grid DCIV helper normally does so.
5. Do **not** use the grid helper’s sequential DCIV reset ladder (`-1.0`, `-1.25`, `-1.5`, etc.) when the user explicitly forbids additional reset sweeps. Patch/override the DCIV function for this run so only the first negative branch is generated.
6. After that one DCIV cycle, run the grid randomized pulse function unchanged unless the user also changed pulse logic.
   - If the one DCIV cycle detects SET without RESET, the existing grid pulse branch may run exactly five strongest `RESET -> read` fallback pairs before randomized pulses. This is pulse-protocol fallback, not an additional DCIV sweep; label it clearly.
7. Cleanup after DCIV and after pulses: SMU outputs off, 707B `open_all`, verify `get_closed_channels == nil`, lights off, machine states idle/null.

## Pitfalls

- The S9 grid runner’s `dciv()` function escalates reset DCIV branches until proper reset is observed. That is **not** allowed when the user says “1 DCIV cycle” / “Do not run additional sweeps for reset.” Override it with a single-cycle DCIV builder.
- The grid `randomized_sigmoid_pulse()` helper seeds randomness with `int(devdir.name.split('_')[-1])`. For current-device or descriptive folders, use a numeric device directory such as `device_07`, pass an explicit device number, or patch the helper; otherwise it fails on folder suffixes like `current_device` or `protocol`.
- Distinguish the two reset concepts in the final report:
  - forbidden: extra **DCIV reset sweeps** after the first cycle;
  - allowed by grid pulse logic unless the user forbids it separately: five strongest `RESET -> read` pulse fallback pairs when DCIV SET is seen but RESET is not.
- If a helper fails before hardware stress because of script/runtime setup, cleanup and retry with the known-good interpreter/environment rather than rerunning already-completed DCIV. Do not rerun hardware just to repair post-DCIV pulse orchestration.

## Concrete session outcome

A current-device run reached stable approach at `~1.0–1.5 nA` and stage `z=-20.75`, ran exactly one 57-point DCIV cycle with max current `~1e-5 A`, SET detected and RESET not detected, then ran the grid randomized pulse branch. The pulse branch executed five `-2.0 V RESET -> read` fallback pairs, collected 200 randomized pulses / 50 trains, and stopped at `reset_not_achieved_at_-2.0V_after_two_chunks`. Cleanup verified Keithley/Keysight outputs off, 707B `nil`, lights off, machines idle/null.
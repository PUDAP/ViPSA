# Bounded contact approach with over-current recovery and step/current plot (2026-07-24)

## When to use

Use this pattern when a ViPSA device is open-like after coarse positioning or pre-approach and the user asks to `approach`.

## Proven workflow

1. Preflight-check that the stage, Keithley 2450, and 707B are idle and no competing approach/grid/pulse runner is active.
2. Keep illumination off unless the user has explicitly latched it on.
3. Route the DUT to the Keithley and read at `10 mV` with `1 µA` compliance.
4. Approach in bounded `+0.5 Z` increments toward the user-standard `50–500 nA` contact window.
5. If the read exceeds `500 nA` or reaches the `1 µA` read compliance, stop forward motion immediately and enter guarded retraction.
6. Retract in small steps, re-reading after each step. If the transition is steep, use final `±0.25 Z` guard trims to land inside the target window.
7. Finish with Keithley output off, 707B `open_all`, closed channels `nil`, light off by default, and machine states idle with cleared run IDs.

## Session result

Artifact directory:

`/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/approach_current_device_50_500na_20260724T115346Z/`

- Initial stage Z: `43.25`
- Initial current: about `25 pA` at `10 mV`
- Forward approach crossed abruptly into the `1 µA` compliance-limited region.
- Automatic guarded retraction and final trim recovered the target window.
- Final current: `187.537 nA` at `10 mV`
- Final stage Z: `70.5`
- Net commanded Z displacement: `+27.25 steps`
- Final status: `in_window_after_final_guard`
- Cleanup and idle-state verification succeeded.

## Progress reporting pitfall

Long-running Python runners may buffer stdout. Do not infer that a silent process is stalled. Check the tracked process status and inspect the newest per-read output artifact. Count actual move files separately from read files: the initial read occurs before the first move, and retract/fine/guard phases use separate filenames.

When reporting mid-run state, state the phase explicitly (`forward`, `retract`, `fine`, or `final guard`) and distinguish:

- total read count,
- number and size of commanded moves,
- cumulative net Z displacement,
- latest current,
- target window and compliance threshold.

## Step-versus-current visualization

After completion, reconstruct cumulative net Z from the ordered approach log:

- add each `move_z.height` to cumulative Z,
- assign the current cumulative Z to each subsequent read,
- plot `net commanded Z displacement` versus `|current| at 10 mV`,
- use a logarithmic current axis,
- use scatter markers only,
- color forward/retract/fine/final-guard phases separately,
- shade the `50–500 nA` target band,
- mark the `1 µA` compliance threshold,
- save both PNG and CSV in the run directory.

Do not plot read index as though it were Z displacement; retraction and extra-retraction steps make that misleading.

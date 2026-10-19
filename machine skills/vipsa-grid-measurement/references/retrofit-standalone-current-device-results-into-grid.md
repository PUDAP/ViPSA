# Retrofitting standalone current-device results into an ongoing grid run

Use when the user runs standalone approach/DCIV/pulse measurements at the current physical position, then says to save those results as a specific/nearest grid device and continue the grid from the next device.

## Pattern from S9 device 15 continuation (2026-07-27)

1. **Identify the physical grid device from live X/Y first.**
   - Query Zaber with `zaber.get_current_position(units=None)` through PUDA.
   - Compare live `(x,y)` against the authoritative substrate `grid_positions.csv` and report the nearest device and offset.
   - In the S9 case, live `(266713, 495997)` was closest to device 15 target `(266765, 496131)`, offset `dx=-52`, `dy=-134`, distance `~144` native units.

2. **Archive stale canonical folders before overwriting.**
   - If `device_N/` already exists but contains stale skipped/partial data, move it under an archive directory before writing the standalone result.
   - Also archive any stale next-device partial folder that would otherwise confuse continuation, e.g. a previous `device_16/summary.json` saying `stopped_after_alignment_before_approach`.
   - Do not rely on deleting only run-level summary entries; stale `DONE.json` or partial folders can cause later runners/reporters to skip or misreport.

3. **Normalize standalone artifacts into the grid device folder.**
   - Copy DCIV rows to grid-compatible names such as `device_N/dciv.csv`, plus `dciv.json` with compact metrics (`points`, SET/RESET detection, max current, compliance hits, source path note).
   - Copy pulse artifacts to `randomized_pulse_results.csv`, `randomized_pulse_plan.csv`, `switching_probability.csv`, and `randomized_pulse_summary.json`.
   - Preserve original standalone summaries as `standalone_dciv_summary.json` / `standalone_randomized_pulse_summary.json` so future analysis can see protocol differences.
   - If the standalone protocol differs from the grid protocol, state this explicitly in `summary.json` (e.g. standalone DCIV used `0→+1→0→-2→0 V`, while the grid runner normally uses one shorter cycle).

4. **Write a canonical per-device summary and DONE sentinel.**
   - `summary.json` should mark `status: completed`, include target row/col/x/y, live Zaber readback/offset used to identify the device, source artifact directories, compact DCIV and pulse metrics, and cleanup verification.
   - Generate/verify `device_plot.png` from the saved CSV/JSON.
   - Write `DONE.json` only after the canonical summary and plot exist.

5. **Patch run-level summaries before continuation.**
   - Update both `summary.partial.json` and `summary.json` to include the completed device record and remove stale entries for the overwritten/current-next devices.
   - Preserve completed devices before the boundary.
   - Record a note like `device15_manual_result_note` explaining that standalone results were intentionally assigned to the grid device.

6. **Continue from the next serpentine device, not the saved device.**
   - Compute the next device using the grid’s serpentine traversal order; after S9 device 15, the next device was 16.
   - Clone/patch the continuation runner with `START_DEVICE=<next_device>` and local/current NATS settings as needed.
   - Verify the cloned runner compiles before launch.
   - Start it as a tracked background process and set up/verify a per-device reporter keyed to the run directory and device number.

## Reporting

Report three concrete facts before saying the continuation is started:

- The canonical `device_N` directory and key artifacts saved.
- Any stale folders archived.
- Background runner session/log path and latest observed event for the next device.

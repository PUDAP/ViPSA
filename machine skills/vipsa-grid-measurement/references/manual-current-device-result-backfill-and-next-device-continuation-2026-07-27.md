# Manual current-device result backfill and next-device continuation (2026-07-27)

## Trigger

Use this pattern when standalone measurements were run on the physically current device, then the user asks to save those artifacts as a specific grid device and continue the grid from the next device. Example: live Zaber position was closest to S9 device 15, standalone DCIV + randomized pulses had already completed, and the user said device 15 was already probed and to continue the S9 grid from the next device.

## Workflow

1. **Reconcile physical identity first**
   - Query live Zaber `get_current_position(units=None)` through PUDA.
   - Compare the live X/Y to the substrate `grid_positions.csv` and identify the closest device by Euclidean distance.
   - Report the offset from the target so the handoff is explicit.

2. **Save standalone results as canonical device folder**
   - Create/update `device_N/summary.json` with `status: completed` and a clear `manual_save_note` explaining that standalone artifacts were assigned to the grid device by user request.
   - Copy/normalize key artifacts into the grid device folder using normal grid names when possible:
     - `dciv.csv`, `dciv.json`, DCIV plots
     - `randomized_pulse_results.csv`, `randomized_pulse_plan.csv`, `switching_probability.csv`, `randomized_pulse_summary.json`, pulse plot
     - `DONE.json`
   - Preserve the source standalone run directories in `source_artifacts`.
   - Record when protocol shapes differ from the grid default, e.g. standalone DCIV path `0 -> +1 -> 0 -> -2 -> 0 V` versus a grid one-cycle DCIV `0 -> +0.6 -> 0 -> -0.75 -> 0`.

3. **Archive stale canonical folders before overwrite**
   - If `device_N` or the next-device partial folder already exists from an earlier failed/skipped run, move them under an archive directory before writing the manual result.
   - Do not merely prune `summary.partial.json`; stale `DONE.json` or partial `summary.json` can cause later runners/reporters to skip or misreport devices.

4. **Patch run-level summaries**
   - Update both `summary.partial.json` and `summary.json` when present.
   - Preserve pre-boundary completed devices and replace only the current manual device and stale next-device partial.
   - Include a note such as: `device N manually saved; continuation resumes from serpentine next device M`.

5. **Continue from the next serpentine device**
   - Compute the next device from the saved grid traversal order (serpentine), not from naive numeric order unless equivalent.
   - Clone/patch the runner with `START_DEVICE=<next_device>`.
   - Preserve the manually saved device in the new run-level `SUMMARY['devices']` before appending new results.
   - Force explicit local/known-good NATS override when project config may still point at stale `bears`.
   - Compile the runner before launch.

6. **Per-device reporting**
   - If the user wants updates/plots after every measurement, install or verify a no-agent reporter that watches `device_*/DONE.json`, parses `summary.json`, and attaches `device_plot.png` if it exists.
   - Pause that reporter on stop.

## Stop/cleanup follow-up

When a continuation is stopped mid-device:

- Kill the tracked process and verify no orphan runner remains.
- Pause the reporter.
- Run electrical cleanup: Keithley output off, Keysight output off, 707B `open_all` + `get_closed_channels`, light off.
- If `stage` is `idle` but has a stale non-null `run_id` or enters `error` after reset, run a harmless full-metadata protocol with `stage.abort_motion()` then `stage.get_current_position()`; verify `stage` returns `idle/run_id:null`.
- Mark the interrupted device summary with a status such as `stopped_after_first_approach_no_contact`, include the last runner event, and explicitly state that no DCIV/pulses were run if they were not.

## Pitfalls

- Do not infer the physical device from stale conversation state or the newest partial folder; use live Zaber + grid CSV.
- Do not leave stale `device_N/DONE.json` in place when the user explicitly wants the current standalone result to become canonical.
- Do not restart from the saved device again if the user says it is already probed; start from the next serpentine device.
- Do not claim cleanup is safe until outputs/routes/lights and machine states are actually verified.

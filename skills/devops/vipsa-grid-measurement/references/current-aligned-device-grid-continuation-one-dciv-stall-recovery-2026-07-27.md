# Current aligned-device grid continuation with one DCIV and stall/pause recovery (2026-07-27)

Use this reference when the user has manually moved/retracted/aligned a ViPSA grid device and then asks to continue the grid from this device onward with `approach -> 1 DCIV -> randomized pulse measurement`.

## Boundary and live-device handling

- Identify the boundary from live Zaber X/Y plus the grid map, not from the newest partial folder.
- If the current device has just been aligned manually/optically, preserve the aligned XY offset for the first boundary device; do **not** snap back to nominal `grid_positions.csv` X/Y.
- For the first boundary device, avoid generic travel/pre-approach moves that undo the user's intentional Z state. Run cleanup, lights off, low-bias approach, then measurement.
- For subsequent devices, use normal grid travel: cleanup -> safe Z retract -> absolute Zaber X/Y -> pre-approach lower -> vision alignment -> approach -> measurement.
- Remember serpentine order: for an S9 7×7 row-major map, continuing from device 8 starts `8, 15, 16, 17, ...`, not numeric `8, 9, 10, ...`.

## If the user says “restart the grid measurement; start with aligning the current device”

1. Verify no old runner remains and all machines are idle/null or clean them first.
2. Run standalone current-device alignment first with the canonical `tools/align.py --execute` workflow and attach the final annotated image.
3. Record the final residual pixel offset and final Zaber readback.
4. Launch the grid runner only after alignment is verified.
5. In the fresh runner/run summary, mark the first device as externally/currently aligned; skip duplicate first-device vision alignment but still perform electrical approach.
6. Start a fresh output folder for the restart so old paused/stalled `device_08` artifacts cannot masquerade as new progress.

## Electrical sequence for this request class

- Treat `1 DCIV` literally: run exactly one cycle such as `0 -> +0.6 -> 0 -> -0.75 -> 0` at the configured grid step/compliances.
- Do not run the grid DCIV reset ladder as extra DCIV cycles when the user asked for one DCIV.
- It is still valid for the randomized-pulse helper to run its documented five `RESET -> read` fallback pairs after a DCIV SET-without-RESET result; report this as pulse-helper fallback, not extra DCIV.
- Gate stress on the active contact policy. For this user's current S9 grid policy, require three stable `1-10 nA @ 10 mV` reads after bounded attempts; if the gate fails, skip DCIV/pulses for that device and continue or pause as requested.

## Runner design lessons

- Prefer a fresh output directory for every restarted continuation so stale `DONE.json`/partial artifacts cannot silently skip the boundary device.
- Create `summary.partial.json` with traversal order before launch and verify a fresh `device_N/summary.json` appears for the boundary.
- Use a tracked background process with `notify_on_complete=true`; send concise startup status with process id and run folder.
- If the plotting environment lacks pandas/matplotlib but electrical execution uses a different venv, keep hardware running in the NATS-capable venv and force plotting through the known plotting venv with `MPLBACKEND=Agg`.

## Pause/stop recovery

When pausing a current grid continuation:

1. Kill the tracked process and verify no matching runner process remains.
2. Reconcile the runner log with device artifacts; `DONE.json` is not proof of electrical completion.
3. Run explicit cleanup, not just process kill:
   - `stage.abort_motion()` if approach/stage motion may have been active.
   - `stage.get_current_position()` for the final Z.
   - `keithley-2450.set_output(false)`.
   - `keysight-b2902b.set_output(false)`.
   - `keithley-707b.open_all()` and `get_closed_channels()`; require `nil`.
   - `light.turn_off()`.
4. Verify all six machines are `idle` with `run_id=null`.
5. Mark the run and current `device_##/summary.json` as paused/interrupted, preserving the exact highest phase reached and recording the cleanup summary path.
   - If the runner log shows `after_align` but no approach artifact, use a status like `stopped_after_alignment_before_approach` and explicitly report that approach/DCIV/pulses did not start.
   - If approach artifacts exist but no DCIV/pulse artifacts, preserve them and report the final approach status/current without calling the device electrically tested.
6. If only alignment/approach artifacts exist and no `dciv.csv` / `randomized_pulse_results.csv`, report that no electrical stress sequence started.

## Stage/NATS stall recovery pattern

A continuation can stall with a machine state such as `stage: busy, run_id=<uuid>` while the Python runner prints no progress beyond `device_start`. If that happens:

1. Poll the tracked process and read the boundary `summary.json` to see whether any approach data was written.
2. Check six machine states with short timeouts.
3. Kill the tracked runner if it is stuck before electrical stress has started.
4. Do **not** use unsupported CLI verbs such as `puda machine reset stage` if the CLI rejects them.
5. Recover through PUDA commands: `stage.abort_motion`, `stage.get_current_position`, `keithley-2450.set_output(false)`, `keysight-b2902b.set_output(false)`, `keithley-707b.open_all`, `keithley-707b.get_closed_channels`, and `light.turn_off`.
6. Verify all machines are `idle` with `run_id=null` before restarting.
7. Restart into a new run folder or archive the stalled folder so stale boundary artifacts do not confuse the continuation.

## Reporting

- For startup: report boundary device, traversal order head, alignment residual if just aligned, sequence, process id, and run folder.
- For each completed device: report approach status/current, DCIV SET/RESET/max current, pulse trains/stop reason, cleanup, and attach `device_plot.png`.
- For plotting “devices tested so far,” do not imply a measurement completed from the presence of `device_##/summary.json`; count completed devices by `summary.status == completed` and presence of expected DCIV/pulse artifacts. If the current device is only in approach, plot/report it as in-progress and state that no DCIV/pulses exist yet.
- If a runner was killed and restarted, say so explicitly and include the recovery summary path; do not hide the stale/stalled attempt.

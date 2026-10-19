# No-skip grid resume with manual contact handoff (2026-07-01)

Use this reference when continuing ViPSA gridwise electrical measurements after a pause, manual contact recovery, or a user instruction such as "do not skip measurements" / "re-do from device N".

## Durable workflow lesson

When the user explicitly says not to skip measurements, safety/contact gates should become **record-only diagnostics** for that grid run unless there is a hard instrument fault. Do not silently skip weak/open-like devices just because contact diagnostics are poor. Attempt the requested DCIV and randomized pulse measurements, record the contact/safety classification in per-device metadata, and preserve normal cleanup.

## Re-do from a specific device

1. Identify the active grid run directory and runner script.
2. Preserve existing completed device results; do not delete or overwrite unrelated `DONE.json` devices.
3. Set the runner start point to the requested device (for example, `START_AT_DEVICE=14` or the current paused device).
4. Ensure skip logic checks `DONE.json` only for devices that should remain preserved. If the requested device already has a completed folder but the user asked to re-do it, archive/rename the old attempt or otherwise force a fresh measurement for that device.
5. Verify the runner will attempt both DCIV and randomized pulse flow even if pre-checks classify contact as weak/open-like.
6. Compile or syntax-check the runner before launching.
7. Check machine states before launch and clear stale `run_id` values via machine reset if needed.

## Manual contact / stage-zero handoff

If the user manually approaches a device, obtains in-window contact, then sets the current stage position as zero:

- For the first resumed device only, **do not retract, realign, or re-approach** unless the user asks.
- Reuse the manual approach artifact as the approach record.
- Add explicit metadata such as:
  - expected device number,
  - expected Zaber target/readback,
  - manual approach artifact path,
  - reused approach status/current,
  - `no_initial_stage_or_zaber_move: true`,
  - `no_initial_alignment_or_reapproach: true`.
- Immediately run a low-bias post-handoff health check. If it is voltage-responsive and not short-like, proceed to DCIV/pulses.
- Preserve cleanup and hard-fault handling exactly as usual.

## Monitoring pattern

Background process capture may be empty when the runner is wrapped with `tee`; use the tee log file and device directory artifacts as ground truth:

- tail the grid log for `device_start` / `device_finished` events,
- check `device_N/DONE.json`,
- inspect `device_N/summary.json`, `dciv.json`, `randomized_pulse_summary.json`, and plot outputs,
- verify machine states after completion/failure.

Report concise verified progress: current device, completed device metrics, pulse count/failure reason if any, plot path, and cleanup/machine state.
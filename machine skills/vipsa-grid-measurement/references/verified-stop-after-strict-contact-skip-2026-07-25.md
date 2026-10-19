# Verified mid-grid stop after strict contact-gate skip

Use this reference when a narrow-window grid runner is stopped after one or more devices may have progressed beyond the last visible process preview.

## Stop and reconciliation sequence

1. Kill the tracked grid runner immediately and pause its per-device reporter.
2. Search the process table for surviving runner, recorder, watcher, or reporter children; do not assume killing the tracked session killed a shell pipeline or child process.
3. Read the **full terminated-process log**, not only the last poll/preview. Buffered output may reveal completed or skipped devices and a later active device that were not visible during earlier polls.
4. Reconcile the boundary from per-device summaries:
   - `completed` with expected measurement sections: completed device.
   - `skipped_contact_not_in_window`: processed, but electrical measurement intentionally blocked.
   - `started` without `finished_utc`: interrupted device; inspect which phase keys exist.
5. Run explicit emergency cleanup with bounded per-command `START → one command → COMPLETE` transactions when the normal runner was killed mid-command:
   - Keithley: `abort_measurement`, then `set_output(false)`.
   - Keysight: `abort_measurement`, then `set_output(false)`.
   - 707B: `open_all`, then require `get_closed_channels == nil`.
   - Light: `turn_off`.
   - Stage: `abort_motion`, then read position.
   - Zaber: read position; do not move it during stop cleanup.
6. Verify all six ViPSA machine states are `idle` with `run_id: null`. Save cleanup responses as a JSON artifact and append the stop boundary to `project.md`.

## Explaining a strict-contact skip

When asked why a device was skipped, report the gate evidence directly:

- alignment result;
- requested current window and test bias;
- final current from each configured bounded attempt;
- stability requirement and whether it passed;
- highest relevant post-attempt check if available;
- explicit statement that DCIV/pulses were not run.

A final pA/sub-nA current below a `1–10 nA` gate is `no_contact_after_max`, not a failed electrical device. The skip prevents unreliable or meaningless DCIV/pulse data under open/weak contact. Do not call it a bad memristor unless later electrically valid measurements support that conclusion.

## Important artifact detail

An interrupted next device may have only `status: started` and alignment fields. Preserve it as partial history. Do not create a synthetic completion marker, and do not infer that approach or electrical stress ran when those sections are absent.

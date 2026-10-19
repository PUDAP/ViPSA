# Failure-prevention restart from an unfinished grid device (2026-06-30)

## When this applies

Use this pattern when an active/paused ViPSA grid run shows overstress/contact-edge failures and the user asks to patch the runner and restart from a specific unfinished device while preserving the existing run folder.

Concrete case: S1 8x8 probabilistic-computing grid was paused after devices 1–8, 16, and 15; `device_14` was stale with `status=started` and no `DONE.json`. The user wanted to restart from device 14 with softer failure-prevention measures while keeping approach step `0.5`.

## Safe patch/restart sequence

1. Verify no active measurement runner is still operating:
   - inspect grid/retest/python processes;
   - inspect the target run folder for completed `DONE.json` files and stale `summary.json` states;
   - compute the remaining devices by **serpentine traversal order**, not naive numeric order.
2. Back up the exact runner before editing.
3. Patch runner constants and metadata together. In this session the requested failure-prevention settings were:
   - `START_AT_DEVICE = 14`;
   - approach lower/upper window `1e-9` to `1e-8 A`;
   - approach stage-Z step `0.5` (respecting the user override);
   - lower approach read compliance, e.g. `2e-8 A`, so a soft-contact target is not hidden by a high compliance ceiling;
   - post-approach low-bias health check written into `summary.json`;
   - lighter pre-characterization DCIV instead of full/stressful DCIV before pulse behavior, e.g. `0 -> +0.6 -> 0 -> -1.2 V`, coarser `50 mV` step, while preserving reset-side compliance when requested;
   - post-DCIV low-bias health check before pulses;
   - lower randomized SET range initially, e.g. `0.2–0.6 V`;
   - shorter pulse width, e.g. `2 ms`;
   - smaller chunks, e.g. `100 pulses` (`25` SET-read-RESET-read trains);
   - reset pulse matched to DCIV reset side when requested, e.g. `-1.2 V`.
4. Add an over-current fine-trim guard: if a fine forward step overshoots above the upper approach threshold, command one minimum-valid retract (`-0.25` in the current stage-Z convention), re-read, and classify as `in_window`, `contact_edge_below_lower`, or still `over_current`. Do not leave the probe over-contacted merely because the final read was recorded.
5. Archive, do not delete, a stale target-device folder that has `status=started` and no `DONE.json`, e.g. rename `device_14` to `device_14_archived_failure_prevention_restart_<UTC>`.
6. Prune `summary.partial.json` from the restart boundary onward using traversal order, preserving completed devices before the boundary. Add a `resume_events` entry with the patch/restart reason, runner backup, and archive path.
7. Compile the patched runner (`python3 -m py_compile ...`) before launching.
8. Launch as a tracked background process with a dedicated log file and completion notification.
9. Verify immediately after launch:
   - background process is running;
   - fresh `device_N/summary.json` exists with `status=started`;
   - patch strings/settings are present in the runner;
   - if the user requested no recording or the prior run was no-recording, verify no new `camera*_resume_*.mp4` files appear.

## Reporting standard

Keep the update concise. Report:

- patched settings actually verified in the runner;
- background process/session id and PID;
- fresh target-device summary status;
- stale-folder archive path;
- log file path;
- no-recording verification if relevant.

Do not claim the device completed until `DONE.json` and per-device artifacts prove it.

## Pitfalls

- A stale `device_N` folder with no `DONE.json` can cause a restart to skip or merge data incorrectly. Archive it first.
- Patching only constants but not run-summary metadata makes later retrospective analysis misleading; update both.
- Serpentine traversal means the restart boundary after device 14 may include device 13/12/… before device 17/18/…; prune by traversal order.
- Lowering SET stress and chunk size should not silently remove health checks; the point is to gate pulses after approach and after DCIV.

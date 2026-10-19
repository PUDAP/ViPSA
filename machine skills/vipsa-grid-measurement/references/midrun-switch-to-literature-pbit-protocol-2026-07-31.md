# Mid-run switch from finalized grid protocol to literature p-bit protocol (2026-07-31)

## Trigger
Use when an active ViPSA grid run is already measuring devices, and the user says to switch **subsequent devices** to the literature-derived/finalized p-bit protocol.

## Reusable workflow
1. **Do not patch a running hardware loop in place.** Stop the tracked old runner at the current boundary/interruption point.
2. **Pause the old per-device reporter** before launching the continuation, so stale `DONE.json` updates from the previous protocol do not keep arriving.
3. **Verify no old runner children remain.** Shell pipelines (`python ... | tee run.log`) can have multiple child processes; check/kill the process group if needed.
4. **Run and verify cleanup before restart:**
   - Keithley output off.
   - Keysight output off.
   - 707B `open_all()` then `get_closed_channels == nil`.
   - lights off.
   - `stage.abort_motion()` if the old runner may have been in approach/motion.
   - read Stage and Zaber positions.
   - all six ViPSA machines idle / `run_id: null` when available.
5. **Treat SIGTERM notification for the old runner as expected**, not as failure of the new run. Reconcile against the new process ID and run directory before reporting.
6. **Identify the interrupted device from live logs and summaries.** In the concrete case, the old runner had completed device 17, then started/aligned device 18 and was killed before measurement. The continuation started at device 18.
7. **Create a new continuation run directory** whose metadata says the protocol changed and names the previous run. Preserve old device summaries before the restart boundary as `preserved_previous_devices`; do not merge them as if they used the new protocol.
8. **For the first continuation device**, reuse the current physical position if the old runner already aligned/pre-approached it; do not do a second Zaber/vision travel unless live X/Y no longer matches the intended device.
9. **Install a new reporter** keyed to the new run directory and protocol name. Pause or remove the old reporter.

## Literature p-bit continuation parameters used
- Contact gate: Keithley `0 V`, `+10 mV`, `-10 mV`, `+50 mV`, `-50 mV`, three reads each, `1 µA` compliance.
- Only run p-bit stress if the gate is nA-scale / voltage-scaled and not read-compliance-limited.
- DCIV: `0 -> +0.8 -> 0 -> -1.0 -> 0 V`, 50 mV step, `1 µA` positive compliance, `10 µA` reset compliance.
- Pulse train order: `RESET -> READ_RESET -> SET(random V_SET) -> READ_SET`.
- `V_SET = 0.20..1.00 V` in 50 mV steps; 20 attempts/level for grid screening.
- `V_READ = +0.1 V`; pulse width `10 ms`; pulse compliance `10 µA`.
- If DCIV shows SET without RESET, run exactly five strongest RESET-read fallback pairs, save them, and continue only as explicitly labeled degraded-state p-bit data when the protocol/user permits.

## Reporting standard
When the user receives the old runner's SIGTERM notification after the switch, answer concisely:
- old runner stopped intentionally;
- new runner process and run directory are the active run;
- current device/status from the new summary/log;
- live machine state snapshot if checked.

Do not summarize the old termination as a new failure of the active continuation.

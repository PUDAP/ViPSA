# Grid continuation preflight and hard-stop recovery after electrical-edge failure

## Trigger
Use when resuming a long ViPSA grid from the current/interrupted device, especially after manual Stage-Z changes or a prior 707B/SMU edge outage.

## Preflight before launching the unattended loop
1. Reconcile live Zaber X/Y against the grid CSV and confirm the nearest/resume device.
2. Read live Stage-Z, but treat it as controller/software state if physical motion was previously disputed.
3. Check all six machine states for `idle` and `run_id: null`.
4. Do an **actual harmless hardware transaction**, not just a KV/state check:
   - 707B `open_all()` then fresh `get_closed_channels()`; require `nil`.
   - SMU outputs off.
   - Keysight and Zaber edges must accept a read-only transaction if later phases need them.
5. If 707B reports `[Errno 19] No such device`, stop before measurement/travel, restart only the 707B edge to create a fresh VISA session, verify the VISA resource is visible, then repeat `open_all` and `get_closed_channels == nil`.

## Current-device handoff after manual Z changes
- Do not automatically approach forward on the first resumed device when a recent low-bias check was compliance-limited/short-like.
- Preserve current X/Y and run the literature multi-bias contact gate directly. Skip stress if it is short-like or open/no-scaling.
- Subsequent devices use the normal cleanup → `Z -50` → absolute Zaber X/Y → align → `Z +40` → approach sequence.

## Required runner behavior
An electrical route/cleanup failure is a **run-level hard stop**, not a per-device result that may be caught and followed by travel to the next device. In particular:
- If `connect_keithley_smu`, `connect_keysight_smu`, `open_all`, output-off, or route verification fails, exit the whole grid loop before any Stage/Zaber motion.
- A per-device `except` block may save artifacts, but must re-raise a route/cleanup exception or set an abort flag checked before the next traversal iteration.
- Never continue lateral travel when 707B route state is unverified.

## Recovery after a failed launch
1. Kill the runner **and all pipeline children**; pause the reporter.
2. Reconcile the full run log, device summaries, and live Stage/Zaber positions. The runner may have started the next device and issued its `-50` retract before the kill; do not assume the failed device is still contacted.
3. Archive the failed device folder instead of silently overwriting it.
4. Reset that device key in reporter dedupe state so the replacement result is delivered.
5. Clear stale machine run IDs, verify 707B `nil`, recreate the first device fresh, then resume the reporter and runner.

## Reporting
Separate the transient failed-launch artifact from the verified resumed run. State the last completed device, any unexpected travel already executed, live positions, route cleanup evidence, and the active process/reporter handles.

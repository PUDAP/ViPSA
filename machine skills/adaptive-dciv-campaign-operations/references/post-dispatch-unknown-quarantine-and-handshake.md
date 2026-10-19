# Post-dispatch UNKNOWN quarantine and campaign continuation

Use this pattern when a continuous DCIV batch was dispatched but the transport closed before the native result returned.

## Evidence classification

1. Freeze the scheduler or other concurrent controller.
2. Preserve the failed batch directory, terminal record, wire journal, and all allocated operation IDs.
3. Decode the wire journal rather than relying on the wrapper exception:
   - command intent with no matching native response is **possible exposure**, not zero exposure;
   - no receipt files, no rows, and no native response do **not** prove that hardware stress did not occur;
   - a pre-dispatch capacity/control rejection can be zero exposure only when the wire proves the measurement command never reached hardware.
4. Keep every affected branch `UNKNOWN`; do not mark it COMPLETE and do not replay it.

## Restore safe hardware control

1. Confirm the matrix cleanup independently (`open_all` success plus explicit `nil`/empty closed-channel readback).
2. If the SMU rejects harmless commands with `RUN_ID_MISMATCH`, reset only that PUDA machine state. Do not restart NATS.
3. If the edge is absent, restart only the affected protected edge process and ensure a single owner.
4. Force output OFF and read back output OFF, matrix open/`nil`, and no instrument errors.
5. Hardware safety recovery does not erase the device-level UNKNOWN exposure.

## Quarantine and continue

After hardware safety is freshly verified:

- retain the verified cycle prefix and its health checks;
- generate plots/CSV only through the last verified full cycle;
- label the device `infrastructure_unknown_exposure_quarantined` (or equivalent), preserving all UNKNOWN branch intents;
- advance to the next physical device without replaying the uncertain batch;
- exclude the quarantined unknown batch from optimizer/scientific training.

This is compatible with an autonomous campaign directive: fail closed on the affected device, recover hardware safety, quarantine the device, then continue the broader campaign.

## Coupled runner/handshake bookkeeping

A device transition is incomplete until both state machines agree:

1. Runner: clear `pending` and advance the sequential initial-design cursor by one.
2. Optimizer handshake: append a history entry containing the acknowledgement, recipe, result, result hash, and relevant operation IDs; then clear `active`.
3. Preserve the distinction between:
   - physical traversal ID (for example a reverse-row sequence), and
   - sequential initial-design cursor/index.
4. Verify the next publisher sees `runner.pending == null`, `handshake.active == null`, and the last acknowledgement for the just-finished physical device.

Custom bookkeeping that updates only the runner leaves a stale active recipe and blocks the next publication.

## Variable stop-boundary plotting

Do not copy a fixed 10-cycle plotting script unchanged when a device stops at 20, 30, or another boundary. Derive the final verified cycle set from COMPLETE SET+RESET ledger records, require every cycle in the prefix, set color normalization/title/filenames to the actual boundary, and verify the CSV row count from native point totals.
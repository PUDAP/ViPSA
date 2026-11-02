# ViPSA partial-run recovery case

## Observed sequence

A fresh current-device grid run failed before stress because the 707B edge was alive but its USB/VISA write returned `[Errno 19] No such device`. The Stage pre-approach move had completed, so the electrical retry reused that exact Z and did not repeat motion.

After edge recovery, a later runner was terminated after operation 11. Artifacts proved operations 1–11 completed; operation 12 had no returned CSV and could have been in flight. The correct classification was `outcome_unknown_after_possible_partial_stress`, requiring a user decision before repetition.

## Validated recovery

1. Verify there are no surviving runner children.
2. Command Keithley output off.
3. Reset 707B logical state.
4. Confirm the expected VISA USB resource is visible.
5. If `open_all` still fails, stop only the 707B edge process, confirm no duplicate owner, and start exactly one replacement.
6. Require `open_all` success and `get_closed_channels == nil` before retry.
7. Preserve every completed operation CSV and operation index.
8. Do not repeat the completed Stage pre-approach move.
9. For user-selected stop, merge only operations 1–11, make a partial plot, record zero endurance cycles, cleanup, and retract.

## Cleanup-parser bug

A helper accepted `str(None) == 'none'` as an open matrix. Because command errors left `closed_channels=None`, it falsely set `matrix_open_verified=true`. Verification must require successful command responses plus explicit hardware `nil`.

## Motion reconciliation

A `Z −100` CLI transaction printed stale-run/database errors, but fresh readback changed exactly from `17.5` to `−82.5`. The move was therefore completed and must not be repeated.

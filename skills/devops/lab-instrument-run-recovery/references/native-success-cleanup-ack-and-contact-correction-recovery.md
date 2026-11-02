# Native-success / cleanup-ack recovery for interrupted ViPSA runs

Use this note when a controller is killed or exits after an instrument operation may have been dispatched.

## Verified recovery pattern

1. Freeze further stress and inspect the permanent ledger plus the run's durable wire journal.
2. Match the unresolved operation to the exact native reply using machine, command, run ID, ordered voltage list, compliance, timing, and expected point count.
3. If the native reply is successful and complete, reconstruct the normalized rows from that exact envelope, verify ordered points and monotonic timestamps, and recompute sampled energy exactly once.
4. If the ledger stopped at `INTENT` with no charged result, append the recovered envelope/rows and charge the recomputed energy once. Mark the operation complete only after fresh output-OFF, matrix-open and error-queue checks.
5. If the ledger already contains rows, energy, `complete=true`, and the only failure was a redundant cleanup acknowledgement timeout, do **not** charge or replay. A narrow reconciliation is valid when the operation cleanup has explicit output readback `0` and matrix `nil`, and an independent final cleanup repeats those readbacks. Preserve the timed-out acknowledgement in history.
6. Clear the device-level UNKNOWN flag only after every operation on that device is resolved; do not bypass another unresolved exposure.
7. Resume in a fresh execution directory from the first missing boundary. Preserve completed operation IDs and write `no_replay=true` provenance.
8. Carry counters across the boundary. If an every-N-sweeps health read became due on the reconciled sweep, run that health read before the next stress operation.

## Contact-correction continuation

When a user orders a contact correction after an interrupted candidate run:

- reconcile the in-flight branch first;
- require electrical cleanup before motion;
- execute and read back the exact authorized Z delta with no XY change;
- run only the requested conditioning suffix, retaining original operation order;
- preserve the pre-correction candidate history separately;
- restart candidate cycle numbering at 1 under a fresh execution identity when explicitly requested;
- enforce the normal minimum-cycle and hard-cap policy on the restarted run;
- advance to the next device only after terminal cleanup and ledger completeness are verified.

## Do not

- infer zero exposure from a killed Python process;
- resend a command because its caller lacks a receipt;
- treat `set_output(False)` acknowledgement timeout as unsafe if independent readbacks prove output `0` and matrix `nil`—record and reconcile it narrowly instead;
- reset energy, sweep counters, or prior history;
- merge pre- and post-contact-correction cycles into one scientific series without labels.

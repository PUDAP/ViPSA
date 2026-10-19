# Recovering a completed batch with a cleanup-ack UNKNOWN

Use this pattern when all stress operations in a batch completed, a post-batch health measurement returned valid data, but its cleanup acknowledgement timed out and the ledger conservatively marked the health operation `UNKNOWN`.

## Preconditions

Do not use this procedure for incomplete or ambiguous stress exposure. Require all of the following:

- every SET/RESET operation has its complete native trace and permanent-ledger entry;
- the health command returned the expected data rows and a successful native response;
- no later stress has been dispatched;
- a later batch-level cleanup record explicitly reports output OFF and matrix open;
- after repairing control connectivity, a fresh independent proof again reports output OFF, matrix open, and no instrument errors.

## Recovery sequence

1. Stop the supervisor and pause autonomous continuation.
2. Inventory the batch terminal, candidate receipts, native row counts, and ledger states. Do not replay the batch merely because its wrapper exited nonzero.
3. Localize the UNKNOWN operation. Distinguish a successful measurement with lost cleanup acknowledgement from an unknown measurement exposure.
4. Repair only the affected command edges. When NATS reconnect logs show broken consumers (for example repeated pull attempts against an uninitialized subscription), map running edge PIDs to `/proc/<pid>/cwd`, terminate only the stale affected owners, and launch exactly one replacement per edge. Preserve any separately deployed protected driver path rather than replacing it with the generic workspace copy.
5. Require each replacement edge to report fresh queue/immediate subscriptions and `idle` with `run_id: null`.
6. Run a harmless independent safety sequence: force output OFF, open the matrix, read output `0`, read closed channels `nil`/empty, and read instrument errors.
7. Reconcile only the cleanup-ack UNKNOWN operation if all preconditions hold. Preserve its original cleanup record, add paths and hashes for the batch terminal and fresh proof, record that neither measurement nor stress was replayed, set that operation `COMPLETE`, and clear the device UNKNOWN flag only after confirming no other UNKNOWN entries remain.
8. Resume at the first missing batch boundary, never at the interrupted batch.

## Important distinctions

- A nonzero supervisor exit does not mean the candidate cycles failed or are absent.
- A complete health measurement can still be UNKNOWN solely because cleanup verification timed out.
- Later OFF/open evidence is useful, but recovery still requires a fresh post-repair OFF/open/error proof.
- Do not restart local NATS when the rig is configured for a remote cluster.
- Keep the autonomous scheduler paused until the fresh safety proof passes and the ledger is reconciled.

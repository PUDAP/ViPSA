# Long initial-design cursor, handshake, and motion recovery

Use this reference for long ViPSA campaigns that consume a frozen design table while physical traversal is non-numeric (for example, `...29 → 30 → 40 → 39...`).

## Cursor and physical-device identity

- Keep the design cursor separate from the physical device number.
- Increment the cursor once per fully recorded physical device.
- Never assign the cursor from the physical ID after traversal diverges from numeric order.
- Recipe provenance should point to the previous physical device’s published artifact while the design vector comes from `design[cursor]`.

## Publication preflight

Require:

- preparation terminal complete and matched to permanent-ledger operations;
- cleanup verified and device not UNKNOWN;
- runner `pending == null`;
- handshake `active == null`;
- last handshake acknowledgement names the previous physical device;
- exact live/final pose and native SET/RESET point counts;
- output-OFF native list proofs before candidate stress.

## Completion bookkeeping

A physical device is not ready for the next publication until both state stores agree:

1. Validate every completed candidate branch and health read.
2. Generate final plots through the actual terminal cycle.
3. Write the physical-device acknowledgement.
4. Append handshake history and clear handshake active.
5. Clear runner pending and increment the design cursor once.
6. Read both stores back before publishing the next recipe.

A stop can occur at cycle 10, 20, or any later validated batch boundary. Apply the configured consecutive-failure criterion; preserve all earlier full cycles and health reads.

## Native list capacity

When a 10-cycle batch exceeds the protected native-list limit:

- deterministically split into bounded lists;
- preserve one output-ON interval spanning every SET/RESET branch;
- generate one final OFF block;
- validate every list’s size, total native points, all segment boundaries, the actual generated final trigger block, source-status ON for every acquired row, final output OFF, and cleanup.

Do not reject or replay a valid completed native acquisition solely because a wrapper assumed one list or a hard-coded final trigger block.

## Preparation fault after motion

A transport fault may occur after a guarded Z move but before its electrical sweep. Recovery must distinguish motion from stress:

1. Preserve all COMPLETE sweep receipts.
2. Verify OFF/open state; pause autonomous scheduling while safety is unresolved.
3. Read the live stage and Zaber pose directly.
4. If the next-attempt motion already happened but no sweep receipt exists, resume that attempt at the live pose without another move.
5. Continue the health counter from retained sweeps.
6. Aggregate retained and recovered receipts into the final preparation terminal.

## PUDA run-state recovery

For `RUN_ID_MISMATCH` after interrupted transport:

- verify NATS reachability without restarting shared NATS;
- inspect/reset only the affected machine’s PUDA run state;
- obtain fresh SMU output-OFF, matrix-open/nil, and no-error readbacks;
- continue only after cleanup is verified;
- never replay completed stress to make bookkeeping look contiguous.

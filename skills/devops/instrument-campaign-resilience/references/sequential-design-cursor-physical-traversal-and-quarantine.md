# Sequential design cursor, physical traversal, and quarantine handoff

Use this pattern when a campaign's optimizer design index is sequential but physical device traversal is non-monotonic (for example `...30 -> 40 -> 39...31 -> 41...`).

## Separate identities

Track these independently:

- physical `device_id` and absolute grid target;
- zero-based design-row index;
- runner `initial_cursor` / next sequential design count;
- handshake request/candidate IDs;
- completed candidate-cycle boundary.

Never infer the design index from the physical device number after traversal changes direction or jumps rows. Assert the expected cursor before publishing, then bind the next design row to the current physical device explicitly.

## Atomic completion handoff

After final validation or a policy stop:

1. Verify complete branch/native-point/health counts and fresh hardware cleanup.
2. Write the device aggregate and optimizer acknowledgement.
3. Under runner and handshake locks, append handshake history, clear handshake `active`, clear runner `pending`, and increment the sequential cursor exactly once.
4. Preserve the physical device ID, design index, request ID, candidate ID, classification, and artifact hashes in the acknowledgement.
5. Read back the runner/handshake state before publishing the next candidate.

A custom completion path that advances only the runner but leaves handshake `active` stale will block the next publisher. Repair only after proving the stale active candidate is already finalized; append its verified acknowledgement before clearing it.

## UNKNOWN-exposure quarantine

When a continuous native command intent exists but no matching reply exists:

- retain every planned branch as UNKNOWN;
- do not count or replay the ambiguous cycles;
- restore and verify output OFF, matrix open, and empty errors;
- plot only the contiguous verified prefix;
- acknowledge the result as infrastructure UNKNOWN exposure with scientific-training acceptance false;
- preserve the device UNKNOWN flag while allowing the broader campaign to continue on a fresh physical device only after safety verification;
- atomically clear active/pending and advance the design cursor as above.

## Verification

- The next publisher must see `handshake.active == null`, `runner.pending == null`, and the expected cursor.
- Handshake history's last acknowledgement must identify the immediately prior physical device, even when physical numbering and design-row numbering differ.
- No UNKNOWN operation may be compacted, silently cleared, or treated as zero exposure from row count alone.

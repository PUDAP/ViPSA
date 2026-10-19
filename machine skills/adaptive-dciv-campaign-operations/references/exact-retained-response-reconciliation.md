# Exact retained-response reconciliation after client transport loss

Use when a client reports `UnexpectedEOF`, `ConnectionClosedError`, timeout, or termination after durable dispatch, while the edge may have finished the native command.

## Fail-closed procedure

1. Immediately classify every dispatched-but-unreceipted branch as `UNKNOWN`; stop progression. A missing client reply never proves zero exposure.
2. Find the edge's durable response for the **same run ID** recorded in the wire request. Require exactly one match.
3. Verify full command identity: machine, command name, exact segment arrays/settings, reset/ADR flags, segment/point counts, and immutable recipe/binding identity.
4. Accept only complete native evidence: success, all expected segments/points, finite rows, strictly monotonic native timestamps, native preproofs, empty runtime errors, idle trigger state, one bounded output interval, and output OFF afterward.
5. Retire stale controllers before recovery and hold the global owner lock for the ledger commit.
6. If edge state is stale, restart/reset only that edge. Obtain a fresh independent proof of output OFF, matrix open/`nil`, empty errors, correct terminal/driver identity, and unchanged live pose. The proof must issue no stress.
7. Reconcile by immutable operation IDs, not list position; later zero-exposure attempts may have been appended during recovery.
8. Convert only matched UNKNOWN operations to COMPLETE. Attach original UNKNOWN records as fault history; mark `recovered_from_edge_response=true` and `no_replay=true`; preserve later zero-exposure attempts; record response and safety-proof paths/hashes.
9. Recompute metrics and sampled energy from retained rows exactly once, then apply the configured consecutive-cycle failure rule.
10. Run only the missing post-batch health read and verify cleanup again. Candidate and health completion stay distinct.

An autonomous supervisor may perform only this branch: edge reset → fresh safety proof → exact response validation → atomic reconciliation → health. If the response is absent, duplicated, mismatched, incomplete, or safety verification fails, leave UNKNOWN latched and stop. Pre-dispatch zero-exposure failures must not enter retained-response acceptance.

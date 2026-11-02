# Ledger-First Recovery After Post-Commit Failures

Use this note when a controller faults after an instrument operation but before local validation, receipt writing, metric generation, or archival compaction finishes.

## Durable ordering rule

An acquisition helper may commit a COMPLETE operation to the permanent ledger before the controller validates or writes its per-operation receipt. Therefore:

- `controller status=fault` is not exposure truth;
- a missing receipt file does not imply zero exposure;
- inspect the permanent ledger and native wire evidence before any retry.

If the ledger entry is COMPLETE with full native rows, measured energy, and verified cleanup, treat the branch as complete and never replay it. Reconstruct the missing receipt from that exact ledger entry, add only controller metadata such as category/cycle, run the corrected validator, write the receipt, record `no_replay=true`, and resume at the next missing branch.

## Keithley 2450 representation validation

Do not invent a loose voltage tolerance when native list representations differ. Validate two independent discrete facts:

1. list readback equals recalled level at the instrument's query precision;
2. stored seven-significant TSP level exactly matches the requested host value or its binary32 encoding.

Do not require host-side six-digit rounding of the unrestricted request to reproduce the instrument's decimal-tie rendering. The 2450 can render six-digit queries differently at ties while the recalled level/list readback and stored seven-digit configuration remain mutually consistent.

Apply this rule consistently in both layers: the edge driver's native-list proof and every controller/receipt validator. A corrected edge proof can still be rejected post-commit if a host validator retains `actual == [float(format(v, '.6g')) ...]` or independently recomputes nearest-grid rounding from the unrestricted request. For modern proofs with `stored_configs`, validate `raw_readback[i] == stored_configs[i].recalled_level_V`, then rely on the edge proof's exact stored-level/request-or-binary32 checks. Keep host `.6g` comparison only as a legacy-fixture fallback when stored per-index evidence is absent.

## Compactor safety

Incremental compaction runs after receipt durability, not merely after ledger COMPLETE.

- Never remove `raw_envelope`, `available_rows`, or `rows` unless the unique external receipt/archive exists and its hash is recorded.
- If receipt lookup fails, leave the ledger payload intact; reconcile/write the receipt first, then rerun compaction.
- Prefer an explicit receipt path recorded by the controller or exact operation-ID lookup over ambiguous basename globs.
- Compactor failure must not convert a completed electrical branch into a replay.
- Preserve operation state, energy totals, cleanup proof, native row count/hash, recipe/cycle identity, and UNKNOWN entries.

## Recovery checklist

- [ ] Freeze automatic retry.
- [ ] Inspect ledger entry before local progress/terminal files.
- [ ] Corroborate exact operation identity in native wire evidence.
- [ ] Verify output off, matrix open, and error queue clean.
- [ ] Reconstruct and validate a missing receipt only from durable native evidence.
- [ ] Resume at the first genuinely missing branch.
- [ ] Compact only after receipt/archive durability is proven.

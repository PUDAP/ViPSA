# Canonical validation for derived per-device controllers

Use when creating the next device's preparation, candidate, health, supervisor, plotting, or navigation controller from a previously verified device.

## Before any motion or electrical dispatch

Treat text substitution as generation, not validation. Import/compile the derived controller offline and assert:

- `DEVICE` is exactly `substrate16/deviceN`;
- the adapter hardware mapping has numeric `device=N` and its canonical `device_id` names the same device;
- recipe path, candidate ID, recipe digest, proposal `source_row`, and manifest binding index all refer to the same immutable binding;
- operation-ID prefixes, output directories, status labels, plot titles, and terminal paths name Device N;
- expected SET/RESET native point counts are recomputed from the exact endpoint/step values rather than inherited;
- nominal, aligned, pre-approach, and final pose assertions match the current device's verified records;
- no stale prior-device token remains in executable fields.

A syntax check is necessary but insufficient. Exercise pure constructors such as `make_segments()` and `initial_ledger()` and assert segment count, native-point total, binding hash, preparation hash, and canonical identity before hardware use.

## Preparation ordering pitfall

A canonical identity mismatch can be discovered only when the first electrical branch reaches the adapter, after a script has already made its `Z+40` pre-approach. Prefer an explicit identity-only preflight before pre-approach so stale mappings fail with zero motion.

If an old controller does fail after pre-approach but before electrical dispatch:

1. Prove zero forming/conditioning/candidate receipts and no native acquisition dispatch.
2. Verify output OFF, matrix open, empty errors, and confirmed pose.
3. Record the failed attempt as zero electrical exposure; do not relabel it as preparation.
4. Return by the exact inverse pre-approach move to the verified baseline pose.
5. Correct only the stale canonical field, rerun offline identity assertions, and start a fresh append-only attempt.

Never simply rerun from the raised pose: that would apply pre-approach twice.

## Standing authorization

After alignment, preparation, immutable binding validation, health gates, and cleanup all verify, dispatch the candidate immediately under the standing campaign authorization. Plot/status requests are read-only side work and do not pause automatic progression.
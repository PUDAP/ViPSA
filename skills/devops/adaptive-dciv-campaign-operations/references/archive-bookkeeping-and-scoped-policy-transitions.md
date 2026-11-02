# Archive bookkeeping and scoped campaign policy transitions

## Verified techniques

This reference captures successful saved-data reconciliation and scoped-policy verification. It does not prescribe an untested executor restoration or claim that a blocked BO batch ran.

### 1. Separate policy scopes

A cumulative-device energy override changes only the cumulative stop. Preserve actual sampled-energy charging exactly once, phase-specific forming/read limits, compliance, cleanup, nonfinite/UNKNOWN stops and no replay unless the operator explicitly changes another scope. Check adapter admission, controller reservation gates and receipt validators: changing only one layer can leave an obsolete stop elsewhere. Record a versioned effective policy linked to the operator authorization and immutable recipe hash. Test charge above the former ceiling, retained phase-limit rejection, UNKNOWN rejection, cleanup, replay rejection and stage-specific cycle caps.

### 2. Match records by identity, not folder order

Inventory every requested device and candidate. Resolve acknowledgements lacking candidate IDs through frozen recipes and batch-terminal identities, then verify request IDs, recipe hashes and receipts. Preserve explicitly repeated/revisited executions as separate histories even if their cycle labels restart at 1. A legacy checkpoint can identify a device in `proposal.device_id` rather than top-level `device_id`; recognize that schema without inventing identity.

### 3. Validate compacted payloads

A compacted permanent-ledger operation may replace `rows`, `available_rows` or other payloads with:

- `archived_payload.receipt_path`
- `archived_payload.receipt_sha256`
- `archived_payload.payloads[field].item_count`
- `archived_payload.payloads[field].sha256_canonical_json`

Read the exact referenced receipt and verify its file SHA-256. Recompute each payload hash using the serializer that produced the manifest. The verified session schema used:

```python
hashlib.sha256(json.dumps(value, sort_keys=True,
    separators=(',', ':'), allow_nan=False).encode()).hexdigest()
```

Check `item_count` when it is a numeric count; a null count is not a list-length assertion. Rehydrate only in an in-memory comparison copy, remove the archive descriptor from that copy, and compare the remaining operation fields. A saved health receipt can add presentation-only `category` and `campaign_cycle` tags absent from the permanent operation; explicitly identify and validate such differences rather than weakening measurement, settings, energy, identity or execution-state comparison. Keep original files untouched.

### 4. Count full cycles correctly

Some batch terminals record cumulative endpoints: batches covering 1–10, 11–20 and 21–30 can report `completed_cycles` of 10, 20 and 30. Summing those values falsely yields 60. Reconcile explicit interval sets, reject overlaps, require coverage of the intended range, and verify unique completed SET/RESET branch IDs and native row counts. Exclude health reads, preparation, intent-only operations and zero-exposure/non-counted reconciliations from candidate-cycle counts.

### 5. Append bookkeeping without scientific tell

For an explicitly requested archive/checkpoint reconciliation:

1. Hold the existing execution-owner and runner-state locks; acquire other relevant shared-write locks when those targets can be concurrently changed.
2. Require an appropriate paused boundary and capture checkpoint/ledger hashes.
3. Validate receipt hashes, recipe identities, cleanup, ledger correspondence and quarantines.
4. Test an append-only transition on a fixture: original input untouched, existing record prefix unchanged, null objectives, explicit non-training status, preserved pause/safety state, and idempotence or fail-closed conflict detection.
5. Back up the checkpoint, atomically append only evidence-backed missing bookkeeping entries, and read back the exact target.
6. Verify old records and unrelated checkpoint fields unchanged; verify the electrical-ledger hash unchanged.
7. Publish one disposition row per requested device, distinguishing measured records, quarantine and administrative infrastructure-fault completion. Do not turn an administrative fault into recipe failure, hard-cap censoring or a training observation.

Complete inventory coverage is not scientific dataset completeness. Existing contrast metrics with invalid pairs remain invalid; descriptive geometric means are not automatic training submissions.

### 6. Handle delayed independent audits

A peer audit describes its captured source hashes. If the checkpoint has since been reconciled, preserve the original audit and link a post-transition report. Compare old and new snapshots; do not repeat the migration because an asynchronous result still reports the old record count. Reconcile explicit identities and counts programmatically before declaring coverage complete.

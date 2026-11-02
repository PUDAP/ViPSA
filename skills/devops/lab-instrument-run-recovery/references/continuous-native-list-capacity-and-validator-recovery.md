# Recovering continuous-output batches across native list limits

Use this when a multi-branch electrical batch exceeds a per-configuration-list point limit, or when native acquisition succeeds but a downstream validator rejects newer evidence fields.

## 1. Classify the failure before retrying

Decode the retained native command response and distinguish:

- **Pre-execution rejection:** response is an error, no native result/rows exist, and the driver rejected capacity or parameters before enabling output. Reconcile pre-registered intents as zero-exposure, retain the failed intent records, verify OFF/open state, and create new operation IDs for a replacement.
- **Acquisition succeeded; validator failed:** native response reports `complete=true`, exact expected/actual points, all expected segments, one ON and one final OFF transition, source-status ON for every point, no runtime errors, final trigger state at the OFF block, and output OFF. Never replay. Recover receipts, metrics, and ledger state from that response; run only genuinely missing post-batch work such as a health check.
- **Ambiguous/incomplete exposure:** preserve UNKNOWN and stop for reconciliation.

A wrapper exit code or terminal status alone is not the exposure classification.

## 2. Preserve one output-ON interval above a list-size limit

When the instrument limits each source/sense configuration list (for example, 2,500 points) but the full authorized batch is larger:

1. Partition complete zero-to-zero recipe segments into chunks, each within the native list limit.
2. Build and size-verify **all** source/sense configuration-list pairs while output is OFF.
3. Build one trigger model containing:
   - one output-ON block before the first chunk;
   - a configuration-next pair and bounded loop for every chunk;
   - chunk transitions only at recipe segment boundaries where commanded voltage is zero;
   - one final output-OFF block.
4. Use a shared trace buffer sized for the whole batch and retain a global monotonic native timestamp sequence.
5. Verify exact list sizes, dynamic final block state, exact total trace count, source-status ON on every point, no runtime errors, and final output OFF.
6. Keep compliance/range/NPLC/dwell encoded per point so crossing a chunk boundary cannot silently reuse the wrong side's settings.

Do not split the experiment into separate output intervals merely to fit the list limit when continuous output is an explicit policy requirement.

## 3. Test before deployment

Add a fake-instrument regression at the real oversized point count. Assert:

- expected total points and segment count;
- expected number and sizes of configuration-list pairs;
- exactly one trigger-model ON block and one final OFF block;
- complete segment reconstruction and source-status continuity;
- any exception forces output OFF.

Run all existing driver tests, hash the deployed driver, restart only the affected edge, and repeat harmless OFF/open/native-list proofs before live acquisition.

## 4. Keep validators schema-flexible but strict

Validators must not hard-code a historical final block such as `IDLE;IDLE;10` or require one aggregate `configuration_list_sizes` object. Instead:

- derive the final OFF block from the retained trigger program and require exactly one final OFF;
- require trigger completion at that derived block;
- accept either the legacy single-list evidence or a list of per-chunk evidence;
- require every chunk size to be within the native limit, source size = measure size = declared points, and summed points = expected = actual trace count;
- retain all prior source-status, timestamp, energy, cleanup, and recipe checks.

## 5. Post-validator recovery

If acquisition already succeeded but receipt validation failed:

1. Read the exact native response from the wire journal.
2. Confirm the full completion proof above and fresh OFF/open safety.
3. Verify whether the permanent ledger already contains complete operations and rows.
4. Patch and test only the stale validator schema.
5. Rebuild receipts and cycle metrics from retained ledger rows/native response.
6. Execute only missing health/cleanup work under a separately identified operation.
7. Continue from the first unmeasured cycle; never rerun the acquired batch.

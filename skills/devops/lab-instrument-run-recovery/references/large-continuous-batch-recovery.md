# Recovering large continuous instrument batches without replay

Use this pattern when a continuous multi-operation batch exceeds a native list/configuration limit, completes physically but fails downstream validation, or reaches a health boundary while storage/infrastructure fails.

## 1. Separate dispatch failure from post-acquisition validation failure

Inspect the retained native command response before deciding whether to retry.

- **Zero exposure:** command was rejected before execution, with no native result, no rows, and no output-ON evidence. Reconcile pre-registered intents as zero-exposure; create new operation IDs for a replacement.
- **Completed exposure:** native result reports `complete=true`, exact expected/actual point counts, all expected segments, one ON and one final OFF transition, output-ON source status at every point, idle final trigger state, no runtime errors, and output OFF afterward. Recover receipts and metrics from that result; never replay.
- **Ambiguous exposure:** missing/incomplete native evidence. Keep UNKNOWN and stop.

A wrapper status such as `fault` or `Blocked` does not override complete native evidence. Determine the physical outcome first.

## 2. Native configuration-list capacity

When each branch fits the instrument’s per-list limit but the full batch does not, partition only at zero-voltage segment boundaries into multiple source/measure configuration-list pairs. Build every list while output is OFF, then compile one trigger program with:

1. one output-ON block before the first chunk;
2. per-chunk CONFIG_NEXT + measure loops;
3. recipe/compliance changes encoded in the stored per-point configurations;
4. timeout branches to one common final block;
5. exactly one final output-OFF block.

Verify list sizes individually and require their sum to equal the global expected point count. Validate the final trigger-state block dynamically from the actual OFF block rather than hard-coding the single-list block number.

## 3. Validator compatibility

Evidence validators must accept both:

- legacy `configuration_list_sizes={source:N,measure:N}`; and
- chunked `configuration_lists=[{points,source_size,measure_size}, ...]`.

For chunked evidence require every list to be `1..native_limit`, source and measure sizes to match the chunk, and summed chunk points to equal `expected_points == actual_points`.

If acquisition completed but an old validator rejects the new evidence shape, patch the validator, reconstruct receipts from the retained native response plus permanent ledger rows, regenerate cycle metrics, and run only the missing health operation.

## 4. Health-boundary and storage failures

If candidate cycles completed but the health operation failed before acquisition (no raw response and zero rows), preserve candidate cycles, classify only the health intent as zero-exposure, restore storage, independently verify output OFF/matrix open, and execute a separately identified replacement health check.

Before long high-point-count batches, check free disk space. If the filesystem is full, remove only clearly disposable caches; never delete campaign data, permanent ledgers, environments, or provenance artifacts. Recheck free space and live OFF/open state before recovery.

## 5. Required verification before continuation

- permanent ledger has no unresolved UNKNOWN entries;
- candidate point/segment counts match exactly;
- native source status proves output ON for every candidate point;
- one ON and one final OFF transition are retained;
- health check exists at each required cycle boundary;
- fresh output readback is OFF and matrix readback is explicitly open/`nil`;
- recovered metric files contain the full metric object, not only the failure-history summary.

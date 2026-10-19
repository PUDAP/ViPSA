# Continuous trigger batches above one configuration-list limit

## Trigger-model construction

When a full continuous-output batch exceeds the Keithley 2450 per-configuration-list capacity, do not reduce recipe points or split the batch into separate output intervals merely to fit one list.

1. Partition only at complete segment boundaries (SET or RESET), keeping each segment intact and each chunk within the native list limit.
2. Create one source-list/measure-list pair per chunk.
3. Compile one finite trigger model:
   - deadline/error branch targets one final OFF block;
   - first chunk enables output exactly once;
   - each chunk advances its own source and measure lists and loops for its exact point count;
   - later chunks do not toggle output;
   - the last block disables output exactly once.
4. Before `INIT`, verify every list's exact source/measure size, all CONFIG_NEXT list identities from trigger-model readback, and all branch targets.
5. After execution, require: exact total point count, complete ordered segments, one ON and one OFF transition, source-status ON for every sample, no runtime errors, final trigger state at the dynamically derived OFF block, and output OFF readback.

## Downstream validator compatibility

Do not hard-code a single-list schema such as `IDLE;IDLE;10` or a flat `configuration_list_sizes` dictionary. Derive the final OFF block from the retained program and accept a list of chunk records only when:

- `sum(points) == expected_points == actual_points`;
- every chunk is within the native limit;
- source and measure sizes equal that chunk's point count;
- the retained trigger program contains exactly one ON and one final OFF block.

A successful acquisition can be misclassified after exposure if the driver is upgraded but the receipt validator still expects old evidence fields. Regression-test the actual driver→adapter→runner result shape, including an over-limit full batch, before hardware use.

## Recovery after post-acquisition schema failure

If native evidence proves the full batch completed but an outdated validator blocks afterward:

1. Force and freshly verify output OFF and matrix open.
2. Read the wire response and require full native completion evidence.
3. Inspect the permanent ledger; if complete rows/energy are already committed, validate those operations against the retained global response.
4. Rebuild missing receipts, cycle metrics, and summary artifacts from retained data.
5. Do not replay the candidate batch.
6. Run only a health check that is genuinely missing.

If the health intent failed before acquisition (no rows, no raw envelope) due to a host-side fault, reconcile it as zero exposure only with fresh cleanup proof, then issue a separately identified replacement health check.

## Bookkeeping pitfalls

- Keep the full cycle metric object under `metric`; the failure-history entry `{cycle, signal}` is not a substitute.
- Count candidate cycles only when both branches are complete.
- Exclude reconciled zero-exposure intents when checking the effective ledger prefix, while requiring them to remain COMPLETE with zero energy and explicit reconciliation provenance.

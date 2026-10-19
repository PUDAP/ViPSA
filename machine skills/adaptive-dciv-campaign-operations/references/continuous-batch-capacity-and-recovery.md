# Continuous DCIV batch capacity and recovery

Use this when a recipe-defined continuous SET/RESET batch exceeds one native configuration-list capacity or when post-acquisition bookkeeping fails.

## Capacity-safe trigger construction

- Compute the total native point count before dispatch.
- Partition only at complete zero-to-zero recipe-segment boundaries; never split inside a SET or RESET trajectory.
- Keep each native source/sense configuration-list pair within the instrument limit (Keithley 2450 observed limit: 2500 entries per list).
- Build one finite trigger model that chains the list pairs, contains exactly one output-ON block before the first acquisition loop, and exactly one output-OFF block after the final loop.
- Preserve compliance, range, NPLC, and dwell changes at zero-voltage segment boundaries.
- Read back every list size and every CONFIG_NEXT identity before INIT. Derive the expected final trigger block dynamically; do not hard-code the single-list final block number.
- After completion require: expected points == actual points; all segments present and ordered; runtime error queue empty; native source-status indicates output ON for every acquired point; trigger state ended at the derived final OFF block; output readback is OFF.

## Validator compatibility

When the driver evolves from one list pair to multiple pairs, update validators to accept either schema:

- Legacy: one `configuration_list_sizes` object.
- Multi-list: `configuration_lists[]`, where each item records expected points plus source/measure readback sizes.

Validate the sum across list pairs against the retained native point count. Never weaken continuity, source-status, ordering, or final-OFF checks merely to accept the new schema.

## Failures after native acquisition

Treat hardware acquisition and host bookkeeping as separate phases.

1. Inspect the retained native response before considering replay.
2. If it proves all points, segments, source-status continuity, no runtime errors, and final OFF, preserve the candidate cycles.
3. Rebuild missing branch receipts and metrics from the retained trace, validating each reconstructed receipt against the frozen recipe.
4. If the post-batch health operation did not execute, preserve its intent as zero-exposure and run a separately identified replacement health check only.
5. Never replay retained candidate cycles because a validator, receipt write, plotting step, ledger compaction, or health setup failed afterward.

## Storage preflight

Long campaigns can fail after acquisition when the root filesystem fills. Before each batch, verify sufficient free space for the native response, wire journal, receipts, ledger rewrite, plots, and safety margin. On ENOSPC:

- stop new dispatches and verify output OFF/matrix open;
- preserve completed native data;
- free only disposable caches unless the user authorizes deleting artifacts;
- re-check free space and live safety;
- reconcile zero-exposure intents and resume from the first genuinely missing operation.

## Tests

Include a synthetic batch larger than one list (for example 3700 points) and assert:

- multiple source/sense list pairs with each size at or below the native limit;
- exactly one ON and one final OFF trigger block;
- every segment and point retained;
- all source-status records ON;
- any fault forces output OFF;
- existing single-list tests continue to pass.

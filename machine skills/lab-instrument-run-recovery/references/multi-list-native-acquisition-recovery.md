# Multi-list native acquisition and stale-validator recovery

## Capacity-safe trigger model

When a continuous Keithley batch exceeds one native configuration-list capacity, treat the limit as per-list unless the instrument documents a whole-trigger limit. Partition only at complete zero-to-zero segment boundaries. Build and verify all source/measure list pairs while output is OFF, then compile one trigger model with exactly one ON block before the first list and one OFF block after the last list. Validate list identities/sizes, block targets, runtime errors, final trigger state, exact trace count, and output-ON source status at every point. Regression-test a real over-capacity shape and every forced-OFF failure path.

## Stale post-acquisition validator

A runner can say `Blocked`, zero completed cycles, or no receipt files after the native command succeeded. Before retrying stress:

1. Decode the exact wire response.
2. Require `complete=true`, exact expected/actual points, ordered segments, one ON/one OFF, empty runtime errors, final output OFF, and per-point output-ON status.
3. Compare the permanent ledger. Full rows, `COMPLETE` state, and verified cleanup establish the acquired boundary even when the runner summary is stale.
4. Update and test only the evidence validator. For multi-list data, derive the final block from the sole OFF instruction; require each source/measure pair to have matching sizes within the list cap and require their summed points to equal the trace count.
5. Rebuild receipts, summaries, and cycle metrics from retained evidence; execute only missing work such as the health check. Never replay the completed candidate batch.

When reconstructing cycle JSON, store the full nested positive/negative metric under `metric`; `{cycle, signal}` is only a failure-history entry and will break later continuation.

## Near-zero branch plotting

If an endpoint magnitude is below its requested voltage step, a branch may be only `[0, endpoint, 0]`. On a shared axis dominated by the opposite polarity it appears as a near-zero sliver, and forward/backward contrast may be `1×`. Verify unique commanded voltages and row counts before calling data missing; explain the scale mismatch or add a zoom/inset without implying a normally resolved sweep was commanded.

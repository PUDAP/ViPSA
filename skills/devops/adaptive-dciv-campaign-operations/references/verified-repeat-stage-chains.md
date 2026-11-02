# Verified stage chains for historical-recipe repeats

Use alongside `archival-recipe-repeats-and-partial-preparation-rebinding.md` when repeating an unchanged batch across a fresh grid.

## Acquisition-unit correction

Process isolation must preserve the authorized native acquisition unit. A fresh process per cycle is suitable only for single-cycle acquisition. For continuous multi-cycle batches, isolate at the batch boundary; never split the batch or insert output toggles to satisfy a generic process-per-cycle rule.

## Actual pose, not inherited height

Freeze each device's native clearance readback and compute the authorized relative pre-approach from that pose. Fixed retract/pre-approach increments do not imply a fixed absolute first-trial Z. Keep absolute ceilings, attempt counts and fresh-device scope explicit. Reference completed motion and forming when a recipe binding changes; do not replay them.

## Verified phase chaining

A tracked per-device process chain can execute forming, OFF-only list qualification plus physical-history audit, then pending preparation and candidate cycling. Propagate failures at every boundary. A successor must validate positive-completion, UNKNOWN, cleanup, exact binding and sampled-energy records, not just an exit code: reaching the Z ceiling without the forming criterion can be a normal process exit but is not permission for candidate stress. Preserve the shared owner lock and prohibit a second controller.

Run full mocked-main tests covering write-root restrictions, backend command scope, context selection, once-only pre-approach, PB-only compliance stop, health cadence, postread clamp and cleanup after dispatch loss. Keep TEST ONLY fixtures and mock logs distinct from actual native qualification. OFF-only proof commands should use the established validation path rather than broadening the stress backend's allowlist.

## Native export and scientific accounting

Audit every retained COMPLETE batch, its ordered native points, batch-local index/time boundaries, contiguous full-cycle numbering, preparation prefix, final health and cleanup. Export signed currents unchanged. Plot ordered PF/PB/NF/NB with one color per cycle and distinct branch styles.

Record completed cycles separately from valid paired-contrast cycles. Invalid polarity, voltage matching or compliance comparisons remain failed/invalid outcomes, not invented ratios. Label a geometric mean over valid paired cycles with its actual denominator; it is neither an all-cycle mean nor independent retained-state ON/OFF. Recipe-specific failure, physical destruction and right-censoring are different claims.

## Current status and automatic continuation

Answer status queries from current worker/journal evidence. Distinguish forming, OFF-only checks, preparation, candidate cycling and idle; queued work is not active measurement. A successful worker notification still requires native-result and cleanup audit before the next device. Continue after verified terminal gates under the existing authorization, without letting plotting or status generation pause the live measurement.

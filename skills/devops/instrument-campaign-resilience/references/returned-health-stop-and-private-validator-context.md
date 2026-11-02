# Returned health safety stops and private validator context

## Returned data is not permission to resume a failed device

A controller can record UNKNOWN because a native health reply fails a safety validator, even though the complete reply is available. Distinguish this from missing/partial acquisition. In the observed campaign, post-cycle10 health reads reached the configured 100µA compliance; the commanded 100mV was not attained. Native cleanup completed. The correct action was terminal assessment and progression to the next saved physical device, not relaxing compliance, repeating preparation, or replaying the stopped device.

The additive assessment must verify the exact binding, recipe/compiler hash, health command/parameters/run identity, native configuration and raw triples, finite timing, complete wire inventory, forming-first-qualification boundary, preparation-once counts, candidate metrics and existing energy ledger, permanent claims, cleanup and final pose. Bind the assessment to immutable source hashes. Preserve the original UNKNOWN event and journal. A reviewed returned-health terminal is not a blanket UNKNOWN waiver: any additional unresolved event, mismatched native reply, changed source or uncertain motion still blocks progression.

If the original ledger omitted health energy because validation raised before charging it, preserve that ledger and explicitly state the omitted contribution is not assumed zero. Do not claim complete total-energy accounting from known returned rows alone. Keep further stress prohibited for the stopped device; the assessment only admits the exact next-device handoff under existing authorization and fresh safety/readiness/image checks.

## Private recursive validator context

Legacy validators may import a shared compiler module inside inherited methods. Rebinding only a top-level function does not isolate recursive historical validation. The tested approach used instance-private function/module globals and scoped inherited imports while retaining original code, recipe arrays, canonical locks and native prefix validation. No shared historical module or stopped journal was rewritten.

Preserve the historical compiler context when constructing the private current-device adapter. Setting the shared compiler's CURRENT to the new device before constructing the adapter caused archived device26 plan reconstruction to use the wrong target and fail operator bounds. Keeping the shared historical context unchanged and setting CURRENT only in the private adapter passed native navigation/replay tests and subsequent live launches.

Use a separate exact reconciliation dispatch for each reviewed historical safety-stop boundary, with ordinary native terminal reconciliation elsewhere. Derive travel start from actual final pose: forming attempts can change terminal Z, so next clearance/preapproach must not reuse a previous device's fixed Z.

## Regression and reporting

Test real temporary SQLite with the actual recursive prefix (including stopped operations and completed recovery attempts), production native transport with a fake connector, full next navigation, owner-bound current INTENT, timeout-before-XY and no replay. Keep fixtures outside the production inventory and preserve old sources, claims and seals. Recheck raw recipe parameter parity before stress.

Export actual native rows with phase, original event state, physical/recipe IDs, run IDs and raw hashes. UNKNOWN health rows remain labelled UNKNOWN in exports even when a separate assessment admits next-device progression. Report actual electrical start only after a durable acquisition INTENT/run ID; a process handle or completed navigation is insufficient.

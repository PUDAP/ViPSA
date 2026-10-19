# Serpentine BO-batch rebinding and interrupted-cycle accounting

## Physical traversal is not numeric cursor order

For a 10-column row-major substrate traversed serpentine, crossing a row boundary reverses direction. In the Substrate-16 continuation after Device 50, the next row is:

`50 → 60 → 59 → 58 → … → 51`

A request for the “next eight” therefore means Devices `60,59,58,57,56,55,54,53`, not `51..58`. Resolve the actual grid/traversal order before assigning recipes or moving.

## Rebind optimizer recipes without modifying the proposal

If an optimizer batch was originally labelled with placeholder physical devices in numeric order:

1. Keep source recipe files immutable.
2. Preserve recipe order, candidate IDs, request IDs, full-precision parameters, applied voltages, and source hashes.
3. Create a versioned execution-binding manifest mapping recipe position 1..N to the corrected physical traversal.
4. Update only physical identity, absolute target, and result destination in the execution binding.
5. Hash and verify every binding; record `parameters_changed=false` and `source_recipes_modified=false`.

Do not silently rewrite the optimizer handoff or pretend the physical assignment was its original proposal.

## Forming semantics

“Three consecutive forming signals” means three consecutive qualifying points within one outbound forming sweep, not three successful forming sweeps. Evaluate only the outbound branch so the intentional return-to-zero does not look like a destructive down-jump. Stop forming on the first sweep satisfying the point-level gate. If it fails, perform one durable, verified `Z +5` motion before the next sweep, within the bounded attempt count.

## Candidate failure semantics

Recipe failure is based on consecutive complete candidate cycles. Health reads are separate telemetry and must not increment or reset the candidate-cycle failure streak. In continuous 10-cycle acquisition, evaluate cycle metrics after the full native batch and apply the consecutive-cycle rule at the batch boundary.

## UNKNOWN cycle slots and truncation

Track two indices when an acquisition may have run but its result is unresolved:

- physical cycle slot: advances past every dispatched uncertain batch so it is never replayed;
- verified-cycle ordinal: advances only for complete SET+RESET cycles.

On user truncation at a physical boundary, plot and export every slot through that boundary, mark UNKNOWN ranges null, and break plot lines across them. If a post-boundary batch was already dispatched, preserve it as UNKNOWN and exclude it explicitly; never claim it did not occur.

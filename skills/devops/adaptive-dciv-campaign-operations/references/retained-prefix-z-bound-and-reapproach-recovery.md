# Retained-prefix preparation recovery with revised Z bounds

Use when a ViPSA preparation stops cleanly at a software Z ceiling, the operator authorizes a revised bound or a retract/re-align/re-approach, and completed forming sweeps must not be replayed.

## Evidence gate

Before recovery, require all of the following:

- the preparation ledger and terminal agree on completed forming/conditioning counts;
- latest state for every operation ID is `COMPLETE`;
- `unknown=false` and cleanup proves output `0`, matrix `nil`, and an empty error queue;
- live Stage/Zaber pose agrees with confirmed persistent Stage state;
- no candidate ledger/cycles have started;
- the operator authorization is written as a versioned artifact with the exact maximum Z or retract/re-approach plan.

Preserve the stopped terminal and ledger before modifying the active aggregate. Link their byte hashes from the recovery authorization.

## Ceiling extension without replay

1. Retain all completed forming sweeps and motion readbacks.
2. Resume from the next missing forming attempt only.
3. When a fixed `+5` step would exceed the authorized ceiling but some range remains, use one final bounded partial step (for example `Z268 -> Z270` via `+2`) and run one forming attempt there.
4. If that attempt fails, stop before another sweep; do not exceed the ceiling by rounding to the normal increment.
5. Keep the authorization hash hard-gated in the executor and test wrong bytes, wrong device, changed counts, `unknown=true`, and mismatched pose.

## Retract, re-align, and re-approach recovery

When the operator explicitly retracts and requests another approach:

1. Journal and verify the manual retract separately from the failed preparation ledger.
2. Capture a fresh image at the retracted Z. Register it to the previously verified aligned image using substrate-only ROIs; exclude the probe. If the selected pad is partly occluded, prefer agreement across multiple substrate ROIs over a false neighboring contour.
3. Write a new alignment record with the fresh pose/image/hash and keep `physical_contact_claim=false`.
4. Preserve prior forming attempts as retained stress history. After the authorized pre-approach (for example `+40`), execute the next missing forming attempt at that pose without adding the usual inter-attempt `+5` first.
5. Subsequent attempts return to the normal bounded step sequence.
6. If the operator requires darkness, issue and retain a successful `light.turn_off` immediately before recovery; the worker should also force lights off before approach/stress.

## Preflight edge recovery

A harmless preflight getter can fail during START/COMPLETE lifecycle exchange before any motion or electrical stress. Classify this separately from preparation:

- confirm no recovery event, motion intent, or stress intent was appended;
- inspect the exact wire run ID;
- if the affected local edge process is absent, start exactly one canonical edge process;
- allow it to consume the retained COMPLETE and require `idle/run_id=None`;
- never use `machine reset stage`, because it redefines Stage logical zero;
- verify all locally required edges (matrix, Stage, Zaber, light) are singular and alive before retrying the zero-exposure preflight.

## Tests and publication

Regression-test both accepted recovery boundaries and rejection of altered prefix counts/pose/authorization/UNKNOWN state. Publish candidate results only from the aggregate successful preparation terminal containing retained plus newly completed operations. Report preparation sweeps separately from candidate cycles.
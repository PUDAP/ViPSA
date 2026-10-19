# Re-probe an Earlier Device and Append Until Failure

Use this reference when an operator explicitly returns to an already screened device, asks to re-probe it, reuse its frozen recipe, skip preparation, append prior verified cycles, and continue until the established recipe-specific failure criterion.

## 1. Separate three histories

Keep these distinct:

1. **Original verified history** — completed full SET+RESET cycles that remain scientific evidence.
2. **Original unresolved physical slots** — a dispatched/timeout batch whose exposure is UNKNOWN; preserve permanently and never replay.
3. **New re-probe epoch** — fresh motion/alignment/contact evidence and fresh operation IDs.

Do not clear the original device UNKNOWN latch merely to enable the re-probe. Use a separate append-only retest ledger/namespace that references the original permanent ledger and its hash.

## 2. Dual cycle numbering after an UNKNOWN gap

If the original run has 30 verified cycles and physical slots 31–40 are UNKNOWN:

- the verified ordinal resumes at 31;
- the next physical campaign label begins at 41;
- record both on every metric, operation, and terminal artifact.

This avoids replaying uncertain stress while still satisfying the user's request to append the previous verified cycles. Never relabel physical cycle 41 as if it were the original cycle 31.

## 3. Re-probe motion sequence

1. Verify no active controller owns the campaign.
2. Perform real output-OFF, matrix-open, and error-queue checks.
3. Read the exact current Stage/Zaber pose.
4. Retract before lateral travel.
5. Move to the device's approved absolute nominal target, not a relative offset from the current device.
6. Capture a fresh Camera 1 image.
7. If the current nominal view matches the prior nominal geometry, the prior validated aligned offset may be used as the bounded initial correction; still capture a fresh residual image.
8. Apply only bounded residual corrections and save the pixel residual plus exact encoder pose.
9. Approach only to the prior established prepared/contact Z unless the user separately authorizes new forming/contact search.

A user instruction to reuse preparation means: no forming, no conditioning, and no preparation-derived stress replay.

## 4. Frozen recipe authority

Load the exact durable recipe from a verified completed batch or publication artifact. Preserve:

- candidate and request IDs;
- ordered voltage arrays;
- endpoint, step, dwell, NPLC, ranges, and compliances;
- continuous-output policy;
- health-read operation;
- failure criterion.

Do not mutate optimizer state or publish a new recipe for a manual earlier-device retest.

## 5. Controller recovery after temporary orchestration cleanup

Campaign closure may legitimately delete temporary helper modules. Do not pretend stale `/tmp` authority still exists.

Rebuild a dedicated controller from durable artifacts and currently installed adapters. Before hardware dispatch:

1. test the rebuilt native result validator against a saved successful batch;
2. reproduce a historical metric exactly (both polarity ratios and failure signal);
3. verify the live loaded driver hash, not only the file hash;
4. require the re-probe pose, REAR terminals, empty errors, output OFF, and matrix open.

This offline historical-reproduction test is the acceptance test for a rebuilt metric/parser path.

## 6. Durable intent and dispatch boundary

Write unique operation intents before connecting the DUT route. Track a `dispatched` flag that changes only immediately before invoking the stress-bearing acquisition command.

- A fault before dispatch is zero exposure/non-counted when the wire journal confirms no acquisition command was sent.
- A fault after dispatch is UNKNOWN unless native evidence proves zero exposure under the full reconciliation rule.
- Do not mark every preflight failure UNKNOWN merely because intents were created.
- Never reuse operation IDs, even for a proven zero-exposure retry.

Use the canonical matrix token parser (`closed_channels` or equivalent). Matrix firmware may delimit routes with commas or semicolons; hand-written `split(',')` parsing can reject a valid route. A parser rejection before the acquisition command is a zero-exposure control fault, not a hardware fault.

## 7. Batch execution and stopping

Use fresh 10-cycle continuous-output batches when required by the frozen recipe:

- exact native point count;
- one output-ON interval and one final OFF transition;
- all source-status points ON;
- exact segment order and arrays;
- health check after each completed batch;
- final output-OFF/matrix-open/error-empty cleanup.

Evaluate only full verified SET+RESET pairs. Preserve the original consecutive-failure rule. If the recipe batches 10 cycles continuously, a failure recognized inside the batch cannot stop stress already programmed in that same native interval; classify and stop at the batch boundary.

For an explicit **until-failure** retest, do not silently reapply an old screening cap unless the user asked to retain it. Mandatory safety, cleanup, nonfinite-energy, and UNKNOWN-exposure faults still stop fail-closed.

## 8. Required artifacts

- motion journal and exact source/target/readback poses;
- fresh alignment images and residual record;
- re-probe/approach record stating preparation was not repeated;
- frozen recipe copy per attempted batch;
- separate retest ledger with original-history references;
- wire journal, execution claim, native result, per-cycle metrics, health record, and terminal record;
- zero-exposure reconciliation records for pre-dispatch attempts;
- final plot that clearly distinguishes original verified cycles, original UNKNOWN physical slots, and re-probe verified cycles.

## Verification checklist

- [ ] Original 30 verified cycles preserved.
- [ ] Original UNKNOWN slots preserved and not replayed.
- [ ] No forming or conditioning repeated.
- [ ] Fresh alignment residual is within gate.
- [ ] Exact previous prepared/contact Z used.
- [ ] Rebuilt parser reproduces a saved historical metric.
- [ ] Canonical route-token parser used.
- [ ] Pre-dispatch versus post-dispatch faults are classified correctly.
- [ ] Fresh IDs and physical labels are monotonic beyond uncertain slots.
- [ ] Output OFF, matrix open, and errors empty at every batch boundary.

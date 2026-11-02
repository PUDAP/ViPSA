# Continuous batched device progression and monitor scope

Use this reference for later-device progression in an adaptive ViPSA campaign where preparation is separate from candidate testing and candidate SET/RESET cycles run in continuous 10-cycle batches.

## Scope separation: campaign vs monitor

A status cron/reporter is observational and is not the measurement campaign. If the user says **stop/remove the cron job**, stop only the named monitor. Do not cancel, pause, or reinterpret a separately authorized device start unless the user also says to stop the hardware/campaign. Conversely, a hardware stop must include runner termination and verified electrical cleanup; removing a reporter alone does not stop acquisition.

When an out-of-band correction interrupts setup, cancel only actions that conflict with the correction. Do not erase an unrelated still-valid instruction.

## New-device sequence

1. Verify the previous device has terminal cleanup, no UNKNOWN state, output OFF, and matrix open.
2. Verify the next device is ledger-pristine.
3. Bind travel to a fresh live source pose and the approved absolute grid target.
4. Execute the campaign travel order: safe Z retract, absolute Zaber XY, Camera-1 alignment, bounded residual correction, then pre-approach. Optical alignment is not contact.
5. Run forming-as-approach at the pre-approach Z; advance only by the authorized `Z+5` step after a failed operational-contact criterion. Stop on sustained operational contact or the bounded attempt limit.
6. Run all fixed conditioning sweeps. Carry the stress counter through forming and conditioning and insert configured health reads at exact boundaries.
7. Verify the preparation terminal against the permanent ledger before publishing the next deterministic candidate.

Forming and conditioning belong to the preparation terminal/receipts. Their absence from a candidate-batch terminal is expected and is not evidence that forming was skipped.

## Revisit/retry sequence

For a previously tested device that is fully retracted and revisited:

- preserve original preparation, candidate, failure, and energy history immutably;
- create a separate revisit navigation/alignment record;
- re-establish operational contact with forming-as-approach rather than calling the device pristine;
- run the configured recovery conditioning tail (five sweeps in the validated CsFAPbI3 campaign pattern);
- use a separate retry epoch with fresh execution/operation IDs and retry-local cycle numbering;
- do not mix retry metrics or plots with original cycles;
- preserve the original recipe-specific-failure result even if the retry is requested explicitly.

A failure before candidate IDs are allocated can be retried only after wire evidence proves no continuous command was sent, the ledger gained no retry operations, UNKNOWN remains false, and cleanup is verified.

## Continuous candidate batches

Before each candidate device:

- compile and validate the exact optimizer recipe;
- prove every SET/RESET native array output-OFF, including exact count, stored representation, compliance, and driver identity;
- verify current pose, terminals, empty instrument error queue, driver capability/hash, owner lock, output OFF, and matrix nil;
- run one fresh process per bounded 10-cycle batch;
- keep output ON through SET/RESET branches and cycles, changing configuration at zero-volt boundaries;
- run a health read after every complete 10-cycle batch;
- continue automatically until the configured consecutive recipe-failure rule fires or the 100-cycle cap is reached;
- classify a cap survivor as right-censored, never as a failure.

For every batch, require exact native point count, 20 segments, one ON and one final OFF transition, source-status ON at every measured point, monotonic global native timestamps, complete branch receipts, and verified cleanup.

## Regression fixture requirements

When the continuous driver evolves, update offline fakes to model the real native contract. In particular:

- answer source/measure configuration-list size queries;
- return trigger-model readback with the exact two single-list `CONFIG_NEXT` identities and block numbers;
- return the real terminal trigger state (for the validated model, `IDLE;IDLE;10`);
- model the current output-ON/OFF block numbers;
- use one globally monotonic timestamp/index sequence across all segments, not timestamps restarted per segment;
- include source-status/output-on and native trace-window fields expected by the adapter.

A stale fake failure is not a reason to bypass tests. Patch the fixture to the current verified contract, rerun driver and adapter tests, then perform live output-OFF proofs.

## Final verification and reporting

Compute totals programmatically from the ledger and batch summaries. Cross-check declared operation, branch, health, segment, and point counts. Generate separate preparation and candidate artifacts. For a 100-cycle survivor, the final plot title and terminal language must explicitly say **right-censored survivor**. Finish with an independent output-OFF/matrix-nil/error-queue check.
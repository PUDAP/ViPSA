# Unknown Exposure and Continuous-Batch Recovery

Use this reference when a long instrument campaign loses transport after dispatch, especially for a native continuous multi-list batch.

## Evidence classification

- Preserve terminal, wire journal, frozen recipe, operation IDs, and cleanup evidence before retrying anything.
- Decode the wire journal and distinguish **request sent** from **native success reply received**.
- A dispatched command with no native reply is unresolved exposure even when the ledger contains zero rows. Zero rows alone never prove zero exposure.
- Classify zero exposure only from positive pre-execution evidence: rejection before INIT/output enable, trigger compilation failure before the ON block, or equivalent preserved native proof.
- Never replay an unresolved batch. Keep its operation intents UNKNOWN and exclude them from verified cycle/point totals.

## Fail-closed recovery

1. Pause autonomous progression while output/matrix safety is unverifiable.
2. Independently force and verify matrix open/`nil` when possible.
3. For stale PUDA command state (`RUN_ID_MISMATCH`), reset only the affected machine state; do not restart shared messaging infrastructure.
4. If an edge disappears, recover only that edge service.
5. Require a fresh proof of output OFF, matrix open, and empty instrument error queue.
6. Keep hardware-safe recovery separate from DUT-exposure classification: OFF/open now does not prove zero prior exposure.

## Quarantine and wider-campaign continuation

After safety is restored:

- Retain every earlier COMPLETE cycle and health operation.
- Preserve unresolved intents and the device UNKNOWN flag.
- Plot only completed, non-superseded cycles.
- Record a quarantine acknowledgement with verified cycles/points, UNKNOWN intent count, fault artifacts, and fresh safety proof.
- Append that acknowledgement to optimizer/handshake history before clearing the active request.
- Advance to the next device only when policy allows; never clear UNKNOWN merely to make progression easier.

## Continuous multi-list invariants

When a batch exceeds the instrument’s per-list capacity:

- Split deterministically into lists that each satisfy the native limit.
- Keep one continuous output-ON interval across all lists and exactly one final OFF transition.
- Validate all global trace slices and source-status rows.
- Derive the final trigger block from the generated program instead of hard-coding its number.
- Regression-test the real driver → adapter → runner receipt shape before stress.

## Interrupted preparation

If preparation fails after retained sweeps:

- Do not replay COMPLETE forming/conditioning sweeps.
- Read live pose before resuming; the next guarded motion may have completed before the electrical command failed.
- Resume at the first missing electrical operation, skipping any already-executed motion.
- Seed sweep counters, health cadence, and final bookkeeping from retained receipts.

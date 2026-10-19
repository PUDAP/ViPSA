# Earlier-device re-probe with retained cycles, UNKNOWN gaps, and user truncation

## Trigger
Use when an already-tested device is physically revisited, prior verified cycles must be retained, one or more dispatched batches have unresolved exposure, and the operator later requests a physical-cycle truncation boundary.

## Separate three counters
Maintain distinct, explicit counters:

1. **Physical cycle slot** — monotonically increases for every dispatched candidate slot, including UNKNOWN exposure.
2. **Verified-cycle ordinal** — increases only after a complete SET+RESET pair with validated native evidence.
3. **Batch/attempt index** — identifies transport attempts; zero-exposure attempts and UNKNOWN attempts remain in history but are not scientific cycles.

Never reuse an UNKNOWN physical slot. After an UNKNOWN 31–40 batch, the next dispatch begins at physical slot 41 even though the verified ordinal resumes at 31.

## Re-probe semantics
- Preserve prior preparation and candidate evidence; do not repeat forming or conditioning when the operator explicitly requests appending to the retained cycles.
- Re-probe under a fresh motion/alignment namespace: safe retract, absolute nominal target, fresh Camera-1 alignment, bounded residual correction, then approach only to the previously established prepared/contact Z.
- Record the new aligned X/Y and contact Z separately from the original pose.
- Keep optimizer/initial-screen records unchanged unless the user separately authorizes a new optimization-data version.

## Pre-dispatch versus post-dispatch failures
- A route/parser or other pre-dispatch failure can be reconciled as zero exposure only when the wire journal proves the acquisition command was never sent, cleanup is independently verified, and the original attempt remains recorded as non-counted.
- A timeout, disconnect, cancellation, or user stop after acquisition dispatch is UNKNOWN unless complete native rows are recovered. Preserve every intended branch as UNKNOWN and continue only at the next unused physical slots.
- Final cleanup proves present safety; it does not retroactively prove zero exposure.

## User truncation while a batch is active
When the operator says to stop at physical cycle `N` after a later batch has already been dispatched:

1. Persist a STOP/no-further-dispatch sentinel first.
2. Stop the supervisor and active batch/edge without issuing another waveform.
3. Mark the entire in-flight dispatched range UNKNOWN; do not claim it ended at `N` and do not replay it.
4. Restore instrument communication and obtain fresh output-OFF, matrix-open, error-queue, driver-fingerprint, and pose evidence.
5. Close the scientific analysis at physical slot `N`.
6. Explicitly list any dispatched slots greater than `N` as post-boundary UNKNOWN and exclude them from the truncated plot/table.

## Plotting a truncated run
- Emit PNG plus CSV.
- CSV has one row for every physical slot `1..N`; UNKNOWN slots have null metrics and an explicit status.
- Plot only verified ON/OFF values, shade UNKNOWN ranges, and use `NaN` gaps so lines never bridge unmeasured intervals.
- Mark the truncation boundary and state verified-cycle count separately from physical-slot count.
- Do not classify failure unless the configured consecutive-failure rule is satisfied by consecutive verified full cycles.

## Verification checklist
- No controller/supervisor remains active.
- Final output OFF, matrix open, errors empty, pose recorded.
- Prior verified cycles retained exactly once.
- Every zero-exposure and UNKNOWN attempt preserved with operation IDs and wire evidence.
- Physical slots, verified ordinals, and analysis boundary agree across ledger, terminal record, CSV, and plot.

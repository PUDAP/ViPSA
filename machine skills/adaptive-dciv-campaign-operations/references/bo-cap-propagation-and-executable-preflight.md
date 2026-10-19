# Later BO batch cap propagation and executable preflight

Use when an already validated optimizer proposal is authorized with a revised hard-cycle cap.

## Cap propagation

A policy-only cap change must be represented consistently in three enforcement layers:

1. the frozen per-device recipe policy;
2. the candidate controller's terminal/right-censor condition; and
3. the supervisor's completed-batch stop condition.

Search generated controllers for stale literals from the previous cap. Keep batch size, minimum-cycle gate, health cadence, failure rule, and no-replay semantics unchanged unless the operator separately changes them.

## Executable schema preflight

Syntax compilation is insufficient. Before motion or bias:

1. Import the generated candidate controller in the real execution environment.
2. Call its real `initial_ledger` against the frozen recipe and manifest.
3. Build the first batch's real segments.
4. Verify required manifest compatibility fields such as `batch_id`.
5. Verify source-row/binding index, candidate ID, recipe hash, preparation-terminal hash, exact SET/RESET point counts, total points, and revised hard cap.
6. Verify the supervisor and candidate controller agree on the cap.

If this preflight fails, repair only the immutable execution manifest/controller compatibility before hardware action; do not regenerate optimizer candidates or silently alter recipe parameters.

## Device assignment

Audit occupancy across all campaign namespaces, then use the authoritative absolute-grid map. Do not infer eligibility from the immediately preceding BO directory or calculate coordinates by adjacent motion. Preserve proposal row order when mapping candidates to the next eligible physical sequence.

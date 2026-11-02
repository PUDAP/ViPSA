# Acquired-but-uncommitted stress and authorized routine recovery

## Resume from raw evidence, not summary counters

A native sweep may return its complete trace and save raw JSON plus CSV, then fail on the error-queue read before the summary commits the operation. An `intent` label or one-short operation counter does not mean the sweep was unexecuted.

1. Compare raw response and ordered CSV to the exact planned list: record count, phase/cycle, commanded trajectory, measured current/voltage/time and finiteness.
2. If fully matched, recover a ledger entry as `completed_verified_acquired_before_postprocessing_failure`.
3. Preserve missing post-operation checks as a caveat; do not claim a successful error-queue check.
4. Resume at the next operation, preserving original sources and indexes in a fresh linked continuation.
5. If a pre-sweep position guard failed instead, prove no stress command was serialized/submitted before treating the operation as not started.

Validated examples: an interrupted current-device test resumed at cycle 9 RESET after eight complete pairs plus cycle 9 SET; forming and conditioning were not repeated. A later run saved all 161 RESET records but stopped during an error-queue query before committing the operation. The raw trace, not the stale intent marker, establishes the acquired boundary. Do not describe a subsequently proposed continuation as validated until it is actually launched and verified.

## Authorized routine repair

When the user explicitly authorizes fixing standard control errors and continuing, do not repeatedly request permission for each routine stale-session recovery. Establish exclusive ownership and inactive manual controls first. Complete the exact orphaned run when possible, then verify fresh cleanup and unchanged XYZ. Restart only an affected stale/offline edge if needed and authorized; do not restart healthy services merely because cached discovery disagrees.

A stale Zaber session was successfully completed without coordinate reset or motion, followed by a fresh matching XYZ handoff and acquisition of the first missing conditioning RESET. This is the validated recovery pattern—not blanket reset/home or automatic sweep replay.

Use a small bounded retry budget for read-only/idempotent cleanup. Error-queue reads drain state: preserve acknowledged responses and annotate lost-reply uncertainty. Do not retry motion or stress when execution could be unknown. Broad repair authorization does not bypass collision, hard limits, failed cleanup or unknown routing.

## Launch/status reporting

A child-agent launch claim requires parent verification of the exact fresh summary and live PID. A delayed failure notification for the superseded attempt is not a failure of the active retry: compare handles/runpaths and read current artifacts. Report preparing, running, and completed distinctly; counts come from fully acquired SET/RESET pairs, not intent markers.

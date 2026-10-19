# Initial-design campaign fault-boundary checklist

Use this checklist when an autonomous per-device campaign must continue through recoverable infrastructure faults without replaying electrical stress.

## Before retrying or advancing

1. Classify the interrupted operation from durable evidence, not wrapper exit code:
   - complete native response with exact points/segments: retain and do not replay;
   - pre-execution rejection with no hardware action: zero exposure may be reconciled;
   - command intent with no native reply: preserve UNKNOWN and never replay.
2. Restore hardware safety with explicit output `0`, matrix `nil`/open, and empty instrument errors.
3. If harmless commands return `RUN_ID_MISMATCH`, reset only the affected PUDA machine state; do not restart NATS or unrelated edges.
4. For preparation, read live Stage-Z and Zaber X/Y. A guarded motion may have completed before the next sweep failed; resume the missing sweep at the live pose without repeating that move.
5. For an UNKNOWN candidate batch, quarantine the physical device at the last fully verified cycle boundary and continue only on a fresh device after safety is proven.

## Evidence and bookkeeping

- Preserve terminal, progress, frozen recipe, execution claim, wire journal, and all operation IDs.
- Decode wire `raw_b64` envelopes programmatically using the actual native command name.
- Plot only complete nonsuperseded cycles and label the verified range.
- Keep UNKNOWN intents permanent and separate from complete branch/native-point/health totals.
- Advance runner cursor and optimizer handshake together: append the acknowledgement/history record, clear active/pending, and fsync both stores under their locks.
- For a recipe-specific stop after multiple batches, aggregate every completed batch and record the actual final cycle and consecutive failure cycles; do not use a one-batch template.

## Reporting

State the verified completed range, unknown or zero-exposure intents, what was not replayed, fresh safety readbacks, classification, and next physical device.

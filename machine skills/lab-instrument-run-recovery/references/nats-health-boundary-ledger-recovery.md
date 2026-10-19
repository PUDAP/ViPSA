# NATS-interrupted health-boundary recovery

## Trigger

Use when a continuous electrical batch completes all candidate branches, but its post-batch health read or cleanup becomes `UNKNOWN` because NATS disconnects or times out.

## Verified recovery pattern

1. Stop/pause autonomous continuation so no later batch or device starts against an UNKNOWN ledger.
2. Preserve the completed candidate batch. Validate from native evidence:
   - expected and actual point counts match;
   - all expected SET/RESET segments exist;
   - source-status evidence is ON for measured points;
   - exactly one output-ON and one final output-OFF transition are retained;
   - every candidate operation is `COMPLETE`.
3. Classify the health operation from its durable record:
   - **Measurement completed, cleanup acknowledgment lost:** valid raw response and rows exist, but cleanup verification failed. Do not reacquire. Reconcile only after later batch cleanup plus a fresh independent OFF/open/error proof.
   - **Failed before hardware action:** no raw response, zero rows, and transport failed while connecting/before dispatch. Record the abandoned intent as zero-exposure; do not pretend it was a completed health measurement. Execute one separately identified replacement health read after control and safety are restored.
   - **Possible partial stress:** any ambiguous dispatch or incomplete response remains UNKNOWN and requires explicit operator authorization before repetition.
4. Repair only affected edge ownership. For PUDA edges stuck after reconnect (for example queue pulls failing after NATS interruption):
   - map each process PID to its working directory;
   - stop only the affected instrument edge processes;
   - start exactly one replacement process per edge using the same deployment and configuration;
   - do not restart NATS, stage, Zaber, camera/light, or unrelated instruments.
5. Verify each replacement edge reports fresh subscriptions plus `idle` and `run_id: null`.
6. Run a harmless independent safety proof: force output OFF, open matrix, read output `0`, read channels `nil`, and read an empty instrument error queue.
7. Reconcile ledger state atomically with evidence paths/hashes. Never delete or overwrite the original failed cleanup or transport record.
8. Resume from the first genuinely missing boundary. Never replay completed candidate cycles.
9. At a cycle cap, finalize only after the required replacement health read succeeds and cleanup is verified.

## Artifact expectations

Retain:

- original batch terminal and continuous summary;
- original UNKNOWN operation record;
- edge-restart evidence/log excerpts;
- fresh independent OFF/open/error proof;
- reconciliation classification (`cleanup_ack_lost` or `zero_exposure_before_dispatch`);
- replacement health receipt when required;
- final completion record linking all recovery artifacts.

## Important distinction

A batch terminal may say `fault` even when all candidate cycles are scientifically complete. Do not equate process exit code with missing candidate data. Decide from native points, segments, operation ledger, health record, and cleanup evidence.

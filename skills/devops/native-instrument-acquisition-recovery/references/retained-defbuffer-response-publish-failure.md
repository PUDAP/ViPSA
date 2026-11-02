# Recovering a completed continuous batch from retained `defbuffer1`

Use when a Keithley 2450 continuous trigger-model acquisition finishes on the instrument, but the edge cannot publish the native response because NATS disconnects or times out.

## Required evidence

Do not use this path unless all are true:

- The exact dispatched request and run ID are present in the wire journal.
- The edge log shows the command handler reached idle/completion before response publication failed.
- The ledger marks the batch UNKNOWN after the original caller times out; no replay has occurred.
- The SMU remains connected and no later command has cleared/reset `defbuffer1`.

If a complete matching published response exists, prefer ordinary exact-response reconciliation. This buffer path is for the narrower case where publication failed before the response envelope was logged.

## Procedure

1. Let the original request reach its timeout so its exception/finally path preserves UNKNOWN history and attempts cleanup. Do not kill it early unless an active hazard requires emergency shutdown.
2. Stop only the idle 2450 edge by verified PID and CWD. Do **not** USB-reset, `*RST`, `:TRAC:CLE`, or replay the recipe.
3. Open the same VISA resource directly. Issue `:ABOR` and `:OUTP OFF`; these must not clear `defbuffer1`.
4. Query and require:
   - matching 2450 identity;
   - `:OUTP?` = OFF;
   - `:ROUT:TERM?` = REAR;
   - `:TRIG:STAT?` begins `IDLE;IDLE;`;
   - `:TRAC:ACT? "defbuffer1"` equals the exact expected point count.
5. Read trace windows with:

   ```text
   :TRAC:DATA? start,end,"defbuffer1",SOUR,READ,REL,SOURSTAT,STAT
   ```

6. Validate every row:
   - five fields per point;
   - finite values;
   - strictly increasing `REL` time;
   - `SOURSTAT` includes source-readback bit 3 (`& 8`);
   - `SOURSTAT` includes output-on bit 7 (`& 128`);
   - point count and order match the exact flattened dispatched voltage arrays.
7. Drain and require an empty instrument error queue. Save raw trace windows, reconstructed rows, run ID, hashes, and explicit `recovered_from_retained_instrument_buffer=true`, `no_replay=true` provenance.
8. Restart the protected edge without USB reset. Independently require output OFF, matrix open, empty errors, correct driver hash, unchanged pose, and lights off.
9. Under the controller lock, atomically reconcile only the matching UNKNOWN batch and operations. Preserve each prior UNKNOWN record under `original_fault_history`; charge recovered energy exactly once.
10. Run the mandatory post-batch health check. Continue only if it and cleanup verify and the configured failure rule is not met.

## Why this is valid

The trigger-model driver reads and validates all native points before returning to the edge handler. An edge transition back to idle followed by `Error publishing command response` proves execution returned to the transport layer. The retained buffer independently supplies the scientific rows and native source/output status. Together with fresh OFF/open/error/pose proof, this supports no-replay reconciliation without inventing a response envelope.

## Stop conditions

Keep UNKNOWN and do not continue if the buffer count differs, timestamps are nonmonotone, source/output status is missing, the buffer was cleared, a later acquisition ran, output cannot be proved OFF, matrix cannot be proved open, errors remain, or pose changed unexpectedly.

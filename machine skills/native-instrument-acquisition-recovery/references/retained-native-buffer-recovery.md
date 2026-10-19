# Retained native-buffer recovery after response loss

Use this workflow only when a native acquisition was dispatched, the instrument handler finished, but the transport failed while publishing the response. It is a **reconciliation path, not a replay path**.

## Preconditions

- Keep the affected batch `UNKNOWN`; do not count it or dispatch a replacement.
- Let the original client reach its configured timeout so its `finally` cleanup and durable UNKNOWN bookkeeping run normally.
- Prove from the edge log that the intended command/run was received and that execution reached handler completion before response publication failed. A dispatch marker alone is insufficient.
- Confirm the native method stores its complete trace in a persistent instrument buffer and that no later command has reset or cleared that buffer.

## Recovery sequence

1. Preserve the exact dispatched request from the wire journal, including run ID, ordered segments, parameters, and expected native point count.
2. Stop only the **idle** instrument edge. Do not USB-reset, initialize, reset, or clear the instrument.
3. Open the existing instrument resource directly and issue only bounded recovery/safety operations:
   - abort any inactive trigger model;
   - force output OFF;
   - query identity, terminals, trigger state, trace count, and error queue;
   - read the retained native trace in bounded windows.
4. For Keithley 2450 trigger-model batches, read `defbuffer1` using native fields `SOUR, READ, REL, SOURSTAT, STAT`.
5. Validate all of the following before accepting anything:
   - exact expected point count;
   - every value finite;
   - strictly increasing native relative timestamps;
   - native source-readback status present at every point (`SOURSTAT` bit 3);
   - output-ON status present at every acquired point (`SOURSTAT` bit 7);
   - reconstructed commanded-voltage sequence exactly matches the dispatched request;
   - trigger is idle, output is OFF, terminals are correct, and the error queue is empty.
6. Save the raw native windows, reconstructed result, extraction proof, and SHA-256 before restarting the edge.
7. Restart the protected edge **without a USB reset**, then independently verify output OFF, matrix open, empty errors, protected-driver hash, unchanged pose, and no active motion.
8. Atomically reconcile the ledger:
   - preserve the original UNKNOWN operation/batch objects under `original_fault_history`;
   - mark recovered operations COMPLETE only from the validated retained trace;
   - record `recovered_from_retained_instrument_buffer: true` and `no_replay: true`;
   - update energy, metrics, latest terminal record, and reconciliation proof together;
   - clear the UNKNOWN latch only after the atomic commit verifies.
9. Run the mandatory post-batch health measurement and OFF/open cleanup before starting the next batch.

## Fail-closed conditions

Keep the exposure UNKNOWN and stop if the buffer is absent, has the wrong count, was modified by a later command, has nonmonotone timestamps, lacks source/output status, disagrees with the exact request, or any safety/pose/cleanup proof fails. Never reconstruct missing points, infer completion from elapsed time, or replay the batch automatically.

## Proven pitfall

Do not restart or USB-reset the edge before extracting the retained trace. The instrument buffer may be the only independently recoverable copy after a publish timeout.
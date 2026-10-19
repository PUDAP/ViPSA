# Continuous-Output DCIV Batches

Use this mode when the operator requires Pratap-style candidate sweeping: electrical continuity across SET/RESET sides and successive cycles is part of the experiment.

## Required sequence

1. Freeze the device-specific SET/RESET arrays, per-side compliances, point dwell, NPLC, cycle count, and health cadence.
2. Prove the complete native batch while output is OFF. The proof must cover every voltage point, segment boundary, compliance transition, expected count, and deployed driver hash.
3. Reserve energy and create one ledger intent for the whole electrically atomic batch. Preserve segment and cycle identifiers inside that operation.
4. Route once and turn output ON once.
5. Execute SET, change compliance in place at the zero-voltage side boundary, execute RESET, and continue into the next cycle without output-OFF cleanup or matrix opening.
6. After the requested number of complete SET+RESET cycles—ten when specified—end the batch, force output OFF, open the matrix, read back OFF/nil, and drain instrument errors.
7. Perform the health check only at the full-cycle batch boundary, not every ten individual sweeps.
8. Write native rows and per-cycle metrics durably, then mark the batch COMPLETE and compact it.

## Controller compatibility gate

Do not reuse branch-isolated adapters unchanged. A controller is incompatible if it:

- calls cleanup after each SET or RESET side;
- opens the matrix or verifies output OFF between sides/cycles;
- starts a fresh process per cycle;
- records each side as independently replayable after continuity has begun;
- schedules health by individual stress-sweep count when the operator specified full-cycle cadence.

Pause before electrical dispatch until a driver command and ledger model represent the complete continuous batch atomically.

## Safety and recovery

- Cleanup still runs on normal batch completion and every exception/cancellation path.
- A process loss during an output-continuous batch is an UNKNOWN batch unless native trace/guard evidence proves an exact completed prefix and verified shutdown. Never resume from a guessed side or cycle.
- Preserve per-point compliance provenance and segment boundaries so SET/RESET plots and energy accounting remain separable.
- Recipe-specific stopping is evaluated only after the batch and its health check; it must not interrupt a requested ten-cycle continuous block unless a hard safety/control fault occurs.

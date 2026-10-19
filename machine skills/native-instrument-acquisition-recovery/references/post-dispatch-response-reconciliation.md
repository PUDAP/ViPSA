# Recovering post-dispatch transport loss without replay

Use this when a native instrument command was dispatched but the client received `UnexpectedEOF`, timed out, or was terminated before its terminal receipt.

## Evidence-first sequence

1. **Freeze execution.** Stop/retire the parent supervisor before it can retry. Preserve its PID, command line, output directory, wire journal, and durable INTENT records.
2. **Assume UNKNOWN initially.** A post-dispatch transport failure is never zero exposure. Mark the exact operation IDs/physical slots UNKNOWN until stronger native evidence is found.
3. **Search the edge log by run ID.** Match exactly one published response for the original run ID and command name. Cross-check it against the wire journal’s request intent.
4. **Require exact command identity.** Confirm device, segment order, voltage arrays, compliance, dwell, NPLC, point counts, and empty kwargs match the dispatched request byte-for-byte/semantically.
5. **Validate native completion.** Require success status, expected segment and point counts, finite ordered rows, monotonic native timestamps, one output-ON interval where applicable, runtime errors empty, trigger idle, native preproofs valid, and output OFF afterward.
6. **Prove fresh hardware safety independently.** Restart only the affected edge if needed; verify output OFF, matrix open, errors empty, terminals correct, driver hash, and unchanged pose. A successful historical response does not replace a fresh safety proof.
7. **Reconcile—do not replay.** Convert only the matched original INTENT/UNKNOWN operations to COMPLETE, calculate metrics/energy from the retained native response, and keep a nested copy of the original fault/UNKNOWN record. Preserve later zero-exposure lock attempts as separate administrative history.
8. **Run required post-batch health checks.** A recovered candidate batch still needs the same health read and cleanup gates as an ordinary batch.

## Important distinctions

- A client-side EOF can coexist with a complete native acquisition whose reply was published after the client disconnected.
- A lock failure before the dispatch marker is zero exposure and does not consume physical cycle labels.
- Candidate-cycle failure is determined from consecutive complete candidate cycles, not from consecutive health-read results.
- Physical labels and verified ordinals must diverge after a genuinely UNKNOWN dispatched range; never reuse physical labels unless native completion is later proven.

## Edge/USB recovery

If the edge process survives while holding VISA/USB, identify the exact PID by deployment CWD and command line, terminate only that process, verify the USB node has no owner, reset the specific instrument USB ID if the interface is wedged, then launch with the known VISA-capable interpreter. Verify the edge reaches idle before safety readback. Never install/change VISA dependencies during an active campaign merely to make a restart work.

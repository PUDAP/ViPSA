# Long continuous-batch transport recovery and cap-controlled continuation

Use when a long native instrument acquisition outlives its NATS/client connection, or when a campaign hard cap is explicitly extended for a newly frozen batch.

## Exact post-dispatch transport recovery

1. Treat a dispatched command followed by `UnexpectedEOF`/connection loss as **UNKNOWN**, even if local output suggests cycles may have completed.
2. Stop the campaign controller, but do not reset or reopen the instrument before checking retained native state. Preserve the original run ID, wire intent, operation IDs, and expected voltage arrays.
3. Stop only the protected edge process that owns the VISA/USB interface. Do **not** reset USB merely to release ownership; a USB reset can disconnect the instrument or erase the retained buffer.
4. With the edge stopped, read the instrument buffer directly in the known instrument environment. Require:
   - exact expected point count;
   - exact dispatched voltage sequence and segment geometry;
   - monotonic native timestamps;
   - output-on evidence for acquired points;
   - trigger idle after completion;
   - output OFF, expected terminals, and empty error queue;
   - a hash of the retained result.
5. Restart exactly one protected edge **without USB reset**. Obtain fresh output-OFF, matrix-open, empty-error, expected-driver-hash, terminal, and unchanged-pose proof.
6. Atomically reconcile the same operation IDs from UNKNOWN to COMPLETE, charge energy exactly once, preserve the original fault history, set `no_replay=true`, and clear the UNKNOWN latch only after every operation is accounted for.
7. Run the missing post-batch health check separately. Resume only at the next unexecuted batch boundary.

Do not kill a hung controller before its exception handler has latched UNKNOWN unless necessary for safety. If it must be killed, immediately correct any still-`INTENT` dispatched batch and its operations to UNKNOWN/no-replay before inspecting retained data.

## Process-only edge restarts

For a healthy, enumerated Keithley 2450, routine between-batch recovery should restart only the protected edge process. Do not include `usbreset 05e6:2450` in every batch supervisor. Use a USB reset only for a demonstrated stale USB/VISA condition after all owning processes are stopped; verify re-enumeration before starting an edge. If the device disappears from enumeration, do not dispatch and require reconnect/power-cycle.

## Explicit hard-cap extension for a new frozen batch

A hard-cap change is campaign policy, not a recipe-parameter mutation.

- Freeze the new proposal and bind every immutable candidate row to an eligible physical device.
- Put the explicit cap in each recipe binding and the campaign manifest (for example, `maximum_full_cycles: 300`).
- Keep batch size, health cadence, failure rule, and no-replay policy explicit.
- Validate candidate terminal logic and supervisor stop logic against the same cap (`verified_end == cap`; completed batches `>= cap/batch_size`).
- Never retroactively reinterpret a prior 200-cycle survivor as a 300-cycle run. The new cap applies only to the newly authorized namespace unless the user explicitly authorizes continuation of an existing device.
- Before device binding, audit occupancy. Use the authoritative absolute grid map; do not infer adjacent coordinates. Bind only unused positions and retain the grid hash.

## Safe automatic device handoff

After a terminal device boundary:

1. Verify terminal classification, complete cycle count, no UNKNOWN, final health, output OFF, matrix open, and empty errors.
2. Retract by the authorized clearance move before lateral travel.
3. Move to the exact absolute grid coordinate.
4. Apply the retained alignment offset only as a candidate alignment, then verify with camera registration. Same-row moves should show the expected lattice shift on one image axis; next-row moves should show it on the orthogonal axis. Gate on the small residual axis and visually reject wrong-camera/obstruction states. Do not infer contact from imagery.
5. Run preparation, verify cleanup, freeze the preparation hash into the candidate ledger, then dispatch the first bounded batch.

Preparation/forming/conditioning sweeps are not candidate cycles. A device may finish below the hard cap when the configured consecutive-failure criterion is met; hard-cap survivors remain right-censored.
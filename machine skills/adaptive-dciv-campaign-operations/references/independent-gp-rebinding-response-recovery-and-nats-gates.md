# Independent-GP batch rebinding and transport recovery

## Full-precision proposal authority

When the operator replies to a rounded Telegram proposal, locate the proposal's saved CSV and manifest. Validate the CSV hash against the manifest and execute the full-precision rows; never reconstruct recipes from displayed decimals. If the proposal has no candidate IDs, derive deterministic IDs from the proposal hash, row index, and physical device, and record the derivation.

If an earlier device is declared spent, close it explicitly with its verified-cycle count and safe-state evidence, then bind rows one-to-one to the remaining physical traversal. Preserve both proposal order and physical order in an immutable manifest. Example: row 1→Device 59 through row 8→Device 52 after Device 60 is excluded.

## Continuous-batch response-delivery stalls

A client EOF or stuck response does not imply the native acquisition failed. Before killing anything:

1. Match exactly one wire-journal request by run ID, command name, and complete native segment payload.
2. Match exactly one edge-log response with the same run ID and payload.
3. Require success, exact segment/point counts and order, monotonic timestamps, empty runtime errors, native preproofs, and output OFF afterward.
4. Save and hash the response before retiring processes.
5. Stop the supervisor first, then its child, so it cannot advance after recovery.
6. Convert remaining durable INTENT records to UNKNOWN before reconciliation.
7. Restart only the affected edge/USB interface; independently prove output OFF, matrix open, error queue empty, driver identity, and unchanged pose.
8. Commit rows, metrics, and sampled energy exactly once. Attach each operation's original UNKNOWN history and mark `recovered_from_edge_response=true`, `no_replay=true`.
9. Run the required post-batch health read before continuing.

Keep zero-exposure controller/lock attempts as separate non-counted records. Distinguish physical labels from verified ordinals whenever unresolved ranges create gaps.

## Partial NATS outage during preflight

If one or more configured NATS peers accept TCP poorly or fail the NATS handshake, do not infer instrument failure and do not restart local NATS. A preflight that fails before motion/bias is zero exposure only when durable records prove no operation intent and unchanged persisted pose. Preserve optical alignment and the exact pose, fail closed, and retry only after heartbeat discovery plus the full OFF/open/errors/driver/pose gate succeeds. A bounded monitor may wait for recovery, but it must not dispatch hardware while transport health is incomplete.

## Plot-type distinction

A request for an IV/DC-IV plot means commanded voltage versus `log10(|I|)` or log-scale `|I|`, preserving native acquisition order and PF/PB/NF/NB styles. An ON/OFF-versus-cycle figure is a different summary and must not be substituted for the requested IV plot.

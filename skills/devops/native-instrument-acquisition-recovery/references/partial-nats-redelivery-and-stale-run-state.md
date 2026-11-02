# Partial NATS recovery, redelivery, and stale run state

## Recognize partial transport recovery

TCP accept is not a complete NATS health check. A peer may accept TCP while the NATS handshake or JetStream publish still times out. Conversely, heartbeat discovery may omit a required edge that answers direct commands.

Do not restart local NATS merely because remote peers are partial. Preserve any aligned pose and fail closed while direct safety commands cannot complete. Once bounded direct probes work, use them as the authoritative operation gate rather than waiting for complete discovery membership.

## Zero-exposure preflight failure

A preparation/preflight fault is zero exposure only when durable evidence shows:

- no electrical operation intent;
- no motion intent or persisted pose change;
- no pre-approach marker;
- zero forming/conditioning/candidate operations;
- no unresolved earlier exposure.

Save this classification in the failed attempt directory. A fresh attempt is allowed because there is nothing to replay, but only after independent OFF/open/error/pose proof.

## Conflicting lifecycle replies

After transport recovery, one START may be redelivered and produce both `RUN_ID_MISMATCH` and success for the same run ID. Do not immediately conclude that two edge processes exist.

1. Decode raw replies and correlate machine, run ID, lifecycle command, and timestamp.
2. Inspect exact process CWDs and independent parent trees; one launcher parent plus its Python child is one edge.
3. If duplicate independent parents exist, retire only the stale duplicate.
4. If only one edge exists but run state is stale and the CLI reset endpoint is unavailable, restart only that affected edge service.
5. Require a fresh idle/null run state and full direct safety gate before continuing.

Never replay a native acquisition while resolving lifecycle ambiguity. If a complete exact retained native response exists, use the normal retained-response reconciliation path instead.

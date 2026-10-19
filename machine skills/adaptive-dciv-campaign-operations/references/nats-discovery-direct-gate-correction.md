# NATS discovery versus direct safety gates

## Authoritative recovery gate

Heartbeat/discovery membership is advisory. A required edge can be absent from `machine list` while still answering commands, especially for motion and light services. Do not wait indefinitely for every expected name to appear.

After a partial broker outage:

1. Confirm the transport can carry bounded requests.
2. Probe only the edges required for the next operation with harmless commands/readbacks.
3. Require the operation-specific safe gate: electrical output OFF, matrix open, empty/acceptable errors, intended protected driver/capabilities, unchanged mechanical pose, and no active UNKNOWN exposure.
4. Continue when those direct gates pass even if discovery remains incomplete.
5. Never restart local NATS merely because remote peers or discovery are incomplete.

A bounded monitor must issue no hardware commands while direct safety probes fail. Once direct probes succeed, retire an all-machines-discovered monitor rather than letting it block the campaign.

## Conflicting lifecycle replies

After transport recovery, one START may be redelivered and yield both `RUN_ID_MISMATCH` and success for the same run ID. This does not by itself prove duplicate edge processes.

- Inspect exact process CWDs and independent parent trees.
- Correlate every reply by machine, run ID, command, and timestamp in the raw wire journal.
- If only one edge exists and the reset endpoint is unavailable, restart only that affected edge to clear stale run-manager state.
- Repeat the full direct safe-state gate before motion or stress.
- Do not replay any electrical acquisition while resolving lifecycle state.

This correction supersedes any older campaign reference that requires complete heartbeat discovery before direct safe-state probing.

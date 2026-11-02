# Manual jog panel: persistent NATS connection closed

## Diagnosis

For `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-jog-panel/server.py`, the manual client is a persistent nats-py connection on a dedicated asyncio loop thread. Two defects can cause a permanently broken panel:

- `_connect_nats` originally passed `allow_reconnect=False`, so a network drop closes the persistent client permanently.
- HTTP handlers invoke `asyncio.run`, but directly awaiting NATS operations from those request loops violates the persistent client's event-loop ownership.

The bears server also advertises private `192.168.50.6` cluster URLs. Persistent reconnect must retain the configured reachable bears endpoints rather than relying on those advertised routes.

## Safe repair requirements

1. Record GET `/api/status`, original process environment, all six read-only `MACHINE_STATE` KV entries, and a hash of the Stage coordinate JSON before restart. Do not use START, COMPLETE, reset, jog, or electrical commands to validate connectivity.
2. Reconnect options apply only to the persistent client: configured endpoint list, `allow_reconnect=True`, `max_reconnect_attempts=-1`, and suppression of discovered private routes. Installed nats-py may reject `ignore_discovered_servers`; use a persistent-only `Client` subclass filtering `connect_urls` in `_process_info` when required, and retain the pending-publish safety guard in every version path.
3. Disable buffering of non-idempotent jogs during reconnect (`pending_size=0` in nats-py), wait a bounded interval for a connection before publish, and never replay/retry a publish or flush failure. **`pending_size=0` alone is insufficient:** installed nats-py can retain native `_pending` PUB/HPUB frames from before disconnect and flush them on reconnect. A persistent-only client safeguard must discard those pending publish frames on disconnection/reconnect and publish/flush failure, preserving SUB/UNSUB/PING frames and updating `_pending_data_size`. Verify this against an actual disposable local NATS server, not just mocks. An exception does not prove the edge did not receive the command; already-written wire bytes cannot be undone.
4. Marshal complete immediate/queue transactions onto the owning asyncio loop with `run_coroutine_threadsafe` and `asyncio.wrap_future`; do not move NATS client operations between request loops.
5. Expose read-only connection status and a connection+flush health probe that publishes no PUDA hardware messages.
6. Keep an inactive panel inactive. If active, preserve its exact run/session explicitly or stop for approval; never clear edge ownership to recover the UI.
7. Restart only the panel with durable log output and original non-network launch settings. Never restart bears/local NATS or edges as part of this UI-only fix.
8. Verify HTTP root/status/connection health, unchanged session and machine states, unchanged Stage coordinate file, offline fail-closed/no-replay tests, and actual reconnect against a disposable loopback NATS test server.

## Local tools

- Panel interpreter: `/home/amdm/.venvs/align-cv2/bin/python`.
- Disposable test server executable: `/home/amdm/.local/bin/nats-server`; bind to a dynamic loopback port and clean up the test subprocess. Never use the real cluster for deliberate disconnect testing.

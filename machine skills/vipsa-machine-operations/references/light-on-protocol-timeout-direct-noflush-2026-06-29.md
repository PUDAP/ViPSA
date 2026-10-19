# Light-on protocol timeout → direct no-flush fallback (2026-06-29)

Use this note when a simple ViPSA light command is requested, the preferred PUDA protocol path validates but fails at NATS connect/read timeout, and the light edge is still reachable by raw/direct NATS.

## Observed pattern

- A full-metadata one-step protocol with `light.turn_on()` validated successfully.
- `puda protocol run --file ... --nats-servers nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224` failed before command execution with a NATS read/connect timeout.
- An older direct fallback that called `nc.flush()` after publish failed with `nats.errors.FlushTimeoutError` even though direct publish/subscribe transactions were still usable.
- A no-flush direct fallback succeeded by:
  1. connecting to one of `100.109.131.12:{4223,4222,4224}` with `allow_reconnect=False`,
  2. subscribing to `puda.light.cmd.response.immediate` and `.queue`,
  3. sleeping briefly after subscriptions instead of flushing,
  4. publishing `start` to `.immediate`, waiting for a matching `start` success,
  5. publishing `turn_on` to `.queue`, waiting for matching `turn_on` success with `data.result: true`,
  6. publishing `complete` to `.immediate`, waiting for matching `complete` success.
- If the direct helper imports `nats` but the active Python environment does not have `nats-py`, run it ephemerally with `uv run --with nats-py python <helper.py> turn_on`; do not modify the system Python environment during an active hardware session.
- Final verification used the CLI with a single known-good server override:
  `timeout 8 puda --nats-servers nats://100.109.131.12:4222 machine state light`
  and confirmed `state: idle`, `run_id: null`.

## Reusable rule

For simple light commands, stay protocol-first. If protocol-run is blocked by the known NATS advertised/reconnect timeout but raw edge responses still work, use a short direct fallback that avoids `flush()` and gates success on real matching responses. Do not report the light command as done unless the queued command response is `success` and final state is verified idle/null-run.

## Minimal reporting

Report:

- protocol path blocked by NATS timeout, if applicable
- fallback method used: direct NATS no-flush
- command response: `success`, `result: true`
- final state verification: `idle`, `run_id: null`

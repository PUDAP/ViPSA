# One-off ViPSA light command when the edge requires an active run

Use this pattern when `puda machine run light turn_on` (or `turn_off`) is rejected with `Send START command to start a run before sending commands`.

## Preconditions

1. Use the bears NATS cluster: `nats://bears:4222,nats://bears:4223,nats://bears:4224`.
2. Confirm `light` appears in `puda machine list --json`.
3. Inspect `puda machine state light`; proceed only from `idle` with `run_id: null`, unless intentionally recovering a known run.
4. Confirm the command exists with `puda machine commands light`.

## Safe transaction

Generate one non-empty UUID and reuse it for all three calls:

```bash
export NATS_SERVERS='nats://bears:4222,nats://bears:4223,nats://bears:4224'
RUN_ID=$(tr -d '\n' </proc/sys/kernel/random/uuid)
test -n "$RUN_ID" || exit 1

puda machine start light --run-id "$RUN_ID"
rc=0
puda machine run light turn_on --run-id "$RUN_ID" || rc=$?
puda machine complete light --run-id "$RUN_ID" || true
puda machine state light
exit "$rc"
```

Substitute `turn_off` only when requested. The final state must be `idle` with `run_id: null`.

## Pitfalls and recovery

- Do not omit `--run-id` on any of the three calls. Each omitted/empty value causes the CLI to generate a different UUID, producing `Run ID mismatch` and potentially leaving the edge active.
- Validate `RUN_ID` before START. Never continue with an empty variable.
- If a failed attempt leaves the machine active, read the live `run_id` from `puda machine state light`, send `puda machine complete light --run-id <that-exact-id>`, and verify idle before retrying.
- A successful command response proves the edge accepted the light action; the final state check verifies run cleanup. Report both concisely.

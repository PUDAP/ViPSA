# Manual stage Z and light commands — 2026-06-24

Session pattern for terse Telegram hardware commands such as `move z down by 30 steps`, `move stage up by 120 steps`, and `turn the lights on`.

## Confirmed operational pattern

- Load/consult the ViPSA machine operations flow and use PUDA protocol-first control.
- For stage Z-only movement, user convention remains:
  - `down` -> negative `height`
  - `up` -> positive `height`
  - keep `feedrate: 450` unless the user specifies otherwise
- Before active motion, verify the active env and that `stage` is `idle` with `run_id: null` using a bounded state check (`timeout 3 puda machine state stage`).
- Run a one-command full-metadata protocol from `/home/vipsa/vipsa-puda-project`:
  - `stage.move_z_by(height=<signed_steps>, feedrate=450)`
- Verify by running a **separate** one-command position protocol:
  - `stage.get_current_position()`
  - report the returned `response.data.result` exactly, e.g. `[0, 0, -30]`, `[0, 0, -50]`, `[0, 0, 70]`.
- Final verification should include `stage` state returning to `idle`, `run_id: null`.

## Explicit OpenFlexure X/Y jogs

The normal safeguard remains: never move OpenFlexure `stage` X or Y unless the user explicitly names the axis and movement. Once they do, map signed step requests directly to the axis method:

- Y up / `+N` → `stage.move_y_by(steps=+N)`
- Y down / `-N` → `stage.move_y_by(steps=-N)`
- equivalent explicit X requests → `stage.move_x_by(steps=<signed N>)`

For an ordered sequence such as “Y +10, then -15,” preserve that order in one full-metadata protocol with sequential `move_y_by` commands. Only after all movement steps succeed, run a separate `get_current_position()` protocol and verify final `idle`, `run_id: null`. Report each commanded leg, net displacement, and exact `[x,y,z]` readback. Do not infer physical motion solely from tracked coordinates if the user reports that the motor did not move.

## NATS retry note

If the movement protocol succeeds but a follow-up position-read protocol fails to connect to one member of the configured NATS cluster (example: `dial tcp 192.168.50.6:4223: i/o timeout`), retry the readback once with a single known working ViPSA server override, for example:

```bash
puda protocol run --file /tmp/stage_pos.json --nats-servers nats://100.109.131.12:4223
puda --nats-servers nats://100.109.131.12:4223 machine state stage
```

Do not report position unless the retry returns a real `get_current_position` response. If only the move succeeded and readback remains blocked, report the motion success separately from the missing position readback.

## Direct raw-NATS fallback for stale stage run / CLI route failure

When `puda protocol run` fails because the NATS cluster advertises an unreachable private route (for example `dial tcp 192.168.50.6:4224: no route to host`) or `puda machine state stage` hangs, use the direct-NATS command path from `references/direct-nats-command-path-and-align-approach-edge-2026-06-09.md` rather than retrying the same CLI loop. If a fresh `start` returns `RUN_ID_MISMATCH` with an exact currently-running run id, publish `complete` for that exact run id first, then retry the stage command. A raw socket NATS client may be more reliable than `nats-py` if `nats-py` `flush()` times out despite TCP connectivity.

## Light-on pattern

For terse `turn the lights on`, use a one-command full-metadata protocol:

```json
{"step_number": 1, "name": "turn_on", "machine_id": "light", "params": {}}
```

Verify `response.status: success`, `response.data.result: true`, then confirm `light` returns to `idle` with `run_id: null`. Keep the user-facing result terse: `Lights on` plus the two verification bullets.

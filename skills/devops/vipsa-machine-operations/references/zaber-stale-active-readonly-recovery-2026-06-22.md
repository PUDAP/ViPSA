# Zaber stale-active/error recovery with read-only protocol

## Context

A previous alignment attempt can leave `zaber` stuck `active` with an old `run_id`. Calling `puda machine reset zaber` may return `Unknown or restricted command: reset` and temporarily show `state: error` with `run_id: null`.

## Recovery pattern

Before treating Zaber as unusable, run a harmless one-command protocol that starts and completes a normal Zaber run:

```json
{
  "commands": [
    {
      "step_number": 1,
      "machine_id": "zaber",
      "name": "get_current_position",
      "params": {"units": null}
    }
  ]
}
```

Use full PUDA protocol metadata and run from `/home/vipsa/vipsa-puda-project` with the active NATS servers. A successful read returns native `x`/`y` values under `response.data.x` and `response.data.y`, then sends COMPLETE and can restore `zaber` to `idle`.

## Verification

After the read-only protocol, verify:

```bash
timeout 4 puda --nats-servers nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224 machine state zaber
```

Proceed with motion only if `zaber` is `idle` and `run_id` is `null`.

## Reporting

Report the reset command only as an attempted recovery if it returned `Unknown or restricted command`; do not frame it as successful reset. Report the read-only protocol response and final idle state as the actual recovery evidence.
# Grid run active-device status after manual motion/interruption

Use this when the user asks which device is currently being tested during or after a long ViPSA grid run, especially if manual stage/Z commands or stale background-process notifications occurred in the same session.

## Durable lesson

A background completion notification can refer to an older/killed runner and does not prove the current grid run stopped. Conversely, a manual Z jog can execute while a continuation runner is still alive. Answer status questions from live process + run-folder evidence, not from the last notification alone.

## Status check recipe

1. Identify active grid/resume Python processes, e.g. match `resume_grid_8x8`, `grid_8x8`, and the known substrate/batch runner names.
2. Read the active runner's `OUT` path from the script if needed; for S2 batch 1 it may be under `data/probabilistic_computing/.../runs/...`, not only under top-level `runs/`.
3. Inspect the newest `device_*/summary.json` files in that `OUT` directory:
   - newest `status: started` with no `finished_utc` is the current or interrupted device
   - newest `status: completed` with `finished_utc` is only the last finished device
4. Report device number, row/col, x/y target, and whether the status is `started`, `completed`, or ambiguous.
5. If `puda machine state` probes time out or return no body, do not claim a measurement phase. Say the device is in-progress/possibly stalled and include the evidence (runner PID alive, summary status, state probe timeout).

## Reporting standard

Keep the answer concise:

- `Currently active runner: PID ...`
- `Current device: N (row R, col C; x=..., y=...)`
- `Summary status: started/completed/...`
- `Confidence: ...`

Avoid re-surfacing stale device numbers from old background notifications unless explaining that they are stale.
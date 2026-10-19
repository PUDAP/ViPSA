# Long-batch EOF recovery, INTENT latching, and edge restarts

Use when a continuous native batch was visibly dispatched but the controller loses NATS with `UnexpectedEOF`, hangs in cleanup, or is terminated before its exception handler commits UNKNOWN.

## Validated fail-closed workflow

1. Leave the instrument operation unreplayed. Stop only the hung supervisor/controller after confirming the dispatch line and exact wire request exist.
2. Inspect the batch and operation ledger states. A controller killed inside shielded/final cleanup can leave them at `INTENT` with the device-level UNKNOWN latch still false even though dispatch occurred.
3. Under the global owner lock, atomically convert that exact dispatched batch and all its operation IDs from `INTENT` to `UNKNOWN`; set `unknown_exposure=true`, `zero_exposure=false`, and `no_replay=true`. Preserve the original INTENT objects as fault history.
4. Stop only the protected electrical edge that owns VISA. Do **not** reset USB before retained-buffer extraction.
5. Extract `defbuffer1` directly and accept it only when it matches the exact run/request and immutable recipe arrays, expected point count, strictly increasing native timestamps, source/output-on status, idle trigger state, REAR terminals, output OFF afterward, and an empty error queue.
6. Restart the protected edge **without USB reset** first. Obtain fresh OFF/open/error/driver-hash/pose proof.
7. Atomically convert only the matched UNKNOWN batch and operations to COMPLETE, charge energy once, preserve original UNKNOWN history, mark retained-buffer provenance and `no_replay=true`, then run the missing post-batch health check.
8. Resume from the first missing batch only after the health cleanup passes.

## Edge restart rule

Routine per-batch restarts should be process-only. Do not call `usbreset` as ordinary batch hygiene: a reset can cause a USBTMC device to disconnect and fail to re-enumerate. Use USB reset only for a demonstrated stale USB/session condition after stopping every exact edge owner, and verify OS/VISA enumeration before launching the replacement edge. If the instrument is absent, do not dispatch.

## Why `INTENT` is not proof of zero exposure

The durable dispatch print and wire request can precede the ledger exception update. If the controller hangs or is killed during cleanup, the ledger may remain `INTENT` even though the native acquisition completed. Reconcile from exact hardware evidence; never infer execution state from the stale ledger label alone.

## Live plotting

Generate completed-cycle plots from a read-only frozen ledger snapshot while acquisition continues. Include only COMPLETE batches, record the frozen cycle boundary and ledger hash, and keep one CSV row per native point. Shared turning points may appear in both plotted forward/backward traces, but must not be duplicated in the CSV.

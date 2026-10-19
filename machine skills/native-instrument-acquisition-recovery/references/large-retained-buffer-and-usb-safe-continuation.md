# Large retained-buffer recovery and USB-safe continuation

Use after a long continuous native acquisition was dispatched but the controller lost NATS before receiving or committing the response.

## Proven sequence

1. Latch the whole unreceipted batch `UNKNOWN`; stop supervision and never replay it automatically.
2. Decode the exact wire request and bind recovery to its run ID, immutable segment arrays, expected segment count, and expected point count.
3. Before touching USB, identify the protected edge by exact CWD and PID. A live edge can own the interface even after NATS EOF.
4. If direct PyVISA reports `Resource busy`, stop only that edge. **Do not USB-reset before retained-buffer extraction**; reset/re-enumeration can erase or strand the evidence.
5. Run extraction with the instrument environment that contains `pyvisa-py`, not the controller environment. Keep the instrument under `ABOR` and output OFF while reading `defbuffer1` in bounded windows.
6. Accept only the exact expected count and order. Require finite values, strictly increasing native relative timestamps, source/output-on status at every acquired point, idle trigger state afterward, REAR terminals, output OFF, and an empty error queue.
7. Save the complete normalized result plus raw trace windows, hash it, and mark `no_replay=true`.
8. Restart one protected edge **without USB reset**, then require fresh output OFF, matrix `nil`, empty errors, expected driver hash, and unchanged pose.
9. Under the owner lock, convert only the matching UNKNOWN operations to COMPLETE, preserve original fault history, charge energy once, recompute metrics, clear UNKNOWN only if the whole ledger is resolved, and run only the missing post-batch health read.

## Pre-batch USB restart pitfall

Do not USB-reset an instrument as a routine action before every batch. First try a clean targeted edge restart. Use USB reset only for a demonstrated stale interface/session while the VID:PID is present. After reset, require OS and VISA re-enumeration before starting the edge. If the device disappears, stop retry loops, keep the next batch undispatched, and wait for physical reconnect/power-cycle. Once it reappears, start one protected edge without another reset and repeat full safety proof before a fresh batch.

## Distinguish failed recovery attempts

An extraction launched in the wrong Python environment or blocked by an edge-owned USB interface performs no scientific replay. Record the failed tooling attempt, fix the environment/ownership issue, and continue recovery against the same retained buffer. The scientifically relevant acceptance event is the later exact buffer validation and atomic ledger reconciliation.

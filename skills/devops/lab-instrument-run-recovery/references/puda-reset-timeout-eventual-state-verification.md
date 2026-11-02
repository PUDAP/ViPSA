# Stale run reset timeout with eventual recovery

A reset timeout is not proof that the reset failed. In PUDA recovery, a stale run can clear asynchronously just after `puda machine reset <machine>` reports a short response timeout.

Validated recovery sequence:

1. Record the stale machine state and run ID.
2. Attempt the harmless safety command (for an SMU, output off). If blocked by `RUN_ID_MISMATCH`, open the matrix independently and verify its hardware readback.
3. Reset only the affected machine.
4. If reset reports a timeout, do not immediately restart the edge or repeat measurement stress. Reissue the harmless output-off command and read machine state.
5. Accept recovery only when the harmless command succeeds and state reads `idle` with `run_id: null`; also require 707B `open_all` success plus explicit `nil`/empty readback.
6. Preserve the timeout and eventual readback in the recovery ledger.

This is an eventual-state verification pattern, not a general instruction to ignore reset failures. If harmless control still fails or state remains active/stale, continue with affected-edge recovery or stop for hardware intervention.

# Contact approach cleanup and fallback notes

Session pattern captured 2026-06-29.

## Situation

During ViPSA contact approach, the normal PUDA protocol path can be blocked by route/request timeouts while some machines may still hold outputs, switch closures, or run IDs from the prior attempt. The safe lesson is not that any tool is unusable; it is that fallback control must start from verified cleanup and continue logging every motion/read.

## Safe fallback sequence

1. Stop or let the active approach runner terminate; do not start a second approach without checking the first process/run state.
2. Verify/force cleanup before any continuation:
   - Keithley output off.
   - Keysight output off if it may have been armed.
   - Keithley 707B `open_all`.
   - Confirm closed channels are `nil` / empty.
   - Light off unless image capture or alignment still requires it.
   - Affected machine run IDs cleared or reset if a stale `run_id_mismatch` blocks commands.
3. If the protocol wrapper is blocked, direct per-command NATS control is an acceptable temporary fallback only after the cleanup above succeeds.
4. Continue approach in bounded increments, preserving a machine-readable run directory and `summary.json` with:
   - all Z moves and net Z from fallback start,
   - all low-bias read currents,
   - contact thresholds and compliance,
   - final status/error and cleanup results.
5. Report honestly when the process is still running: give latest measured current, target window, net Z, process/session ID, and summary path. Do not imply physical contact or completion from intent alone.

## Contact window used in this session

For a conservative contact approach continuation after weak/no contact, the target current window was `1e-8 A` to `1e-7 A` at `10 mV`, with `0.5` coarse Z steps and `0.25` fine Z steps. Treat these as context, not universal constants; adjust for the device/run plan.

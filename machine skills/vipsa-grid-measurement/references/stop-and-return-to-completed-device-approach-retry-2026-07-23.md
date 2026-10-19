# Stop an S1 Grid, Return to a Completed Device, and Retry Approach (2026-07-23)

## Reusable class pattern

Use when a user stops an active grid during device **N+1**, then asks to return to completed device **N** for one additional bounded approach attempt.

1. Stop the tracked grid runner and pause its per-device reporter.
2. Run explicit cleanup before any travel:
   - Keithley and Keysight outputs off
   - 707B `open_all`, verify `get_closed_channels == nil`
   - lights off
   - verify stage, Zaber, both SMUs, 707B, and light are `idle`, `run_id: null`
3. Determine the true stop boundary from runner logs plus per-device `summary.json`; do not infer it from `DONE.json` alone. Preserve completed devices and the interrupted device's partial artifacts.
4. Resolve the requested prior device from the authoritative substrate `grid_positions.csv` and query live stage/Zaber positions.
5. Travel safely in one lifecycle-complete PUDA protocol:
   - retract stage Z by the established clearance amount
   - move Zaber to the requested device's **absolute** X/Y
   - restore only the same clearance amount to the verified pre-travel Z baseline
   - read back stage and Zaber positions
   This restores the interrupted-device baseline, not a historical contact Z; the retry itself must establish contact.
6. Keep the grid paused. Run one isolated bounded approach retry in a timestamped retest folder rather than overwriting the completed device's original artifacts.
7. Reuse the grid campaign's approach policy unless the user supplies an override. Save start/final stage Z, net approach movement, current trace, target window, compliance, cleanup, and final positions.
8. If the terminal current equals or closely hugs read compliance, report **contact criterion reached at compliance**. Do not claim that value is the uncapped physical current.
9. Cleanup again and verify all machines idle/null before reporting.

## Concrete S1 example

- Grid runner intentionally stopped during device 32 after alignment; devices 22, 29, 30, and 31 were complete.
- Cleanup succeeded and device 32 remained partial.
- Returned from live Zaber `(39383, 514373)` to S1 device 31 absolute target `(34383, 514373)` using stage `-35`, absolute X/Y, then stage `+35`.
- Stage baseline before retry: Z `236.5`.
- One bounded grid-style retry used `0.1 V`, target `5–50 nA`, read compliance `20 nA`, `+0.5` Z steps, and max 100 attempts.
- Contact criterion was reached after `+20.5` Z at final Z `257.0`; measured current `19.99958 nA` was compliance-limited.
- Original `device_31` artifacts remained intact; retry artifacts were stored separately.

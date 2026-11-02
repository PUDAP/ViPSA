# Verified Z-increment then zero-dwell DCIV retry pattern

## Trigger
Use when the user asks to move ViPSA stage Z by an exact signed amount, repeat an established multi-cycle DCIV recipe, remove dwell, and deliver the artifacts.

## Safe ordered workflow
1. Capture the exact previous recipe from its script/summary rather than reconstructing it from memory.
2. Execute a single lifecycle-managed stage protocol containing `get_current_position`, `move_z_by` with only the authorized Z value, and `get_current_position`. Verify the signed delta before electrical stress.
3. Copy the prior run script to a new script/run directory and change only:
   - output directory/run label,
   - native-list `delay_s` to `0.0`,
   - all explicit per-point sleeps to zero/removed,
   - metadata/title so no stale nominal V/s label remains.
4. Keep the same voltage paths, step size, compliance, NPLC, autorange, routing, and cleanup unless the user changes them.
5. If preflight fails before routing or acquisition, preserve that attempt separately. Record whether any DCIV records or possible stress occurred. After hardware recovery, retry in a fresh run directory; never move Z again unless explicitly authorized.
6. Verify the completed CSV, not only script settings: expected row count, all `commanded_dwell_s == 0.0`, per-cycle endpoint/order, and instrument timestamps.
7. Verify `source off`, `707B open`, `get_closed_channels == nil`, final machine states idle, and visually inspect the plot before delivery.
8. Resolve the named Telegram destination first and verify each attachment independently. A successful text message with an attachment warning is not successful file delivery.

## Concrete validated comparison
The same four native lists at 50 mV steps contained 764 points total:

- `0 -> +10 -> 0 V`: 401 points
- `0 -> -2 -> 0 V`: 81 points
- `0 -> +3 -> 0 V`: 121 points
- `0 -> -4 -> 0 V`: 161 points

With `1.0 s` commanded dwell, instrument sweep time was about `1112.6 s` (`18.54 min`). With zero commanded dwell, the same 764 points took about `352.6 s` (`5.88 min`). The remaining time is NPLC/autorange/trigger/instrument overhead, not dwell; do not call zero-dwell instantaneous.

## Retry classification example
A 707B `open_all` failure with USB `ENODEV` occurred before routing and before any sweep records. The safe response was:

- classify the attempt as no acquired DCIV/no high-voltage stress,
- restart only the 707B edge,
- verify `open_all` and closed channels `nil` in a short protocol,
- retry the electrical run in a fresh directory,
- preserve the original verified Z movement and do not repeat it.

For the targeted edge-restart details, load `vipsa-machine-operations/references/electrical-machine-readiness-idn-and-direct-nats-2026-07-07.md`.

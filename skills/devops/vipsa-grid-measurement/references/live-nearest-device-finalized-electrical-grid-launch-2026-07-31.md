# Live nearest-device finalized electrical grid launch (2026-07-31)

Use this pattern when the user asks to run the finalized electrical grid protocol “on the current grid” or “starting from the device in contact right now” without naming a device.

## Trigger

- User says to start from the current contacted/probed device.
- A grid CSV already exists for the active substrate/run family.
- The device number is not explicitly named.

## Procedure

1. **Use live readbacks, not narrative state.**
   - Query live Zaber X/Y through a lifecycle-managed PUDA/NATS command path.
   - Compare the live X/Y to the relevant `grid_positions.csv` and choose the nearest device.
   - Record the live readback, nearest-device target, `dx/dy`, and native-distance in the run summary before launch.

2. **Use the current grid CSV and serpentine boundary.**
   - Keep the existing grid map; do not regenerate a new grid from the current position.
   - Compute the standard serpentine traversal and slice it at the nearest/current device.
   - Store `traversal_order_from_boundary` in `summary.partial.json` before the runner begins.

3. **First-device handoff.**
   - For the first/current device, do **not** perform Zaber travel or vision re-alignment before checking the contact.
   - Turn lights off and run a low-bias contact verification: three 10 mV reads in the configured contact window.
   - If all reads are stable/in-window, reuse the contact and save an `approach.json` handoff artifact with `net_z_steps: 0`.
   - If the live contact is over-window or below-window, run the configured bounded approach/correction from the current Z without a generic Zaber/vision move first.
   - If the finalized protocol requires a strict contact window, do not run DCIV/pulses until the final contact gate passes.

4. **Later-device travel sequence.**
   - Cleanup: SMU outputs off and 707B open/nil.
   - Stage safe travel: `stage.move_z_by(-50)`.
   - Zaber absolute move to CSV X/Y.
   - Vision align at safe/retracted Z.
   - Stage pre-approach: `stage.move_z_by(+40)`.
   - Run approach/contact gate, then electrical measurements.

5. **Finalized electrical protocol used here.**
   - Exactly one DCIV cycle: `0 -> +0.6 -> 0 -> -0.75 -> 0 V`.
   - Do **not** run extra DCIV reset-ladder sweeps under this finalized/current-grid handoff unless the user explicitly changes the protocol.
   - After DCIV, run the grid randomized SET-read-RESET-read pulse helper.
   - If the one DCIV shows SET without RESET, run exactly five RESET-read fallback pairs at the strongest configured pulse RESET voltage, save them, then continue randomized pulses.

6. **Launch and reporting.**
   - Use the active bears NATS servers unless the user explicitly overrides.
   - Disable recording unless requested.
   - Create the run directory and `run.log` parent before starting a `tee` pipeline.
   - Launch the long runner as a tracked background process with completion notification.
   - Install/enable a stateful recurring no-agent reporter keyed by run directory + device number; it should parse `summary.json` before reporting and attach `device_plot.png` when present.

## Pitfalls

- **Do not infer the device from the latest partial folder** when live X/Y is available; stale folders often remain after prior restarts.
- **Do not regenerate the grid using live X/Y** for a continuation. Use live X/Y only to identify the boundary device against the saved grid.
- **Do not snap the first/current device back to nominal CSV X/Y** before checking contact; preserve the live aligned/probed offset.
- **Do not insert gross inter-attempt retracts during strict contact retries** unless the user explicitly asked; continue from verified current Z, preserving only minimum safety trims after over-current/overshoot.
- **Do not report success immediately after launch.** Verify at least: run directory/summary exists, traversal boundary is recorded, process is running, and the first `device_start` log line appears.

## Concrete session artifacts

- Script: `runs/grid_7x7_batch1_S9_from_live_device10_final_electrical_20260731.py`
- Run dir: `data/probabilistic_computing/batch_1/substrate_S9/runs/grid_7x7_batch1_S9_from_live_device10_final_electrical_20260731T1637Z/`
- Reporter script: `~/.hermes/scripts/vipsa_s9_device10_final_reporter.py`
- In this session, live Zaber `(277155, 491430)` mapped to S9 device 10 with offset `(+390, +299)` native units; traversal began `10, 9, 8, 15, 16, ...`.

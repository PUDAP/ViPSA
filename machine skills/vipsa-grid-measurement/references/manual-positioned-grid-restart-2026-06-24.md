# Restart grid measurement from a manually positioned device (2026-06-24)

When a ViPSA grid run is interrupted and the user wants to manually reposition to a device before restarting, treat the manual physical handoff as part of the restart protocol, not as an incidental setup.

## Recommended restart pattern

1. Stop/verify no old grid process is still running.
2. Determine the existing run folder and grid coordinate for the requested restart device from `grid_positions.csv` / `grid_row_major.json`.
3. Archive or move stale `device_N+` folders before restarting, or patch the runner to ignore old `DONE.json` for the restart range. Otherwise the runner can silently skip the requested restart device.
4. Execute and verify the user's explicit physical handoff separately:
   - Z retract/down by the requested signed amount.
   - Zaber X/Y to the requested device coordinate.
   - Z up/pre-approach by the requested amount.
   - Zaber readback equals the grid coordinate.
5. Turn lights off before electrical approach/DCIV/pulses unless the user explicitly asks otherwise.
6. Run the contact approach as a standalone bounded phase and save `approach.json`.
7. Launch the continuation runner from the requested device. For the first device, reuse the standalone approach result and avoid repeating the manual motion. Subsequent devices can use the normal grid sequence.
8. Resume device-finish reporter/cron only after the continuation process is started and its PID/session ID is known.

## Reporting

Report in one concise update:

- restart device number and coordinate readback
- Z motions performed
- lights-off state before measurement
- approach status/final current
- continuation runner process ID and reporter status

If approach remains weak/open-like but the current run policy says to continue open/weak devices, make that explicit; do not imply a good contact was established.

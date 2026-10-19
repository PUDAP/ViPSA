# Chained Z-up + approach at a grid device: over-current trim and parameter override (2026-06-25)

Context: After moving to a grid device with a safe Z retraction (`stage.move_z_by(height=-30)`), the user replied to the completion message with “Move z stage up and perform approach.” The intended Z-up distance was the same magnitude as the immediately preceding safe retraction, so the handoff used `stage.move_z_by(height=+30)` before approach.

Workflow that worked:

1. Turn lights off before electrical approach.
2. Force electrical safety before the Z move/approach: `keithley-2450.set_output(false)` and `keithley-707b.open_all()`.
3. Move stage Z forward/up by the inferred prior retraction amount (`+30` in this session) using a full-metadata PUDA protocol.
4. Run the Keithley-guided approach.
5. If the first 10 mV read is already above the target window, do **not** move further forward/up. Treat it as over-current/over-contact and perform bounded minimum-step retractions (`-0.25` steps) with reads after each trim.
6. If the user changes approach parameters after seeing the result (for example, “use step size 1, max attempts 100”), rerun with the requested parameters, but be clear that a larger coarse approach step does not affect the path when the initial read is already over-current; the routine will enter trim/retract immediately.
7. Always cleanup: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, final machine states idle/null.

Observed outcome in this session:

- After `+30` Z, the initial 10 mV current was already about `286 nA`, above the `10–100 nA` target window.
- The approach routine performed 20 trim retractions of `-0.25` steps (`-5.0` total) but current remained about `285 nA`.
- Rerunning with user-requested `coarse_step_z=1.0` and `max_attempts=100` again started over-current and trimmed `-5.0`; final current remained above target.

Reporting pattern:

- Report the pre-approach Z move, whether approach actually moved forward or immediately trimmed, final current relative to the target window, net Z movement during approach, final stage readback, and cleanup verification.
- Do not call this a successful in-window approach when the final current remains above the upper threshold; describe it as over-current/over-contact not stabilized in the requested window.

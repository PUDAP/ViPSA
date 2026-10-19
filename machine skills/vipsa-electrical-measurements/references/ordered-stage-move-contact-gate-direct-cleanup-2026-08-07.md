# Ordered stage move → contact gate → DCIV, with safe Direct cleanup

## Trigger

Use when a ViPSA user requests an exact signed stage-Z move followed by DCIV, forming, SET, RESET, or another potentially destructive electrical sweep.

## Ordered chain

1. Read and record the live stage position.
2. Execute exactly the newly authorized signed `stage.move_z_by(N)` call. Do not silently replay an interrupted earlier move or alter the sign.
3. Read back the stage position and verify the expected delta before electrical routing.
4. Run multiple low-bias contact reads at the campaign-specific test voltage and current window. Preserve all reads and use a robust statistic such as median absolute current.
5. Run the high-voltage sweep only if contact passes. If it fails, save a `dciv_skipped_contact_gate` artifact and clearly report: move succeeded; DCIV did not run.
6. If a current camera image helps diagnose pad placement or probe deflection, capture it with temporary illumination and restore lights off before/after electrical work.
7. Finish with SMU outputs off, 707B `open_all`, closed channels `nil`, and every touched machine idle with `run_id: null`.

## Contact-window rule

Use the target window established for the active campaign/device. Do not silently substitute an older skill default. For example, a Pratap-style HRS approach may use `1–10 nA` at `10 mV`, whereas another campaign may use a different window.

## Direct-session cleanup pitfall

A shared cleanup helper may call machines beyond the main measurement. Every machine it calls must be included in the same `Direct([...])` run context, or cleanup must be scoped to only machines owned by that session.

A concrete failure mode is calling `keysight-b2902b.set_output(false)` from cleanup while `keysight-b2902b` is absent from the Direct machine list. The machine can receive START without matching COMPLETE and remain `active` with a stale run ID.

### Prevention

- Include all cleanup-touched machines, commonly `keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, and `stage` as applicable.
- Or use a cleanup helper limited to machines in that session.
- Verify all touched machines live after cleanup; do not infer completion from a local `finally` block alone.

### Recovery

On `run_id_mismatch` or stale `active` state, reset the affected machine and then query live state. A reset command can time out while edge recovery succeeds moments later, so trust the subsequent verified `idle` / `run_id: null` state rather than interpreting the timeout alone as persistent failure.

## Reporting

Keep the user-facing result concise:

- exact requested move and actual before/after readback;
- contact readings and threshold;
- whether DCIV completed or was skipped;
- cleanup and idle verification;
- fresh camera media when diagnostically useful or expected by the user.

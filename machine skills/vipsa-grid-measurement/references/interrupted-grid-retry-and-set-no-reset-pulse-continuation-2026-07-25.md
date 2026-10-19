# Interrupted-grid prior-device retry and SET-without-RESET pulse continuation

Use this pattern when a live ViPSA grid is stopped mid-device so an earlier device can receive another bounded approach attempt, and when pulse acquisition must continue after DCIV detects SET but not RESET.

## Safe prior-device retry

1. Stop the tracked grid runner and its reporter/monitor. Preserve the interrupted device folder as partial evidence; do not treat `DONE.json` alone as completion.
2. Check machine states. If a killed command leaves an idle machine with a stale non-null run ID, reset that machine, then re-check.
3. Before any X/Y travel, verify both SMU outputs off and `707B.get_closed_channels() == nil`; turn lights off unless alignment is needed.
4. Read live stage Z and Zaber X/Y. Retract stage Z by the established safe-travel distance.
5. Return by the prior device's recorded **aligned absolute Zaber coordinates**, not merely its nominal grid coordinate and not an adjacent relative move.
6. Restore only the matching pre-travel Z amount, verify Zaber and stage readbacks, then run one isolated bounded approach in a timestamped retest folder. Preserve the original device folder.
7. If the final current remains outside the strict contact window, do not run DCIV or pulses. Record the final current, net Z advance, stage position, and verified cleanup; leave the grid paused until explicitly resumed.

A validated bounded retry used 100 increments of `+0.5` Z with a 50–500 nA gate. It ended at 1.5458 nA after `+50` Z, so DCIV/pulses remained blocked. The durable lesson is the strict numeric gate and isolated retest artifact, not that particular current.

## SET observed, RESET not observed

For randomized pulse workflows, treat `DCIV set_detected == true && reset_detected == false` as an explicit branch:

1. Route to the pulse SMU with the normal pulse compliance and width.
2. Run exactly **five RESET-read pairs** at the strongest configured RESET voltage (for the validated ladder, `-2.0 V` RESET and `+0.1 V` read).
3. Save all five read currents in a dedicated artifact such as `forced_five_reset_read_fallback.json`.
4. Select that RESET voltage and proceed immediately to randomized `SET → read → RESET → read` trains. Do not require successful RESET calibration as a prerequisite to entering the pulse loop.
5. Keep independent hard safety checks during pulse acquisition, including pulse/read compliance checkpoints and cleanup on exit.
6. Record the trigger, voltage, number of pairs, read currents, and that randomized pulses continued in the pulse summary.

## Verification

- Compile the runner after patching.
- Exercise the conditional with a deterministic fake pulse backend: the first pulse call must contain 10 voltages (five RESET-read pairs), followed by a normal randomized chunk.
- Verify the retest/fallback artifacts exist and cleanup leaves SMU outputs off and 707B open.

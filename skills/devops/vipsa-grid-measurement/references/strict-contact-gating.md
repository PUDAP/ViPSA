# Strict contact-gating for ViPSA grid measurements

Use this policy when the user requires electrical measurements only after verified contact.

## Gate definition

- Evaluate the **numeric final absolute contact current**, not the textual approach status alone.
- The current passes only when `lower_a <= abs(I_contact) <= upper_a`.
- Configure the approach read compliance above the upper bound (with reasonable headroom), otherwise the requested window cannot be observed.
- Statuses such as `no_contact_after_max`, `below_lower_after_retract`, and `contact_edge_below_lower_after_post_fine_retract` do **not** pass merely because later DCIV shows current.

## Required sequence

1. Perform one bounded approach and persist its complete log.
2. If the final current is outside the window, preserve attempt 1, re-check alignment, and perform one complete bounded approach again.
3. Repeat the low-bias contact-health read after the second attempt.
4. Recompute the gate from the second attempt's numeric final current.
5. Run DCIV and pulse measurements only if the gate passes.
6. If both bounded attempts fail, do not approach indefinitely. Record `skipped_contact_not_in_window`, omit DCIV/pulses, clean up outputs/switches, then continue or pause according to the run policy.

## Changing policy during an active run

Editing a Python runner does not alter code already loaded in a running process. To apply a new contact policy:

1. Identify the current device and phase from live runner output.
2. Stop before electrical measurement if possible.
3. Disable SMU outputs, open all 707B channels, turn lights off, and complete/reset machine lifecycle state.
4. Read back stage and Zaber position.
5. Archive the current device's partial directory.
6. Create and compile a continuation runner at that same device using the live position as the handoff.
7. Start the replacement runner and verify its first event explicitly names the strict gate.

Do not repeat a lateral move for the handoff device. Keep every approach bounded; never turn a strict gate into unlimited Z motion.

## Reporting

- Distinguish `completed` from `skipped_contact_not_in_window`.
- Do not generate or report a normal combined electrical plot for a device whose DCIV/pulses were blocked.
- Include window bounds, both attempt results, final gate current, and the reason measurement was blocked.

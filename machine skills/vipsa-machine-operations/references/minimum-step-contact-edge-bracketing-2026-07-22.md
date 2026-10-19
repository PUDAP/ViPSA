# Minimum-step contact-edge bracketing during approach

Use this when a Keithley-guided `+Z` approach crosses from open-like current to over-current within one stage increment, and the minimum valid Z adjustment cannot place the current inside the target window.

## Observed pattern

With the standard approach window (`10–100 nA` at `+10 mV`), a coarse `+1.0 Z` approach stayed near the pA noise floor, then jumped to `174 nA` at one position. A minimum valid `-0.25 Z` retract returned the current to about `21 pA`. The two verified positions therefore bracketed a sharp contact edge, but neither was in-window.

## Reusable procedure

1. Record the last below-threshold Z/current pair and first above-threshold Z/current pair.
2. Retract by exactly the hardware minimum (`-0.25 Z`) and re-read.
3. If the retract returns below the lower threshold, stop safely below contact. Do not oscillate repeatedly between the two positions and do not use unsupported sub-`0.25` moves.
4. Classify the result as `contact_edge_below_lower_after_trim`, not `in_window` or stable contact.
5. Preserve the bracket in artifacts: `[Z_below, Z_above]`, currents at both positions, target window, commanded net Z motion, and final readback.
6. Cleanup with Keithley output off and 707B `open_all`/`get_closed_channels == nil`; verify idle/null machine states.

## Reporting language

Say that the contact edge was detected but a stable target-window position was unavailable at the stage's resolution. Report the final safely retracted Z/current, plus the over-current edge position/current. Do not claim successful contact from the transient over-current point.

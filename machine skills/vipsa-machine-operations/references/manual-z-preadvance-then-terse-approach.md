# Manual Z pre-advance followed by terse contact approach

Use this pattern when the user explicitly moves Stage Z forward in one or more manual commands and then says `approach`.

## Reusable rules

1. Treat each explicit Z move as its own completed, verified motion. Preserve the latest numeric Stage-Z readback.
2. A later terse `approach` authorizes a **fresh bounded Keithley-guided approach block from that verified position**. Do not repeat the prior manual moves, and do not silently count them as approach-loop attempts unless the user specified one total travel budget.
3. Before the first approach move, turn lights off, force Keithley output off, route the 707B to Keithley, and take a fresh `10 mV` read with `1 µA` compliance.
4. If the fresh read is already in the `10–100 nA` window, stabilize/re-read and command no Z motion.
5. Otherwise move only `+Z` in the configured bounded increments, reading after every move. Do not infer contact from substantial cumulative Z travel; the current measurement is the contact gate.
6. If the bounded block ends in pA/sub-nA current, stop as `no_contact_after_max`. Do not auto-extend, run DCIV, or claim approach success.
7. Report both:
   - approach-block travel and start/end Z;
   - prior manual pre-advance separately when useful for cumulative context.
8. Cleanup and verify Keithley output off, 707B `open_all`, closed channels `nil`, and all involved machines idle with null run IDs. Leave lights off after electrical approach unless explicitly requested otherwise.

## Session-derived example

Two verified manual forward moves brought Stage Z from `50` to `200` (`+100`, then `+50`). A subsequent default step-1 approach started with a fresh low-bias read, advanced a separate bounded `+100` steps to Z `300`, and remained near `22.5 pA` at `10 mV`. Correct outcome: `no_contact_after_max`; no contact detected; cleanup verified. The large cumulative `+250` travel did not constitute electrical contact evidence.

# Pulse characterization completion versus scientific validity

Use this note when a staged device campaign reaches its assigned pulse recipe after forming and conditioning.

## Core distinction

A normal runner exit or status such as `completed_pulse_doe` means the control flow finished. It does **not** mean the pulse recipe passed. Read the explicit characterization fields and classify the recipe separately.

## Required scoring

1. Compare `read_after_SET` and `read_after_RESET` at the same read bias for every characterization cycle.
2. Under the declared SET-high convention, require `|I_read_after_SET| > |I_read_after_RESET|` and the prespecified ratio/validity floor.
3. Ratios below `1` are directionally inverted. Repeated inversion across all cycles is an executed-but-rejected recipe, not successful switching.
4. Do not start endurance unless every prespecified characterization cycle is valid.
5. Distinguish:
   - **withheld/unevaluated:** activation or conditioning blocked recipe execution;
   - **executed/failed:** recipe ran, but characterization direction or validity failed;
   - **characterization passed:** all short characterization cycles passed, allowing endurance;
   - **endurance/retention qualified:** only after those later gates actually pass.

## Plot and recovery pattern

Generate a focused diagnostic from saved `summary.json` or CSV:

- cycle versus `|I_read_after_SET|` and `|I_read_after_RESET|` on a log axis;
- cycle versus SET-read/RESET-read ratio on a log axis;
- reference lines at ratio `1` and the declared acceptance floor.

If the normal analysis environment lacks plotting dependencies, render from the saved artifacts in a plotting-capable environment. Never rerun hardware solely to regenerate a plot.

## Campaign interpretation

Keep recipe attribution conditional on prerequisite gates. A campaign can have many clean forming events but few recipes actually executed. Report activation yield, conditioning yield, recipes executed, characterization passes, endurance passes, and retention passes separately. Systematic inversion after a passed conditioning gate is evidence against that pulse recipe under the declared state convention; it is not evidence that earlier withheld recipes failed.

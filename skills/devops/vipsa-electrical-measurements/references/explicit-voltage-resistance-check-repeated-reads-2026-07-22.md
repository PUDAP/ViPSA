# Explicit-voltage resistance check with repeated reads (1 V example, 2026-07-22)

## Trigger

Use when the user specifies a resistance-check voltage explicitly, e.g. “check resistance at 1 V.” Honor the requested bias instead of substituting the default low-bias multi-point recipe.

## Protocol shape

1. Verify `light`, `keithley-2450`, `keithley-707b`, and `stage` are idle / `run_id: null`.
2. Ensure lights are off.
3. `keithley-2450.set_output(enabled=false)`.
4. `keithley-707b.connect_keithley_smu()`.
5. Run `keithley-2450.hold_voltage_measure_current` with:
   - requested voltage (example `1.0 V`)
   - `current_compliance=1e-6 A` unless overridden
   - `settle_s=0.2`
   - `read_count=3`
   - `reset=true`
6. Compute resistance from the median current: `R = V / median(I)`; use absolute resistance for the headline while retaining current sign in raw results.
7. Report all readings or their range. If current drifts monotonically across the reads, explicitly report the resistance range/trend rather than implying a perfectly stable scalar.
8. If `|I|` is near compliance, report a bound (`R <= V/Icomp`) instead of a precise resistance.
9. Cleanup and verify: Keithley output off, 707B `open_all`, closed channels `nil`, all relevant machines idle / `run_id: null`.

## Parsing pitfall

PUDA output may expose the same readings under more than one current-key path (for example both `I_meas (A)` and a nested/aliased current field). A regex that scans several key names and concatenates matches can duplicate the same three readings. Parse the response JSON structurally when possible, or deduplicate repeated identical sequences before counting samples. Do not misreport six reads when `read_count=3`.

## Session example

At `1.0 V`, `1 µA` compliance, three readings were approximately `115.9`, `155.8`, and `189.7 nA`. Median current was `155.8 nA`, giving `~6.42 MΩ`; the range corresponded to roughly `8.63 → 5.27 MΩ`. The measurement was not compliance-limited, but the rising current was reported as instability/drift.

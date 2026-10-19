# Post-DCIV health gate before repeat cycles — 2026-06-14

## Trigger

Use this when the user asks to check device health after a DCIV/forming sweep and then run repeated DCIV cycles only if the device is still working.

## Observed pattern

A preceding DCIV sweep showed a SET-like transition and ended with a post-read around `38.5 nA @ 10 mV`. On a later health check before requested repeat cycling, low-bias Keithley reads had relaxed back to pA / ~0.1 nA scale:

```text
0 V:      ~7.06e-11 A
+10 mV:   ~7.80e-11 A
-10 mV:   ~5.91e-11 A
+50 mV:   ~1.08e-10 A
-50 mV:   ~2.76e-11 A
```

This was treated as weak/open-like or not-retained contact/state, not a working device ready for repeat stress. The requested 10 DCIV cycles were gated off.

## Workflow rule

When the user says “if the device is working, run N DCIV cycles”:

1. Run a low-bias health gate first, not a stress sweep:
   - `0 V`
   - `±10 mV`
   - `±50 mV`
   - low read compliance such as `1e-6 A`
2. Compare the health reads to the immediately preceding useful state/read-probe if available.
3. If the device has relaxed from nA/tens-of-nA state back to pA/~0.1 nA and does not show convincing voltage-scaled current, classify as weak/open-like or not retained.
4. Do **not** run the requested repeated DCIV cycles under the conditional wording.
5. Cleanup and verify:
   - Keithley output off
   - 707B `open_all`
   - `get_closed_channels == nil`
   - final electrical machines idle with `run_id: null`

## Compliance interpretation

For “1 order of magnitude lower on both sides” after a previous sweep with:

```text
positive compliance = 1e-4 A
negative/reset compliance = 1e-3 A
```

use:

```text
positive compliance = 1e-5 A
negative/reset compliance = 1e-4 A
```

Only run the lower-compliance cycles if the health gate passes.

## Reporting standard

Be concise and explicit:

- Say the health gate failed and the cycles were not run.
- Report the low-bias currents.
- State why: device/contact is pA/~0.1 nA weak/open-like or did not retain the prior post-sweep nA state.
- Include cleanup verification and saved summary/CSV paths.

Do not call the device “dead” if it is merely weak/open-like; reserve hard-short/dead language for compliance-limited low-bias or no-response evidence.

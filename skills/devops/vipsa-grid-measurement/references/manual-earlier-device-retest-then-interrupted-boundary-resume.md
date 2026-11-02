# Resume a literature p-bit grid after manual return to an earlier device

## Trigger
Use when an interrupted grid has already processed/skipped several devices, the operator manually returns to one of those earlier devices for alignment and staged Z/contact checks, then asks to continue the grid protocol.

## Core rule: separate the current retest from the true continuation boundary
The live device and the first unfinished device can differ. Do not restart the original traversal slice blindly: doing so can overwrite valid results between them.

1. Reconcile live Zaber X/Y against `grid_positions.csv` and identify the live device.
2. Inspect the run's per-device `summary.json` files to identify the true interrupted/unprocessed traversal boundary.
3. Build the continuation order as:
   - current live device once, for a fresh gated handoff/retest;
   - then the serpentine slice beginning at the true interrupted boundary.
4. Preserve already terminal devices between those boundaries in the new run summary; do not revisit or overwrite them unless the user explicitly requests a redo.

Example pattern: live device 26, devices 25–23 already terminal, device 22 interrupted → traversal starts `[26, 22, ...remaining serpentine devices]`, not `[26, 25, 24, 23, 22, ...]`.

## Current-device electrical handoff after manual Z changes
- Preserve the live aligned X/Y offset; do not snap back to nominal CSV coordinates.
- If recent repeated low-bias checks are compliance-limited/short-like, do not approach farther.
- Run the literature multi-bias contact gate directly at the current position.
- A compliance-limited/short-like result is a hard literature safety skip for DCIV and p-bit pulses unless the user explicitly overrides that gate.
- Save this as a fresh continuation artifact rather than silently replacing the prior result.

## Preflight before launch
Perform real transactions, not state-only checks:
- Keithley and Keysight outputs off.
- 707B `open_all()` followed by `get_closed_channels()`; require `nil`.
- Lights off.
- Read live Zaber X/Y and Stage-Z.
- Require all relevant machines idle with null run IDs and no old runner process.

Treat Stage-Z after an edge restart as a relative software/controller coordinate; record the before/after readbacks without calling it an absolute physical position.

## Runner hard-stop behavior
A per-device exception must not be swallowed followed by lateral travel. Save the device error and cleanup evidence, then re-raise or set a run-level abort flag. Route/output/open-all verification failure must stop the grid before Stage/Zaber motion.

## Reporting
Use one fresh stateful reporter keyed to the new continuation directory. Report skipped contact gates honestly (including max current and that no DCIV/pulses ran), then report each terminal device once. Keep reporters for older run directories paused.

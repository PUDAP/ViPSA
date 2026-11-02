# Z increment then repeat randomized 3400-pulse Keysight test: no-bimodal analysis fallback (2026-06-30)

Use this when the user explicitly asks to manually improve contact by a small stage-Z increment and then rerun the **same** randomized Keysight SET-read-RESET-read pulse train.

## Verified workflow

1. Execute the requested stage Z move first using a full-metadata PUDA protocol.
   - For this session: `stage.move_z_by(height=+1.0, feedrate=450)`.
   - Verify with a separate `stage.get_current_position` protocol; do not combine move + position readback in the same protocol if the separate-read pattern is safer.
   - Confirm final `stage` state is `idle`, `run_id: null`.
2. Rerun the exact same Keysight/707B randomized pulse train in chunks:
   - Sequence per cycle: `SET -> READ -> RESET -> READ`.
   - SET levels: `0.20` to `1.00 V` in `0.05 V` steps.
   - Attempts: `50` per SET level (`850` cycles total).
   - Total pulses: `3400`.
   - READ: `+0.05 V`.
   - RESET: `-1.0 V`.
   - Pulse width: `50 ms`.
   - Compliance: `1e-4 A`.
   - Chunking: `100 cycles/chunk` (8 full chunks + 1 final 50-cycle chunk).
3. Cleanup is mandatory even when post-processing fails:
   - Keysight `set_output(false)`.
   - 707B `open_all()`.
   - 707B `get_closed_channels()` should return `nil`.
   - Verify Keysight and 707B final states are `idle` / `run_id: null` when state commands are available.

## Analysis pitfall: no bimodal distribution

The earlier analysis helper tried to fit a two-component threshold unconditionally and failed with `ValueError('attempt to get argmin of an empty sequence')` when the read-after-SET distribution had no meaningful separation.

Do not treat this as a failed hardware measurement if the CSV contains all expected rows. Instead:

1. Verify row count: `3400` total rows, `850` read-after-SET, `850` read-after-RESET.
2. Inspect read-current range/dynamic range.
3. If the read-after-SET log-current span is tiny (example: ~`0.097 decades`) and all reads are far below a prior bimodal threshold, mark `bimodal_available: false`.
4. Do **not** fit a new sigmoid from a unimodal/no-switch run.
5. If comparison to a previous bimodal run is useful, compute `P_switch` using the previous threshold only as a consistency reference and label it clearly.
6. Generate scatter-only plots for read-after-SET/read-after-RESET currents and a histogram labeled as no-bimodal mode.

## Reporting pattern

Report the motion and measurement separately:

- Z command and readback: signed Z move, final stage position, final idle state.
- Pulse execution: returned rows vs expected rows, chunk count, exact parameters.
- Analysis: read-current medians/ranges, positive/negative read counts, near-compliance count, switched count under the reference threshold.
- Interpretation: for TE probing, stable negative nA readings during positive READ pulses remain open / very-high-HRS / poor-contact-like unless corroborated by paired-bias/contact diagnostics.

Example result from this session after `+1 Z`:

- Returned points: `3400 / 3400`.
- Read-after-SET median: `7.1e-9 A`; range `6.4e-9` to `8.0e-9 A`.
- Read-after-RESET median: `6.9e-9 A`; range `6.2e-9` to `7.7e-9 A`.
- Positive reads: `0`; negative reads: `1700`.
- Near-compliance reads: `0`.
- Switched reads using previous `8.83e-6 A` threshold: `0 / 850`.

The key durable lesson is the **fallback analysis path**: completed hardware data should still be summarized and plotted when a bimodal-threshold helper fails because the distribution is not bimodal.
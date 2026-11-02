# Device-transition templating and live-snapshot safeguards

Use this reference when advancing an adaptive DCIV campaign to the next device by deriving motion, preparation, recipe-publication, proof, batch, plotting, or completion scripts from a prior device.

## Why this matters

Copying a verified prior-device controller is efficient, but simple text substitution can leave internally consistent-looking stale literals. Common survivors include:

- user-facing status strings naming the prior device;
- optimizer `initial_cursor` assertions;
- zero-based design-row indexes;
- prior completion-ack paths;
- expected preparation operation counts and health counts;
- aligned/final poses;
- nominal absolute grid targets;
- hardware route device numbers;
- proof/deployment filenames;
- output plot titles and cycle limits.

A script that compiles can still publish the wrong provenance or fail only after hardware exposure. Treat cloning as template instantiation followed by an invariant audit, not as validation.

## Pre-execution invariant audit

Before running a derived controller, inspect the generated file and assert all of the following from live/durable state:

1. **Identity** — every device ID, display label, route ID, filename prefix, and output directory names the new device.
2. **Optimizer state** — `initial_cursor` equals the zero-based design index; pending is empty before publication; the previous acknowledgement names the immediately preceding completed device.
3. **Recipe source** — parameters come from the exact saved design row for the new device; status/source text names the same device and row.
4. **Navigation** — source pose is the fresh live pose; destination is the approved absolute grid target; aligned pose is preserved after correction rather than snapping back to nominal.
5. **Preparation** — terminal path, forming count, conditioning count, health count, receipt count, final pose, and permanent-ledger operation count agree exactly.
6. **Candidate proof** — SET/RESET counts, compliance values, recipe digest, driver hash, device route, OFF proof directory, output OFF, and matrix nil all match the newly published recipe.
7. **Batch expectations** — baseline ledger count equals preparation operations; each prior 10-cycle batch contributes exactly 21 operations (20 branches plus one health check); expected final pose and deployment file are device-specific.
8. **Completion** — batch glob, native-point total, plots, independent cleanup proof, optimizer record, `devices_consumed` key, cursor increment, and printed status all name the new device.

Run a syntax check after generation, but never substitute syntax success for this semantic audit. Audit both pre-publication and post-write cursor assertions: cloning can update `r['initial_cursor']` while leaving `load(rp)['initial_cursor']` stale. If only that final assertion fails after durable publication, do not rerun the publisher. Read back runner pending, active request, recipe equality/digest, exact design parameters and ledger prefix; preserve the original request identity and continue only if all match. Repair the stale source assertion for future use without republishing.

## Fail-closed schema corrections

If a controller rejects a prerequisite record before motion or stress (for example, alignment evidence lacks a required provenance field), verify from output and live readback that no command executed. Amend only the missing schema/provenance field from retained evidence, then rerun. Do not weaken the prerequisite check and do not claim contact from optical alignment.

For alignment records used by pre-approach, retain at minimum:

- device ID and preparation request ID;
- source image and evidence-reference paths;
- verified pose at the image;
- probe and lattice-target pixels;
- residual vector/norm and correction decision;
- `physical_contact_claim: false`.

## Plotting while a later batch is active

When the user requests a plot during acquisition:

1. Find the highest **terminal-complete, cleanup-verified** batch boundary.
2. Freeze the plot to that boundary (for example, cycles 1–20).
3. Include only cycles with both COMPLETE SET and RESET receipts and cleanup-qualified source artifacts.
4. Apply an explicit `cycle <= frozen_boundary` filter before grouping. Do not let recursive file discovery include receipts being written by the active batch.
5. Assert the resulting cycles equal the contiguous range `1..frozen_boundary` and validate the expected native-row total.
6. Title the figure as a snapshot (for example, `completed through cycle 20; testing continues`), not a final result.
7. Preserve PF/PB/NF/NB line styles, one color per cycle, cycle colorbar, `Vcmd` versus log `|I|`, and the switching-contrast panel.
8. Visually inspect the PNG before delivery. Regenerate the final plot after the terminal stop.

Plot generation is read-only and must not interrupt, duplicate, or alter the active batch.

## Completion and delivery ordering

Do not synthesize `delivered: true` or a delivery handle in a pre-delivery bookkeeping script. Correct ordering is:

1. verify terminal/ledger and independent cleanup;
2. generate and inspect artifacts;
3. deliver the plot/status;
4. verify real delivery evidence;
5. write the delivery record;
6. ingest the optimizer acknowledgement and advance the cursor.

If the optimizer requires delivery evidence, hold the campaign at the safe completed boundary until delivery is real. Normal recipe-specific failure is still a completed device outcome and should progress after this ordering is satisfied.

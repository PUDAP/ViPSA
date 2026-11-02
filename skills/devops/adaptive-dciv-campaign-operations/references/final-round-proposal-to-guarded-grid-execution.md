# Final-round proposal to guarded grid execution

Use when an optimizer has produced a validated multi-candidate proposal but deliberately left `executor_handoff_created=false` and the operator subsequently authorizes labels such as F1–F8 for live execution.

## Freeze and bind before motion

1. Treat the proposal CSV and its proposal manifest as immutable sources; verify both hashes and the manifest validation fields before creating hardware artifacts.
2. Resolve physical devices from the authoritative grid map and audit prior campaign occupancy. Do not assume the next labels imply device numbers. Bind the candidates in explicit grid order only after confirming unused targets.
3. Resolve testing policy from the active authorization and established campaign contract. Record the cycle cap explicitly in every recipe, manifest, executor guard, and supervisor; never infer it from predicted endurance.
4. Create one recipe file per label/device. Derive `candidate_id`, `device_id`, recipe digest, and all later alignment/ledger identity fields programmatically from the frozen recipe. Never manually type or invent an identifier in an alignment or execution record.
5. Preserve two hashes: the full recipe-file SHA-256 and a semantic recipe digest over sorted compact JSON excluding only `recipe_sha256`. Verify both at every binding load.
6. Keep the immutable manifest unchanged after freezing. Record live dispatch state in a separate executor handoff/ack file rather than mutating `hardware_dispatched` inside the frozen manifest.

## Reuse a validated executor safely

Existing durable manifest-driven modules may be copied as a starting point, but this is source generation, not blind device-number substitution. Update and verify:

- batch ID and frozen manifest hash;
- allowed device range, binding index offset, and explicit device order;
- recipe filename pattern and labels;
- authoritative-grid equality checks;
- predecessor terminal/health/ledger path for the first device;
- subsequent-device predecessor logic;
- CLI choices, compiler loops, plotting loops, and every offline fixture/test.

The first device must source its starting pose from the predecessor preparation terminal and require the predecessor candidate terminal, health cleanup, result, and `unknown=false`. Historical cleanup in a closure record is provenance only; live travel still requires fresh output-OFF, matrix-open, empty-error, REAR-terminal, loaded-driver, sole-edge, global-owner, and exact Stage/Zaber pose gates.

Before hardware execution, run syntax checks, the complete offline no-replay/safety suite, and the real compiler for all candidates. Verify actual SET/RESET point counts and native points per 10-cycle request. A missing optional test runner is not a reason to skip tests when the suite also has standard-library entrypoints.

## Alignment handoff

1. Travel once to the frozen absolute target under a durable motion INTENT/COMPLETE journal.
2. Review the fresh nominal Camera-1 image and select the physical pad immediately adjacent to the probe apex; do not use frame center blindly.
3. Compute the bounded correction from the calibrated native-per-pixel response and write `correction-reviewed.json` before motion.
4. Apply the correction once. Recapture and quantify displacement with substrate-only phase correlation using a Hanning window and a probe-excluding ROI.
5. Propagate the selected pad centroid from the nominal image using the measured substrate shift. Require same-pad visual identity, acceptable residual, and no gross obstruction before writing `alignment-verified.json`.
6. Copy `candidate_id` and `recipe_sha256` from the immutable recipe when sealing alignment. Optical alignment remains `physical_contact_claim=false`.

A bright-pad contour may disappear after successful correction because the blunt probe overlaps it. In that case, do not declare detection failure or move again: use the visible same-pad review plus probe-excluding nominal-to-final substrate registration to compute the residual.

## Worker and continuation separation

- Start exactly one per-device `run_device` worker holding the shared global owner through preparation and candidate supervision.
- Preparation/forming/conditioning sweeps never increment candidate-cycle count.
- While that worker is alive, continuation automation must not send hardware getters, edit running source, restart an edge, start a duplicate worker, or interrupt for plots/status.
- Keep read-only hourly reporting separate from acting continuation. The reporting job reads ledgers/process state only. The continuation job advances only after the worker exits and exact terminal, health, cleanup, and `unknown=false` evidence are persisted.
- Any unresolved motion INTENT, acquisition UNKNOWN, transport ambiguity, cleanup failure, source-pose mismatch, or owner conflict stops progression without replay.
- On completion, stop both recurring jobs and aggregate only verified full cycles.

## Verified session pattern

A final-round eight-candidate proposal after a 74-recipe dataset was bound to the next eight authoritative grid devices, frozen under a fresh namespace, validated with the existing 18-test no-replay suite, and compiled for all native point geometries before live travel. The first device used a reviewed bright-pad correction followed by a sub-5-pixel substrate-registration residual; only then was its preparation worker launched. This pattern is reusable, but proposal hashes, labels, device range, grid targets, policy, predecessor paths, and calibrated corrections must always come from the current campaign.
# Round-2 BO batch with revised 300-cycle cap

Use this note when executing an already-generated multi-candidate BO batch after the operator changes only the endurance cap.

## Validated pattern

- Reuse the retained proposal only after verifying its hash, candidate count, bounds/finite checks, duplicate checks, and explicit not-dispatched state.
- Audit device occupancy across every campaign namespace. Do not assume the numerically previous device is unused. Resolve eligible positions from the authoritative absolute-grid map while preserving proposal-row order.
- Freeze a new append-only execution namespace. Record proposal/model/grid hashes, immutable per-row recipe hashes, candidate IDs, absolute targets, and `hardware_commands: 0` before motion.
- Propagate the cap to all enforcement layers: recipe policy, candidate right-censor/terminal test, and supervisor completed-batch stop. Leave 10-cycle batches, health cadence, minimum-cycle rule, three-consecutive-failure rule, and no-replay semantics unchanged unless separately authorized.

## Executable preflight

Compilation is not enough. Import the generated candidate controller in the actual environment, call its real `initial_ledger`, and build Batch 1 segments before bias. Assert:

- required manifest fields (including `batch_id` where the controller expects it);
- exact source-row and manifest-binding index;
- candidate ID and recipe hash;
- preparation-terminal hash and final pose;
- SET/RESET point counts and total native points;
- recipe and supervisor both enforce the revised cap.

A missing runtime-schema field caught here is a pre-dispatch compatibility defect, not grounds to regenerate the optimizer proposal. Repair the manifest/controller interface, retain the new manifest hash, and rerun the real constructors.

## Derived-controller audit

Text substitution can leave stale device labels even when binding, output path, pose, and hash are correct. Treat console labels as provenance fields: correct them for future batches, but identify actual dispatches from durable binding/path/hash/wire evidence rather than the label alone. Never modify a controller file that is already executing merely to change a cosmetic label; patch only the future invocation source.

## Transition and alignment

At every device boundary: verify the prior terminal ledger and final health cleanup, retract by the authorized clearance, move to the absolute target, apply only the retained alignment offset, and validate the fresh image against the prior aligned image. For a regular grid, phase correlation should show the expected lattice displacement on the moved axis and a small residual on the orthogonal axis; this is a geometric registration gate and never a physical-contact claim.

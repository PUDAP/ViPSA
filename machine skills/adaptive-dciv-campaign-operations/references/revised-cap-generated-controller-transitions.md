# Generated-controller transitions for revised-cap BO batches

Use this checklist when a validated multi-candidate proposal is authorized with a new hard-cycle cap and each candidate advances automatically to a fresh device.

## Freeze before hardware action

- Preserve proposal row order and source hash; do not regenerate an already validated proposal.
- Audit device occupancy across all campaign namespaces, then select eligible positions from the authoritative absolute-grid map. Never infer eligibility or coordinates from adjacent motion.
- Freeze one recipe per device with the revised cap while retaining batch size, minimum-cycle gate, health cadence, consecutive-failure rule, and no-replay policy unless separately authorized.
- Propagate the cap to three enforcement layers: recipe policy, candidate terminal/right-censor logic, and supervisor completed-batch boundary.

## Executable preflight

For each generated device controller:

1. Recompute exact SET and RESET arrays from the immutable recipe and assert branch and total native-point counts.
2. Compile travel, alignment, preparation, candidate, health, and supervisor scripts.
3. Import the candidate controller in the real environment; execute `initial_ledger` and construct the first batch's segments.
4. Verify campaign root, device ID, source row/binding index, candidate ID, recipe hash, preparation-terminal hash, cap, and supervisor boundary.
5. Search every generated file for stale prior-device IDs, binding indices, cap literals, poses, point-count assertions, and console labels.
6. Use the preparation terminal's actual final pose in candidate and health preflight; forming attempts make final Z device-specific.

A stale console label is cosmetic only when bindings, paths, pose, candidate ID, and recipe hash independently prove the correct target. Fix future logs without interrupting an active acquisition.

## Transition gate

Advance only after the previous device is terminal with:

- complete verified-cycle accounting;
- recipe-specific failure or right-censored cap classification;
- final health check;
- output OFF, matrix open, empty error queue;
- cleanup verified; and
- no UNKNOWN exposure.

Then retract from the actual final Z, move to the next device's authoritative absolute XY, apply/verify optical alignment, and run preparation. Optical alignment is not contact.

## Hourly reporting

Keep periodic status reporting observational and independent from acquisition. Read manifests, candidate ledgers, health records, and process state. Report active device/phase, verified cycles, latest health/cleanup, failure criterion, configured cap, UNKNOWN/transport faults, completed candidates, and pending devices. Process absence alone is not proof of completion; terminal ledger evidence controls. If the user requested hourly updates, send a brief heartbeat even when no material change occurred.

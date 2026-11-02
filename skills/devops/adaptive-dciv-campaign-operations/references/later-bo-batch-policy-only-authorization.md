# Later BO-batch authorization with a revised cycle cap

Use when an optimizer has already generated and validated the next batch, and the operator authorizes execution while changing only a campaign policy such as the hard cycle cap.

## Validated workflow

1. Prefer the existing hash-validated proposal that already incorporates the prior batch outcomes. Do not refit or regenerate merely because execution authorization arrived later.
2. Verify the source proposal hash, candidate count, finite/in-bounds validation, absence of within-batch duplicates, and an optimizer manifest stating that no hardware dispatch occurred.
3. Audit durable device occupancy across campaign namespaces before assigning candidates. The immediately preceding BO directory may not contain older initial-design devices.
4. Resolve eligible positions from the authoritative absolute-grid file and serpentine traversal—not adjacent-motion arithmetic. At a row boundary, the sequence can be `...52 → 51 → 61 → 62...`.
5. Freeze a new authorized execution namespace. Preserve proposal row order, candidate parameters at full precision, source hashes, and acquisition provenance.
6. Change only the explicitly authorized policy field. If the user changes the hard cap from 200 to 300, retain the 10-cycle batch size, minimum-cycle gate, health-after-each-batch cadence, three-consecutive-failure rule, and no-replay policy unless separately changed.
7. Bind each row to a unique eligible device and authoritative absolute target. Record proposal, optimizer-manifest, and grid hashes; per-device recipe hashes; physical sequence; and `hardware_commands: 0` before motion.
8. Start only Candidate 1 after fresh output-OFF, matrix-open, empty-error, pose, alignment, and preparation gates. Keep the other seven recipes frozen and undispatched until automatic progression reaches them.

## Verification

- Proposal and optimizer-manifest hashes match their retained source values.
- Exactly eight recipes exist and preserve the eight proposal rows in order.
- Every device is unused in the campaign and has an authoritative grid coordinate.
- Every recipe carries the revised cap and unchanged remaining policy fields.
- No hardware command occurs until the execution manifest is durable and re-read successfully.

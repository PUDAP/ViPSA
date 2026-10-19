# Operator-supplied notebook BO handoff validation

Use when an optimizer supplies immutable recipes for a default-owned instrument executor. These checks were exercised successfully on an eight-recipe qLogNEHVI handoff; they establish software-artifact consistency, not execution or physical qualification.

## Preserve the requested workflow and provenance

When the operator explicitly requests the supplied notebook workflow unchanged, do not substitute a preferred surrogate, acquisition function, objective definition or training snapshot. Record the exact approved changes, such as joint batch size. Keep notebook/data/output hashes and identify mixed measured, projected and operator-assigned coordinates as such. A user-approved proxy coordinate is not retroactively a measured endurance result. Predictions in a proposed recipe are not acquired datapoints.

## Validate every recipe before dispatch

1. Hash the exact notebook, source snapshot, proposal CSV, campaign configuration and diagnostics referenced by the handoff; compare each to its declared file SHA-256.
2. Preserve batch/device/candidate/request identifiers literally. Validate UUID format before lookup; require uniqueness and agreement between handoff entry and recipe file.
3. Distinguish semantic recipe hashes from file-byte hashes. If the producer hashes a recipe excluding its self-referential `recipe_sha256` field, use that documented serialization exactly; do not normalize numbers or repair identifiers to make a mismatch pass. Record both hashes.
4. Verify full-precision controls against frozen bounds, and compare complete control tuples for duplicates within the new batch and against the source snapshot. Never execute the rounded chat display values.
5. Compile both polarity arrays through the existing compiler and settings resolver. Record native commands and complete point counts. Do not hand-assemble an incomplete settings dictionary or silently change a short/low-amplitude proposed waveform.
6. Read the cap from the current batch policy; distinguish full SET/RESET pairs from individual write sweeps and from the preceding initial-screen cap.
7. Assert exact recipe/device coverage in code and persist the per-recipe validation manifest. Artifact validation does not replace live checks, exclusive ownership or execution-software tests.

## Acknowledgement and execution status

Preserve the immutable source handoff and recipes. Write a separate executor acknowledgement linked by batch ID and handoff hash; mutable batch state can point to it without changing the source hash. Distinguish `acknowledged`, `artifacts verified`, `live getters verified`, `dispatched`, and `completed`. Report started only after an actual acquisition dispatch is recorded, with its native run ID and raw response path.

For live readiness, observe heartbeat connectivity over a sufficiently long discovery interval and use fresh output/matrix/terminal/pose readbacks under the existing owner. Sparse CLI discovery is not proof of offline edges. A successful readiness readback is not proof that a candidate test ran.

Do not create fake per-device result placeholders to satisfy an optimizer monitor. Completed, censored, infrastructure-fault and UNKNOWN records must preserve their distinct provenance. Confirm whether a monitor belongs to the optimizer or executor profile before changing it; do not duplicate model-update or hardware-dispatch ownership.

# Verified ENOSPC preparation-boundary recovery

## Exercised pattern

A controller stopped with ENOSPC and a journal label claiming preparation had not started. Exact native START/command/COMPLETE receipts instead proved four forming sweeps, preparation operations 01–07, and the preceding health read completed. The last saved position-read INTENT also had a returned native receipt. The first missing stress operation was prep-08, not forming or prep-01.

A separate, exclusively claimed continuation preserved the original journal, bound the native evidence and recipe, obtained fresh owned schema/idle/output-OFF/matrix-open/error/position checks, and ran only remaining preparation followed by the unchanged candidate recipe. Eleven offline recovery tests passed before live execution. The live continuation completed preparation and ten candidate cycles, stopped at the recipe-specific failure latch, and verified cleanup. This validates the no-replay boundary technique, not any later device's acquisition handoff.

## Reusable safeguards

- Journal status strings are lower-confidence than identity-bound native receipts; conflicting flags require audit, not a reset.
- Preserve original interruption/UNKNOWN history separately from a subsequently proven terminal outcome.
- Report inherited total energy separately from continuation incremental energy. A continuation's cumulative total must not be added again to the original total.
- Storage recovery does not authorize replay. Restore reserve first, then reconcile the exact outstanding operation.
- Clear regenerable caches only with the user's approval; preserve experimental raw data, CSVs, journals, recipes, provenance and frozen release inputs.
- Standing continuous-campaign permission avoids repeated consent requests, not fresh safety checks. An offline-only child can hand a verified executable to its authorized parent; readiness-only success is never measurement execution.
- Freeze only after current-source full tests pass, and independently verify the package before live launch.

## Scope limit

A later navigation identifier-drift issue remained under investigation. Its acquisition recovery is not a validated workflow and is not described here as one.

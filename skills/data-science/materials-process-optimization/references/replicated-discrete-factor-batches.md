# Replicated discrete-factor batch designs

## Durable lessons

- Treat independently fabricated specimens as process replicates; multiple devices on one specimen are nested observations.
- Interleave anchor repeats over fabrication time and distribute them spatially.
- Balance the unique-screen subset separately from repeated anchors. If all anchors occupy one factor level, allocate indivisible extra screen counts to underrepresented levels rather than further overweighting the anchor level.
- Verify component-ratio mappings algebraically. For `A:B`, component-B fraction is `B/(A+B)`.
- Keep ratio text and both component percentages in separate CSV columns.
- Use constrained maximin or D-optimal selection with low pairwise factor correlation; reject infeasible corners before optimization.
- Keep fabrication order, carrier placement, and measurement order independent.
- Export an exact per-sample CSV, carrier-layout CSV, no-jitter pairwise plot, and programmatic verification of totals, distinct recipes, identical anchors, factor-level counts, and checksum.

## Example ratio mapping

For `DMF:DMSO`:

| DMF:DMSO | DMF vol.% | DMSO vol.% |
|---:|---:|---:|
| 3:1 | 75 | 25 |
| 2:1 | 67 | 33 |
| 1:1 | 50 | 50 |
| 1:2 | 34 | 66 |
| 1:3 | 25 | 75 |

When a requested factor is absent from historical process tables, label it as a new prospective factor, state the assumed centre/levels, and hold coupled variables fixed.

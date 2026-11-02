# Discrete small-batch DOE with anchor replication

Use this pattern when a first prospective materials batch must estimate repeatability while screening several discrete process factors.

## Recommended structure

For a 16-specimen batch:

- 4 independently fabricated repeats of one high-fidelity anchor;
- 12 distinct screening recipes;
- repeats interleaved through fabrication time rather than made consecutively;
- repeats distributed across carrier positions rather than clustered;
- measurement order randomized independently of fabrication order.

Treat specimens/substrates as the experimental units. Multiple devices on one substrate are nested observations, not fabrication replicates.

## Constructing the 12-recipe screen

1. Declare allowed discrete levels for every factor.
2. Preserve one known high-fidelity anchor separately from the screen.
3. Balance marginal level counts as evenly as 12 runs permit.
4. Select combinations using a maximin or D-optimal criterion while penalizing pairwise factor correlation.
5. Apply feasibility constraints before selection; do not populate implausible corners merely to improve geometric balance.
6. Verify programmatically:
   - 16 total rows;
   - 4 identical anchors;
   - 12 distinct screen recipes;
   - every allowed level represented as intended;
   - no accidental anchor duplicate among screen rows;
   - declared factor correlations and minimum normalized separation.

A small screening batch primarily estimates main effects. Treat interactions as exploratory unless the design explicitly supports them.

## Solvent-ratio notation guard

Keep the ratio label and component percentages in separate columns. For a ratio written `DMF:DMSO`:

| DMF:DMSO | DMF vol.% | DMSO vol.% |
|---:|---:|---:|
| 3:1 | 75 | 25 |
| 2:1 | 67 | 33 |
| 1:1 | 50 | 50 |
| 1:2 | 34 | 66 |
| 1:3 | 25 | 75 |

Do not infer percentage ordering from a user-provided list without checking which component the percentage names.

## New factors absent from historical data

If a requested factor was absent from the historical tables, such as annealing time:

- label it as a new prospective factor;
- state the assumed centre and low/high levels;
- keep coupled variables such as annealing temperature fixed;
- place the assumption directly in the CSV rather than hiding it in prose;
- ask for correction when the centre value is not already established.

## Deliverables

Produce at minimum:

1. Main CSV with fabrication order, sample ID, design type, all factor values, fixed-variable placeholders, carrier row/column, and recipe role.
2. Carrier-layout CSV.
3. Pairwise plot using exact values without jitter, distinguishing unique recipes from repeated anchors.
4. Short verification record with row counts, distinct-recipe counts, level counts, and a checksum.

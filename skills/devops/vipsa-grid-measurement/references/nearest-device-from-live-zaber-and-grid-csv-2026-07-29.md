# Nearest grid device from live Zaber X/Y (2026-07-29)

## Context

The user asked for the closest device "according to grid runner" after manual stage/electrical work. The useful workflow was to identify the current physical device from live Zaber X/Y and the relevant `grid_positions.csv`, not from stale run narrative or newest partial device folder.

## Procedure

1. Query live Zaber position through PUDA (`zaber.get_current_position`).
2. Select the active/relevant grid runner's `grid_positions.csv` for the substrate/run. If several exist, prefer the current substrate/run family and the file referenced by the active/continuation runner.
3. Parse `device_number,x,y` rows.
4. Compute Euclidean native-unit distance from live `(x,y)` to each grid target.
5. Report the nearest device plus live position, target position, `dx`, `dy`, and distance. Keep it concise.

## Concrete example

Live Zaber: `(x=271765, y=490910)`.

For S9 7x7 `grid_positions.csv`, nearest devices were:

| device | target x | target y | dx | dy | distance |
|---:|---:|---:|---:|---:|---:|
| 9 | 271765 | 491131 | 0 | -221 | 221 |
| 2 | 271765 | 486131 | 0 | 4779 | 4779 |
| 8 | 266765 | 491131 | 5000 | -221 | 5004.9 |

So the nearest/current device was S9 device 9.

## Pitfall

Do not infer the current device from the newest directory, incomplete `DONE.json`, or a prior message. Use live Zaber X/Y plus the grid CSV.
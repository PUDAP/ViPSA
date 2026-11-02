# Split-run substrate assembly and 4x4 overview packaging

Use when one substrate campaign is split across an isolated Device-1 run and a continuation covering Devices 2–16.

## Source assembly

- Define one explicit source directory per device; do not rely on newest-file discovery alone.
- Require exactly one `all_measurements.csv` for each expected device.
- Verify identity from both folder naming and per-device summary metadata.
- Preserve the two source-run paths in the package manifest.
- A split acquisition is still one substrate package only after all 16 device identities and cycle counts validate.

## Standard Pratap 30-cycle contract

For each complete device:

- export root `Forming.xlsx`, `Set.xlsx`, and `Reset.xlsx`;
- retain `all_measurements_source.csv` and source summary;
- create `30/` with paired SET/RESET workbooks and per-cycle sheets;
- require cycles 1–30, 121 SET rows/cycle, 161 RESET rows/cycle, totals 3,630 SET and 4,830 RESET rows;
- create a 282-row combined trace table per point index with voltage/current pairs for all 30 cycles;
- preserve acquisition order and commanded-voltage plotting;
- create connected semilog I–V, ON/OFF, and Vset artifacts.

## Root overview

Create a 4×4 shared-axis overview for Devices 1–16 from canonical source rows. Overlay all 30 ordered SET+RESET traces per device with one cycle color scale. Treat it as an overview, not a replacement for per-device artifacts.

## Validation

- exactly 16 device folders;
- readable XLSX files and expected cycle sheets;
- non-empty plots and raw sources;
- correct row/cycle totals per device;
- 282 combined rows per device;
- package manifest records source provenance;
- ZIP `testzip()` passes;
- report ZIP entry count, bytes, and SHA-256.

Packaging is file-only. Do not issue instrument, motion, camera, light, or matrix commands during export.

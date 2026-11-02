---
name: data-saving-pattern
description: "Use when packaging Pratap data in the New.zip layout."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pratap, vipsa, data-packaging, xlsx, provenance]
    related_skills: [xlsx, puda-data]
---

# Data saving pattern

## Overview

Package Pratap device datasets into the exact user-supplied `New.zip`-style layout. Preserve original runs; select a complete canonical dataset; document any partial, interrupted, superseded, or retested history without contaminating canonical endurance data.

## When to use

Use when arranging or returning a Pratap substrate or device folder. Treat an uploaded reference device folder as authoritative over older inferred conventions.

## Exact device layout

```text
device X/
├── Forming.xlsx
├── Set.xlsx
├── Reset.xlsx
├── all_measurements_source.csv
├── README.txt
├── deviceX_partial_history.json       # only when documented history exists
└── 30/
    ├── pair_device_X_s.xlsx
    ├── pair_device_X_r.xlsx
    ├── pair_device_X_COMBINED.csv
    ├── pair_device_X_SEMI_LOG.png
    ├── pair_device_X_On_Off_Plot.png
    ├── pair_device_X_On_Off_Ratio_VALUES.csv
    ├── pair_device_X_Vset_Histogram.png
    └── pair_device_X_Vset_Values.csv
```

Preserve exact labels, case, primes, spaces, and filename tags (`7`, `7'`, `d1`, and `D1` are distinct).

## Root files

- `Forming.xlsx`: sheets `Forming` and `Metadata`; includes all canonical forming SET attempts and forming RESET. Forming rows use `forming_attempt` when present.
- `Set.xlsx`: sheets `Conditioning SET` and `Metadata`.
- `Reset.xlsx`: sheets `Conditioning RESET` and `Metadata`.
- `all_measurements_source.csv`: unfiltered canonical source in acquisition order.
- `README.txt`: substrate/device identity, canonical source, protocol, retest/canonical-selection policy, and every warning or exception.
- `deviceX_partial_history.json`: include only when prior/partial history materially exists and the README explains it. Never fabricate it for an ordinary complete device.

A normal complete device has 13 files. A device with one documented partial-history JSON has 14. Do not enforce 13 files when the exception is scientifically required.

## `30/` endurance files

### SET workbook

`pair_device_X_s.xlsx` has 32 sheets:

```text
All SET cycles
Metadata
Cycle 001
...
Cycle 030
```

Require exactly 3,630 SET rows total and 121 rows per cycle.

### RESET workbook

`pair_device_X_r.xlsx` has 32 sheets:

```text
All RESET cycles
Metadata
Cycle 001
...
Cycle 030
```

Require exactly 4,830 RESET rows total and 161 rows per cycle.

Use three-digit cycle sheet names (`Cycle 001` through `Cycle 030`).

### Combined CSV

`pair_device_X_COMBINED.csv` has 282 data rows and 61 columns:

```text
index, V1 (V), I1 (A), ..., V30 (V), I30 (A)
```

For each cycle, concatenate its 121 SET rows followed by its 161 RESET rows. Preserve acquisition order; never sort by voltage.

### Semilog I–V plot

`pair_device_X_SEMI_LOG.png`:

- one axis combining all 30 cycles;
- X = commanded voltage;
- Y = `|Current|` on logarithmic scale;
- connected measured points in acquisition order;
- one cycle color progression;
- no sorting, interpolation, or scatter-only substitution.

### ON/OFF products

`pair_device_X_On_Off_Ratio_VALUES.csv` has 30 rows:

```text
CycleNumber, Current_Off_A, Current_On_A, On_Off_Ratio
```

Use SET forward current at `+0.1 V` as OFF and SET return current at `+0.1 V` as ON. `pair_device_X_On_Off_Plot.png` uses Cycle on X and log `|Current|` on Y with separate connected `o-` OFF and ON series.

### Vset products

`pair_device_X_Vset_Values.csv` has 30 rows:

```text
Cycle, Vset_V
```

`pair_device_X_Vset_Histogram.png` is a simple 10-bin histogram with Vset on X and Count on Y.

## Per-device reporting plot (authoritative user reference)

Return one two-panel figure per device: upper panel contains only forming SET attempts, forming RESET, and six conditioning SET/RESET pairs; lower panel contains only the recorded endurance cycles, colored by cycle with PF solid, PB dashed, NF dotted, NB dash-dot and a cycle colorbar. Both panels use **commanded/programmed voltage** on X and actual measured |current| on logarithmic Y. Preserve acquisition order, no smoothing/interpolation or voltage sorting. Measured voltage is retained in raw data and may appear only in separately labeled diagnostic plots, never substituted in the standard report. Title must identify substrate and device. Never mix source devices/retests. Substrate summary I–V panels contain **only the 30 endurance SET/RESET cycles**, excluding all forming and conditioning, using commanded voltage × measured |current|. This does not remove forming/conditioning from the upper panel of individual two-panel device reports. Label incomplete cycles honestly. Send the figure itself after each device, not routine status. When patching a running Python plotter, changing disk code does not update a cached imported module: verify actual delivery path and reload/restart only at a safe measurement boundary, or regenerate from saved data without rerunning hardware.

## Substrate package

```text
substrate N/
├── device 1/
├── ...
├── device 16/
├── package_manifest.json
└── optional substrate overview plot/README
```

Use canonical complete datasets. A successful full retest replaces an invalid/partial run as canonical while the prior run remains unchanged and is documented as history. Never merge uncertain stress into canonical cycles.

## Procedure

1. Inventory every source run and exact label. Completion criterion: each intended label has one explicit canonical source and any superseded sources are listed.
2. Verify canonical source phases and cycle counts. Completion criterion: all 30 SET and 30 RESET cycles have exact 121/161 row counts.
3. Generate root workbooks, source CSV, README, and any justified history JSON. Completion criterion: sheets, schemas, and warnings match source truth.
4. Generate all eight `30/` products. Completion criterion: 32-sheet SET/RESET workbooks; 3,630/4,830 rows; 282-row combined CSV; 30-row ON/OFF and Vset CSVs; three plots exist and are legible.
5. Write `package_manifest.json` with source paths, row counts, canonical/retest policy, warnings, files, and screening flags.
6. ZIP the package and run `ZipFile.testzip()`. Preserve original runs unchanged.
7. If Telegram rejects the full ZIP, split on device-folder boundaries into independent ZIPs below 20,000,000 bytes. Each part must retain the `substrate N/` root; verify every part CRC and SHA-256. Send parts as separate messages.

## Common pitfalls

- Do not put raw operation JSON, alignment frames, `DONE.json`, or runner internals into ordinary user-facing device folders.
- Do not discard scientifically relevant partial history; use a documented history JSON or clearly named extra folder only when justified.
- Do not assume all root conditioning workbooks are complete when the README declares a partial-history exception.
- Do not use `Cycle 01`; use `Cycle 001`.
- Do not call a 30-cycle dataset healthy solely because it completed. Preserve RESET-compliance-pinned/short-like screening metadata.
- Do not normalize case or prime marks.
- When auditing resumed CSVs against prior aggregate or operation CSVs, later aggregates may union metadata headers (for example adding `cycle` to earlier forming rows). Compare every recorded field and acquisition order; absent metadata fields may correspond to blank aggregate values. Document this equivalence rather than claiming byte-identical row dictionaries. Never permit a changed recorded value or missing measurement row.

## Verification checklist

- [ ] Exact device labels and folder names preserved
- [ ] Canonical source and history policy documented
- [ ] Root workbook sheets and row counts verified
- [ ] SET workbook: 30 cycle sheets, 121 rows each, 3,630 total
- [ ] RESET workbook: 30 cycle sheets, 161 rows each, 4,830 total
- [ ] Combined CSV: 282 rows, 61 columns
- [ ] ON/OFF CSV: 30 rows, exact four-column schema
- [ ] Vset CSV: 30 rows, exact two-column schema
- [ ] Plots visually inspected
- [ ] Package manifest complete
- [ ] ZIP CRC, file count, and SHA-256 verified
- [ ] Every Telegram part is below 20 MB and independently extractable

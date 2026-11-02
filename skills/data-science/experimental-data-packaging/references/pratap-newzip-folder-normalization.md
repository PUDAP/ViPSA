# Pratap/New.zip device-folder normalization

## Source identity gate

Before transforming a folder received through chat, confirm the actual artifact rather than selecting the newest local ZIP:

1. Record filename, bytes, SHA-256, and arrival time.
2. Inspect archive root plus internal substrate and device labels.
3. If the requested substrate and internal labels disagree, stop—never transform or relabel the wrong substrate.
4. Never assume an older Downloads file is the attachment referenced by the current message.
5. Preserve the source unchanged and write normalized output separately.

## Standard device layout

Each complete 30-cycle device folder contains exactly:

```text
device X/
├── Forming.xlsx
├── Set.xlsx
├── Reset.xlsx
├── all_measurements_source.csv
├── README.txt
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

Preserve exact labels/case (`7` ≠ `7'`; `D1` ≠ `d1`). Keep raw operation JSON, alignment frames, machine manifests, and histories outside the user-facing device folders.

## Content and verification

- Root workbooks hold forming/forming-RESET and conditioning operations with Metadata sheets.
- `all_measurements_source.csv` preserves the complete canonical acquisition order.
- Standard SET workbook: cycles 1–30, 3630 rows total, 121 rows/cycle.
- Standard RESET workbook: cycles 1–30, 4830 rows total, 161 rows/cycle.
- Combined CSV: 282 rows. ON/OFF and Vset CSVs: 30 rows each.
- Plot connected measured points in acquisition order on semilog `|I|`; never sort/interpolate.
- For >30-cycle sources, preserve the full source CSV and state which 30 cycles populate `30/`.
- Verify every workbook opens, all expected sheets/rows exist, each of the 13 files is nonempty, and ZIP CRC passes.
- For a 20 MB transport limit, make independently valid ZIP groups below 20,000,000 bytes and send each in a separate message with a common root folder.

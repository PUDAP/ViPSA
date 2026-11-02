# ViPSA multi-device all-cycle export

## Validated campaign shape

A Pratap comparison artifact labeled Devices 0–9 mapped to ten distinct source CSVs. Device `4` used the display label `Device 4R` (replacement/compensation device). Each device contained:

- 30 endurance cycles;
- 121 SET rows/cycle (`0 → +3 → 0 V`);
- 161 RESET rows/cycle (`0 → −4 → 0 V`);
- 282 rows/cycle;
- 3,630 SET rows and 4,830 RESET rows;
- 8,460 endurance rows/device;
- 84,600 endurance rows across ten devices.

The same source files also contained forming and conditioning phases. Those were kept separate from the endurance export rather than silently mixed into cycle data.

## Correction captured

A request for “all cycles of all these 10 devices” was initially misread as “the last 10 cycles.” The correct approach is to locate the manifest behind the supplied multi-device comparison plot and resolve every device’s source file before exporting.

## Correct workbook handoff

For a plain Excel handoff:

- one workbook per device;
- `Summary` sheet;
- `All 30 cycles` sheet;
- `Cycle 01` through `Cycle 30` sheets;
- consolidated workbook with 84,600 endurance rows;
- source manifest, comparison plot, README, and SHA-256 manifest;
- ZIP integrity plus workbook row/sheet verification.

## Uploaded-template mirroring

A supplied example ZIP used root-level Forming/Set/Reset files and a numbered subfolder containing paired-cycle data and analyses. The correct mirrored output was:

```text
device data/
  device 0/
    Forming.xlsx
    Set.xlsx
    Reset.xlsx
    all_measurements_source.csv
    README.txt
    30/
      pair_device_0_s.xlsx
      pair_device_0_r.xlsx
      pair_device_0_COMBINED.csv
      pair_device_0_SEMI_LOG.png
      pair_device_0_On_Off_Ratio_VALUES.csv
      pair_device_0_On_Off_Plot.png
      pair_device_0_Vset_Values.csv
      pair_device_0_Vset_Histogram.png
```

This was repeated for `device 0` through `device 9`. The folder remained `device 4`, while metadata and README preserved the authoritative label `Device 4R`.

## Derived outputs

- The combined CSV used one V/I column pair per cycle and concatenated each cycle’s SET and RESET acquisition order.
- ON/OFF values were explicitly documented as derived at a chosen read voltage and branch.
- Vset was documented as a derivative/jump-based estimate rather than an instrument-native field.
- Semi-log plots used connected traces in acquisition order and `|I|` on the log axis.

## Verification checklist

- Ten exact device folders exist.
- Every paired workbook has 32 sheets: all-cycle data, metadata, and 30 cycle sheets.
- Every SET cycle sheet has 121 rows; every RESET cycle sheet has 161 rows.
- Required raw, derived, and plot files are non-empty.
- ZIP integrity test reports no errors.

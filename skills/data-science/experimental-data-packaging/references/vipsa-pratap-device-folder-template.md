# ViPSA/Pratap multi-device folder export

## Trigger

Use when packaging all cycles for multiple Pratap devices into the folder pattern demonstrated by an uploaded `New.zip`-style template.

## Authoritative source and identity

- Start from the comparison directory's `manifest.json`.
- Resolve manifest paths to the current project root and require each source CSV to exist.
- Distinguish devices from cycles. For a Devices 1–25 comparison, “initial 10” means Devices 1–10 and “last 15” means Devices 11–25.
- Preserve manifest labels such as Device 4R even if the required folder remains `device 4`.

## Verified 30-cycle contract

For the established Pratap endurance protocol:

- include `phase == set` or `phase == reset` with a non-empty cycle;
- cycles must span 1–30;
- each cycle must contain 121 SET rows and 161 RESET rows;
- each device must contain 3,630 SET rows, 4,830 RESET rows, and 8,460 total endurance rows.

Keep the complete unfiltered `all_measurements.csv` as `all_measurements_source.csv`, so forming and conditioning history is preserved.

## Folder pattern

```text
<requested parent>/
  device N/
    Forming.xlsx
    Set.xlsx
    Reset.xlsx
    all_measurements_source.csv
    README.txt
    30/
      pair_device_N_s.xlsx
      pair_device_N_r.xlsx
      pair_device_N_COMBINED.csv
      pair_device_N_SEMI_LOG.png
      pair_device_N_On_Off_Ratio_VALUES.csv
      pair_device_N_On_Off_Plot.png
      pair_device_N_Vset_Values.csv
      pair_device_N_Vset_Histogram.png
```

The SET/RESET workbooks should contain an all-cycles sheet, metadata, and Cycle 01–30 sheets.

## Derivation provenance

- State the read voltage and branch used for ON/OFF values.
- State the Vset algorithm; do not silently substitute a largest-log-jump heuristic when a second-derivative method is required.
- Use commanded voltage for the main plot when compliance collapses measured voltage, but retain measured voltage in exported tables.

## Verification

Before delivery assert:

- exact device range and count;
- all required artifacts are non-empty;
- workbook sheet counts and per-cycle dimensions match the contract;
- every combined CSV has 282 rows (121 SET + 161 RESET) per cycle trace;
- the package manifest records labels, source paths, counts, and hashes;
- ZIP integrity (`testzip`) passes.

Never report success based only on archive creation.
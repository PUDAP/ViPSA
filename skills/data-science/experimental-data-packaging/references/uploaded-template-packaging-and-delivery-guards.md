# Uploaded-template packaging and delivery guards

## Why this guard exists

When a user supplies or replies to an archive and asks for a template-mirrored package, two independent identities must be verified before conversion:

1. **Transport identity** — the attachment actually arrived and is locally readable.
2. **Dataset identity** — its internal labels and source paths match the substrate/sample named by the user.

A recent file in Downloads is not proof that it belongs to the current message. Never substitute the newest or similarly named archive when the referenced attachment is unavailable.

## Mandatory source confirmation

Before processing an upload:

1. Locate the exact attachment from the current message or obtain its explicit local path.
2. Record filename, byte size, modification time, and SHA-256.
3. Test archive integrity.
4. Inspect top-level names, device/sample labels, and manifest substrate identity.
5. Report the source identity before conversion when prior ambiguity or rejected uploads exist.
6. If the current attachment is missing, rejected, or over the channel limit, stop and request named parts or an explicit local path. Do not fall back to a stale archive.

When multiple parts are expected, require all filenames, verify every part, and inventory their union for duplicates and missing units before merging.

## New.zip-style Pratap deliverable boundary

The user-facing device folder is a processed analysis package, not a raw run dump. For a canonical 30-cycle device it must contain exactly:

```text
device X/
  Forming.xlsx
  Set.xlsx
  Reset.xlsx
  all_measurements_source.csv
  README.txt
  30/
    pair_device_X_s.xlsx
    pair_device_X_r.xlsx
    pair_device_X_COMBINED.csv
    pair_device_X_SEMI_LOG.png
    pair_device_X_On_Off_Plot.png
    pair_device_X_On_Off_Ratio_VALUES.csv
    pair_device_X_Vset_Histogram.png
    pair_device_X_Vset_Values.csv
```

Do not place per-operation raw JSON/CSV files, alignment frames, `DONE.json`, internal summaries, checksum files, or run-history directories inside this user-facing device pattern. Keep the original upload/run unchanged as provenance.

Preserve exact labels and case (`7'`, `d1`, `D1` are distinct). Use a filename-safe deterministic tag only inside `pair_device_*` names, and document that mapping in the manifest.

For a source with more than 30 endurance cycles, retain the complete source in `all_measurements_source.csv`, but use explicitly selected cycles 1–30 for the canonical `30/` export unless the user requests another policy. Document the selection.

## Validation contract

For every canonical 30-cycle device verify:

- exactly 13 files in the device tree;
- SET workbook: all-cycles + metadata + 30 cycle sheets;
- RESET workbook: all-cycles + metadata + 30 cycle sheets;
- 3,630 SET rows (121 per cycle);
- 4,830 RESET rows (161 per cycle);
- 282 rows in the combined CSV;
- 30 ON/OFF rows and 30 Vset rows;
- all plots and workbooks are non-empty and readable;
- ZIP CRC test passes.

## Messaging-platform delivery

Treat the platform limit as **per message**, not merely per file or per final response. If the full ZIP exceeds the limit:

1. Create independently extractable ZIP parts, each safely below the byte limit.
2. Give every part the same root folder so extraction into one destination reconstructs the package.
3. Group whole device folders; never binary-split a ZIP unless the user explicitly accepts concatenation instructions.
4. Include common README/manifest files in each part when small.
5. CRC-test every part and record size/hash.
6. Send each part as a separate platform message; attaching several sub-limit files to one response can still exceed a per-message aggregate limit.

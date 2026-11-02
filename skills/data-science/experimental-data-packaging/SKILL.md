---
name: experimental-data-packaging
description: "Use when packaging multi-device experimental datasets."
version: 1.0.0
metadata:
  hermes:
    tags: [experimental-data, excel, packaging, provenance, validation]
---

# Experimental Data Packaging

## Scope

Use this class-level workflow when turning laboratory or instrument outputs into user-facing Excel workbooks, per-sample/per-device folders, consolidated datasets, plots, and ZIP archives. It applies across electrical, materials, imaging, and other repeated-measurement campaigns.

## Resolve the experimental unit before exporting

Words such as **device**, **sample**, **cycle**, **run**, and **measurement** are not interchangeable. Before building files:

1. Identify the requested experimental unit from the user’s wording.
2. Inspect the authoritative source behind any supplied plot, manifest, path, or archive.
3. Programmatically enumerate units and repetitions.
4. Verify expected counts before packaging.

Never substitute “the last N cycles” when the user asked for “N devices.” If a plot shows devices 0–9, resolve those device sources and all cycles belonging to each device.

## Source-first and provenance rules

- Prefer an artifact manifest or source paths referenced by the supplied comparison plot.
- Preserve display labels such as replacement-device suffixes even when folder names use numeric IDs.
- Keep raw source files alongside derived outputs when practical.
- Separate setup/forming/conditioning phases from endurance or production cycles unless the user explicitly asks to combine them.
- Record extraction rules for derived metrics such as ON/OFF and threshold voltage.

## Excel package contract

For multi-unit repeated measurements, default to:

- one workbook per unit;
- one all-cycles/all-repetitions sheet;
- one sheet per cycle/repetition;
- typed numeric columns with explicit units;
- a consolidated workbook across all units;
- a machine-readable manifest with sources, labels, counts, and hashes;
- a README explaining scope and derived fields.

## Mirroring an uploaded folder template

Inspect the uploaded archive before creating output. Reproduce the **semantic hierarchy**, not just filenames:

- root-level setup/forming/conditioning files;
- a repeated-cycle subfolder named with the actual cycle count;
- raw paired data, combined data, derived tables, and plots;
- exact user-requested parent and unit folder names.

Do not blindly copy the example’s cycle-count folder if the target data has a different count.

## Validation gates

Before delivery:

1. Verify every requested unit folder exists.
2. Verify every expected cycle/repetition exists and has the expected row count.
3. Open generated workbooks and validate sheet names, dimensions, and types.
4. Check consolidated totals arithmetically from unit × repetition × points.
5. Verify every required file is non-empty.
6. Run ZIP integrity testing.
7. Report concise totals: units, repetitions/unit, rows/unit, total rows, and any exclusions.

## Domain-specific references

- For a validated ViPSA/Pratap example covering Devices 0–9, 30-cycle endurance workbooks, replacement labels, and template-folder mirroring, see `references/vipsa-multi-device-all-cycle-export.md`.

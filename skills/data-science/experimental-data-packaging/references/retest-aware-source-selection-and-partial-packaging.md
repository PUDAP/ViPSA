# Retest-aware source selection and partial-run packaging

Use this reference when a device/substrate package has multiple completed runs, interrupted retests, contact-suspect repeats, or extra user-authorized cycles.

## Select sources by validity, then repeatability

1. Inventory every candidate source per device. A complete 30-cycle source must contain 30 SET and 30 RESET cycles with the expected ordered points; `DONE.json` alone is not proof.
2. Exclude invalid candidates before ranking: unverified/lost contact, offset-dominated open-like response, compliance-clamped pseudo-consistency, malformed operation order, or incomplete cycles.
3. Among comparable valid candidates, rank cycle variation consistently. A robust default is the median over ordered SET+RESET point index of the across-cycle IQR of `log10(max(|I|, floor))`.
4. Choose the lowest-variation valid source, not automatically the latest. Save source path, metric, exclusion reasons, and warnings in the manifest.
5. Do not call a contact-invalid or compliance-pinned run “best” merely because traces overlap tightly. If no contact-verified source exists, label the device unresolved/contact-suspect.

## Complete-device folder contract

Honor the requested root folder name literally. A complete repeated-cycle device folder should contain root setup/forming/conditioning workbooks, raw source and provenance, plus a cycle-count subfolder containing aggregate workbooks, one sheet per cycle, combined CSV, ordered semilog plot, and derived metric tables/plots.

Preserve raw acquisition order. Never sort hysteretic sweep rows by voltage.

## Partial and exceptional data

- A retest-only package must not silently substitute an older complete run for an interrupted retest.
- Preserve partial rows and raw operation files; clearly label status and uncertainty.
- Do not create a canonical cycle-count folder for a partial run because it implies completeness.
- When operation CSV schemas differ, concatenate files in numeric operation order, use the union of columns, fill absent fields with blanks, and preserve all row order.
- Keep extra user-authorized cycles in a separate subfolder retaining flags such as `contact_verified=false` and `user_contact_override=true`.
- Historical complete data may be linked separately, but not represented as the retest itself.

## Verification before delivery

Programmatically verify:

- exact requested root folder name;
- complete and partial unit lists;
- expected SET/RESET cycle and row counts for complete units;
- source/generated CSV totals and combined-file dimensions;
- every XLSX opens and expected sheets exist;
- required plots/files are non-empty;
- partial folders lack misleading canonical cycle-count folders;
- warning/override flags survive into manifests and READMEs;
- ZIP integrity with `testzip()`;
- ZIP entry count, byte size, and SHA-256.

Packaging is file-only work. Never issue instrument, motion, light, camera, switch-matrix, or SMU commands while producing an export, especially when the user holds manual control.

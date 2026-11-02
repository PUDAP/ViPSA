# Canonical retest-aware raw dataset packages

Use when consolidating multi-device experimental runs after interruptions, retests, extra endurance blocks, or case-sensitive device naming.

## Canonical selection

- Enumerate physical/device labels programmatically from source runs; preserve exact case and punctuation (`D1` ≠ `d1`, `7'` is distinct from `7`).
- Choose one complete canonical dataset per label. Prefer a later full retest over an interrupted/resumed trace when it fully repeats the requested protocol.
- Never discard earlier history. Place interrupted, resumed, failed-gate, or additional-endurance runs under clearly named history directories and record their source paths and interpretation.
- Do not replace a valid canonical full protocol with an additional endurance-only run, a contact-invalid nanoscale run, or a forming-gate failure.

## Package contract

Create a dedicated human-readable root folder and ZIP. Include:

- one canonical folder per exact device label;
- raw operation JSON/CSV, combined CSV, summary, alignment/camera evidence, completion markers, and plot;
- source-run metadata and any whole-substrate overview;
- `dataset_manifest.csv`, `package_manifest.json`, README, and `SHA256SUMS.txt`;
- clearly separated noncanonical history folders.

Manifest fields should include exact label, source role/path, row count, SET/RESET cycle counts, per-cycle RESET peak statistics, file count/bytes, and hashes of key files.

## Screening and verification

- Compute compliance incidence per cycle from each cycle's peak current; do not count compliance-clamped points as cycles.
- Keep completion and electrical quality separate: a completed run may still be compliance-pinned, contact-invalid, or nonswitching.
- Verify every canonical folder has non-empty `all_measurements.csv`, summary, and plot.
- Recompute every checksum from the packaged copy, test ZIP CRC, verify manifest row count equals canonical folder count, and report exclusions/history explicitly.
- Preserve original run directories unchanged.

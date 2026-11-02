# Relocating large PUDA legacy trees from a full disk

Use when a large legacy PUDA tree must be moved to another filesystem while active campaigns depend on durable local writes.

## Safety order

1. Pause new measurements before storage reaches zero free bytes. A campaign cannot safely continue if intents, receipts, ledgers, plots, or session state may fail to persist.
2. Identify whether the user performed a true move or only a partial copy. Compare source and destination file/directory counts and total apparent bytes; do not infer completion from the destination existing.
3. Keep the source untouched until a complete independent artifact is verified.
4. On NTFS or other metadata-poor destinations, hundreds of thousands of files can make `rsync -a`, hard-link preservation, or timestamp updates stall in filesystem metadata calls. Do not repeatedly restart the same metadata-heavy copy.
5. A single tar archive is a robust fallback:
   ```bash
   tar --sparse -cf /external/path/legacy-complete.tar -C /source/parent legacy
   ```
   Avoid verbose per-file progress when the source disk is nearly full because process logs can consume the remaining space.
6. Verify before deleting the source:
   - `tar -tf archive >/dev/null` exits zero;
   - count archive entries and compare with source files + directories + links;
   - stream a critical file such as `puda.db` from the archive and compare its SHA-256 with the source;
   - confirm archive size and external free space.
7. Preserve direct access to critical files separately when future tools expect a stable path. Extract the verified database to the external disk, hash it again, then create only the narrow compatibility symlink required by tooling. Do not present an incomplete partially copied tree as a complete mirror.
8. Delete the local source only after all verification passes, sync, and confirm meaningful free space before restarting edges or measurements.

## Reporting

State clearly whether a transfer is running, stalled, failed, or verified. Exit code 20 from an rsync process deliberately terminated during recovery is expected; distinguish it from the active replacement transfer. Never claim a move completed merely because a background copy process exited.

# Current-position overwrite continuation after standalone approach

Use this pattern when the user says “continue the grid from this device and overwrite previous data” after manual motion or a standalone contact approach.

## Resolve the physical device from live state

1. Stop assuming the device from the latest project note, partial folder, or prior runner boundary.
2. Verify no grid runner remains active.
3. Run a read-only PUDA preflight for microscope-stage Z, Zaber native X/Y, and 707B closed channels.
4. Compare live Zaber X/Y against `grid_positions.csv` and any verified aligned-device coordinates. The closest nominal device plus a plausible saved alignment offset identifies the physical device.
5. The live identity is authoritative. In the motivating S9 case, stale context pointed to device 4, but live `(287105, 486145)` matched device 5 nominal `(286765, 486131)` plus alignment offset.

## Prepare an overwrite boundary safely

1. Pause the per-device reporter before touching folders or reporter state.
2. Compute the restart boundary in actual serpentine traversal order.
3. Preserve pre-boundary summaries exactly once, including legitimate interrupted records if the user did not ask to backfill them.
4. Move canonical `device_N` folders at and after the boundary into a timestamped `overwrite_archives/from_device_N_<UTC>/` folder. Do not let stale `DONE.json` sentinels remain in active canonical paths.
5. Save an archive manifest containing:
   - overwrite boundary;
   - remaining serpentine order;
   - moved folders;
   - preserved summary device numbers;
   - reporter state before/after.
6. Prune `summary.partial.json` by traversal boundary and deduplicate device records.
7. Move any stale run-level `summary.json` into the archive so it cannot imply the restarted run is finished.
8. Invalidate reporter state for all replaced devices and clear `final_reported`; keep pre-boundary device reports marked as delivered.

## Runner handoff from the current device

- Clone the latest validated continuation runner; do not modify historical runners in place.
- Patch `START_AT_DEVICE` and every handoff metadata field together: device number, live aligned X/Y, stage Z, overwrite boundary, contact policy, and event labels.
- For the first device, preserve live X/Y and do not repeat alignment or lateral motion.
- If the standalone approach ended over-current, begin with a fresh low-bias read and guarded minimum-step retraction. Do not assume cleanup made contact valid.
- Gate stress on the active contact policy. For the current narrow-window policy:
  - `10 mV` read;
  - three unchanged-Z reads in `1–10 nA`;
  - two bounded `+0.5 Z` attempts, then one bounded `+1.0 Z` attempt;
  - retract each failed attempt’s exact positive net Z;
  - skip DCIV/pulses after final unstable/out-of-window contact.
- Preserve the SET-without-RESET branch: exactly five strongest RESET-read pairs, save their reads, then continue randomized pulses with independent compliance guards.
- Disable recording if the active campaign says no recording.

## Validation and launch

1. Compile the cloned runner.
2. Assert boundary, contact constants, stability-read count, attempt step sizes, exact-failed-attempt retraction, pulse fallback, and recording policy from source.
3. Start as one tracked background process without a `tee` pipeline that can orphan the Python child.
4. Require fresh `device_start` output for the intended boundary before reporting success.
5. Patch the reporter’s displayed contact window to match runner constants, resume it, and verify replacement devices were removed from its dedupe state.
6. Record preflight, archive, runner path/PID/session, policy, and reporter state in `project.md`.

## Pitfalls

- **Stale narrative identity:** “we previously resumed device 4” does not prove the probe is still on device 4 after later moves.
- **Numeric pruning without traversal:** use the serpentine boundary, not naïve numeric comparison unless equivalence is proven.
- **Summary-only cleanup:** stale canonical `device_N/DONE.json` folders can silently skip requested remeasurement.
- **Reporter mismatch:** a reporter can describe an obsolete 50–500 nA gate while the runner enforces 1–10 nA.
- **Over-contact handoff:** a compliance-limited standalone approach is not valid contact; the continuation must recover and revalidate before electrical stress.

# No-skip restart from device boundary: stale DONE skip recovery — 2026-06-30

## Use case

A ViPSA 8×8 grid continuation was restarted from device 14 after the user explicitly corrected the policy: **do not skip measurements**. The runner had been patched so contact/safety gates were record-only and DCIV + randomized pulses were still attempted. Device 14 completed correctly, but the next launch silently skipped stale `device_13` and `device_12` folders because the runner's resume filter excluded any folder with `DONE.json`, regardless of the requested restart boundary.

## Durable lesson

When the user asks to re-do measurements from device `N`, the restart boundary must override stale `DONE.json` files from that boundary onward. It is not enough to prune `summary.partial.json`; stale per-device folders can still cause the runner to skip old devices.

## Correct workflow

1. Stop any active runner and cleanup/verify:
   - SMU outputs off.
   - 707B `open_all()` and `get_closed_channels == nil`.
   - Stage motion aborted/idle if a previous approach was killed.
2. Compute restart set by serpentine traversal order from the requested boundary, not numeric `>= N`.
3. Before launching, archive every `device_XX` folder in the restart set unless it is a freshly completed artifact produced by the new no-skip override and intentionally preserved.
4. Prune `summary.partial.json` to retain only:
   - devices before the restart boundary; and
   - any newly completed no-skip override devices that should be preserved after an interrupted restart attempt.
5. If a restart already ran and skipped old `DONE.json` devices:
   - do not let the skip continue silently;
   - stop after the current in-progress device reaches a safe `device_finished` boundary when possible;
   - archive the stale skipped folders and any partial next-device folder;
   - restart so the skipped devices are measured.
6. Patch/verify runner logic so no-skip override is explicit in metadata:
   - `no_skip_override: true`
   - contact/open/short gates recorded as warnings only
   - DCIV artifacts present
   - randomized pulse artifacts present
7. Add coarse progress prints to long runners (`device_start`, `before_align`, `after_align`, `after_approach`, `device_finished`) so a future operator can distinguish a real hang from a long approach/DCIV/pulse phase.
8. Add a bounded timeout around NATS publish calls in resume runners to avoid indefinite silent hangs during flaky NATS/subscriber states.

## Verified pattern from the session

- Device 14 was re-measured under no-skip override: approach remained open-like, DCIV still ran, randomized pulses still ran, and `no_skip_override` was recorded.
- Old `DONE.json` folders caused devices 13/12 to be skipped on the next pass.
- The runner was stopped after a safe device boundary, stale folders for 13/12 and the partial next folder were archived, summary was pruned, and the runner restarted.
- Device 13 then completed freshly with DCIV and randomized pulses under the no-skip override.

## Pitfall

A runner comment such as “Devices >= START_AT_DEVICE are re-run even if old DONE.json files exist” is not sufficient if the actual filter still says:

```python
remaining = [d for d in remaining if not (OUT / f"device_{d['device_number']:02d}" / "DONE.json").exists()]
```

Either patch that filter to honor the restart boundary, or archive stale device folders before launching.

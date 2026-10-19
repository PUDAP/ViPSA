# Manual retest of a completed grid device with custom approach parameters (2026-06-30)

Use this when the user asks to retest a prior/completed grid device while a long grid/supervisor run is active or paused, and changes a single retest parameter such as approach Z step size.

## Safe sequence

1. Treat the request as a manual retest, not a normal continuation boundary.
2. Stop/pause any active grid runner and supervisor first; verify no old runner PIDs remain.
3. Run electrical cleanup before motion:
   - SMU outputs off.
   - `keithley-707b.open_all()`.
   - Verify `get_closed_channels() == nil`.
4. Create a distinct retest artifact folder instead of overwriting the original completed device unless the user explicitly requests overwrite, e.g.:
   - `device_15_retest_approach0p5_<timestamp>/`
5. Move to the target device using the recorded absolute Zaber X/Y coordinates:
   - Safe stage-Z retract before X/Y travel.
   - Absolute Zaber `move_x_to` / `move_y_to` with `units: null`.
   - Conservative pre-approach stage-Z return.
6. Re-align if the retest involves fresh contact or uncertain positioning.
7. Run the requested approach parameter override only for the retest and write it into `approach.json` and `summary.json`.
8. Execute the requested electrical sequence, save all artifacts, and cleanup again.
9. Keep the grid paused after a manual retest unless the user explicitly says to resume the normal grid run.

## Important implementation pitfall: helper functions that parse `device_##`

Some grid-run helper functions assume `devdir.name.split('_')[-1]` is an integer device number. Retest folders like:

```text
device_15_retest_approach0p5_20260630T133657Z
```

break that assumption and can fail with:

```text
ValueError: invalid literal for int() with base 10: '<timestamp>'
```

Avoid this in future retest scripts by doing one of:

- Preferable: patch/refactor helpers to accept an explicit `device_number` parameter instead of parsing the directory name.
- Quick bounded workaround: create a temporary symlink whose final underscore token is numeric, e.g. `device_15_retest_tmp_device_15 -> <actual retest folder>`, call the helper through the symlink, then rewrite any output paths in summary metadata back to the real retest folder and remove the symlink.

Always verify that the expected files landed in the real retest folder after using a symlink workaround.

## Reporting pattern

Report concise verified fields:

- Device and retest folder.
- Approach parameters and result (`status`, final current, net Z movement).
- DCIV flags: SET/RESET detected, max current/compliance hits.
- Pulse outcome: pulses collected, stop reason, threshold/ON-OFF caveat if reset reads remain high.
- Cleanup: especially `707B get_closed_channels == nil`.
- Attach `device_plot.png` if generated.

If a custom approach step lands over-current or contact-edge, say so plainly; do not call the retest successful just because DCIV/pulse artifacts were produced.
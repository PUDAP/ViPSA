# Grid trial live updates + combined DCIV plotting (2026-06-06)

Context: during a ViPSA 3x3 grid trial, the user requested live updates of every move, then immediately corrected the update policy: **do not spam per-step approach steps**. Later they asked for DCIV curves from completed devices so far in a single image while the grid run was still active.

Reusable lessons:

- Live grid/status update jobs should report coarse events and status transitions, not every contact-approach loop iteration.
- Suppress repetitive approach-loop protocol descriptions such as:
  - `approach read N`
  - `approach forward N`
  - `approach retract trim N`
- Still report:
  - device-to-device travel moves (`stage` safe retract/pre-approach, `zaber` X/Y moves)
  - routing changes and cleanup
  - resistance-check/DCIV/pulse-test starts/completions
  - final approach result/status (`contact_window`, `max_attempts_no_contact`, etc.) from the summary/trace
- For live-update cron/watchdog scripts, keep a small state file in the run directory (for example `.live_update_state.json`) tracking seen protocol files and last summary rows. Emit nothing when there are no new non-suppressed events.
- If cron only supports minute-level cadence, batch updates once per minute rather than attempting sub-minute scheduling.

Combined DCIV plot recipe for an in-progress grid run:

1. Read the run summary CSV and select devices whose `status` is `completed`.
2. For each completed device, load `device_##/device_<n>_forming_dciv.csv` if present.
3. Preserve row order; never sort by voltage.
4. Plot `Voltage (V)` vs `abs(Current (A))` on a log y-axis.
5. Use one subplot per completed device in a single PNG, with PF/PB/NF/NB segment labels/colors.
6. Save the image in the run directory, e.g. `dciv_completed_devices_so_far.png`, and attach it with `MEDIA:`.

Minimal plotting behavior:

```python
for dev in completed_devices:
    rows = list(csv.DictReader(open(csv_path)))
    vcol = 'Voltage (V)' if 'Voltage (V)' in rows[0] else 'V_cmd (V)'
    icol = 'Current (A)' if 'Current (A)' in rows[0] else 'I_meas (A)'
    for seg in ['PF', 'PB', 'NF', 'NB']:
        segment_rows = [r for r in rows if r.get('segment') == seg]
        ax.plot([float(r[vcol]) for r in segment_rows],
                [max(abs(float(r[icol])), floor) for r in segment_rows],
                '.-', label=seg)
    ax.set_yscale('log')
```

Reporting standard:

- State exactly which devices were included.
- Provide the saved PNG path and attach it.
- Mention that measurement order was preserved and the y-axis is log `|I|`.

# Direct revisit to a device from a previous grid run

Use this when the user asks to go to a specific device from a previous grid run and approach/contact it again.

## Sequence

1. Locate the device's previous summary and target coordinates:
   - target row/column
   - absolute Zaber X/Y
   - last known approach/contact Z
   - prior contact status and whether an open/weak override or over-contact override was used
2. Before any travel, force electrical safety:
   - Keithley output off
   - Keysight output off
   - 707B `open_all`
   - verify `get_closed_channels == nil` when possible
3. If the user says “if in contact, move Z down first,” perform a live low-bias Keithley check if safe/available. Even if it reads open-like or is uncertain, still retract to a safe travel height before Zaber X/Y motion unless the user explicitly forbids it.
4. Move microscope stage Z down/back by a safe amount before Zaber motion.
5. Move Zaber X/Y to the device's absolute native-unit target.
6. If using the prior contact Z as a speed aid, move only to a conservative pre-approach height, not to the prior contact Z itself. If the user asks for a fraction such as “move to 50% of previous Z,” interpret it as **50% of the previous approach distance from previous approach-start Z toward previous contact Z**, not half of the absolute Z coordinate:

   ```text
   Z_pre = previous_start_Z + fraction * (previous_contact_Z - previous_start_Z)
   ```

   This preserves clearance while still shortening the mechanical search.
7. Immediately run a live 10 mV Keithley read after pre-approach:
   - If inside target window, report contact.
   - If open/noise-floor, continue fine approach.
   - If above target or at compliance, retract in bounded 0.25-step increments and stop/report over-contact/short-like if it remains high.
8. Cleanup at the end: SMU outputs off, 707B open/nil, machines idle.

## D52 revisit pitfall

A D52 revisit from a previous 8x8 run used prior target X/Y `(41766, 939310)` and historical usable Z around `180`. After safe retract and Zaber travel, pre-approach to `Z=172` (8 steps below historical contact) still read at the 200 nA approach compliance at 10 mV. Retracting by 10 steps to `Z=162` did not clear the compliance-limited read. Lesson: prior contact-Z estimates can become unsafe after time/alignment changes or if the device/substrate state changed; always gate predictive pre-approach with a live low-bias read and stop/retract on compliance.

## D29 fractional-preapproach example

For a D29 revisit, the user requested safe Z-down before Zaber travel, then “move to 50% of previous Z and approach.” Use the previous run's approach interval, not absolute coordinate halving:

```text
previous approach start Z = 208.5
previous contact Z        = 224.75
previous approach span    = 16.25
50% pre-approach Z        = 208.5 + 0.5*16.25 = 216.625
```

After moving Zaber to the historical X/Y plus current alignment offset, the live 10 mV check at `Z=216.625` was already above the soft window (`~142 nA`), so the correct behavior was to retract by minimum valid 0.25-step increments until the soft window was reached (`Z=216.125`, `~5.9 nA`). Lesson: fractional pre-approach is useful and faster, but it still needs the immediate live low-bias gate and bounded retract trimming before electrical stress.

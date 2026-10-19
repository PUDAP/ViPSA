# Returning from substrate edge contact to an aligned S9 grid device (2026-07-26)

Use when the user manually moves the Zaber stage away from the grid, for example to the substrate edge or bottom-electrode contact area, and then asks to return to a named S9 device.

## Durable lesson

A manual edge-contact excursion can put live Zaber X/Y far from the last grid device. Do not apply a relative grid pitch from the edge location. Resolve the destination from S9 run artifacts, then command absolute Zaber positions.

For S9 device 6 in the 7x7 run, the nominal grid row was:

```text
device_number,row,col,x,y
6,0,5,291765.0,486131.0
```

The device summary also contained two verified alignment corrections:

```text
first alignment move_native:        x=+643, y=+166
recheck alignment move_native:      x=-305, y=+202
net alignment offset:               x=+338, y=+368
aligned revisit target:             x=292103, y=486499
```

A successful return from a manually moved edge position used:

```text
pre Zaber:        x=219814, y=506186
stage clearance:  z=-70 -> -105 via stage.move_z_by(height=-35)
absolute Zaber:   move_x_to(292103, units=None), move_y_to(486499, units=None)
post Zaber:       x=292103, y=486499, error dx=0/dy=0
```

## Workflow

1. Load the authoritative S9 `grid_positions.csv` and the requested device `summary.json`.
2. If `summary.json` contains verified alignment correction(s), compute the aligned target as nominal grid X/Y plus the **net** of those corrections. If multiple alignment blocks exist, include all verified move-native corrections that were applied to the physical device position.
3. Before lateral travel, force electrical safety:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should return `nil`
4. Retract Stage Z by `-35` for clearance unless a fresh safe clearance is already verified and stacking another retract would be inappropriate.
5. Use absolute native Zaber commands, not relative pitch moves:
   - `zaber.move_x_to(position=<aligned_x>, units=None)`
   - `zaber.move_y_to(position=<aligned_y>, units=None)`
   - `zaber.get_current_position(units=None)`
6. Verify exact final readback, final stage readback, and `idle/run_id:null` for Keithley, 707B, stage, Zaber, and light where available.

## Reporting

Report the source of the target, nominal coordinates, net alignment offset, final absolute target, starting live Zaber position, final readback, target error, and the safety cleanup/readback results. If you use aligned coordinates instead of the nominal CSV coordinates, say so explicitly.

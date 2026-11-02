# Grid travel order correction: align before +40 Z pre-approach

Use this for ViPSA multi-device grid measurements unless the user explicitly overrides the travel values/order.

## Correct default sequence

For each subsequent grid device:

```text
stage.move_z_by(-50)
zaber.move_x_to(target_x)
zaber.move_y_to(target_y)
vision align
stage.move_z_by(+40)
electrical approach
```

## Pitfall corrected

Do **not** use the older order:

```text
stage.move_z_by(-50)
zaber.move_x_to(target_x)
zaber.move_y_to(target_y)
stage.move_z_by(+30)
align
approach
```

The user corrected this as a class-level rule for all future grid measurements, not just one S9 runner.

## Implementation notes

- Alignment should happen at the safe/retracted optical position after lateral Zaber travel.
- The +40 Stage-Z pre-approach happens **after** alignment and immediately before electrical approach.
- Current-device/manual handoff exceptions remain possible: if the user explicitly asks to approach the current aligned device in place, do not add the generic travel sequence first.
- Preserve the usual cleanup gates before travel: SMU outputs off, 707B open/nil, lights managed for alignment/approach.

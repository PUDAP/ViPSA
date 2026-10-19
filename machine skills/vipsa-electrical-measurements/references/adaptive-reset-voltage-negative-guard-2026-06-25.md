# Adaptive reset-voltage negative guard (2026-06-25)

## Trigger

During a long ViPSA grid/forming continuation, adaptive reset-voltage logic updated `reset_v` by adding `+0.2 V` to the prior negative branch endpoint. For shallow negative endpoints this crossed or touched zero, e.g. producing `reset_v = +0.1 V` or `+0.05 V`.

## Failure mode

A reset-side DCIV builder that expects the reset target to be negative can silently produce missing or empty normal reset branches (`NF`/`NB`) when adaptive `reset_v` becomes positive. The resulting DCIV CSV may contain only positive/forming branches (`PF`, `PF2`, `PB`, etc.) even though the run appears to have performed a DCIV step. Devices then need reset-side remeasurement.

## Durable fix pattern

Guard adaptive reset targets at the point of assignment and at the start of the DCIV builder:

```python
def normalize_reset_v(value, min_negative=-0.05):
    """Return a strictly negative reset voltage for NF/NB sweep construction."""
    v = float(value)
    if v >= 0:
        v = -abs(v) if v != 0 else min_negative
    # protect against -0.0 and near-zero values that collapse branches
    if v >= -abs(min_negative):
        v = -abs(min_negative)
    return v

# Before constructing NF/NB segments
reset_v = normalize_reset_v(reset_v)

# Adaptive update example
next_reset_voltage = normalize_reset_v(round(neg_up["to_v"] + 0.2, 2))
```

Use the experiment's intended minimum negative step/floor if `-0.05 V` is not appropriate. The invariant is stricter than "non-positive": reset-side targets used to build `NF`/`NB` must be **strictly negative**.

## Verification

After patching a live or continuation runner:

1. Compile the patched runner (`python3 -m py_compile <runner.py>`).
2. Inspect the generated or next-run DCIV metadata/CSV for `reset_v < 0`.
3. Confirm normal reset-side branches exist (`NF` and `NB`) and contain more than one point.
4. If an already-running process loaded old code, stop/restart it safely after the current device or use a watcher that waits for the current device to finish, performs cleanup/stop, and restarts the patched continuation.

## Reporting standard

When this guard fixes a grid continuation, report which runner(s) were patched, that the active code was compiled, and whether the currently running process already had the old code loaded. Do not claim old in-flight DCIV branches were fixed retroactively; the patch applies from the restarted/next continuation onward.

# Post-revisit DCIV on a grid device after fractional pre-approach

Use this pattern when the user revisits a device from a previous grid run, establishes a soft-window contact by predictive/fractional Z pre-approach plus live low-bias trimming, and then asks tersely to “run a DCIV sweep.”

## Preconditions

- Probe is already at the target device.
- A recent live Keithley contact check/approach ended in the intended soft contact window.
- If the device had an over-current pre-approach read, it was retracted and rechecked into the soft window before stress.
- Electrical cleanup state is known, or the DCIV protocol begins with `keithley-2450.set_output(false)` and `keithley-707b.connect_keithley_smu()`.

## Conservative grid-revisit sweep used successfully

For the device-29 revisit after a 50%-of-previous-approach-distance pre-approach, the requested default DCIV was run as the same style as the recent grid sweep:

```text
path:        0 -> +1.0 -> 0 -> -1.5 -> 0 V
step:        50 mV
points:      101 non-duplicated path points
PF/PB comp:  300 nA
NF/NB comp:  10 µA
```

Construct non-duplicated branches so endpoints are not repeated unnecessarily:

```text
PF:  0, +0.05, ... +1.00
PB:  +0.95, ... 0
NF:  -0.05, ... -1.50
NB:  -1.45, ... 0
```

Run the full requested sweep unless a hard instrument/safety fault occurs. Compliance-limited points are expected outcomes to report, not a reason to silently change the electrical recipe after the user asks for DCIV.

## Reporting fields

Report concisely:

- sweep path, step size, compliance by polarity/branch, point count
- max `|I|`
- compliance-hit counts per branch (`PF`, `PB`, `NF`, `NB`)
- start/end 0 V currents
- one or two salient low-voltage points, e.g. `+0.1 V PF` and `-0.1 V NF`
- plot as `MEDIA:` and raw CSV path
- final cleanup: Keithley/Keysight outputs off, 707B `get_closed_channels == nil`, machines idle, final stage/Zaber positions

## Interpretation language

If PF hits positive compliance very early (for example by `+0.1 V`) and negative/reset side also hits compliance for part of the branch, say the device is electrically active but compliance-limited early. Do not overclaim clean SET/RESET unless the row-ordered curve and low-bias read probes show a clear retained state transition.

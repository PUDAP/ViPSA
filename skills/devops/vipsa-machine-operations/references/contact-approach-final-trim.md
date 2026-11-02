# Contact approach final trim note

Session learning from a ViPSA `+Z` contact approach using:

```text
test_voltage = 0.01 V
lower_current_threshold = 1e-9 A
upper_current_threshold = 5e-8 A
step_size = 1
max_attempts = 50
settle_delay = 0.2 s
forward = +Z
```

Observed pattern:

1. Coarse approach detected contact after multiple `+1` Z moves.
2. Over-current retraction with `-0.5` Z steps brought the current back below the upper threshold temporarily.
3. After stabilization, a fine `+0.25` approach put current above the upper threshold again.
4. A single final `-0.1` guard retraction was insufficient; current remained above the requested upper threshold.
5. Repeating bounded `-0.1` trim retractions with a measurement after each move settled the contact inside the requested window.

Reusable rule:

- Final guard should be a bounded loop, not a single retraction: while `abs(current) > upper_current_threshold`, move `-0.1 * signed_step_size`, wait `settle_delay`, remeasure, and stop when inside the window or after a hard trim limit such as 10 attempts.
- Always run cleanup after the trim loop: Keithley output off, 707B `open_all`, `get_closed_channels`, then final machine states.

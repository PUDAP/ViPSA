# Adaptive per-device grid reporting, logbook updates, and recorder dependency guard (2026-06-22)

## Context

During an 8×8 ViPSA grid continuation, the user asked that after each device finishes the agent should:

1. Send the plot immediately.
2. Analyze the device result.
3. Add any failure to the project logbook.
4. Tweak the protocol based on the observed failure before continuing.

The active run had already produced device 5 and 6 artifacts, then needed a continuation from device 7 with softer settings.

## Reusable pattern

For long grid runs, treat per-device reporting as part of the measurement loop, not a post-run summary.

Recommended implementation:

1. Keep a persistent report-state file, e.g. `runs/.grid_per_device_reported.json`, keyed by `run_dir:device_number`, so device plots are sent only once.
2. After each `device_XX/DONE.json` + `summary.json` appears:
   - verify `device_plot.png` exists and is non-empty;
   - parse `summary.json`, `dciv.csv`, and `randomized_pulse_summary.json` if present;
   - send the plot with `MEDIA:/absolute/path/to/device_plot.png`;
   - provide concise analysis: pre-contact current, approach final current/Z, DCIV max |I| and compliance hits, pulse count/trials, pulse compliance flags, sigmoid/threshold if present;
   - classify failures: open-like, short/over-contact, compliance-limited DCIV, pulse compliance-limited, skipped by safety gate;
   - append a timestamped logbook line to `project.md` with links to the plot and summary.
3. If the analysis reveals a failure mode that can safely be mitigated, update the continuation protocol from the next unfinished device rather than waiting until the end.

## Adaptive tweak examples from this run

- Device 5: soft approach reached the 1–20 nA target, but DCIV became compliance-limited/short-like (`max |I| ~ 10 µA`, many PF/PB/NF/NB hits). Tweak: keep soft 1–20 nA approach, lower positive/forming DCIV compliance toward `300 nA`, and stop PF early if `+50–100 mV` is already compliance-limited.
- Device 6: DCIV still had PF/PB compliance hits and pulse run showed heavy compliance flags. Tweak: lower pulse compliance and cap SET-voltage range for subsequent devices.

## Safe continuation rule

Do not kill an active hardware command just to apply a tweak. If a previous continuation must be replaced:

1. Wait for a safe boundary or verify machine states.
2. Stop the old background process.
3. Run cleanup/recovery through PUDA where possible: SMU outputs off, 707B open-all, relevant machine COMPLETE/reset/recovery commands.
4. Verify machine states are idle before launching the new continuation.
5. Resume from the next unfinished device by inspecting run folders, not by assuming the last requested device completed.

## Camera recorder dependency guard

If a grid script starts video-recorder threads using OpenCV (`import cv2`), verify OpenCV availability before launching the long run, or make the recorder optional so missing video dependencies do not crash/obscure the electrical workflow.

A setup fix used in this session was:

```bash
python3 -m pip install opencv-python-headless
python3 - <<'PY'
import cv2
print(cv2.__version__)
PY
```

This is a dependency/setup fix for recorder-enabled runs, not a reason to label the measurement tools broken. If the recorder fails but the electrical loop continues, report that video recording was affected separately from hardware measurement status.

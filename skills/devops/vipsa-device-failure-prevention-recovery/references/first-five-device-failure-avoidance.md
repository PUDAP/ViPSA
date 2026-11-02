# Avoid repeating first-five-device failures

Use this reference when a ViPSA grid/device run has produced repeated weak/no-contact or damaged/failed first devices and the user asks how to continue without repeating failures.

## Durable lessons

- Do not treat picoamp/tens-of-picoamp readback at low bias as contact. Example: `~3.5e-11 A` at `10 mV` is open/weak-contact, not a safe basis for DCIV/pulse cycling.
- If an approach reaches `no_contact_after_max`, stop advancing the grid recipe blindly. The failure is likely lateral alignment, pad/probe geometry, oxide/non-pad landing, or contact-stack condition; another device with the same recipe is likely to fail the same way.
- Before another electrical stress/cycle run, reacquire camera context and verify probe-to-pad placement. Use the user's alignment conventions and send image evidence when relevant.
- Prefer a conservative contact-establishment phase before stress: low voltage, current-limited probing, small Z increments, cleanup after each attempt, and explicit classification as contact / weak contact / open.
- Preserve electrical safety cleanup before and after failure recovery: outputs off, 707B `open_all`, lights off unless needed for imaging, and verify closed channels are `nil`.
- When plotting/testing cycles so far, use only written run artifacts (CSV/summary files) and label incomplete/running cycles separately; do not infer unwritten cycles from a running process.

## Suggested continuation recipe after repeated first-device failures

1. Stop the current traversal or stress recipe if contact evidence is weak/open.
2. Verify machine cleanup: Keithley/Keysight outputs off, 707B open, no closed channels.
3. Capture/inspect camera image for pad/probe lateral alignment.
4. Re-align or move only as requested by the user; do not assume the current device coordinate is valid.
5. Run a gentle contact check at low bias with a defined current window before any DCIV/pulse stress.
6. If current remains in the open/weak range after the allowed Z budget, classify the device as no-contact and diagnose alignment/landing before moving to the next device.
7. For reporting, include actual measured current, voltage, net Z movement, cleanup status, and artifact paths/plots.

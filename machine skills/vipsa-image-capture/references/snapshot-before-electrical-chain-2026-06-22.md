# Snapshot before approach/DCIV chain (2026-06-22)

## Trigger

Use this when the user asks for a combined sequence like:

```text
take a picture from both cameras and send it to the chat, then run approach and a DCIV sweep
```

## Pattern

1. Treat the latest request as a **fresh image capture plus electrical chain**; do not drift into older run artifacts.
2. Capture fresh frames from both streams and verify non-zero JPEG files before reporting.
3. If the electrical part follows immediately, the snapshot light requirement is temporary:
   - use/turn lights on for imaging if needed;
   - after snapshots, turn lights off before the Keithley-guided approach/DCIV unless the user explicitly asks to leave them on.
4. Continue into the electrical workflow after capture; do not stop after sending images if the user also requested approach/DCIV.
5. For the approach→DCIV portion, follow the safety gate in `vipsa-electrical-measurements/references/approach-to-dciv-no-contact-gate-2026-06-18.md`: DCIV is authorized only if approach establishes the target contact window.
6. Final report should include both `MEDIA:` attachments and the electrical outcome/cleanup verification.

## Reporting template

```text
Camera 1:
MEDIA:/path/to/camera1.jpg

Camera 2:
MEDIA:/path/to/camera2.jpg

👇 Approach ...
- Approach target: ...
- Final current: ...
- DCIV: run/skipped because ...
- Cleanup verified: Keithley output off; 707B open_all; closed channels nil; relevant machines idle
- Light final state: off/idle unless explicitly left on
```

## Durable lesson

For combined camera→electrical chains, the final light state belongs to the **next hardware phase**, not the image phase. After a snapshot, darken the illumination before electrical approach/DCIV by default, then verify the light edge is idle.
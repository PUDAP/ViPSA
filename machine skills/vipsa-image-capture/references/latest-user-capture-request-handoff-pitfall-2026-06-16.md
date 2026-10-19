# Latest-user capture request vs stale handoff pitfall (2026-06-16)

## Trigger

A Telegram request asked to turn the lights on, capture a picture from both ViPSA stations, send the images to chat, and leave the lights on afterward. A context-compaction handoff then surfaced an older/compacted active task about device health.

## Reusable lesson

For image-capture tasks, the latest explicit user message is the execution contract. If a handoff/summary mentions an unrelated older active task, do not switch to that task or answer it first. Complete the capture workflow end-to-end:

1. Treat “both stations” as `camera1` + `camera2`.
2. Turn lights on via PUDA protocol and verify command success.
3. Capture both frames from the RTSP streams and verify non-empty files.
4. Because the user said to leave lights on, skip `turn_off` cleanup; verify the light edge is `idle` after `turn_on`.
5. Send both image files with `MEDIA:` attachments and a terse status line.

## Reporting standard

Do not report unrelated device-health/electrical results in response to a camera-capture request. If a stale background job or previous task output appears during the turn, ignore it unless the latest user explicitly asks for it.
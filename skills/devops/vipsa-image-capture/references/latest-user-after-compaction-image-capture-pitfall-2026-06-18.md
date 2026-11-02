# Latest-user-after-compaction image-capture pitfall (2026-06-18)

## What happened

A context-compaction handoff described an older task: generating an alignment demonstration video. Immediately after the compaction block, the actual latest user request was a new ViPSA image-capture task:

> turn the lights on, and capture a picture from both the stations and send it to the chat. Leave the lights on afterwards.

The agent incorrectly continued the stale alignment-video task from the compaction summary, marked its old todo complete, and replied with old video artifacts. It also reported the light was turned off afterward, directly contradicting the latest request to leave lights on.

## Durable lesson

For ViPSA capture requests, the message after `--- END OF CONTEXT SUMMARY ---` is the only active instruction. Compaction summaries are reference-only and may contain stale active tasks. Do not complete old todos, send old artifacts, or continue a previous align/electrical workflow when the latest user asks for fresh pictures.

## Correct behavior for the same request

1. Load `vipsa-image-capture`, `vipsa-machine-operations`, and `puda-env`.
2. Treat "both stations" as both camera streams/stations.
3. Turn the light on using PUDA protocol and verify success.
4. Capture fresh frames from both station streams.
5. Send both image attachments in chat.
6. Because the user explicitly said to leave lights on, skip the normal `turn_off` cleanup and verify/report only that the light edge is idle after successful `turn_on`.

## Red flags before replying

- If the response mentions an align video, DCIV, old run directory, or previously completed todo, stop: it is stale.
- If the response says the light was turned off after a leave-on request, stop: it violates the request.
- If no new `MEDIA:` image attachments are included for both stations, the task is not complete.
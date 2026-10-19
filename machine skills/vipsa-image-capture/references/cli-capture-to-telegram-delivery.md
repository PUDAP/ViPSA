# CLI capture → Telegram delivery

Use when a ViPSA image is captured from a Hermes CLI session and the user asks to send it to Telegram.

## Key distinction

`MEDIA:/absolute/path.jpg` is interpreted as an attachment only by messaging-platform delivery. In a CLI final response it is printed literally, so do not claim that it displays or uploads the image there. Give the local path for local viewing, or send it through the messaging transport when explicitly requested.

## Preferred delivery

If the `send_message` tool is available, send to the configured Telegram home chat:

```text
send_message(action="send", target="telegram", message="Camera 2 capture\nMEDIA:/absolute/path.jpg")
```

A bare `telegram` target intentionally uses the configured home channel; do not ask for a chat ID unless the user requests a different chat.

## Standalone fallback from a cached CLI session

Toolset changes require a new session, so the messaging tool may be configured but absent from the current CLI tool schema. If Telegram is already configured and the user explicitly asks to send the image now, call Hermes' existing standalone sender instead of exposing or manually handling the bot token:

```bash
cd ~/.hermes/hermes-agent
venv/bin/python -c 'from tools.send_message_tool import send_message_tool; print(send_message_tool({"action":"send","target":"telegram","message":"Camera 2 capture\nMEDIA:/absolute/path.jpg"}))'
```

This path reads the active Hermes gateway configuration and uses the platform plugin's standalone sender. Do not place Telegram tokens in shell arguments, logs, or replies.

## Verification

Require all of the following before reporting success:

- result contains `"success": true`;
- platform is `telegram`;
- a Telegram `message_id` is returned;
- the image path existed and was non-empty before sending.

Report only the successful destination (home chat unless another target was specified) and message ID. A text-message success alone is insufficient when an image was requested; confirm the media upload request also succeeded.
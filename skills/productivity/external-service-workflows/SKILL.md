---
name: external-service-workflows
description: "Umbrella for operating external productivity, communication, social, smart-home, note-taking, and presentation services from Hermes. Use for email, notes, decks, social posting, Yuanbao, Hue, and similar SaaS/device integrations."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [productivity, integrations, email, notes, presentations, social, smart-home, umbrella]
---

# External Service Workflows

Use this class-level skill when Hermes needs to operate an external service or user-facing integration: email, notes, slides, social platforms, messaging communities, smart-home devices, and similar tools.

## Routing by service class

- **Email:** Use Himalaya/IMAP-SMTP flows; verify account configuration and prefer dry-run/search before destructive mail actions.
- **Notes/knowledge bases:** Use Obsidian workflows when reading, searching, creating, or editing markdown notes in a vault.
- **Presentations:** Use PowerPoint package utilities and validate the produced `.pptx` package rather than assuming the file opens.
- **Social platforms:** Use the X/Twitter workflow for posting/searching/DM/media operations; verify credentials and API mode.
- **Messaging/community platforms:** Use Yuanbao workflow notes for group/member queries and @mentions.
- **Smart home/devices:** Use OpenHue workflow notes for Philips Hue lights, rooms, scenes, and bridge state. Favor reversible actions and report actual device responses.

## Absorbed specialist packages

The former narrow service skills are consolidated here. Their complete SKILL.md files and support files were re-homed under `references/absorbed-skills/<skill>/`, `templates/absorbed-skills/<skill>/`, `scripts/absorbed-skills/<skill>/`, and `assets/absorbed-skills/<skill>/` when present.

Absorbed areas: Himalaya email, Obsidian, PowerPoint, X/Twitter via xurl, Yuanbao, and OpenHue.

## Safety and verification

1. For actions with external side effects, confirm the target when ambiguity could affect another person/channel/device.
2. List available targets before sending to a named channel/person when the tool supports listing.
3. Prefer read/search/status probes before write/send/delete operations.
4. Return verifiable handles: message IDs, URLs, file paths, device response JSON, or command output.
5. Keep credentials out of summaries and never paste raw tokens into files.

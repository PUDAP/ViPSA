---
name: apple-ecosystem
description: "Use when working across Apple personal-productivity and device services: Notes, Reminders, Find My, iMessage, and macOS UI automation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, findmy, automation]
    related_skills: []
---

# Apple Ecosystem Operations

## Overview

This umbrella skill covers Apple-local and Apple-cloud workflows that usually appear together on macOS hosts: Notes, Reminders, Find My, iMessage/BlueBubbles, and direct macOS computer-use automation. Prefer this skill over narrow one-service skills when a task touches Apple apps, local AppleScript/JXA, Shortcuts, or macOS UI state.

## When to Use

- Reading, creating, updating, or searching Apple Notes.
- Creating, listing, or completing Apple Reminders.
- Locating devices/items via Find My.
- Sending or inspecting iMessage/BlueBubbles messages.
- Driving macOS GUI actions when there is no safer API.

## Service Playbooks

### Notes
Use the highest-level API available first (Shortcuts, AppleScript, or local export), then fall back to UI automation only when data is not exposed. Preserve folder/account context and avoid rewriting whole notes for small edits.

### Reminders
Treat list name, due date, priority, and completion state as separate fields. Confirm the target list before creating many items; recurring reminders and shared lists are easy to mis-target.

### Find My
Use for status/location checks, not continuous tracking unless the user explicitly requests monitoring. Report timestamp/staleness with every location result.

### iMessage
Prefer gateway/native messaging tools when available. If using BlueBubbles or local Messages data, verify the recipient identity before sending and distinguish SMS fallback from iMessage delivery.

### macOS Computer Use
Prefer scriptable APIs before cursor/keyboard automation. If UI automation is necessary, capture or inspect the active window before acting and keep actions reversible.

## Common Pitfalls

1. Apple app data is often account-scoped; include account/list/folder/device identifiers in summaries.
2. UI automation can act on the wrong foreground app; verify focus before typing or clicking.
3. Message sending is an external side effect; verify recipient and content before dispatch.
4. Location data may be stale; always include the reported timestamp.

## Verification Checklist

- [ ] Target account/list/folder/device/contact identified.
- [ ] Non-UI API attempted before GUI automation.
- [ ] Side effects verified with returned ID, timestamp, visible state, or read-back.

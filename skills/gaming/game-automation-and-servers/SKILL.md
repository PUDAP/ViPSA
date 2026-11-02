---
name: game-automation-and-servers
description: "Umbrella for game-related automation: hosting/modpack servers, emulator control, gameplay agents, save/state inspection, and game-specific operational workflows."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [gaming, servers, emulators, automation, minecraft, pokemon, umbrella]
---

# Game Automation and Servers

Use this class-level skill for game operations that Hermes can automate: deploying game servers, managing modpacks, running emulators, reading game state, and coordinating gameplay agents.

## Routing

- **Game servers/modpacks:** For Minecraft and similar servers, resolve the distribution source first (CurseForge, Modrinth, direct server pack), keep world/config state backed up, and verify the server reaches a ready state by inspecting logs or querying the port.
- **Emulator/gameplay agents:** For Pokemon-style workflows, treat emulator state, ROM/save paths, and RAM reads as prerequisites. Verify each in-game action by reading state or capturing the screen before continuing.

## Absorbed specialist packages

The former `minecraft-modpack-server` and `pokemon-player` skills are consolidated here with their SKILL.md references and any support files under `references/absorbed-skills/`, `templates/absorbed-skills/`, `scripts/absorbed-skills/`, and `assets/absorbed-skills/` where present.

## Safety and verification

1. Never overwrite worlds, saves, or ROM-related files without backups.
2. Prefer foreground smoke tests for setup steps and tracked background processes for servers/watchers.
3. Report exact paths, ports, process IDs/session IDs, and commands used for verification.

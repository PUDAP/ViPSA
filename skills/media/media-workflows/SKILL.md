---
name: media-workflows
description: "Use when searching, generating, analyzing, transcribing, or controlling media: GIFs, songs, spectrograms, Spotify, YouTube, and camera streams."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, gif, music, audio, spotify, youtube, camera, streaming]
    related_skills: []
---

# Media Workflows

## Overview

This umbrella skill covers media-centric operations: finding GIFs, generating music prompts/audio, analyzing audio features, controlling Spotify, extracting YouTube content, and bridging camera/video streams across WSL and Windows.

## When to Use

- Searching/downloading GIFs.
- Writing songs or generating music with HeartMuLa/AudioCraft/Suno-like systems.
- Creating spectrograms or audio feature visualizations.
- Searching, playing, queueing, or managing Spotify.
- Fetching YouTube transcripts and turning them into summaries/threads/blogs.
- Troubleshooting WSL/Windows camera and livestream media paths.

## Modes

### GIF Search
Use API-backed search, download the selected result, and return native media attachment paths when possible.

### Music Generation
Separate lyrical content, style tags, structure, and negative constraints. For model-specific tools, preserve seed/config metadata.

### Audio Analysis
Use spectrograms/features for evidence; label axes, time ranges, and sample rates.

### Spotify
Verify active device and track/playlist IDs before playback side effects.

### YouTube Content
Prefer transcripts over summaries from page text. Keep timestamps when useful and distinguish quote from paraphrase.

### Camera / Livestream Bridging
WSL and Windows devices often require explicit host/guest paths. Verify stream readiness with a player, HTTP endpoint, or frame capture.

## Common Pitfalls

1. Media APIs often return many similar IDs; verify the selected item before acting.
2. Playback and queue changes are user-visible side effects.
3. Transcripts can be auto-generated and error-prone; note that caveat.
4. Camera devices may be locked by another app or exposed only on Windows, not WSL.

## Verification Checklist

- [ ] Media source/target ID or path verified.
- [ ] Generated/downloaded artifact exists and is attached or linked.
- [ ] Side effects read back from the relevant service.
- [ ] Timestamp/device/format caveats included.

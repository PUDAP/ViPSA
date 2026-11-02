# Absorbed skill: spotify

Original package: `media/spotify` archived after consolidation into `media-workflows`.

Support files copied: none.

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: spotify
description: "Spotify: play, search, queue, manage playlists and devices."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  tools: [spotify_playback, spotify_devices, spotify_queue, spotify_search, spotify_playlists, spotify_albums, spotify_library]
metadata:
  hermes:
    tags: [spotify, music, playback, playlists, media]
    related_skills: [gif-search]
---

# Spotify

Control the user's Spotify account via the Hermes Spotify toolset (7 tools). Setup guide: https://hermes-agent.nousresearch.com/docs/user-guide/features/spotify

## When to use this skill

The user says something like "play X", "pause", "skip", "queue up X", "what's playing", "search for X", "add to my X playlist", "make a playlist", "save this to my library", etc.

## The 7 tools

- `spotify_playback` — play, pause, next, previous, seek, set_repeat, set_shuffle, set_volume, get_state, get_currently_playing, recently_played
- `spotify_devices` — list, transfer
- `spotify_queue` — get, add
- `spotify_search` — search the catalog
- `spotify_playlists` — list, get, create, add_items, remove_items, update_details
- `spotify_albums` — get, tracks
- `spotify_library` — list/save/remove with `kind: "tracks"|"albums"`

Playback-mutating actions require Spotify Premium; search/library/playlist ops work on Free.

## Canonical patterns (minimize tool calls)

### "Play <artist/track/album>"
One search, then play by URI. Do NOT loop through search results describing them unless the user asked for options.

```
spotify_search({"query": "miles davis kind of blue", "types": ["album"], "limit": 1})
→ got album URI spotify:album:1weenld61qoidwYuZ1GESA
spotify_playback({"action": "play", "context_uri": "spotify:album:1weenld61qoidwYuZ1GESA"})
```

For "play some <artist>" (no specific song), prefer `types: ["artist"]` and play the artist context URI — Spotify handles smart shuffle. If the user says "the song" or "that track", search `types: ["track"]` and pass `uris: [track_uri]` to play.

### "What's playing?" / "What am I listening to?"
Single call — don't chain get_state after get_currently_playing.

```
spotify_playback({"action": "get_currently_playing"})
```

If it returns 204/empty (`is_playing: false`), tell the user nothing is playing. Don't retry.

### "Pause" / "Skip" / "Volume 50"
Direct action, no preflight inspection needed.

```
spotify_playback({"action": "pause"})
spotify_playback({"action": "next"})
spotify_playback({"action": "set_volume", "volume_percent": 50})
```

### "Add to my <playlist name> playlist"
1. `spotify_playlists list` to find the playlist ID by name
2. Get the track URI (from currently playing, or search)
3. `spotify_playlists add_items` with the playlist_id and URIs

```
spotify_playlists({"action": "list"})
→ found "Late Night Jazz" = 37i9dQZF1DX4wta20PHgwo
spotify_playback({"action": "get_currently_playing"})
→ current track uri = spotify:track:0DiWol3AO6WpXZgp0goxAV
spotify_playlists({"action": "add_items",
                   "playlist_id": "37i9dQZF1DX4wta20PHgwo",
                   "uris": ["spotify:track:0DiWol3AO6WpXZgp0goxAV"]})
```
```

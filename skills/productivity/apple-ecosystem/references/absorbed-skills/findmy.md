# Absorbed skill: findmy

Original package: `apple/findmy` archived after consolidation into `apple-ecosystem`.

Support files copied: none.

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: findmy
description: "Track Apple devices/AirTags via FindMy.app on macOS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [FindMy, AirTag, location, tracking, macOS, Apple]
---

# Find My (Apple)

Track Apple devices and AirTags via the FindMy.app on macOS. Since Apple doesn't
provide a CLI for FindMy, this skill uses AppleScript to open the app and
screen capture to read device locations.

## Prerequisites

- **macOS** with Find My app and iCloud signed in
- Devices/AirTags already registered in Find My
- Screen Recording permission for terminal (System Settings → Privacy → Screen Recording)
- **Optional but recommended**: Install `peekaboo` for better UI automation:
  `brew install steipete/tap/peekaboo`

## When to Use

- User asks "where is my [device/cat/keys/bag]?"
- Tracking AirTag locations
- Checking device locations (iPhone, iPad, Mac, AirPods)
- Monitoring pet or item movement over time (AirTag patrol routes)

## Method 1: AppleScript + Screenshot (Basic)

### Open FindMy and Navigate

```bash
# Open Find My app
osascript -e 'tell application "FindMy" to activate'

# Wait for it to load
sleep 3

# Take a screenshot of the Find My window
screencapture -w -o /tmp/findmy.png
```

Then use `vision_analyze` to read the screenshot:
```
vision_analyze(image_url="/tmp/findmy.png", question="What devices/items are shown and what are their locations?")
```

### Switch Between Tabs

```bash
# Switch to Devices tab
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Devices" of toolbar 1 of window 1
    end tell
end tell'

# Switch to Items tab (AirTags)
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Items" of toolbar 1 of window 1
    end tell
end tell'
```

## Method 2: Peekaboo UI Automation (Recommended)

If `peekaboo` is installed, use it for more reliable UI interaction:

```bash
# Open Find My
osascript -e 'tell application "FindMy" to activate'
```

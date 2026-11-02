---
name: baoyu-visual-content
description: "Use when creating Baoyu-style article illustrations, educational comics, or infographics with consistent style, palette, layout, and prompt systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [baoyu, illustration, comic, infographic, visual-content, prompt]
    related_skills: []
---

# Baoyu Visual Content

## Overview

This umbrella skill consolidates the Baoyu visual-content family. Load it for article hero illustrations, knowledge comics, and structured infographics; then choose the subsection matching the deliverable.

## When to Use

- Generating article illustrations with a consistent palette/style system.
- Turning educational, biographical, or tutorial material into comics.
- Building infographics from structured facts, comparisons, flows, or taxonomies.
- Maintaining visual consistency across a set of Baoyu assets.

## Deliverable Modes

### Article Illustration
Use when the output is a single image or small set of editorial illustrations. Extract the central metaphor, select style/palette, and build a prompt that emphasizes composition, mood, subject, and negative constraints.

### Knowledge Comic
Use when the output needs narrative panels. Convert content into beats, define recurring characters/visual metaphors, choose layout density, and preserve continuity across panels.

### Infographic
Use when the output is explanatory structure rather than narrative. Pick a layout class first (matrix, roadmap, hub-spoke, layers, dashboard, etc.), then map facts to regions and choose a style that supports legibility.

## Support Files

Session-specific presets, layouts, palettes, prompt fragments, and workflow notes from the absorbed skills should live under `references/baoyu-article-illustrator/`, `references/baoyu-comic/`, and `references/baoyu-infographic/`.

## Common Pitfalls

1. Choosing style before information architecture leads to pretty but unclear outputs.
2. Comics need continuity constraints; infographics need legibility constraints.
3. Keep palette/style labels consistent across a batch.
4. Preserve source facts separately from prompt prose so revisions are easy.

## Verification Checklist

- [ ] Deliverable mode selected.
- [ ] Style, palette, layout, and content hierarchy explicit.
- [ ] Prompt includes negative constraints and text/legibility guidance.
- [ ] Batch consistency documented when generating multiple assets.

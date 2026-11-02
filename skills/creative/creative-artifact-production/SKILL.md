---
name: creative-artifact-production
description: "Umbrella for producing creative artifacts: diagrams, HTML/design mockups, browser sketches, generative art, animations, pixel/ASCII art, ComfyUI media workflows, and music prompts. Use this before any narrower creative rendering or design-production task."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [creative, design, diagrams, html, generative-art, animation, media, umbrella]
---

# Creative Artifact Production

Use this class-level skill for creative output that becomes an artifact: HTML/CSS mockups, architecture diagrams, Excalidraw-style diagrams, DESIGN.md specs, p5.js sketches, Manim animations, pixel/ASCII art, ComfyUI workflows, TouchDesigner networks, visual-content systems, and AI music prompts.

## Routing by artifact class

- **HTML/UI/mockups:** Start with a one-file artifact when the user needs a landing page, design exploration, deck-like page, or prototype. Compare 2-3 variants when aesthetics are underspecified. Preserve all source in the deliverable and verify in browser when possible.
- **Architecture and hand-drawn diagrams:** Use SVG/HTML for polished dark-themed diagrams; use Excalidraw JSON when the requested style is hand-drawn or needs later editing in Excalidraw.
- **Design-system specs:** For DESIGN.md/token work, keep the token spec valid and separate reusable templates from prose explanations.
- **Browser/generative sketches:** Use p5.js or small HTML/JS demos for interactive visuals. Include a local viewer and an export path for frames when animation output is required.
- **Animation/video explainers:** Use Manim for mathematical or algorithmic explainers; use ASCII-video/pixel-art workflows for stylized renders.
- **Image/video/audio generation pipelines:** For ComfyUI/TouchDesigner/AI music tasks, treat the workflow graph/prompt as the artifact. Validate dependencies and workflow JSON before claiming success.
- **Text style transformation:** Use the humanizer subsection when the task is to remove AI-ish phrasing or add a more natural human voice.

## Absorbed specialist packages

The former narrow creative skills have been consolidated here. Their complete SKILL.md files and support directories were re-homed under `references/absorbed-skills/<skill>/`, `templates/absorbed-skills/<skill>/`, `scripts/absorbed-skills/<skill>/`, and `assets/absorbed-skills/<skill>/` when present.

Absorbed areas: architecture diagrams, Claude-style design artifacts, sketch variants, popular web design systems, DESIGN.md specs, Excalidraw, pretext demos, p5.js, pixel art, ASCII art/video, Manim, ComfyUI, TouchDesigner MCP, songwriting/AI music, and humanizer workflows.

## Diagram artifact notes

- For dense workflow/decision diagrams, especially those rendered with Python `schemdraw`, use `references/schemdraw-flowchart-legibility.md`: generate SVG first, optionally convert to PNG with `cairosvg`, visually verify the rendered PNG, and prefer readable single-column gate/action layouts over tangled side-branch diagrams when labels are long.

## General quality gates

1. Clarify only if the target medium or output format is genuinely ambiguous; otherwise choose the smallest artifact that can satisfy the request.
2. Produce a real file or renderable artifact, not just a prompt, unless the user explicitly asks for a prompt.
3. Validate: open HTML in browser, run scripts, lint/parse JSON, or render a representative frame where feasible.
4. Keep reusable starters in `templates/`, implementation helpers in `scripts/`, and long style guides/provider notes in `references/`.
5. If a generated artifact depends on local files, report the exact path and include any command needed to view or rerun it.

## Pitfalls

- Do not flatten a specialist package and leave links pointing back to an archived skill. Re-home support files with the SKILL.md reference.
- Do not overfit to a named design system unless the user asked for that brand/style; use the absorbed design-system templates as inspiration.
- For dynamic media workflows, verify the runtime is available before promising a final render.

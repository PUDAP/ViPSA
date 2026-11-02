---
name: engineering-cad-visualization
description: "Use when rendering CAD/STL/STEP models for publication."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [cad, stl, step, wireframe, technical-illustration, publication]
    related_skills: [creative-artifact-production, powerpoint, pdf]
---

# Engineering CAD Visualization

Use this class-level skill to turn mechanical CAD and printable meshes into publication figures, comparison sheets, model inventories, and release-ready visual documentation.

## Scope

- STL and STEP rendering
- Hidden-line and shaded technical illustrations
- Multi-variant contact sheets
- Installed-versus-alternative model classification
- Mesh-health-aware publication captions
- CAD figure integration into papers and supplementary bundles

This skill does not establish mechanical fit, manufacturing tolerance, licensing, or installed identity from filenames alone. Those require source evidence or explicit user confirmation.

## Default rendering policy

1. Inventory all candidate files before choosing models.
2. Group duplicate formats by design stem; render one authoritative neutral/mesh export per distinct geometry.
3. Prefer STEP for solid geometry and dimensional provenance when available. State that STL has no embedded units.
4. For engineering-paper figures, default to a clean **hidden-line CAD wireframe**, not a raw STL triangle mesh.
5. Use smooth shaded solids only when the user prefers them or material/assembly appearance matters.
6. Label installed/current, alternative, prototype, component-only, and topology-review status explicitly.
7. Never infer that a model is installed solely because it renders well or has a plausible filename.

## Hidden-line wireframe standard

The preferred wireframe look uses visible feature edges over an opaque near-white body. The body performs hidden-line removal; raw tessellation edges remain suppressed. See `references/hidden-line-cad-wireframes.md` for the validated PyVista pattern.

Do not use literal full-mesh wireframe rendering for publication unless requested: it exposes every STL triangle and creates visual clutter.

## Native CAD limitations

- STEP and STL can be rendered with open tooling.
- Native SolidWorks-only `.SLDPRT`/`.SLDASM` files generally require SolidWorks, eDrawings, or a verified conversion tool.
- If no neutral export exists, list the source-only model explicitly rather than fabricating a render.
- Exclude temporary files such as `~$*.SLDPRT`.

## Multi-model workflow

1. Build a deterministic inventory with filename, format, byte size, hash, dimensions, and topology status.
2. Count distinct design families and enumerate every requested item.
3. Convert STEP to visualization STL only when required; preserve the original STEP as authoritative and label the generated mesh.
4. Render each model individually using consistent camera, line weight, background, and margins.
5. Assemble contact sheets with source filename, dimensions, and status.
6. Include a source-only panel for unrenderable native-CAD variants.
7. Verify rendered count plus source-only count against the inventory before delivery.

## Publication integration

- Use captions that distinguish visual style from model validity.
- A clean render does not prove watertightness or print readiness.
- Keep topology findings in a validation manifest.
- Update figure labels, manuscript text, BOM identity, release README, manifests, and installed-model bundle together when the user corrects which model is installed.
- Recompile and visually inspect affected paper pages after figure replacement.
- Rebuild and integrity-test supplementary archives after any installed-model change.

## Quality gates

- No clipped geometry or labels.
- No dense triangle clutter unless explicitly requested.
- Correct installed/current model is visibly identified.
- Dimensions and units are stated with provenance.
- Topology-review models are not called validated print-ready parts.
- Contact-sheet counts reconcile programmatically.
- Final manuscript and archive are rendered/compiled and integrity-tested before reporting completion.

## Related reference

- `references/hidden-line-cad-wireframes.md` — PyVista feature-edge rendering, contact-sheet accounting, and failure modes.

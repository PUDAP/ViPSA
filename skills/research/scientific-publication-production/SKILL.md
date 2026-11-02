---
name: scientific-publication-production
description: "Use when producing scientific papers and release bundles."
version: 1.0.0
author: Hermes Agent + curator
license: MIT
metadata:
  hermes:
    tags: [research, manuscript, latex, figures, cad, supplementary-materials, reproducibility]
    related_skills: [grounded-citations, pdf, xlsx, powerpoint]
---

# Scientific Publication Production

Use this class-level skill when revising a scientific manuscript together with figures, bills of materials, CAD/model supplements, data appendices, or an upload-ready source bundle.

## Operating principles

1. **Separate collection from implementation.** If the author says corrections will arrive one by one, record the list and do not edit until they explicitly authorize a consolidated implementation. Apply the approved set together so text, figures, tables, BOMs, and README files remain consistent.
2. **Treat source files by evidentiary role.** A slide deck, old figure, or development archive may establish layout intent without establishing current hardware identity or performance. Reuse illustrations only after removing stale labels and unsupported claims.
3. **Prefer measured system-level quantities.** When a component model is unknown, report the generic component class and measured integrated performance. Mark any vendor/product match as a candidate, not an identification, and do not borrow candidate manufacturer specifications.
4. **Do not turn configuration-dependent geometry into a fixed specification.** Working distance, focus height, and clearance may depend on substrate thickness and mounting. Explain the dependency and omit a fixed number unless a controlled condition is defined.
5. **Specify minimum configurations by required performance.** Recommend an optical system by object-plane sampling, field of view, acquisition resolution, exposure control, mechanical clearance, mounting stability, and software access—not camera megapixels or nominal magnification alone.
6. **Keep incomplete cost work visibly incomplete.** Blank prices are evidence gaps, not zeros. A partial priced-item subtotal is not a system cost. Label the BOM as draft, defer manuscript totals, retain currencies separately, and identify excluded reused/custom/model-unspecified items.

## End-to-end workflow

### 1. Establish the correction ledger

- Quote or faithfully paraphrase every requested correction.
- Resolve contradictions before editing.
- Identify every dependent artifact: manuscript prose, table rows, figure captions, source images, BOM generator, workbook, release README, and archive.
- Preserve uncertainty labels such as `candidate`, `unconfirmed`, `reused`, and `configuration-dependent` across all artifacts.

### 2. Audit the current source package

- Parse the LaTeX source for figure references, TODOs, old hardware names, cost claims, and availability statements.
- Inspect supplementary archives and exclude temporary lock files, unsafe paths, commercial reference geometry without redistribution clearance, and obsolete/prototype variants from the primary release.
- Verify that required bibliography and figure files are actually present; do not rely on compiler cache.

### 3. Produce apparatus and CAD figures

- Use photographs for installed-state evidence and CAD for geometry communication.
- When the author asks for “solid objects,” render smooth shaded surfaces with mesh edges suppressed; do not merely recolor a wireframe or triangle-edge plot.
- A suitable off-screen PyVista pattern is `add_mesh(..., smooth_shading=True, show_edges=False)` with antialiasing, a neutral background, and an isometric or top view chosen for the part.
- Rendering a mesh as a smooth solid does not change or validate its topology. Run mesh checks separately and state what they prove.
- Label modified, installed, proposed, and prototype components distinctly. Do not let a polished render imply that a model is the installed revision unless established.
- Inspect every generated figure both standalone and at compiled page scale.

### 4. Handle hardware identity conservatively

- Confirmed model: name it and cite the primary source where relevant.
- Unconfirmed model: use the generic class, record candidate links as candidates, and omit manufacturer-only sensor/rate/pixel specifications.
- Reused subsystem: state its origin (for example, optics retained from an existing probe station) and list unknown individual model numbers as unresolved.
- A vendor URL or filename is not proof that the photographed item is that product.

### 5. Write minimum viable configurations

Define acceptance criteria before suggesting products. For imaging, report:

- target object-plane sampling or resolution;
- target field of view at a stated acquisition resolution;
- exposure/control requirements;
- rigid mounting and probe clearance;
- expected substrate-height/thickness envelope;
- compatible acquisition interface; and
- a calibration procedure that verifies the assembled path.

Product examples may follow, but they remain representative until the complete optical path is validated.

### 6. Maintain BOM integrity

- Generate the workbook from a reproducible script where possible.
- Keep exact quantities, units, currencies, source URLs, price basis, inclusion flags, and notes.
- Highlight missing prices/model details instead of filling proxies silently.
- If subtotals remain useful internally, label them `partial priced-item subtotal` and explicitly prohibit treating them as total system cost.
- Render every sheet to PDF/image and inspect long URLs, wrapped notes, subtotal rows, and page breaks.

### 7. Compile and visually verify

- Compile from a clean output directory with every referenced source file available.
- Extract PDF text to locate changed sections and confirm stale claims are absent.
- Render every affected page, including the continuation page when a paragraph, footnote, or section crosses a page boundary.
- Check tables for cross-column collisions, figures for clipping, captions for consistency, and footnotes for legibility.
- Treat compilation success as necessary but insufficient; visual inspection is part of completion.

### 8. Build the release bundle

Include the compiled paper, manuscript source, bibliography, every referenced figure, BOM, curated supplements, READMEs, manifests, and checksums. Then:

- test archive integrity;
- programmatically confirm expected files and corrected phrases;
- scan included text for credentials and connection strings;
- enforce the platform upload limit using the stricter byte interpretation when uncertain; and
- report archive size, file count, checksum, and remaining unresolved TODOs.

## Common pitfalls

- Editing after each correction when the author asked for one consolidated pass.
- Copying claims from an old slide merely because its illustration is useful.
- Calling a shaded STL render a topology-validated solid; presentation and validation are separate.
- Assigning specifications from a candidate camera to an unidentified installed camera.
- Recommending a minimum camera without specifying the lens and assembled object-plane performance.
- Reporting a partial BOM subtotal as the cost of the apparatus.
- Checking only the page where a section begins and missing its continuation or footnote.
- Packaging stale hidden build copies instead of the newly compiled manuscript.

## Verification checklist

- [ ] All approved corrections applied consistently across manuscript, figures, BOM, and README.
- [ ] Candidate hardware remains explicitly unconfirmed.
- [ ] No configuration-dependent dimension is presented as universally fixed.
- [ ] Minimum configuration has measurable acceptance criteria.
- [ ] Solid-object renders have smooth shading and no visible mesh edges.
- [ ] Mesh validation is reported separately from rendering quality.
- [ ] Manuscript contains no incomplete-BOM system-cost claim.
- [ ] Every affected compiled page was visually inspected.
- [ ] Archive integrity, byte size, expected contents, and text-security scan passed.

## References

- See `references/cad-manuscript-release.md` for the validated CAD-heavy apparatus-paper workflow, rendering pattern, and bundle checks distilled from an applied manuscript revision.

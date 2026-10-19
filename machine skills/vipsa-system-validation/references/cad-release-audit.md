# CAD and 3D-Print Release Audit

Use this when validating a ViPSA model archive for a manuscript, repository, or manufacturing handoff.

## Archive and inventory

1. Record archive byte size and SHA-256, run an integrity test, and reject extraction if any entry is absolute, contains `..`, or is a symbolic link.
2. Extract into a dedicated audit copy; preserve the user's source archive.
3. Inventory file names, sizes, hashes, and formats. Separate printable exports (`STL`, `3MF`), editable/interchange formats (`STEP`), native CAD (`SLDPRT`, `SLDASM`), and documentation.
4. Exclude application lock files such as `~$*.SLDPRT` and tiny placeholder files from releases.
5. Map same-stem files across formats to identify printable models without editable sources and native parts without printable exports.

## Units and geometry

- STL has no embedded units. Infer nothing silently: state the intended units in the release README. Cross-check coordinate extents against known hardware.
- STEP unit declarations are authoritative when present; check every STEP file for its length unit.
- Load STL meshes with geometry processing enabled before judging watertightness. Unprocessed binary STL commonly has per-face duplicate vertices and can produce false non-watertight results.
- For each STL record dimensions, vertices, triangles, connected components, winding consistency, watertightness, degenerate triangles, boundary edges, and non-manifold edges.
- A visually plausible render is not a topology pass. Flag open boundaries, non-manifold edges, and degenerate triangles for repair before print/public release.

## Visual and configuration matching

1. Generate a contact sheet and multi-view renders for similarly named revisions.
2. Compare installed-system photographs only at the level visibly supported. If key geometry is concealed or overexposed, identify the family rather than selecting an exact revision.
3. Ask the operator to label files as installed, minimum proposed, shared, obsolete/reference, and print-tested release.
4. Record corrections from the operator. For the current ViPSA arrangement, the coiled addressable light ring is mounted at the top; do not misidentify the grey curved structures around the stage as the light ring.
5. Native assembly presence does not prove that external references resolve. Open each assembly in its authoring CAD system or provide a Pack-and-Go archive before claiming completeness.

## Release metadata to request

- Material, nozzle, layer height, walls, infill, supports, orientation, tolerances, and post-processing.
- Magnet dimensions/grade, inserts, bearings, screws, plates, wiring, and other non-printed hardware.
- Exact authoritative revision for the installed and minimum configurations.
- License and provenance for third-party reference geometry.

## Deliverables

Produce a file inventory CSV, geometry-validation CSV/JSON, visual contact sheet, repair list, and concise release-readiness report. Update the BOM only after authoritative configuration labels are available.

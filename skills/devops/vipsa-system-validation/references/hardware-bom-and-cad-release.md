# Hardware BOM and CAD release workflow

Use this reference when turning an installed ViPSA setup and a proposed minimum configuration into publication and release artifacts.

## BOM sequence

1. Inventory the **installed system** and the **minimum proposed system** separately.
2. Present component names and quantities for review **before** adding prices or editing the manuscript.
3. Resolve identity conflicts among manuscript text, source-code comments, filenames, and the physical apparatus. Prefer explicit user confirmation or physical inspection; never silently choose one. Record installed model, representative substitute, and proposed model as different statuses.
4. Include printed parts as real BOM items. Describe the ViPSA substrate holder as a custom 3D-printed assembly and separately list magnets, inserts, fasteners, bearings, plates, adhesives, and other purchased hardware.
5. Add prices only where a model or defensible representative proxy is known. Each priced row must include quantity, unit price, currency, observation date, price basis, source URL, and whether it enters the subtotal.
6. Keep currencies separate; do not convert without an explicit exchange-rate source and date.
7. Label totals as **partial priced-item subtotals** until every required row is priced. Reused/inventory assets, vendor-quote items, discontinued hardware, unresolved models, tax, shipping, regional markup, fabrication labour, and calibration must not disappear into an apparently complete total.
8. For proposed systems, state whether a representative component still requires compatibility validation (camera API, field of view, working distance, electrical rating, travel, load, or mounting).

## Spreadsheet requirements

For a two-tab workbook, use `Installed System` and `Minimum Proposed`. Recommended columns:

- Category
- Component
- Manufacturer/model
- Quantity and unit
- Unit price and currency
- Extended price
- Price basis
- Include in priced subtotal
- Source URL
- Notes

Use formulas for extended prices and currency-specific subtotals, hyperlinks for sources, filters, frozen headers, wrapped text, and a visible highlight for unresolved prices/models. Recalculate with a real spreadsheet engine, read back cached formula values, inspect each sheet visually, and test the XLSX container before delivery. A successful write alone is not spreadsheet verification.

## CAD archive intake

1. Hash and integrity-test the archive.
2. Reject absolute paths, parent traversal, and symbolic links before extraction.
3. Inventory formats, sizes, hashes, and same-stem source/export coverage.
4. Separate editable CAD (`SLDPRT`, `SLDASM`, STEP or native sources), printable meshes (STL/3MF), assemblies, drawings, and documentation.
5. Exclude editor lock files such as `~$*.SLDPRT` and unrelated temporary/error artifacts from the public release.
6. Verify units. STEP can declare units; STL cannot, so the release README must state STL units explicitly.
7. Parse every STL and report dimensions, triangle count, watertightness, winding consistency, degenerate faces, connected bodies, boundary edges, and non-manifold edges.
8. Generate a visual contact sheet, but do not substitute appearance for topology checks.
9. Ask the owner to tag each model as installed, minimum/shared, obsolete/reference, or unresolved. Similar filenames and timestamps do not establish authority.
10. Check whether proprietary assemblies open with all references resolved; binary presence alone does not prove a self-contained assembly.

## Release gates

Before incorporating models into the manuscript or public bundle, identify:

- authoritative installed and minimum assemblies;
- final printable revision for each part;
- material, nozzle, layer height, wall count, infill, supports, orientation, tolerances, and post-processing;
- magnet dimensions/grade and all non-printed hardware;
- licence and third-party model provenance;
- repaired/re-exported versions of non-watertight or non-manifold meshes;
- README mapping source CAD to printable exports and assembly figures.

## Pitfalls

- Treating a replacement/list price as historical procurement cost.
- Mixing exact installed products and representative substitutes without labels.
- Quoting a single currency-converted total from mixed regional prices.
- Calling an incomplete subtotal the system cost.
- Omitting 3D-printed holders or their embedded/purchased hardware from the BOM.
- Publishing every file in an archive without removing locks, prototypes, duplicates, or proprietary reference geometry.
- Assuming a visually plausible STL is printable, watertight, correctly scaled, or the final revision.

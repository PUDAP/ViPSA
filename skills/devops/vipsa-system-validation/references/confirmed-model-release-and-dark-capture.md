# Confirmed ViPSA model-release and dark-capture details

## Installed mechanical mapping

- The installed holder is `multi_holder_mag_long`.
- It uses 12 identical printed knubs arranged 4 × 3.
- The OpenFlexure body was modified by removing material to clear the larger holder.
- `main_body-edited.STL` is the print mesh used for the curated release; keep the exact native-source mapping marked pending until the author confirms it.
- The installed coiled addressable light ring is at the top of the assembly.

## Curated paper bundle workflow

1. Release confirmed final parts, not the entire development archive.
2. Preserve native CAD and unit-declared STEP files when available.
3. Generate missing STL exports from STEP, then revalidate watertightness, winding consistency, dimensions, and degenerate faces.
4. Include a model README, per-part quantities, explicit STL units, SHA-256 manifest, validation results, and licence/provenance status.
5. Exclude editor lock files and commercial reference CAD unless redistribution rights are confirmed.
6. Add an annotated installed-system photograph, a CAD part figure, and an electronics diagram only where they replace manuscript placeholders or clarify reproducibility.
7. Compile and visually inspect affected pages, test the archive CRC, scan included text for credentials/connection strings, and enforce the strict delivery-size limit.
8. Keep unverified print settings, magnets/fasteners, native-source mapping, repository/DOI, and licence as explicit blockers rather than inventing values.

## Dark Camera 2 capture

For a request explicitly requiring no illumination, send a successful `light.turn_off` through PUDA before capture and never run a convenience script until checking that it does not call `turn_on`. Probe the current RTSP path with bounded `ffprobe`; prefer local MediaMTX when available. Capture with bounded `ffmpeg`, verify dimensions/size and visually confirm that the top ring is not emitting, then attach the fresh image. `idle` is an edge execution state, not proof that the lamp is off.

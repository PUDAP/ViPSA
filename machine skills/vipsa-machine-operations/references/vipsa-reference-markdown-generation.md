# ViPSA skill/reference Markdown generation

Use this when the user asks for a concise downloadable reference of ViPSA skills, available machines, driver methods, visual/electrical/movement workflows, or compound PUDA protocols.

## Workflow

1. Load the currently relevant ViPSA/PUDA skills before drafting:
   - `vipsa-machine-operations`
   - `vipsa-image-capture`
   - `vipsa-vision-alignment`
   - `vipsa-electrical-measurements`
   - `vipsa-grid-measurement`
   - `approach`
   - when compound protocol/data/report context is requested: `puda-protocol`, `puda-data`, `puda-report`
2. Query live driver capabilities rather than relying only on remembered method lists:
   ```bash
   for m in keithley-2450 keithley-707b keysight-b2902b light stage zaber; do
     puda machine commands "$m"
   done
   ```
3. Include these concise sections:
   - operating baseline and safety rules
   - available machines and one-line descriptions
   - method inventory per machine, grouped by setup/safety/routing/measurement/motion/diagnostics
   - visual input skills: camera capture, lighting, alignment, hybrid visual+electrical checks
   - electrical skills: resistance/contact checks, DCIV, pulse tests, cleanup, plotting/reporting expectations
   - movement/navigation skills: stage Z, Zaber X/Y, grid traversal, manual jog panels
   - compound protocols: PUDA protocol creation, data extraction/hash/export, report generation
4. Create the file in a Windows-downloadable temp path when operating from WSL, for example:
   `/mnt/c/Users/amdm/AppData/Local/Temp/vipsa_skills_reference_<date>.md`
5. Verify the artifact before reporting:
   ```bash
   test -s <file> && wc -l <file> && sha256sum <file>
   ```
6. Return the file as a `MEDIA:` attachment. If the user asks for missing-context questions separately, send the deliverable and the context questions as separate messages.

## Style

Be concise but comprehensive. Prefer grouped method lists over exhaustive prose. Avoid preserving run IDs, one-off data, credentials, or transient failures. If exact driver source file paths/line numbers are requested, add them only after inspecting the current repository/source tree.
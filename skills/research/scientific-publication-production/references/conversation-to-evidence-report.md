# Conversation-to-evidence scientific report workflow

Use this workflow when the requested report is bounded by a chat interval and must integrate scientific results, filesystem evidence, and figures.

## 1. Fix the interval before writing

- Resolve the exact opening message by quoted text or session link.
- Identify the exact closing assistant message/time.
- Scroll the session in overlapping windows and extract user/assistant messages within that ID range.
- Treat tool logs as provenance, not narrative content; use them to verify paths and values.
- If the user changes topic inside the interval, include the resulting clarification when scientifically relevant.

## 2. Build an evidence ledger

Separate claims into:

1. **Qualified evidence** — passes physical/contact, polarity, initialization, compliance, and repeatability checks.
2. **Exploratory evidence** — useful for hypothesis generation but not qualification.
3. **Negative/control evidence** — disconnected paths, failed initialization, compliance stops, rejected contacts.
4. **Proposed work** — designed but not documented as executed.
5. **Explicit exclusions** — adjacent programmes/material systems that must not be used as evidence.

Preserve device identity exactly. If a plot or run lacks substrate/device coordinates, label it unnumbered rather than assigning the nearest plausible identity. A fitted curve does not supply provenance.

## 3. Dedupe sources and campaigns

- Treat copied report snapshots as duplicates unless they add distinct information.
- Distinguish retries/resumes from independent device observations.
- Do not merge imported historical archives with newer campaigns as one uniform design.
- Separate infrastructure validation (motion, vision, contact methods) from the scientific device result.
- Distinguish executed, stopped, and proposed campaigns in tables and prose.

## 4. Design the report around decisions

Recommended structure:

- Title page and evidence boundary
- Executive summary and status-at-a-glance table
- Scope/message provenance
- Scientific objective and evidence hierarchy
- Campaign chronology
- Strongest qualified result
- Controls and rejected interpretations
- Optimization/DOE work
- Infrastructure readiness
- Unresolved gates
- Recommended next campaign
- Evidence paths and cautions

Use denominators that expose attrition: attempted → contact-valid → DCIV-tested → bidirectional → pulse-tested → qualified p-bit → endurance survivor.

## 5. Place figures as evidence

- Reuse verified figures near the claim they support.
- Caption each with both what it supports and what it does **not** establish.
- Include controls beside connected-device results where possible.
- Include rejected/artifact plots when they explain why an apparent success was downgraded.
- Do not include excluded-programme figures merely because they are visually polished.

## 6. Produce and verify the Word artifact

- Use `python-docx` directly for complex report styling/tables when the JSON helper is too limited.
- Add page numbers, consistent headings, restrained table shading, and readable figure captions.
- Run the DOCX package validator and re-extract both structure and text.
- Programmatically assert that critical claims, exclusions, device identities, and stop reasons are present.
- Render through LibreOffice to PDF when available.
- Check representative pages: title, executive summary, dense table, figure-heavy middle, and final appendix. Inspect continuation pages when a table or section crosses a page boundary.
- Report page/figure/table counts only after the rendered artifact confirms them.

## 7. Scientific wording guards

- `completed` is not synonymous with `valid`.
- Compliance-limited current is a bound, not a precise conductance.
- A sigmoid fit is not proof of stochastic switching.
- Requested dwell is not measured pulse/sample timing.
- Matrix-open is not a matched full-route lifted-probe control.
- Report one-device feasibility separately from population-level yield.
- State unachieved system goals explicitly.

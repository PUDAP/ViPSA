---
name: physical-ai-platform-analysis
description: Use when comparing physical-AI control platforms.
---

# Physical-AI Platform Analysis

Use this skill to compare systems that let AI agents observe, control, or orchestrate physical equipment, especially when product terminology blurs protocols, standards, servers, runtimes, and complete automation platforms.

## Procedure

1. **Resolve the product identity first.** Verify the exact launch/product name and gently correct category errors. For example, a hardware standard that supports MCP is not itself merely an MCP server.
2. **Use current primary sources.** Prefer the vendor announcement/specification, official docs, and public implementation. Record announcement date, availability, open-source status, and whether technical details are public or preview-only.
3. **Classify each system by layer:**
   - agent/tool interface protocol
   - device schema or hardware abstraction
   - transport and discovery
   - state and telemetry model
   - orchestration and run lifecycle
   - persistence, audit, and provenance
   - safety metadata and enforcement
4. **Compare equivalent layers only.** Do not contrast MCP directly with an end-to-end runtime as though they are substitutes. State what each answers: how tools are called, how devices are represented, or how operations are executed and recorded.
5. **Separate safety claims from mechanisms.** Identify whether limits are advisory metadata, agent-enforced instructions, CLI approval gates, driver checks, controller limits, or physical interlocks. Note defaults, bypasses, and where enforcement actually occurs.
6. **Distinguish demonstrated behavior from standardized guarantees.** A successful case study is evidence of that deployment, not proof that every implementation enforces the same checks.
7. **Assess complementarity.** Explain whether the systems could interoperate, but label architectural compatibility ideas as inference unless an integration is documented.
8. **Ground the answer.** Cite load-bearing current claims inline and use a concise comparison table when it improves clarity.

## Comparison dimensions

A useful table usually includes: main abstraction, scope, command/state model, transport, workflow execution, safety, model dependence, availability/maturity, and best-fit use.

## Pitfalls

- Do not repeat the user's shorthand if the official product is materially different.
- Do not equate “supports MCP” with “is an MCP server.”
- Do not treat natural-language safety tags as hard enforcement without checking the dispatch path.
- Do not infer an organization-wide AI safety policy from operational hardware safeguards.
- Do not present planned open sourcing, evaluations, or approval rules as already available.
- Do not overstate a compatibility proposal as an existing integration.

## References

- See `references/puda-mhs-comparison.md` for the PUDA versus Anthropic MHS research snapshot and primary-source links.

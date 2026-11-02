# PUDA and Anthropic MHS comparison snapshot

Checked against public primary sources on 2026-09-07. Re-verify before future use because Anthropic MHS was only a research preview and PUDA was actively changing.

## Product identity

Anthropic announced the **Model Hardware Standard (MHS)** research preview on 2026-08-27. MHS is not simply an MCP server: Anthropic says agents can access it through MCP, a CLI, or code APIs. MCP is an access protocol; MHS is the physical-device standard.

## Layer comparison

### PUDA

- Public, open-source distributed runtime/control plane for Physical AI.
- Hardware- and LLM-agnostic.
- Edge drivers expose atomic machine commands.
- NATS provides discovery, command routing, telemetry, and responses.
- JSON protocols define machine IDs, parameters, ordered/parallel steps, validation, and START/COMPLETE run lifecycle.
- SQLite, run logs, IDs, and optional hashes support provenance and audit.
- Safety schema: `summary`, `hazards`, `requires`, `forbidden_when`, and `confirm`.
- Important enforcement boundary: `@safety` publishes advisory catalog metadata and does not itself block edge dispatch. Confirmation is opt-in and defaults false; hard limits must also exist in drivers, controllers, or physical interlocks.

### Anthropic MHS

- Research-preview specification for standardized physical-device drivers.
- Model- and harness-agnostic despite Claude-centered demonstrations.
- Uses standard device descriptions, state, and generic read/write-style primitives.
- Driver tags communicate machine characteristics and safety limits; a generated reference tells agents what can be measured or adjusted and what limits are enforced.
- Supports MCP, CLI, and code-file/API control.
- Emphasizes a shared state dictionary and interactive closed-loop adaptation; agents can package learned procedures into deterministic code files.
- Anthropic reported a CMU deployment that blocked missing plate, rotated plate, reader busy, disconnected camera, unreachable device, and active emergency-stop conditions before movement. Treat this as deployment evidence, not necessarily a universal conformance guarantee.
- Anthropic explicitly said safety evaluations, best practices, additional checks, and human approval rules for high-risk decisions were still being developed.
- Preview access was limited, with open sourcing planned later.

## Useful framing

- **MCP:** how an agent calls tools.
- **MHS:** how hardware state, controls, metadata, and limits are represented.
- **PUDA:** how machines are discovered and commands are transported, sequenced, executed, observed, and recorded.

The systems may be complementary. A future adapter could map MHS device descriptions into PUDA edges while PUDA handles distributed execution and provenance, but do not claim this exists without a documented implementation.

## Primary sources

- Anthropic announcement: https://www.anthropic.com/news/model-hardware-standard-research-preview
- PUDA architecture: https://docs.puda.co/docs/overview/architecture
- PUDA execution flow: https://docs.puda.co/docs/overview/under-the-hood
- PUDA edge safety semantics: https://github.com/PUDAP/skills/blob/main/puda-edge/SKILL.md
- PUDA protocol safety semantics: https://github.com/PUDAP/skills/blob/main/puda-protocol/SKILL.md
- PUDA implementation: https://github.com/PUDAP/puda

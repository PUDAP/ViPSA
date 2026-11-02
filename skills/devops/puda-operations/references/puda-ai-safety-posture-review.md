# PUDA AI safety posture review

Use this note when asked for PUDA's "AI safety policy," safety guarantees, or a comparison with another physical-AI platform.

## Finding (verified 2026-09-07)

PUDA's public documentation and public repositories did not expose a standalone organization-level AI safety policy or prohibited-use policy. Answer by distinguishing that absence from PUDA's implemented **operational hardware-safety posture**. Do not silently turn implementation details into a formal corporate policy.

## Operational controls found

- Natural-language requests are translated into explicit, deterministic JSON protocols rather than sent directly to hardware.
- Protocols identify machine, command, parameters, and step order, and are validated before execution.
- Only driver-exposed commands form the advertised machine command surface; commands should be atomic, typed, and documented.
- A command may advertise structured `@safety` metadata: `summary`, `hazards`, `requires`, `forbidden_when`, and `confirm`.
- Protocol-generation guidance says to retrieve safety metadata from the live command catalog and copy it unchanged; `requires` is a prerequisite and `forbidden_when` is an execution veto.
- For `confirm: true`, current source displays the full command and safety context and waits for operator approval.
- Runs use START/COMPLETE lifecycle messages, ordered steps, structured responses, SQLite/log persistence, and provenance records.
- Public architecture materials claim environment isolation, observability, provenance, and execution within a safe sandbox.

## Limits that must be stated

- `@safety` is authored by the machine integrator and is optional; `confirm` defaults to `false`.
- Safety metadata is advisory at edge dispatch and is not itself a hardware interlock.
- Current source includes a `--yes` bypass for confirmation prompts.
- PUDA does not, by these materials, guarantee emergency stops, physical interlocks, controller limits, formal hazard analysis, model evaluations, universal risk tiers, or a prohibited-use regime.
- Compare installed CLI help/version with current source before claiming a control is deployed locally. In the reviewed session, installed CLI 0.0.36 lacked the confirmation/`--yes` help present in repository source updated later.
- Treat physical interlocks, emergency stops, controller protections, risk assessment, and operator training as separate safety layers.

## Review workflow

1. Fetch `https://docs.puda.co/llms.txt` and inspect whether a dedicated safety/policy page now exists.
2. Inspect current architecture and under-the-hood documentation.
3. Inspect current `PUDAP/skills` safety guidance, especially `puda-protocol` and `puda-edge`.
4. Inspect the current `PUDAP/puda` CLI implementation/help for confirmation behavior and bypass flags.
5. Run the locally installed `puda version` and relevant `--help` commands to separate upstream capability from deployed capability.
6. Report in three sections: formal-policy status, operational controls, and limitations/gaps. Cite primary URLs.

## Primary sources

- https://docs.puda.co/llms.txt
- https://docs.puda.co/docs/overview/under-the-hood
- https://docs.puda.co/docs/overview/architecture
- https://github.com/PUDAP/skills/blob/main/puda-protocol/SKILL.md
- https://github.com/PUDAP/skills/blob/main/puda-edge/SKILL.md
- https://github.com/PUDAP/puda

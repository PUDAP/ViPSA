# Latest DCIV artifact discovery and Telegram handoff

Use this when asked when the latest DCIV was generated or to send its outputs.

## Find the latest real DCIV

1. Consult the live PUDA database schema before SQL. Query `command_log` only if DCIV is expected to be represented by a command name.
2. Locally orchestrated DCIV runs may exist only as run-folder artifacts and produce zero `command_log` rows containing `dciv`. Fall back to artifact discovery; do not conclude that no DCIV exists.
3. Search measurement data roots for characteristic outputs (`dciv*.png`, DCIV CSVs, and `summary.json`). Exclude skill/reference documents and source scripts from the candidate set.
4. Rank measurement artifacts by modification time and inspect the newest run's `summary.json`.

## Timestamp semantics

Prefer:

- `summary.json.finished_utc` for authoritative run completion,
- `summary.json.started_utc` for authoritative run start,
- file modification time for when a specific plot/table was written,
- run-directory timestamps only as discovery hints.

Report UTC and local time when useful. Keep “run finished” distinct from “artifact written”; these may differ by seconds.

## Select artifacts

Use `summary.json.artifacts` as the manifest when present. The default concise DCIV handoff is:

- declared plot (for example `dciv_lines.png`),
- declared combined data table (for example `all_cycles.csv`),
- `summary.json` for provenance and protocol metadata.

Do not send every raw/intermediate cycle file unless the user asks for the full raw bundle.

## Telegram delivery

- If multiple Telegram targets exist and no home channel is configured, do not guess between a DM and a laboratory group. Resolve or ask for the intended target before sending.
- Verify every selected file exists and record its size before upload.
- A successful text message accompanied by attachment warnings is only partial success. Retry failed attachments individually with bounded timeouts/retries.
- Preserve configured credential handling and never print tokens.
- Verify each upload from the platform response and report the destination plus per-file message IDs concisely.

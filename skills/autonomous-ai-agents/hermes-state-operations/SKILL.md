---
name: hermes-state-operations
description: "Operate Hermes user state safely: backups, restores, config/profile state, sessions DB, cron/gateway state, and post-restore verification without downgrading the Hermes runtime."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, backup, restore, config, sessions, cron, gateway]
    related_skills: [hermes-agent]
---

# Hermes State Operations

Use this skill when the user asks to restore, migrate, inspect, back up, or repair Hermes state under `~/.hermes` or a profile directory. This is for user data and operational state, not for editing Hermes Agent source code.

For Hermes CLI syntax and feature docs, also consult `hermes-agent`; this skill captures the operational restore workflow and pitfalls.

## Core principles

1. Restore state, not the runtime, unless the user explicitly asks to downgrade or replace the Hermes installation.
2. Take a safety archive of the current state before overwriting anything.
3. Stop write-producing services such as the Hermes gateway before replacing `state.db`, `cron/`, or `sessions/`.
4. Prefer Hermes-native exports/imports when available; otherwise restore archives carefully into the active Hermes home/profile.
5. Migrate old config after restore, then verify with current Hermes CLI.
6. Do not restart gateway/cron automatically after restoring old state if jobs may be overdue or externally noisy.

## Restore workflow for an old backup archive

For selective skill-only restores/merges, use `references/selective-skill-restore-from-backup.md`: back up active target skills, resolve skills by frontmatter `name`, diff current vs backup before writing, preserve newer current skills, restore archived/consolidated class-level skills to active categories when requested, recover support files from absorbed/umbrella references, patch stale archive notes, then verify with `skill_view` linked files.

1. Identify active paths and current runtime:
   - `hermes config path`
   - `hermes --version`
   - inspect `$HERMES_HOME`; default is usually `~/.hermes`
2. Inspect backup layout before extracting:
   - read `MANIFEST.txt` if present
   - list tar members with Python `tarfile` or `tar -tzf`
   - distinguish profile exports from direct `~/.hermes` essential-files archives
3. Validate backup integrity:
   - if the manifest has checksums with stale absolute paths, rewrite paths relative to the backup directory for `sha256sum -c`
   - if `MANIFEST.txt` itself fails because the path was moved, that alone does not invalidate the payload archives; verify the archive checksums separately
4. Create a current-state safety archive covering only paths likely to be overwritten:
   - `config.yaml`, `.env`, `auth.json`, `channel_directory.json`, gateway state
   - `state.db`, `state.db-wal`, `state.db-shm`
   - `sessions/`, `skills/`, `memories/`, `cron/`, `scripts/`, `hooks/`, `SOUL.md`
5. If gateway is active, stop it before extracting:
   - `systemctl --user is-active --quiet hermes-gateway && systemctl --user stop hermes-gateway`
   - record whether it was active so the user can decide whether to restart
6. Extract the selected state archive into the active Hermes home, preserving the current Hermes runtime/source unless explicitly asked otherwise.
7. Normalize ownership and sensitive file permissions:
   - `chown -R "$USER:$USER"` on restored state paths when needed
   - `chmod 600 ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/config.yaml`
8. Run config migration and checks:
   - `hermes config migrate`
   - `hermes config check`
   - `hermes status --all`
9. Verify sessions DB integrity:
   - use `python3 -c` with `sqlite3` stdlib if the `sqlite3` shell binary is missing
   - check `PRAGMA integrity_check` and count important tables such as `sessions` and `messages`
10. Inspect cron status:
   - `hermes cron list`
   - warn if restored active jobs have old `next_run_at` timestamps or external delivery targets

## Hermes logger / remote log database checks

Use this subsection when the user asks whether Hermes logs exist in a remote observability database (for example a Hermes logger plugin writing to InfluxDB).

1. Inspect the local logger plugin or README first to confirm the expected schema, measurement/table names, tag names, and env var names. Do not guess fields such as `agent_id`.
2. Confirm credentials only by presence/status; never print tokens or `.env` values.
3. For InfluxDB 3 endpoints, prefer the SQL API rather than the InfluxDB 2 Flux client:
   - endpoint: `POST <url>/api/v3/query_sql`
   - headers: `Authorization: Bearer <token>`, `Content-Type: application/json`
   - body: `{"db": "<database>", "q": "<SQL>"}`
   - useful discovery queries: `information_schema.tables` and `information_schema.columns`
4. Check every relevant Hermes table/measurement for the requested tag, not just one table. Typical tables from the logger plugin are `hermes_api_request`, `hermes_approval`, `hermes_llm_turn`, `hermes_session`, and `hermes_tool_call`.
5. Report a concise, evidence-backed answer: total matching rows, per-table counts, latest matching rows if any, and a short list of other observed agent IDs when the target is absent.

## Pitfalls

- Before staging SQLite backups, check the staging filesystem with `df -h`: `/tmp` may be RAM-backed and smaller than the database set. Use a disk-backed temporary directory with capacity for all snapshots; tmpfs exhaustion may surface as SQLite `OperationalError: disk I/O error`. Use SQLite online backup for live databases, exclude their original WAL/SHM from the archive, and read back the finished remote archive for integrity verification.

- InfluxDB 3 can return HTTP 404 from the InfluxDB 2 `/api/v2/query` Flux path even when the server and database are healthy. Treat that as an API mismatch and try `/api/v3/query_sql` before concluding the database is missing.
- The InfluxDB 3 SQL API expects the JSON key `q` for the query string; `query` or raw SQL request bodies can return serde errors.
- Do not blindly extract a profile export named `default/...` over `~/.hermes`; profile exports may contain a top-level profile directory and extra caches. Use the archive whose structure matches the destination or import it with Hermes profile tooling.
- Do not treat missing system binaries such as `sqlite3` as a restore failure; Python's standard `sqlite3` module is a reliable fallback for DB verification.
- Do not restart gateway automatically after a restore when cron jobs were restored from the past. Starting the gateway may immediately fire overdue jobs and send Telegram/other platform messages.
- Do not print `.env`, `auth.json`, tokens, or restored secrets. Report presence/status only.
- Do not conclude the backup is corrupt from a checksum mismatch caused only by the backup directory moving; verify the payload archive checksums with adjusted relative paths.

## Verification checklist

Report concise evidence after restore:

- backup archive verified or reason for partial checksum warning
- safety archive path
- restored destination path
- current Hermes version unchanged unless intentionally changed
- `hermes config check` result, including whether config was migrated
- auth/provider status at a high level only
- SQLite integrity result and session/message counts
- gateway/cron status, including whether the gateway was left stopped

## References

- `references/old-backup-restore-2026-07-06.md` — example restoring an older default-profile backup into a newer Hermes install while preserving runtime and preventing overdue cron side effects.
- `references/influxdb3-hermes-log-checks.md` — InfluxDB 3 SQL endpoint pattern for checking Hermes logger tables by `agent_id` and reporting evidence.

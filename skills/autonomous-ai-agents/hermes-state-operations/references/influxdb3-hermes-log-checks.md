# InfluxDB 3 Hermes log checks

Session-derived note for checking whether a Hermes logger database contains records for a specific `agent_id`.

## Context

The Hermes logger plugin writes measurements/tables such as:

- `hermes_api_request`
- `hermes_approval`
- `hermes_llm_turn`
- `hermes_session`
- `hermes_tool_call`

The plugin adds `agent_id` as a tag when `AGENT_ID` is configured.

## InfluxDB 3 query pattern

InfluxDB 3 may expose an HTTP service on a nonstandard port and reject InfluxDB 2 Flux queries with 404. Use SQL instead:

```http
POST http://host:port/api/v3/query_sql
Authorization: Bearer <token>
Content-Type: application/json

{"db":"hermes-logs","q":"SELECT table_name FROM information_schema.tables WHERE table_schema='iox'"}
```

Important details:

- The database name goes in JSON key `db`.
- The query string goes in JSON key `q`.
- Raw SQL bodies or `query` instead of `q` can fail with serde JSON errors.
- Use `information_schema.columns` to verify `agent_id` exists before filtering.

## Recommended check

For each actual Hermes table, run:

```sql
SELECT COUNT(*) AS n, MIN(time) AS first_time, MAX(time) AS last_time
FROM <table>
WHERE agent_id = '<target-agent-id>'
```

If all counts are zero, also query top observed agent IDs so the final answer can distinguish “database empty/unreachable” from “logs exist, but not for this agent”:

```sql
SELECT agent_id, COUNT(*) AS n
FROM <table>
GROUP BY agent_id
ORDER BY n DESC
LIMIT 10
```

Report: reachable database, tables checked, total matching rows, per-table counts, latest matching rows if any, and other observed agent IDs when useful.

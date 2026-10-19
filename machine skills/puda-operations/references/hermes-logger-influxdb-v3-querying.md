# Hermes logger InfluxDB v3 querying for PUDA/Hermes agents

Use this when checking whether a PUDA/Hermes agent has written observability rows to the shared Hermes logger database.

Known durable connection shape:

- InfluxDB HTTP endpoint: `http://bearsnas:8181`
- Database/bucket: `hermes-logs`
- Org observed for the service: `bears`
- The service requires `Authorization: Token <provided-token>`; do not persist tokens in skills or memory.

Important API pitfall:

- This endpoint behaves like InfluxDB v3. The Python `influxdb_client` Flux query API and `/api/v2/query` may return `404 Not found` even when the database is healthy.
- Verify auth/health with `GET /health` using the token header.
- Query with the SQL API: `/api/v3/query_sql?db=hermes-logs&q=<urlencoded SQL>`.

Minimal shell probe pattern:

```bash
TOKEN='<provided-token>'
DB='hermes-logs'
BASE='http://bearsnas:8181/api/v3/query_sql'
SQL="SELECT COUNT(*) AS n FROM hermes_llm_turn WHERE agent_id = 'vipsa'"
curl -sS -H "Authorization: Token $TOKEN" \
  --get "$BASE" \
  --data-urlencode "db=$DB" \
  --data-urlencode "q=$SQL"
```

Useful SQL checks:

```sql
-- Available Hermes logger tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'iox'
ORDER BY table_name;

-- Per-agent counts and latest timestamps by table
SELECT agent_id, COUNT(*) AS n, MAX(time) AS latest
FROM hermes_llm_turn
GROUP BY agent_id
ORDER BY latest DESC
LIMIT 20;

SELECT agent_id, COUNT(*) AS n, MAX(time) AS latest
FROM hermes_tool_call
GROUP BY agent_id
ORDER BY latest DESC
LIMIT 20;

SELECT agent_id, COUNT(*) AS n, MAX(time) AS latest
FROM hermes_api_request
GROUP BY agent_id
ORDER BY latest DESC
LIMIT 20;

SELECT agent_id, COUNT(*) AS n, MAX(time) AS latest
FROM hermes_session
GROUP BY agent_id
ORDER BY latest DESC
LIMIT 20;

-- Direct existence check for a target agent
SELECT COUNT(*) AS n FROM hermes_llm_turn WHERE agent_id = '<agent_id>';
SELECT COUNT(*) AS n FROM hermes_session WHERE agent_id = '<agent_id>';
SELECT COUNT(*) AS n FROM hermes_tool_call WHERE agent_id = '<agent_id>';
SELECT COUNT(*) AS n FROM hermes_api_request WHERE agent_id = '<agent_id>';
```

Reporting guidance:

- If the database is reachable but the target `agent_id` has zero rows, say so directly and include counts by measurement.
- If other agent IDs have rows, list them as evidence that the DB is populated and the issue is agent-specific ingestion/configuration, not database emptiness.
- Do not store or echo tokens; describe them as a provided token unless the user explicitly needs to re-use the exact credential in-session.

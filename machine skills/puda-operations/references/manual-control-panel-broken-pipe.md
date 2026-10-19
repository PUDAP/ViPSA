# PUDA manual-control web panel: dead logging pipe

## When to use

Use when a PUDA manual-control/jog web panel appears offline while its TCP port is still listening.

## Confirmed failure pattern

A Python `BaseHTTPRequestHandler` server can remain alive and accept connections yet return `Empty reply from server` for every route when:

- stdout/stderr still point to an anonymous pipe created by the launching terminal or agent;
- the pipe reader has exited;
- `log_message()` uses `print(..., flush=True)` without handling `BrokenPipeError`.

`send_response()` invokes request logging before the response is complete, so a logging exception aborts the HTTP handler.

## Deterministic diagnosis

1. Confirm the listener and owning PID with `ss -ltnp`.
2. Reproduce at the HTTP boundary with `curl` against both `/` and a lightweight status endpoint.
3. Inspect `/proc/<PID>/fd/1` and `/proc/<PID>/fd/2`.
4. If they resolve to `pipe:[N]`, scan `/proc/*/fd/*` for that exact inode. If only the server's write descriptors remain, the pipe has no reader and the diagnosis is confirmed.
5. Check service logs, process threads, and resource state to rule out an application deadlock or OOM before changing anything.

## Lab-safety gate before restart

For a control panel tied to PUDA machines, a UI restart can erase in-memory session ownership while edge machines retain an active run. Before stopping the panel:

- query every machine directly with `puda machine state`;
- record the exact active `run_id` and which machines hold it;
- do not issue reset, complete, START, jog, or motion commands merely to recover the UI;
- preserve the active run in the replacement panel only if restoration is explicit and can be verified;
- otherwise stop and obtain user approval.

## Durable prevention

- Make request logging non-fatal by catching `BrokenPipeError` and `OSError`, or route logging through a logger that cannot abort request handling.
- Launch long-lived panels under a service manager with durable stdout/stderr rather than an ephemeral terminal pipe.
- After recovery, require all of these checks:
  1. HTTP 200 from the root and status endpoint.
  2. Expected session/run ID visible in the status response when a run was active.
  3. Live machine states unchanged and no motion/reset commands emitted.

Do not claim recovery unless all checks pass.

# Absorbed skill: hermes-s6-container-supervision

Original package: `software-development/hermes-s6-container-supervision` archived after consolidation into `hermes-agent`.

Support files copied: none.

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: hermes-s6-container-supervision
description: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docker, s6, supervision, gateway, profiles]
    related_skills: [hermes-agent, hermes-agent-dev]
---

# Hermes s6-overlay Container Supervision

## When to use this skill

Load this skill when you're working on:
- Adding or removing a static service in the Hermes Docker image (something that should be supervised at every container start, like the dashboard)
- Diagnosing why a per-profile gateway isn't starting, restarting, or surviving `docker restart`
- Understanding why the container's CMD is `/opt/hermes/docker/main-wrapper.sh` and how leading-dash args reach the user's program
- Modifying `cont-init.d` boot scripts (UID remap, volume seeding, profile reconciliation)
- Changing the rendered run-script for per-profile gateways (Phase 4)

If you're just running the Hermes Agent and want to use Docker, see `website/docs/user-guide/docker.md` instead.

## Architecture at a glance

```
/init                                  ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d                        ← oneshot setup, runs as root
│   ├── 01-hermes-setup                ← docker/stage2-hook.sh
│   │   ├── UID/GID remap
│   │   ├── chown /opt/data
│   │   ├── chown /opt/data/profiles (every boot)
│   │   ├── seed .env / config.yaml / SOUL.md
│   │   └── skills_sync.py
│   └── 02-reconcile-profiles          ← hermes_cli.container_boot
│       ├── chown /run/service (hermes-writable for runtime register)
│       └── walk $HERMES_HOME/profiles/<name>/gateway_state.json
│           → recreate /run/service/gateway-<name>/
│           → auto-start only those with prior_state == "running"
│
├── s6-rc.d (static services, in /etc/s6-overlay/s6-rc.d/)
│   ├── main-hermes/run                ← exec sleep infinity (no-op slot)
│   └── dashboard/run                  ← if HERMES_DASHBOARD=1, runs `hermes dashboard`
│
├── /run/service (s6-svscan watches; tmpfs)
│   ├── gateway-coder/                 ← runtime-registered per-profile
│   │   ├── type        ("longrun")
│   │   ├── run         ("#!/command/with-contenv sh ... exec s6-setuidgid hermes hermes -p coder gateway run")
│   │   ├── down        (marker — present means "registered but don't auto-start")
│   │   └── log/run     (s6-log → $HERMES_HOME/logs/gateways/coder/current)
│   └── ...
│
└── CMD ("main program")               ← /opt/hermes/docker/main-wrapper.sh
    └── routes user args: bare exec | hermes subcommand | hermes (no args)
        — exec'd by /init with stdin/stdout/stderr inherited (TTY for --tui)
```

## Key files

| Path | Role |
|---|---|
| `Dockerfile` | s6-overlay install + cont-init.d wiring + `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]` |
| `docker/stage2-hook.sh` | The "old entrypoint logic" — UID remap, chown, seed, skills sync. Runs as cont-init.d/01-hermes-setup. |
| `docker/cont-init.d/02-reconcile-profiles` | Calls `hermes_cli.container_boot` on every boot to restore profile gateway slots from the persistent volume. |
| `docker/main-wrapper.sh` | The container's CMD. Routes user args, drops to hermes via `s6-setuidgid`, exec's the chosen program. |
| `docker/s6-rc.d/main-hermes/run` | No-op `sleep infinity` — slot exists so the s6-rc user bundle is valid; main hermes runs as the CMD, not as a supervised service. |
| `docker/s6-rc.d/dashboard/run` | Conditional service — `exec sleep infinity` unless `HERMES_DASHBOARD` is truthy. |
| `docker/entrypoint.sh` | Back-compat shim that `exec`s the stage2 hook. External scripts that hard-coded the old entrypoint path still work. |
| `hermes_cli/service_manager.py` | `S6ServiceManager`: `register_profile_gateway`, `unregister_profile_gateway`, `start/stop/restart/is_running`, `list_profile_gateways`. |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` — walks persistent profiles, regenerates s6 slots, emits `container-boot.log`. |
| `hermes_cli/gateway.py::_dispatch_via_service_manager_if_s6` | Intercepts `hermes gateway start/stop/restart` and routes to s6 when running in a container. |

## Why Architecture B (CMD as main program, not s6-supervised)

The original plan (v1–v3) called for main hermes to run as a supervised s6-rc service. Two real s6-overlay v3 mechanics blocked that:

1. **cont-init.d scripts receive no CMD args** — so the stage2 hook can't parse `docker run <image> chat -q "hi"` to set `HERMES_ARGS` for a service `run` script to consume.
2. **`/run/s6/basedir/bin/halt` does NOT propagate the exit code** written to `/run/s6-linux-init-container-results/exitcode`. Containers always exit 143 (SIGTERM) regardless. Confirmed by skarnet (s6 author) in [issue #477](https://github.com/just-containers/s6-overlay/issues/477): _"if you want a container shutdown, you need to either have your CMD exit, or, if you have no CMD, write the container exit code you want then call halt"_.
```

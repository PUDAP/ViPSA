# PUDA machine-listing session notes

A user asked to list current PUDA machines from WSL. The installed CLI was available at `~/.local/bin/puda` and reported version `0.0.28` for `linux/amd64`.

Observed command behavior:

```bash
puda env list
```

returned built-in/known environments even without global login config:

```text
bears    create tower (dev work)
ifim     IFIM setup
imre     CuspAI setup
ntu      PUDA NTU setup
```

But machine discovery failed without the global config:

```bash
puda machine list --json
```

```text
Error: failed to load global config (run 'puda login' first): PUDA config file not found at /home/vipsa/.config/puda/config.json. Please run 'puda login' to create it
```

`puda env current` and `puda config list` also require `~/.config/puda/config.json`.

Useful response pattern when blocked:

- Say the CLI is installed but not logged in/configured for this WSL user.
- Show `puda login --username <your-username>` as the next required setup command.
- After login, rerun `puda env current` and `puda machine list --json`.

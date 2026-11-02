# Gateway config updates

Use this reference when changing Hermes gateway platform settings in `~/.hermes/config.yaml`, especially Telegram allowlists and mention gating.

## Pattern

1. Read/inspect the relevant config keys first (`hermes config path`, `hermes config`, or a narrow file read).
2. Do not edit `~/.hermes/config.yaml` with generic file patch/write tools; Hermes protects security-sensitive config paths. Use Hermes' config CLI:
   - `hermes config set telegram.allowed_chats '<chat_id_or_csv>'`
   - `hermes config set telegram.require_mention true`
3. Verify by reading/parsing the config. For Telegram group allowlists, the effective block should look like:

```yaml
telegram:
  allowed_chats: '-1003732139300'
  require_mention: true
```

4. If the gateway is running, restart it so the new config is loaded:
   - `hermes gateway status`
   - `hermes gateway restart`
   - `hermes gateway status`

## Profile routing and restart pitfalls

- Run profile-specific CLI checks from a neutral working directory (for example `/home/<user>`) and pass `hermes --profile default ...` explicitly. A working directory inside another profile can cause misleading target/plugin discovery results; validate with `hermes --profile default config path` before concluding credentials or targets are absent.
- A running gateway process does not prove messaging adapters are connected. Check its startup logs for `No messaging platforms enabled` and `No env user allowlists configured`; compare narrowly with saved allowlists before changing access policy.
- If `hermes gateway restart` refuses because the command is inside a gateway process, do not bypass that guard using systemd, signals, subprocesses, or scheduling. Ask the user to run the explicit profile restart in an independent shell.

## Telegram notes

- `telegram.allowed_chats` gates group/supergroup chat IDs where the bot may respond.
- `telegram.require_mention: true` means allowed group chats still require an explicit bot mention/trigger, reducing unsolicited replies.
- When adding one chat ID to an empty allowlist, set the string directly. If preserving existing IDs, read the current CSV/list first and append without dropping existing entries.
- Avoid recording bot tokens or any `.env` content while verifying gateway config.

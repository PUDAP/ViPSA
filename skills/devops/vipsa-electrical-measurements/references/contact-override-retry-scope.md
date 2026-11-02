# Scope of explicit contact-gate overrides

When a user explicitly authorizes a high-voltage forming/SET/RESET sequence despite an open-like or failed contact precheck:

- Record the fresh contact evidence and exact override in run metadata.
- Preserve that authorization through fresh retries of the same measurement after infrastructure recovery.
- Do not silently broaden it into general permission for different destructive recipes.
- If the user later requests a verified mechanical approach followed by “the same test,” that authorizes repeating the exact established cycle sequence after the move.
- Keep all output-off, switch-open, endpoint, record-count, and cleanup checks mandatory.
- Continue reporting the electrical result as open-like/no-switching when supported; visual probe overlap is not proof of contact.
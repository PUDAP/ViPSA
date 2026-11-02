# Legacy default-profile skill snapshot

This `legacy` branch preserves the installed default Hermes skill packages before the ViPSA skill-tree cleanup. The existing ViPSA application files are inherited unchanged from the branch base; this is not a deployment branch.

## Included

- All 90 installed default-profile skill packages under `skills/`.
- All 1,185 package files: SKILL.md bodies, scripts, references, schemas, templates, tests, examples and assets where present.
- Nine shared skill-directory symlinks materialized as ordinary files, so this snapshot does not depend on the original host's `~/.agents/skills` directory.
- Kanban-gated installed skills are included even when hidden from a normal chat's runtime index.

## Excluded

Archived skill packages (`.archive`), runtime/curator/usage metadata, credentials and Hermes configuration, Python/dependency caches, virtual environments, and unrelated experiment datasets or external runtime scripts. Runtime instrument/protocol schemas outside the installed skill packages are not included.

## Integrity and publication safeguards

`skill-snapshot-manifest.json` enumerates every skill and included file with SHA-256, byte size and executable status. It records the snapshot timestamp and which shared sources were materialized.

A detect-secrets 1.5.0 static scan was reviewed before publication. Two ambiguous credential-like documentation literals were replaced with explicit placeholders in this publication copy only. Their manifest entries preserve the original source hash and the publication hash, with a `publication_redactions` record; no claim of credential validity was made. The remaining scanner findings are documentation placeholders, environment-variable names and test/example values. Static scanning cannot guarantee the absence of all secrets.

No live skill files, shared skill targets, experiment processes, instrument settings, scheduled jobs or source working-checkout changes were modified to make this snapshot. No skill helper or acquisition script was executed as a test.

This is historical reference material, not a claim that the scripts are safe/current or validated. It intentionally retains stale paths, historical operational examples and mixed-scope content for review. Do not execute embedded hardware commands without current authorization and station-specific validation.

# Selective Skill Restore from a Profile/State Backup

Use this reference when a backup contains useful skills but should not be restored wholesale.

## Principles

- Restore user knowledge, not old runtime state. Do not copy an entire `.hermes/` tree over the active profile just to recover skills.
- Create a current-state safety archive before writing any skill files.
- Prefer current active skills when they are newer than the backup. Backup-only content should be merged selectively.
- Preserve the class-level library shape: restore narrow archived skills only when they are actively useful, or re-home their content into an existing umbrella with references.

## Diff/merge workflow

1. Locate active and backup skills by `name:` frontmatter, not only by path. Skills may move between categories or into `.archive/`.
2. Compare `SKILL.md` hashes/line diffs for the target skills.
3. Compare support files under `references/`, `templates/`, `scripts/`, and `assets/`.
4. If the active skill has only additive newer content, keep active and do not overwrite it.
5. If a backup skill exists only in `.archive/` but is still directly useful, restore it into an active class/category path and bring along support files.
6. If the backup note says a narrow skill was consolidated into an umbrella, inspect the umbrella's `references/absorbed-skills/<old-skill>/` or similarly named provenance directory; the archived `SKILL.md` may be incomplete without those support files.
7. After restoration, validate each restored skill:
   - frontmatter starts at byte 0 with `---`
   - `name` and `description` exist
   - description length is within limits
   - support files are visible via `skill_view`
8. Report exactly what was restored, what was preserved as newer, and the safety archive path.

## Example patterns

- A backup `vipsa-machine-operations` skill may be older than the active skill; preserve active if backup has no backup-only instructions.
- A narrow archived skill such as `vipsa-vision-alignment` may be worth restoring as active when it governs a frequent task. Its useful references may live under an absorbed-skill directory in another umbrella; restore those references too.
- A narrow streaming/camera skill may have an archived `SKILL.md` plus richer references under `media-workflows/references/<skill-name>/`; restore both or point the active skill to the umbrella references.

## Pitfalls

- Do not use `DONE`/archive presence alone as evidence that a skill is obsolete; inspect whether its workflow is still invoked by current tasks.
- Do not overwrite a newer active skill with an older backup copy just because the user said “restore.” Merge the backup-only value, not the timestamp.
- Do not restore secrets, cron jobs, session DBs, or runtime checkout files when the request is only to recover skill knowledge.

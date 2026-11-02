# Selective Hermes Skill Restore / Merge

Use this when a user points at an old `~/.hermes/skills` backup and asks to restore or merge selected skills into the active profile.

## Safe workflow

1. **Back up the active target skills first.** Archive the exact active skill directories that may be overwritten, including `.archive/<skill>` if that is the only active copy.
2. **Resolve skills by frontmatter `name`, not just directory name.** Old backups may have active skills under category paths, archived skills under `.archive/`, or absorbed copies under another umbrella skill's `references/absorbed-skills/<name>/`.
3. **Diff current vs backup before writing.** Compare `SKILL.md` hashes/line diffs and support files. If the current skill only has additions relative to backup, preserve current and do not overwrite it.
4. **Promote archived/consolidated skills only when useful as class-level skills.** Restore them under an appropriate active category such as `devops/<skill-name>/`, not back into `.archive/`, when the user explicitly wants them available as skills.
5. **Restore support files too.** If an archived skill's `SKILL.md` points to `references/...` but its own directory lacks them, search the backup for absorbed/consolidated copies such as:
   - `<umbrella>/references/absorbed-skills/<skill-name>/references/`
   - umbrella-specific reference folders that were created during consolidation
6. **Patch stale reconstruction notes.** If a restored skill says it was consolidated/archive-only, replace that with a short `Restored references` section listing the restored support files.
7. **Verify with `skill_view`.** Confirm the restored skill loads by name, frontmatter is valid, and `linked_files.references` lists the support files.
8. **Report exactly what changed.** Include safety backup path, which skills were restored, which current skills were preserved as newer/identical, and reference counts.

## Merge policy

- Prefer current active skills when they are newer than the backup.
- Use backup content to fill missing class-level skills or missing support references.
- Do not restore old runtime state, cron, secrets, logs, or Hermes source just because a skill merge was requested.
- Do not overwrite a current skill wholesale unless the diff shows the backup has durable missing content and current does not have newer additions.

# Pinned PUDA edge publication handoff

## Scope
Publication, edge deployment/restart, and physical execution are separate scopes. A publication-only request does not authorize hardware commands. Do not change main or force-push. Do not invent external qualification evidence.

## Verified publication pattern
1. Read the handoff and preserve exact repository, bundle ref, expected release SHA, rollback SHA, and prerequisite SHA. Confirm existing authenticated access without printing credentials.
2. Verify the bundle in a repository containing its prerequisite (`git -C <clone> bundle verify <bundle>`).
3. Create an isolated bare clone of the local repository; set its origin to the requested GitHub repository. This avoids changing the active hardware checkout or another profile's workspace.
4. Fetch the exact bundle branch into that bare clone. Confirm the release/rollback objects and review the changed-file scope.
5. Push release and rollback refs atomically, without force:
   `git -C <bare> -c credential.helper= -c 'credential.helper=!gh auth git-credential' push --atomic origin <release-sha>:refs/heads/<release-branch> <rollback-sha>:refs/heads/<rollback-branch>`
   This per-command helper uses existing gh authentication without changing global Git config or embedding tokens in URLs.
6. Read back both exact refs with `git ls-remote`. Compare their SHAs literally before reporting publication. Return branch URLs and full SHAs; explicitly state that no deployment, restart, bias, or motion occurred.

## Shared-checkout deployment safety (verified 2026-10-08)
Before a single-edge update, inspect the installed SDK `edge_updater.py`, exact process cwd, whole-repository dirty diff, pinned-release diff, and `uv sync --dry-run` from the edge cwd. The updater performs whole-repository `git reset --hard` followed by ordinary `uv sync`, not `--all-packages`. In the shared ViPSA workspace, a 2450 member sync would remove 20 installed packages, including pyvisa-py, pyusb, and zaber-motion, even when lockfiles are unchanged. Do not deploy this way during shared-edge operation.

If isolation is authorized, clone the exact published commit into a separate checkout, preserve `.env` and the original process environment privately, and retain the existing interpreter/environment without syncing or upgrading it. Verify direct START -> get_output=0 -> COMPLETE and matrix get_closed_channels=nil first. Release only the target driver with its acknowledged shutdown, stop only its exact Python PID (never the start_all_edges parent), then launch one isolated replacement. Verify fresh API responses, exact commit and code SHA256, OFF/open/idle cleanup, and unchanged original workspace and other edge PIDs. Preserve a pinned rollback ref. Do not prepare/execute a waveform or invent qualification evidence. This isolated live restart does not modify boot/start_all_edges configuration; state that limitation explicitly.

Unknown protected-command probes can set KV state to error although the SDK auto-completes the active run; COMPLETE then reports RUN_ID_MISMATCH because no run remains. Reconcile exact edge logs before any recovery. A fresh successful lifecycle START plus read-only output query and COMPLETE can restore idle without a driver reset when the failed run is proven ended.

## Campaign authorization lesson
Carry forward existing bounded operator authorization rather than asking repeatedly for routine steps. Separate permission from missing implementation and readiness evidence. Reuse unchanged verified transport/mapping/trace/cleanup components, test changed functionality and current hardware state, and resolve code gaps autonomously within scope. Reuse infrastructure, not historical stress recipes. Do not add blanket offline-only/wait-for-go restrictions to steer messages unless requested.

A claimed exact read window needs actual timing evidence; read_count or NPLC alone is insufficient. Post-sweep measured-energy integration reconciles exposure but does not enforce an in-progress limit. These capability questions are not solved by another generic approval or setting qualification flags true. Ask one concrete question only when an unsupported requirement, scope expansion, or limit change needs an operator decision.

# Explicit contact-gate override for queued ViPSA yield runs

Use when a user explicitly says to run a forming/SET/RESET test **regardless of contact**, especially through `/queuerun` or equivalent background execution.

## Authorization boundary

- A failed low-bias contact gate normally blocks high-voltage work.
- An explicit, current-turn override such as “regardless of contact” authorizes bypassing that gate for the requested electrical sequence only.
- A prior-run override does **not** automatically carry to a later device, a new Z height, or a fresh rerun. If the contact check still fails, report the fresh result and obtain a new explicit override before launching. Once the user gives that override, start immediately rather than asking again.
- Still run or reuse a fresh low-bias precheck and record its artifact, measured resistance/current, classification, tracked stage Z, and the exact override text in run metadata. Do not relabel open-like contact as valid contact.
- The override does not authorize different voltage endpoints, compliance limits, timing, extra cycles, or future runs.

## Preflight and recovery

1. Verify all required machines are idle and no conflicting measurement process exists.
2. Turn illumination off before electrical routing.
3. Force SMU outputs off, open the 707B, and verify closed channels are `nil`.
4. If the 707B reports `state=error` with a stale run ID, use the supported PUDA reset form with global flags accepted by the live CLI, then require `idle` / `run_id:null` before proceeding. Do not begin a high-voltage run while routing state is uncertain.
5. Preserve the sample campaign boundary and write to the Pratap-specific run tree when testing Pratap's samples.

## Exact slow-sweep construction

For `0.05 V` steps at requested `0.05 V/s`, use `1.0 s` commanded interpoint dwell. Execute each operation as a complete zero-return native list:

- `0 → +10 → 0 V`, `100 µA` compliance
- `0 → −2 → 0 V`, `100 mA` compliance
- `0 → +3 → 0 V`, `1 mA` compliance
- `0 → −4 → 0 V`, `100 mA` compliance

Keep Keithley source-list chunks at 50 points or fewer. Allow at least 300 s instrument timeout plus sufficient PUDA timeout for long autoranging lists.

## Queue semantics

- For `/queuerun`, launch the bounded runner in the background with completion notification rather than blocking the chat.
- Use a fresh timestamped output directory; never reuse a prior completed or partial run directory.
- The immediate response may say **queued/started** and list the exact requested parameters, but must not imply the sweep completed.
- On completion, verify every expected record count and measured endpoint before accepting the run. Preserve partial summaries after each cycle.

## Final verification

After completion or failure, require:

- Keithley output off;
- 707B `open_all` and closed channels `nil`;
- light off;
- all touched machines idle with null run IDs;
- exact point counts/endpoints, ordered CSV, summary, and connected-line plot verified before reporting results.

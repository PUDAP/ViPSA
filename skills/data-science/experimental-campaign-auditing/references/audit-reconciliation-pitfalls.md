# Experimental log reconciliation checks

## Sources and identity

Use original protocol logs, actual run summaries, response DB rows and raw result files before chat-history attribution. Inventory inclusion/exclusion decisions explicitly; copied resume folders and canonical-site choices do not themselves establish original campaign start/end. Keep primed sites and physical substrates distinct. A final serpentine site may have a lower device number than earlier sites.

## Common false counts

- A protocol JSON is a plan until submission/execution evidence is found.
- A response row may duplicate a submission; lifecycle ACKs are not measurement attempts.
- One native voltage list with hundreds of returned rows is one high-level operation.
- Read-error queue command names are not error events. Match actual failed responses, command failure lines or explicit unsuccessful runner statuses.
- `forming_success` and successful preflight statuses are not interruptions merely because they are not spelled `completed`.
- Several failure lines and resume folders can describe one operational interruption. Report distinct populations rather than summing them.
- A script that measures and plots has mixed purpose; no standalone plotting count can be inferred from the absence of a plotting-only tool invocation.

## Timing checks

Record both timestamp timezone and precision. Header timestamps may be local while returned instrument timestamps are UTC. Second-resolution CLI elapsed is not high-resolution physical motion duration.

For untimed raw operations, map the operation index/path to its saved summary `phase` and `elapsed_s`. Avoid copies and avoid operations already represented by bounded command spans. Report elapsed call duration without fabricated absolute UTC placement. If aggregating into an unclassified gap budget, require nonnegative residuals per campaign and expose the assumptions.

For approach/characterization splitting, identify forming/contact operations using explicit phase evidence first. Voltage-range heuristic candidates must remain labeled candidates. Remove the forming subtotal from electrical characterization; retain total electrical-call duration as the sum of the two. Mechanical contact increments may be unresolved from retract/pre-approach Z moves, so full workflow duration can remain unavailable even when forming elapsed is known.

## Delivery and late notifications

Put limitations next to the plotted metric, not only in an appendix. Missing timing must not look like zero motion. Date-by-time blocks should split at midnight and label proxy boundaries clearly.

Late delegated timeouts or failed redundant reruns do not invalidate a previously verified artifact automatically. Check the exact delivered archive/report and successful execution evidence before announcing changed results; use the configured execution environment for verification. This is a reconciliation pattern, not a claim that a particular interpreter or tool is permanently unusable.

For files-only requests, the README, CSV fields and figure footnotes carry the explanation; the chat delivery contains only file attachments.

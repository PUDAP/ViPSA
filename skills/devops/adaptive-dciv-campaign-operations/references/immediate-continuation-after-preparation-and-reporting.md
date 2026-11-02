# Immediate continuation after verified preparation

For an already-authorized automatic DC-IV campaign, a verified preparation terminal state is the dispatch boundary—not a place to pause for another user prompt.

## Rule

Once alignment, preparation, and cleanup all verify and the immutable candidate binding is validated, dispatch the candidate immediately unless an unresolved safety, control, transport, ownership, or science gate exists.

Progress reports, status replies, and plot requests do not implicitly pause or cancel the campaign. Produce plots/reporting in parallel when safe, then continue the standing authorization. Do not leave a prepared device idle merely because the user requested an artifact or because a user-facing message was sent.

## Required pause conditions

Pause only for concrete unresolved gates such as:

- output/matrix/cleanup cannot be verified;
- active UNKNOWN exposure;
- transport fault after dispatch;
- ownership conflict or duplicate controller;
- pose/alignment uncertainty;
- immutable recipe/binding mismatch;
- configured failure rule or hard cap;
- explicit operator stop or changed authorization.

When pausing, name the exact gate and resume automatically as soon as it is independently cleared under the existing authorization.

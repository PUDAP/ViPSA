# Literature p-bit protocol conversion into ViPSA grid runs (2026-07-31)

## Trigger
Use when the user asks to run the protocol found/finalized from p-bit literature, especially after asking “what was the reported protocol for p-bits?” and then “run this protocol from subsequent devices.”

## Concrete ViPSA-adapted protocol
Name: **contact-gated randomized RESET-read-SET-read p-bit characterization**.

### A. Contact/read gate
Use Keithley + 707B in the dark before claiming p-bit data:

```text
0 V, +10 mV, -10 mV, +50 mV, -50 mV
3 reads per voltage
read compliance: 1 µA
settle: ~0.2 s
```

Classification:
- pA/sub-nA with no voltage scaling → open/weak; skip DCIV/p-bit pulse train for probability claims.
- nA-scale and voltage-scaled without compliance → p-bit candidate.
- read-compliance at low bias → short-like/over-contact; skip long p-bit train unless user explicitly asks for failure/override data.

### B. Conservative DCIV/forming for candidates
For grid screening use:

```text
0 -> +0.8 -> 0 -> -1.0 -> 0 V
step: 50 mV
positive compliance: 1 µA
negative/reset compliance: 10 µA
```

Run post-DCIV low-bias health. If post-DCIV health is read-compliance-limited/short-like, do not run the long p-bit pulse train.

### C. Randomized p-bit pulse train
Use the literature-style order so each trial begins from a reset-side attempt and then samples the SET probability:

```text
RESET -> READ_RESET -> SET(random V_SET) -> READ_SET
```

Grid-screen values used:

```text
V_RESET: -1.0 V normally; -2.0 V fallback/degraded branch when DCIV SET occurs without RESET
V_READ: +0.1 V
V_SET: 0.20..1.00 V in 0.05 V steps
attempts: 20 per V_SET level for screening
pulse width: 10 ms
pulse compliance: 10 µA
```

If DCIV shows SET without RESET, run exactly five strongest RESET-read fallback pairs, save the read currents, and only continue as explicitly labeled degraded-state data.

### D. Analysis
- Threshold `read_after_set` / `read_after_reset` current distributions; log-Otsu is a valid fallback when reset reliability is imperfect.
- Compute `P(1 | V_SET)` by voltage bin.
- Fit sigmoid/logistic and report `V50`, slope/effective-temperature proxy, fit loss, `Pmin/Pmax` when available.
- Compute binary entropy per voltage bin and report stuck/compliance fractions.
- Do not call a high-current/compliance-limited device a p-bit candidate without voltage-tunable read-state probability.

## Mid-run conversion rule
When switching a grid already in progress to this protocol, stop and cleanup the old runner first; do not mutate a running loop. Start a new run from the interrupted/subsequent device and preserve prior results as previous-protocol artifacts. See `vipsa-grid-measurement/references/midrun-switch-to-literature-pbit-protocol-2026-07-31.md` for the hardware-control and reporter handoff.

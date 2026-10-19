# ViPSA Device Failure Logbook

Purpose: cumulative log of DUT failure modes, suspected causes, prevention/recovery strategies, outcomes, and recurrence tallies. Update this file whenever a new failure mode appears or a known mode recurs with new evidence.

## Recurrence tally

- Post-forming (2,3) SET/RESET repeat: RESET touched 10 mA and left a 1 µA read clamp at ±2 mV, short-like landing retired: 1 (2026-10-02). Lower-stress (2,4) non-repeatable state ordering: 4 bounded studies (initial three-pair sequence, 2026-10-02 −2.5 V/5 mA 15-pair batch, 2026-10-02 −2.75 V/5 mA 15-pair batch, and a +3 V/0.5 mA SET factor batch stopped after 11 pairs plus cycle-12 SET); none is a confirmed hard-short endpoint. Stronger-SET independent-read guard crossing: 1 (2,4 cycle 12, +0.1 V read max 53.256 µA versus 50 µA guard; RESET intentionally withheld). Follow-up low-resistance SET-state health check without low-bias clamp: 1 (2,4; ±0.5/±2 mV at 1 µA compliance fully unclamped, paired resistance 16.63/15.83 kΩ). Gentle RESET-first recovery that lowered resistance without clamp: 1 (2,4; −2 V/1 mA, zero stress-compliance hits, post-read 8.09/8.04 kΩ; unresolved safety hold, not confirmed failure). Parser-only matched-measured-voltage assertion after a complete SET sweep: 1 (2,4); no SET replay, missing RESET completed separately. Parser-only null measured-voltage assertion after a complete RESET plus all post-reads: 1 (2,4); actual response reconciled, no stress replay. Source: `data/pratap_samples/runs/optimization_sub_3/run_plan.json`.

- Recentered interstitial over-contact read clamp before forming: 1 (optimization_sub_3 (2,3), 2026-10-02 UTC).
- Runner sweep-construction fault omitting return branch and producing read-limit site stop: 1 (optimization_sub_3 (1,2), 2026-10-01 UTC).
- Candidate state-direction inversion after stronger RESET endpoint: 1 (optimization_sub_3 (1,2), SET 0.25 mA / RESET −3.5 V, 2026-10-01 UTC).
- Independent +0.1 V SET read near configured 100 µA read ceiling during bounded hysteresis repeat: 1 (optimization_sub_3 (1,2) second repeated SET, 2026-10-01 UTC).
- Interstitial retained SET followed by incomplete independent RESET HRS recovery: 1 (optimization_sub_3 (1,2) manual contact, 2026-10-01 UTC).
- Interstitial forming compliance plateau with transient contact-dependent read then lost coupling: 1 (optimization_sub_3 (2,2), 2026-10-02).
- Interstitial contact-edge read-clamp during bounded approach (possible over-contact/short-like, not proven device failure): 1 (optimization_sub_3 (1,2), 2026-10-01).
- Contact unverified at user-authorized Z ceiling (not classified open/failed): 2 sites (optimization_sub_3 interstitial (1,2) and (3,2), 2026-10-01).
- Mechanical coarse-stage collision / OpenFlexure-axis damage: 1
- Over-reset / negative-branch breakdown-like current surge: 1
- Perma-SET / hard short-like low-bias compliance: 2
- RESET-recovery loss with unclamped conductive read (not proven hard short): 4 (optimization_sub_2 (1,2), (2,8), (2,7), and (2,6))
- RESET-recovery loss with compliance-limited negative branch and conductive low-bias read: 3 (optimization_sub_2 (2,5): after +3 V / 500 µA SET, −2 V / 300 and 500 µA RESET clamped and left ~57.5 µA; (2,4): after two recovered +2 V / 300 µA SET and −2 V / 300 µA RESET cycles, the third RESET clamped at −0.956 V and left ~10.9 µA; (4,8): initial −2 V / 300 µA RESET clamped at measured −1.268 V and left ~6.7 µA at +0.1 V).
- Volatile negative-return conductance / failed 1 s RESET gate after higher-compliance SET: 1 (optimization_sub_2 (1,8); later relaxed to nA)
- Over-contact / mechanical short-like contact: 2
- Open / weak contact / contact edge: 21 (I64 lifted-vs-contact diagnostic; optimization_sub_2 (2,3), (2,2), (2,1) unresolved by Z−80; (3,2) later physically contacted at user-set Z−60; (4,7) ambiguous at Z−85; (4,1) and (5,2) open-like through Z−60, the latter pending manual confirmation; (4,2) was reclassified after user-confirmed physical contact at Z−60 and is no longer counted as unresolved; other sites unresolved)
- No forming transition despite voltage-responsive nA current; contact vs high-HRS unresolved: 2 (including I64 manual-contact compliance ladder)
- No forming transition at bounded ceiling with flat nA stress current / uncertain contact: 2 (I61, I62)
- No-retention after switching-like event: 22 (Device 40, I12, I27, I26, I25, I24, I23, I22, I21, I32, I34, I36, I41, I42, I45, I46, I47, I54, optimization_sub_2 (1,4), (1,6), (3,4) third 150 µA SET, and (4,2) user-confirmed contact +2 V/150 µA SET; contact change remains an alternative in ambiguous cases)
- Unstable RESET initialization / no separated persistent pulse states: 1 (2026-09-15, one resumed campaign; not classified as permanent damage)
- Conditioning non-convergence after clean forming: 17
- Compliance-limited false success / misleading branch feature: 0
- State-read compliance saturation during conditioning: 13 (including I64 +8 V / 75 µA immediate +10 mV read)
- State-read compliance saturation during DC-IV characterization: 1
- DC-IV characterization directionally inverted after initial valid cycle: 1
- Repeat forming-like cycle followed by low-bias read compliance saturation: 2
- Post-forming RESET left low-bias read-compliance saturation: 1
- Unstable forming / intermittent pre-compliance collapse: 9 (including optimization_sub_2 (4,5) transient 100 µA plateau at Z−75 with sub-nA post-reads; (4,4) Z−70 plateau then independent sub-nA reads; (4,3) Z−60 plateau then delayed 2.54 nA at +0.1 V)
- Runner control-flow/parser incident causing post-gate unintended stress: 2 (including optimization_sub_2 (4,7) unintentional replay at Z−85 after interrupted prior sweep).
- Post-retract clearance not independently verifiable before lateral travel: 1 site (optimization_sub_3 (2,4), 2026-10-02; Camera 1 top-down overlap plus overexposed Camera 2 qualitative view).
- Stage coordinate invalidation after stale-run recovery reset: 1 control incident (optimization_sub_3, 2026-10-02); no physical reset motion, but the tracked/persisted coordinate was re-zeroed and is no longer trustworthy. Unexpected direct-control lateral motion while clearance remained unverified: 1 incident.

### 2026-10-02 UTC — optimization_sub_3 control incident: unexpected motion and Stage coordinate invalidation

- Evidence: `data/pratap_samples/runs/optimization_sub_3/control_incident_20261002T0531Z/summary.json` plus Stage/Zaber/light edge logs. A pre-existing direct-control run with no live measurement process found during reconciliation moved Stage Z−50 from the last verified −15.75 to physical-equivalent −65.75 and displaced Zaber from `(364946,838551)` to a later verified `(385181,838486)` despite the unresolved clearance blocker. The direct-control run omitted COMPLETE and left stale control state.
- Classification: **hard control/motion-safety blocker; not a DUT failure**. During stale-run recovery, `puda machine reset stage` cleared the run but the driver explicitly set the current physical Stage location as logical zero without moving it. The Stage now reports `(0,0,0)` while the pre-reset command log places the physical equivalent at old logical Z−65.75. The persisted Stage coordinate is untrusted. A new Camera-1 frame was too dark to assess collision, scratch, apex/pad position, or clearance.
- Immediate safety state: no Stage or Zaber motion and no electrical stress after recognizing the invalidation. Keysight output-off, 707B `open_all`, and light-off commands succeeded. Keithley had been verified off before the unexpected Stage/Zaber/light-only sequence; a fresh command was blocked by split/stale PUDA control. Zaber still retained a stale active run, so full cleanup/control verification is incomplete.
- Operational cause: stale direct-control run without COMPLETE, followed by an inappropriate Stage reset for a run-ID mismatch. Mechanistic DUT cause is not applicable. Prevention: never use Stage `reset` to clear a stale run because it redefines coordinates; complete/abort the exact run or stop for operator reconciliation. Before any lateral motion, require current clearance proof and single-owner runner verification. Recovery outcome: **not attempted**—do not repair the Stage position JSON, move either axis, or resume stress until explicit physical-coordinate and clearance reconciliation.

### 2026-10-02 UTC — optimization_sub_3 (2,4) post-retract clearance blocker

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/handoff_retract_for_next_site_20261002T045817Z/summary.json`, `r2c4/post_retract_clearance_camera1_20261002T045911Z/summary.json`, and `r2c4/post_retract_clearance_camera2_20261002T050806Z/summary.json`. Electrical cleanup and Stage Z−100 retract from +84.25 to −15.75 were verified with Zaber unchanged at `(364946,838551)`. Camera 1 still showed the blunt apex optically overlapping a large pad and could not establish vertical separation. An independent Camera 2 qualitative frame was strongly overexposed and did not resolve the probe apex, substrate surface, or a separation gap.
- Classification: **hard motion-safety blocker: clearance unverified, not a DUT failure**. No lateral motion was commanded. Both SMU output-off commands, 707B open/`nil`, and light-off cleanup were re-verified after the independent capture.
- Prevention/recovery: do not infer a vertical gap from Stage readback or top-down optical overlap, and do not use an overexposed wide view as clearance evidence. Require a suitable exposed side/oblique view or another independent clearance method before any Zaber XY travel. Outcome: blocker persists; no electrical stress and no motion replay.

### 2026-10-02 UTC — optimization_sub_3 (2,4) gentle RESET-first recovery lowered resistance

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/continued_until_failure/reset_first_recovery_m2V_1mA_20261002T044806Z/summary.json`, `RESET_trace.json`, `post_RESET_reads.json`, and `RESET_recovery_semilog.png`. Live preflight verified Stage Z+84.25, Zaber `(364946,838551)`, both SMU output-off commands, and 707B open/`nil`. One isolated 0→−2→0 V RESET at 1 mA completed all 81 points, reached −320.287 µA at measured −1.999958 V, and had zero stress-compliance hits. All five post-RESET batches at 0, ±0.5 mV, and ±2 mV completed at 1 µA compliance with no clamp. Paired resistance was 8.09/8.04 kΩ, lower than the preceding 16.63/15.83 kΩ low-bias state.
- Classification: **unclamped lower-resistance state after gentle RESET; unresolved safety hold, not a confirmed hard short or device-failure endpoint**. The intended RESET moved conductance in the wrong direction. Accumulated electrical stress is the operational context; filament/contact mechanisms remain speculative.
- Parser/control note: the first analyzer asserted because `hold_voltage_measure_current` returned valid commanded voltage and current rows but null `V_meas` fields. The actual successful protocol response was recovered from the saved log, all reads were reconciled, and no RESET or read was replayed. Final output-off, matrix-open/`nil`, unchanged position were verified.
- Prevention/recovery: do not issue another SET or automatically repeat/escalate RESET on this landing. Any future action requires a fresh preflight and explicit justification; retain the current conductive-state safety hold. Recovery outcome: did not recover HRS.

### 2026-10-02 UTC — optimization_sub_3 (2,4) stronger-SET read-guard safety hold

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/continued_until_failure/recipe_e_SET0p5_RESETm2p5_5mA_15pairs/analysis.json`, `manifest.json`, cycle summaries/raw traces, `all_completed_measured_traces.csv`, and `all_completed_sweeps_semilog.png`. At live-verified Stage Z+84.25 and aligned Zaber `(364946,838551)`, the one-factor SET-compliance increase to +3 V/0.5 mA with −2.5 V/5 mA RESET completed 11 full isolated pairs. No full pair met all prospective gates; RESET had zero compliance hits. Cycle 12 SET completed with 96 SET-compliance points and PF/PB@0.2 V 6.21×, but the independent +0.1 V read reached 53.256 µA (delayed median 44.683 µA), exceeding the predeclared 50 µA guard. RESET was intentionally not run; no stress was replayed.
- Classification: **increasingly conductive post-SET state / independent-read safety guard crossing; safety hold, not a confirmed device-failure endpoint**. Operationally, the stronger SET factor did not improve retained ON/OFF ordering and pushed the state near the read ceiling. Accumulated electrical stress is a plausible operational contributor; filament growth, ionic redistribution, or contact contribution remain speculative.
- Prevention/recovery: preserve branch-isolated execution and stop immediately at the read guard. Do not automatically run the missing RESET, repeat SET, move laterally, or call the device failed. The next action must begin with electrical cleanup/position preflight and a separate very-low-bias unclamped health check; only then may a specifically justified low-stress recovery branch be considered. Cleanup after cycle 12 succeeded; hardware position was unchanged.

### 2026-10-02 UTC — optimization_sub_3 (2,4) post-guard low-bias classification

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/continued_until_failure/very_low_bias_health_after_recipe_e_20261002T044016Z/summary.json` and `reads.json`. After a fresh output-off, 707B-open/`nil`, Stage Z+84.25 and Zaber `(364946,838551)` preflight, an independent check measured medians of +33.87/−26.25 nA at ±0.5 mV and +130.49/−122.17 nA at ±2 mV with 1 µA compliance. No sample reached compliance. Paired differential resistances were 16.63 kΩ and 15.83 kΩ. No SET, RESET, forming, or motion was commanded.
- Classification: **low-resistance SET state without very-low-bias read clamp; safety hold, not a confirmed hard short or device-failure endpoint**. The roughly bias-scaled, opposite-sign response supports real conductive coupling. The operational cause is the preceding +3 V/0.5 mA SET plus accumulated cycling; filament/contact mechanisms remain speculative.
- Prevention/recovery: do not issue another SET first or infer the withheld cycle-12 RESET. If recovery is continued, use one isolated reset-first branch below the prior −2.5 V/5 mA condition, followed immediately by independent low-bias reads, and stop on any clamp or cleanup/control ambiguity. Outcome of this invocation: classification only; final output-off and matrix-open/`nil` cleanup and unchanged position verified.

### 2026-10-02 UTC — optimization_sub_3 (2,4) midpoint-RESET batch remained non-repeatable

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/continued_until_failure/recipe_d_SET0p25_RESETm2p75_5mA_15pairs/analysis.json`, `manifest.json`, raw per-cycle `SET_trace.json`/`RESET_trace.json`, and `all_completed_sweeps_semilog.png`. At live-verified Stage Z+84.25 and aligned Zaber `(364946,838551)`, +3 V/0.25 mA SET with the single RESET-voltage change to −2.75 V at 5 mA completed 15/15 isolated pairs. RESET had zero compliance hits. No cycle met all prospective gates together (independent ratio ≥5, PF/PB ≥5, NF/NB ≥2); later cycles frequently had inverted state ordering and elevated conductive pre/post reads, but no low-bias read clamp or ≥50 µA guard event.
- Classification: **non-repeatable retained-state ordering; alive, not a confirmed failure endpoint**. The operational evidence disfavors −2.75 V/5 mA as a repeatable recipe on this landing. Increasing RESET magnitude from −2.5 V improved isolated early negative-branch ratios but did not stabilize independent ON/OFF ordering. Filament stochasticity, ionic redistribution, and contact contribution remain speculative.
- Prevention/recovery: do not replay exact −3 V/5 mA, which previously produced RESET compliance, and do not promote within-sweep hysteresis to endurance qualification. Preserve one-factor changes, isolated-cycle artifacts, 15-pair invocation cap, and low-bias/read-compliance stops. Recovery attempted: midpoint RESET magnitude only; outcome was zero qualified cycles, zero RESET compliance hits, and no confirmed hard failure. Final electrical cleanup and unchanged position were verified separately.

### 2026-10-02 UTC — optimization_sub_3 (2,4) gentler-RESET batch remained non-repeatable

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c4/continued_until_failure/recipe_c_SET0p25_RESETm2p5_5mA_15pairs/analysis.json`, `manifest.json`, raw per-cycle `SET_trace.json`/`RESET_trace.json`, and `all_completed_sweeps_semilog.png`. At verified Stage Z+84.25 and aligned Zaber `(364946,838551)`, +3 V/0.25 mA SET with a one-factor gentler RESET change from −3 V to −2.5 V at 5 mA completed 15/15 isolated pairs. RESET had zero compliance hits. Only cycles 1 and 11 met all prospective gates (independent read ratio ≥5, PF/PB ≥5, NF/NB ≥2), never consecutively; other cycles showed inverted or weak independent state ordering despite frequent positive-branch hysteresis.
- Classification: **non-repeatable retained-state ordering; alive, not a confirmed failure endpoint**. Likely operational cause is an under-optimized RESET endpoint/state variability; a mechanistic explanation (filament stochasticity, ionic redistribution, or contact contribution) remains speculative. Prevention: continue one factor at a time, never call within-sweep hysteresis alone repeatable, and preserve the 15-pair invocation cap. Recovery actually attempted: reducing RESET magnitude eliminated the prior −3 V compliance event but did not produce 10–15 consecutive qualified cycles. Outcome: safer RESET stress, repeatability not recovered; no short-like low-bias clamp and no device retirement.

### 2026-10-02 UTC — optimization_sub_3 (2,3) optical approach / pre-forming over-contact stop

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c3/forming_attempt1_summary.json`, `contact_edge_recovery_summary.json`, and `contact_edge_lift_semilog.png`. At nominal large-pad (2,3), retracted Z+9.25 and tip alignment followed by +85 to Z+94.25 showed optical tip X shift, while the first low-bias read remained sub-nA; this is not proof of electrical open on pristine HRS. After a retracted X recenter of −800 native steps, the +10 mV/1 µA read at Z+94.25 clamped in all five samples before the +10 V/100 µA forming sweep could start. A fresh repeated read still clamped; four guarded Z−0.25 lifts to +93.25 also stayed at 1 µA. No high-voltage forming occurred during this first attempt. A safety retract to Z+9.25 released the current to pA/sub-nA. Keithley and Keysight outputs off; 707B open/`nil`; final Zaber `(370146,838551)` verified.
- Classification: **contact-position-dependent low-bias over-conduction / read-compliance stop**; physical origin (tip-pad bridge, over-contact, site defect, or leakage) is not resolved. Do not identify pA pristine-HRS absence as failure on its own, but do not apply forming into a 10 mV clamp. Prevention: at re-centered pads, advance from clearance using *small optical/electrical increments* rather than assuming +85 is a safe high-resolution landing; verify same-pad apex motion and an unclamped low-bias state before stress. Recovery actually tried: 1-step guarded lift ineffective; full retract released current. No repeat forming at the clamped Z+94.25 landing. Follow-up after the user's pristine-HRS correction: at optically centered Z+89.25 (5 steps below clamped landing), low-bias reads were sub-nA and unclamped; one 0→+10→0 V/100 µA forming sweep completed (377/401 compliance hits), with ~45,845× PF/PB at matched measured +0.1 V and an independent unclamped +0.1 V post-read of 4.610 µA. This supports an approach-position-dependent electrical transition; it does not identify the cause of the upper landing's clamp or demonstrate RESET.

### 2026-10-01 UTC — optimization_sub_3 (1,2) incomplete SET list / short-like read state

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r1c2/manual_contact_measurements_20261001T172406Z/hysteresis_0p5mA_repeat3/summary.json`. The fresh three-cycle 0.5 mA/+3 V, −3 V/10 mA repeat runner had a sweep-list construction bug: `range(steps-1,-1)` was empty, so its first SET transaction actually applied only 61 points `0→+3 V` at 0.5 mA, not `0→+3→0`. The parser raised `StopIteration` while scoring the nonexistent return branch; no RESET or further cycle was executed. The actual 100 +0.1 V post-SET reads were pinned at the 100 µA read limit. Confirmatory ±2 mV reads were ±0.47 µA, and ±5 mV reads reached the 1 µA diagnostic limit. Stage/Zaber remained unchanged; both SMUs off and matrix open/`nil` verified.
- Classification: **short-like/read-compliance-limited site stop**, not a completed hysteresis cycle and not proof of microscopic permanent damage. Immediate operational cause is the omitted return branch, but whether it caused the conductive state or accumulated earlier stresses did is unknown. Corrected the list builder to include a descending `range(steps-1,-1,-1)` but will not replay on this site. Prevention: pre-launch assert exact 121-point path and branch order before ANY source-voltage command, validate read guard even when analysis fails, and retire the site on read clamp. No recovery stress was attempted.

### 2026-10-01 UTC — optimization_sub_3 (1,2) four-candidate bounded screen

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r1c2/manual_contact_measurements_20261001T172406Z/candidate_screen_after_high_SET/campaign_summary.json`; one RESET-only recovery from SET-like +0.1 V 32.3 µA to 29.0 nA without RESET stress clamp. Four one-pair candidates were screened at fixed manual contact Z+109.25: SET compliance 0.5/0.25/0.25/0.75 mA, RESET endpoint −3/−3/−3.5/−3 V at 10 mA; independent delayed +0.1 V read ratios were 2.31/4.87/0.085/0.943, respectively. All read currents remained below 50 µA guard, RESET branches did not hit 10 mA stress compliance; none achieved safe repeatable ≥5× separation with ≤20 nA HRS. The −3.5 V branch yielded *higher* read after nominal RESET than after SET (1.80 µA vs 0.152 µA), direction inverted.
- Classification: candidate screen without a qualified winner. Within-sweep loops do not substitute for identical-bias retained states. Operational cumulative stress/order is a confounder; no microscopic cause inferred. Prevention: preserve ordering and independent reads, re-test promising recipes on held-out pads, do not label an inverted recipe successful. No recovery/stress escalation attempted after four candidates; outputs off, matrix nil, light off verified. No until-failure cycling or other-device motion occurred.

### 2026-10-01 UTC — optimization_sub_3 (1,2) hysteresis repeat near-read-limit stop

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r1c2/manual_contact_measurements_20261001T172406Z/hysteresis_repeats_3/summary.json`. User asked for a few repeat SET/RESET cycles despite incomplete absolute HRS recovery, as bounded hysteresis characterization rather than qualified endurance. One additional +3 V/1 mA SET and −3 V/10 mA RESET pair completed with independent +0.1 V delayed read medians 30.678 µA vs 3.422 µA (~8.96×), RESET stress max 2.360 mA, no RESET stress clamp. In second pair, SET completed but +0.1 V read max 73.966 µA exceeded the declared 50 µA near-read-limit stop (100 µA compliance); RESET was not run. Original HRS ≤20 nA gate remains unmet.
- Classification: reproducible directional within-sweep hysteresis and independent partial read contrast, with increasingly conductive SET read and risk of read clamp; not a qualified endurance result. Operational cause may be accumulated electrical stress; filament/chemical cause remains speculative.
- Prevention/recovery: retain the per-branch, per-read guard, record incomplete pair distinctly, and do not automatically apply more stress or move the manually contacted probe. Both SMU outputs off, 707B open/`nil`, Stage Z+109.25 verified. Recovery not attempted; no further stress authorized by this bounded repeat plan.

### 2026-10-01 UTC — optimization_sub_3 (1,2) manual contact: retained SET, incomplete RESET recovery

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r1c2/manual_contact_measurements_20261001T172406Z/summary.json`; manually established Stage Z+109.25, verified native XY (375546,843981). Pre-stress ±10 mV current ~±10 nA unclamped. One +10 V/100 µA forming sweep clamped for 381/401 points; delayed independent +0.1 V ~13.4 nA. One +3 V/1 mA SET yielded 100 independent +0.1 V reads, last 11.93 µA, no near-read-clamp. One −3 V/10 mA RESET did not clamp in stress, but independent +0.1 V read remained ~3.894 µA, above 20 nA HRS ceiling. Delayed SET vs post-RESET read ratio ~5.26 is *not* sufficient qualification because absolute HRS recovery failed.
- Classification: incomplete RESET recovery; not a qualified full cycle, no candidate arms or endurance. No automatic more-negative RESET or stress retries. Both SMUs off, 707B open/`nil`, light off; manual contact Z left unchanged. Raw acquisition-order traces and combined semilog plot saved under that site folder.

### 2026-10-02 — optimization_sub_3 (2,2) transient forming response / lost contact coupling

- Evidence: `data/pratap_samples/runs/optimization_sub_3/r2c2/summary.json` and saved 401-row forming trace/semilog. After requested Z−100 travel and +85 preapproach, +10 mV was ~0.08 nA at Z+101.25. One 0→+10→0 V, 100 µA forming-as-contact sweep hit compliance on 364/401 samples; measured voltage at commanded +10 V was only 0.429 V. Immediate independent +0.1/+0.2 V post-reads were 6.0/24.5 µA (unclamped). Later ±10 mV were ~±8 nA; Z−5 reduced +10 mV to ~0.11 nA, but returning to the same +101.25 Z did not restore coupling (~0.012 nA). Twenty low-bias-only Z+0.25 steps to +106.25 stayed pA/sub-nA.
- Classification: one completed forming check with compliance plateau and **non-sustained contact-dependent coupling**, not qualified SET or stable contact. Mechanical contact drift/relaxation is plausible operationally; filament physics or pad failure is unproven. Do not treat compliance as a contact marker or repeat the same sweep at Z+101.25. No optimization or endurance performed.
- Prevention/recovery: fresh low-bias paired checks, guarded lift/return reference, no replay after uncertain/lost coupling, bound fine rescue and then stop/retract. The actual recovery failed to restore contact; Stage Z−100 to +6.25 at (2,2), both outputs off, 707B open/`nil`, light off verified. Recurrence category initialized at one; revisit only with a newly approved absolute Z ceiling and fresh apex/pad verification.

### 2026-10-01 — optimization_sub_3 (1,2) sharp contact edge and read clamp on retry

- Evidence/artifacts: `data/pratap_samples/runs/optimization_sub_3/r1c2/retry_z180/summary.json`, `approach/low_bias_Z120.json`, `fine_edge/fine_summary.json`, `verification/paired_low_bias_Z116p25.json`, and Camera 1 frames. At +10 mV, Z+116 was ~0.068 nA median, Z+116.5 gave three ~319–321 nA reads. At Z+120 both ±10 mV reads pinned at ±1 µA (read compliance). The safety trim to Z+115 returned pA/sub-nA; subsequent fine approach and Z−0.25 trim left Z+116.25 with five unclamped +10 mV reads, median 284 nA. At that fixed Z, paired ±2 and ±5 mV currents tracked polarity (~±66 and ±170 nA), zero-bias median ~0.9 nA. Apex remained on the intended large pad with no gross damage visible, but Camera 1 cannot prove contact force.
- Immediate classification: strong contact-like Z-dependent coupling at +116.25; +120 read clamp is a short-like/over-contact safety event, not a resistance value. The +116.25 conductance is unusually high for pristine HRS and device health is unqualified. Operational cause plausibly abrupt mechanical contact edge or pre-existing conductive pad; filament mechanism unproven without any forming/SET/RESET.
- Prevention: stop forward motion on read clamp; bracket with small guarded Z steps and do not infer a safe stress recipe from low-bias contact alone. Recovery actually performed: Z−5 to +115, bounded +0.5 steps to +116.5, Z−0.25 trim to +116.25. Keithley and Keysight outputs off, light off, 707B open/`nil`, positions verified. No forming or optimization sweep. Outcome: stable unclamped contact-like low-bias read but possible short-like DUT; no device-failure yield assignment. Tally for this contact-edge read-clamp category initialized at 1; confirmed over-contact category unchanged.

### 2026-10-01 — optimization_sub_3 interstitial contact unverified at Z+100

- Failure mode: contact/path identifiability under a hard motion ceiling, **not** demonstrated DUT failure. Artifacts: `data/pratap_samples/runs/optimization_sub_3/r1c2/approach/`, `r3c2/approach/`, `run_plan.json`, and `stop_retract_verify.log`.
- Evidence: at each site, Stage advanced from Z−50 through bounded readback-verified points only to Z+100; ±10/±50 mV Keithley reads at 1 µA compliance never clamped. At Z+100, the ±50 mV differential was 1.239 nA at (1,2) and 0.897 nA at (3,2). Z-dependent sub-nA conductance and Camera 1 overlap did not distinguish pristine high-HRS contact from leakage or absent contact; no positive apex slide was confirmed. Nearby historically tested D1/D2 recorded forming contact near Z+170/+155, but such heights cannot override the user's +100 ceiling.
- Operational cause: ceiling may be below physical landing height, or low-bias response may be genuine high-HRS; probe/cable leakage remains an alternative. Filament/material mechanism is speculative and **not** established because no forming/SET/RESET occurred.
- Prevention: do not promote a single current threshold to physical contact proof; use a matched lifted/routed reference and optical apex motion if continuing. Do not consume further sites with repetitive no-contact forming checks.
- Recovery: no stress applied; Stage retracted to Z−50 at (3,2), both outputs off, light off, 707B open/`nil`, verified. Outcome: campaign paused at contact gate; no device-failure yield inference. Tally for *contact unverified under hard Z cap* initialized at 2; existing open/weak-contact tally unchanged.

### 2026-10-01 — optimization_sub_2 (4,8) failed initial RESET and (4,7) interrupted contact check

- (4,8) failure mode: compliance-limited initial RESET with conductive low-bias read; not a proven permanent short. Artifacts: `data/pratap_samples/runs/optimization_sub_2/r4c8/summary.json` and eight-sweep semilog plot. At aligned XY (345791,824208), contact-like Z−90, +0.1 V read 25.1 µA after forming. −2 V / 300 µA RESET measured −1.268 V at the commanded endpoint and ten +0.1 V reads remained ~6–7 µA. Operational cause could be a strongly conductive filament or contact configuration; mechanism speculative. Prevention: no SET/conditioning when independent RESET fails. Recovery: outputs off, matrix `nil`, Z−100 retraction to −190, all verified; no further stress.
- (4,7) failure mode: control-plane timeout during sixth forming command at Z−85, followed by ambiguous sub-nA contact. Artifacts: `data/pratap_samples/runs/optimization_sub_2/r4c7/summary.json`, six completed-sweep plot, and recovery logs. The interrupted sweep's stress history is unknown and excluded from the six verified traces. The associated PUDA run held both 2450 and 707B active; fresh direct queue commands in the exact active run returned successful SMU output-off, `open_all`, and `get_closed_channels: nil`, followed by lifecycle completion and fresh full protocol verification. Ten +0.1 V reads at Z−85 had median ~0.65 nA. An agent error then reran forming at the same Z−85 despite stating it would skip that uncertain stress: four compliance hits, but post-read stayed sub-nA, so the site was stopped as ambiguous. Operational cause of the timeout was a transient NATS response failure; physical contact vs high HRS remains unresolved. Prevention: after an interrupted stress, use a low-bias-only probe and do not call a gate whose first iteration repeats the uncertain Z; require a dedicated skip-first mechanism or retire. Recovery: outputs off, matrix `nil`, light off and Z−100 retract to −185 verified. No SET/RESET or endurance.
- (4,5) failure mode: transient compliance-limited forming without persistent low-bias coupling. Artifacts: `data/pratap_samples/runs/optimization_sub_2/r4c5/summary.json` and seven-sweep semilog plot. Same intact nominal pad aligned at (360791,824308); first six 100 µA forming checks Z−105..−80 stayed open-like. At Z−75, 26 compliance hits occurred across commanded +4.65..+5.95 V but the +10 V endpoint measured only 42.4 nA and post-forming +0.1/+0.2 V reads remained ~0.5–0.7 nA. Cause unresolved: volatile electronic event vs contact edge; filament mechanism speculative. Prevention: no SET on isolated compliance plateau without retained reads. Recovery: no extra stress, outputs off, matrix `nil`, light off, relative Z−100 to −175 verified. Outcome: retired; no recipe/endurance.
- (4,4) recurrence: aligned (366441,824658), Z−70 forming hit 100 µA compliance but ten independent +0.1 V and three +0.2 V reads relaxed to sub-nA. Operational contact edge/electronic volatility both possible; mechanism unproven. No SET/RESET; retired Z−170, outputs off, matrix nil. Six-sweep plot and summary in `data/pratap_samples/runs/optimization_sub_2/r4c4/`.
- (4,3) recurrence: aligned (371441,824658), six open-like sweeps Z−90..−65, then 346 compliance hits at Z−60. Immediate +0.1/+0.2 V ~1.71/1.60 µA, delayed independent medians 2.54/13.57 nA. Transient response, not retained LRS; no SET/RESET. Stop at established Z−60 ceiling; retracted to Z−160 with outputs off/matrix nil. Seven-sweep plot and summary in `data/pratap_samples/runs/optimization_sub_2/r4c3/`.
- (4,2) and (4,1) initially open-like: each visually aligned to an intact nominal pad and tested with five +10 V / 100 µA forming checks from Z−80 to Z−60. Neither initially showed compliance or low-bias coupling. The user later physically confirmed (4,2) contact at live Z−60; the earlier automatic open-like label is signal-only, not a physical-contact verdict, and (4,2) was removed from the unresolved contact tally. The separate +2 V / 150 µA SET sweep reached stress compliance with measured voltage collapsed to 0.398 V at the commanded apex. Immediate +0.1 V reads ~8.3 µA; 100-read median 6.17 µA but six reads <100 nA; delayed +0.1/+0.2 V medians 0.71/0.91 nA. Failed retention, so RESET and endurance were withheld. Operational cause of loss could be unstable filament or mechanical contact edge; mechanism unresolved. Prevention: require independent delayed same-bias retention, not compliance/early median alone. Recovery: outputs off, matrix nil, light off, retracted Z−100 to −160, verified. Retest: `data/pratap_samples/runs/optimization_sub_2/r4c2/manual_contact_retest_20261001/summary.json`; all-six-sweep semilog and scatter retention plots in same device directory. (4,1) remains open-like at ceiling with no user contact confirmation. Tally open/contact edge 19→21 then reclassification 21→20; no-retention +1, 21→22.
- (5,2) open-like/contact-height ambiguity: aligned to intact pad (376391,819708). Five forming-as-approach checks Z−80..−60 each delivered full +10 V with ~5–6 nA endpoint, zero 100 µA compliance hits and sub-nA +0.1/+0.2 V reads. Camera1 apex overlies pad interior but cannot prove vertical contact. Operational cause may be height difference from row 4; intrinsic high-HRS remains possible. No blind deeper Z or SET/RESET. Light and both SMU outputs off, 707B open/nil; stage intentionally held at Z−60 awaiting manual physical contact confirmation. Summary/plot/camera in `data/pratap_samples/runs/optimization_sub_2/r5c2/`. Tally open/contact edge +1, 20→21; reclassify if user confirms physical contact.

## Entry template

```markdown
### YYYY-MM-DD — short failure label

- Failure-mode label:
- Artifact paths:
- Context:
- Evidence:
- Immediate classification:
- Anecdotal / operational cause:
- Speculative mechanistic cause:
- Prevention strategy:
- Recovery strategy:
- Outcome:
- Tally update:
```

---

## Entries

### 2026-09-29 — I64 +3 V screen interrupted by 707B device disconnect

- Failure mode: 707B routing/control lost (`Errno 19 No such device`) after the 200 µA SET sweep and immediate low-bias read, before its 20 s read. 707B channel state could not be verified; no RESET performed.
- Evidence/artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I64/3v_set_reset_20260929T0734Z/summary.json` plus eight SET CSV/raw files and measured-order PNG/SVG. At Z+35.5 and unchanged XY, +3 V sweeps at 10–150 µA all failed 20 s retention; 50 µA had 442.3→0.497 nA and 100 µA 16.25→0.448 nA immediate→20 s at +10 mV. The 200 µA SET branch peak 200.159 µA/102.02 µJ and immediate read 347.64 nA; delayed retention unknown. No RESET or ≥300 µA steps. Keithley output-off succeeded with `set_output(enabled=False)` on separate direct check; switch `open_all` and `get_closed_channels` both failed repeatedly, so electrical routing remains unknown.
- Operational cause: switch device path disconnected or driver/serial transport lost; filament mechanism cannot be inferred from this control failure. Stop all stress, restore 707B physically/driver-side and require explicit `open_all` success plus `get_closed_channels == nil` before resuming from the first missing operation (never replay completed SET sweeps). No stage motion or retract. Outcome: 707B recovery not yet achieved; safety verification incomplete. Shared helper `pratap_device1_forming_contact_gate.cleanup` corrected to reject `None` closed-channel results after command error (previously a false-positive matrix-open flag).

### 2026-09-29 — I64 +8 V compliance ladder: 50 µA transient, 75 µA read clamp

- Failure mode: false minimum-stable-filament candidate at 50 µA due to short-lived conductance; immediate read-compliance saturation at 75 µA, with stability untestable at that tier.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I64/8v_compliance_20260929T0720Z/summary.json`, 30 CSV/raw JSON pairs, `I64_8v_set_lines.{png,svg}`, `I64_50ua_100reads_scatter.{png,svg}`.
- Evidence: at user-established Z+35.5, fixed +8 V 0→endpoint→0 sweeps reached SET limits 10/20/30/50/75 µA, with 18.94/32.68/45.99/72.92/125.38 µJ branch energies. Same fixed +10 mV/1 µA read range showed 10–30 µA 20 s medians ≤0.345 nA. The 50 µA tier gave 118.36 nA immediately and 77.40 nA at 20 s, but 100 subsequent reads without RESET fell to ~2–3 nA in first 60 and <1.2 nA by last 40, failing the 5 nA gate. The 75 µA SET branch had 299 compliance-hit points; all three immediate +10 mV reads were pinned ~1 µA with measured read voltage unavailable. No delayed 75 µA read, RESET, or 100–1000 µA escalation was authorized by the safety gate.
- Immediate classification: transient 50 µA state; 75 µA short-like/read-clamped **censored** state, not a confirmed stable filament or resistance value. Operational cause may be cumulative stress/contact edge at fixed Z; filament kinetics speculative. Prevention: 100-read verification before minimum-compliance claim and hard low-bias clamp stop. Recovery attempted: electrical output-off/707B-open cleanup, no further stress; final Z+35.5/XY unchanged, independently read back. Outcome: minimum stable compliance not established. State-read-saturation tally 12→13; do not count as confirmed stable/no-retention device again.

### 2026-09-29 — I64 +8 V event after Z+5; RESET did not recover HRS

- Failure mode: a transient/partially retained conductive state after voltage escalation, followed by incomplete or wrong-direction RESET; not proven stable filament.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I64/voltage_forming_20260929T0624Z/summary.json`, timed SET/RESET CSV/raw JSON, `delayed_postreset_read.json`, and ordered-line PNG/SVG. No lateral motion.
- Evidence: first Z+30.5 pass +3/+4/+6/+8/+10 V at 100 µA stayed 2.63–6.47 nA peak with no retained read. After user-authorized one +5 Z and readback to Z+35.5, +3/+4/+6 V sweeps reached 100 µA but 20 s +10 mV reads fell to ~0.16–0.26 nA. +8 V SET reached 100 µA at 299 points (153.33 µJ), and +10 mV current went from 0.510 nA pre to 808.1 nA immediate, 37.14 nA at 20 s. Single −2 V/1 mA RESET delivered peak 576.3 µA (193.12 µJ) but +10 mV read was 251.5 nA afterward, later 89.23 nA; no return to baseline HRS. +10 V was not applied on the second pass.
- Immediate classification: strong voltage/contact-sensitive SET-like event with rapid relaxation; RESET not validated. Operational alternatives: +5 Z improved coupling, cumulative stress changed the device, or contact/read-path effects. Speculative filament/ionic mechanisms cannot be uniquely assigned.
- Prevention: do not infer minimum compliance from a single cumulative site, monitor 20 s and longer fixed-bias retention, preserve measured rather than commanded voltage on compliance plateaus, stop voltage escalation on candidate. Recovery attempted: one bounded RESET; failed to restore HRS. Outcome: Keithley off, 707B open/`nil`; stage deliberately left Z+35.5 at unchanged XY, independently verified. Same I64 device, so no additional device-level no-retention tally; record RESET-incomplete recurrence qualitatively pending replication.

### 2026-09-29 — I64 manual-contact ascending compliance did not produce retained conduction

- Failure-mode label: no forming/retained-state response through a commanded 1 mA SET compliance ceiling; not evidence that 1 mA was delivered.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I64/manual_contact_compliance_20260929T0611Z/summary.json`, 29 raw read/sweep JSON and CSV pairs, `I64_compliance_ladder_lines.{png,svg}`.
- Evidence: operator manually established physical contact at tracked Z+30.5 and Zaber `(358223,818894)`; no mechanical commands. Seven +2 V, 50 mV-step SET sweeps at 125/150/200/300/500/750/1000 µA programmed limits yielded only 9.86–23.82 nA peak measured currents and zero compliance hits; all measured voltage endpoints reached ~2 V. Same-tier +10 mV pre/immediate/20 s delayed medians stayed ~5–7 nA with no retained separation. No RESET between tiers, no 100-read retention block because no initial candidate. Shared SET/read compliance used; all low-bias reads remained below the 0.9 µA software stop. Sweep energy per branch ~0.0077–0.0082 µJ, far below 0.5 mJ guard.
- Immediate classification: minimum stable-filament compliance is not identifiable on I64; commanded current limit is not actual delivered current. Operational explanations include weak electrical coupling despite manual physical contact or instrument range/offset artifacts (fixed current range changed with tier). A truly high-HRS contact or volatile microscopic filament is speculative.
- Prevention: preserve manual physical-contact provenance, quantify actual measured current and fixed-range read baselines, avoid claiming a 1 mA filament or escalating beyond ceiling. Recovery attempted: bounded seven-tier electrical screen, no stable state. Outcome: independent Keithley output-off and 707B open/`nil` check; stage unchanged at Z+30.5 and XY. No motion or retract. Tally no-forming-with-nA-response 1→2; do not increment confirmed no-retention/short tally.

### 2026-09-29 — I64 reapproach: higher-compliance ladder withheld for unqualified coupling

- Failure-mode label: weak/offset-like electrical response at previously formed I64; contact versus high-HRS unresolved, not proven device damage.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I64/compliance_ladder_20260929T0557Z/summary.json`, raw five-bias lifted and approached reads, 13 +10 mV approach reads; Camera-1 `I64/pre_escalation_lit_20260929T0557Z.jpg`.
- Evidence: visible tip projects over pad. At unchanged Zaber `(358223,818894)`, after verified electrical cleanup, stage approached from −84.5 through −34.5 to prior tested +30.5, with no Z overshoot. Routed lifted ±50 mV median difference was −0.0755 nA; approached ±50 mV difference +0.00256 nA, a change of only +0.0780 nA against a conservative 0.526 nA noise/offset gate. Approached +50/−50 mV medians were both positive (~0.069/0.067 nA); no credible polarity-dependent coupling. Zero higher-compliance tiers executed; 1 mA is an upper ceiling, not delivered stress.
- Immediate classification: weak/non-identifiable electrical contact at I64. Anecdotal operational cause could be changed probe contact on reapproach or measurement-path offset; high-HRS/ionic relaxation is speculative and cannot be separated without stronger controls.
- Prevention: matched routed-probe-lifted reference, no current escalation based on optical overlap or prior 100 µA compliance plateau. Recovery attempted: bounded reapproach to earlier +30.5 only; coupling did not qualify. Outcome: Keithley output off, 707B open/`nil`, light-off command, stage retracted to −84.5 with unchanged XY, independently read back. Tally open/weak contact 13→14; no new proven no-retention occurrence.

### 2026-09-29 — I63 manual-contact exploratory screen, no qualified retention

- Failure-mode label: recurring offset-dominated low-bias reads after bounded SET/RESET; not proof of probe lift, damage, or retained switching.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I63/manual_contact_opt02/summary.json`, 19 raw JSON/CSV pairs (13 read batches and six sweep branches), `exploratory_scatter_semilog.{png,svg}`.
- Evidence: operator confirmed physical contact at Z+40.5, Zaber `(363223,818894)`; previous paired-bias marker was offset dominated. Fresh +10 mV read 0.744 nA, unclamped. C/B/A SET/RESET sweeps completed with 100 µA SET and 1 mA/300 µA/100 µA RESET compliance, respectively; all six integrated energies <0.5 mJ. Delayed SET/post-RESET +10 mV medians C 0.484/0.324 nA, B 0.512/0.677 nA, A 0.502/0.441 nA, all unclamped. B inverted, C/A weak contrasts at offset scale. No reliable retained direction, baseline escalation, or endurance.
- Immediate classification: exploratory hardware-safe execution, **electrical coupling unqualified** despite manual physical-contact confirmation; no recipe optimized. Operational alternatives include read-path offset, weak electrical coupling, or transient state; speculative ionic/filament relaxation unproven.
- Prevention: allow explicit manual override of contact-marker *only* for bounded screen; keep read-compliance and measured branch-energy hard stops, preserve raw times and same-bias delayed reads, never rank offset-scale ratios.
- Recovery: no mechanical motion permitted; no further stress attempted. Outcome: direct Keithley output-off and 707B open/`nil` verified, Z+40.5 and XY unchanged. Tally unchanged (same I63 weak/contact-edge occurrence, no-retention not identifiable).


### 2026-09-29 — I63 fixed-contact offset-dominated read after prior forming

- Failure mode: weak/non-identifiable electrical coupling after earlier forming; **not** proof of probe lift or damaged DUT.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I63/manual_contact_opt01/summary.json`, ten raw read CSV/JSON batches and `paired_bias_scatter_semilog.{png,svg}`.
- Evidence: operator-established Z+40.5, Zaber `(363223,818894)`, unchanged throughout. Two independent 0/±10/±50 mV batches at 1 µA compliance gave paired +10/−10 mV differences −0.320/−0.329 nA, ±50 mV −0.022/+0.096 nA, against zero-bias +0.852/+0.514 nA. None of 30 samples clamped. The earlier Z+35.5 forming produced immediate +10/+50 mV 120.615/295.210 nA, but that earlier transient does not prove retention at the new contact.
- Classification: same-sign/offset-dominated signal, no qualified retained ON/OFF or recipe; contact versus post-form relaxation unresolved. Operational possibilities: changed contact mechanics or drifting SMU/path offset. Speculative mechanism: volatile filament relaxation, unproven.
- Prevention: repeat independent paired-bias reads before stress, distinguish fixed-contact offset from bias-responsive conduction, never rank transient ratios. Recovery: no stage/Zaber motion authorized; C/B/A and stronger Pratap tier deliberately withheld rather than increasing electrical stress. Outcome: Keithley output-off, 707B open/`nil` directly verified after both batches; Z+40.5 contact intentionally preserved. Weak/contact-edge recurrence 12→13; no-retention tally unchanged because contact dependence is not identified.


### 2026-09-29 — I62 no forming transition at bounded approach ceiling

- Failure-mode label: flat low-nA stress response without forming; physical contact versus very high HRS unresolved.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I62/run_summary.json`, 16 timestamped forming CSV/raw JSON sweeps, `forming_scatter_semilog.{png,svg}` and `trajectory_scatter_semilog.{png,svg}`. Nominal XY `(368223,818894)`, visible Camera-1 apex (~750,675 px) on pad (~745,670 px).
- Evidence: sixteen +2 V/100 µA forming-as-approach trials from Z−34.5 through Z+40.5 (+5 steps), flat peak 2.22–2.51 nA, pA/noise-like +10 mV pre-reads, no sustained compliance or clean transition. Summed estimated branch energy 2.156e−8 J. No RESET, multi-recipe, or endurance.
- Immediate classification: contact uncertain/no forming at declared ceiling, not proven DUT damage. Operational cause: no credible electrical coupling or very-high-HRS state; speculative mechanism: insulating film/contact geometry, unproven.
- Prevention: do not infer contact from optical overlap or pA alone; preserve bounded ceiling and use matched electrical-contact controls on future sites. Recovery: additional Z/stress at I62 deliberately withheld; not attempted.
- Outcome: independent direct Keithley output-off command, 707B open/`nil`, lamp off, stage Z−84.5 and unchanged nominal XY verified; no runner. Tally distinct flat-current/no-forming mode 1→2.

### 2026-09-29 — I61 no forming transition at bounded approach ceiling

- Failure-mode label: no forming event with flat low-nA stress current; physical contact versus pristine HRS unresolved.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I61/run_summary.json`, 16 forming CSV/raw JSON sweeps, and `forming_scatter_semilog.{png,svg}`. Nominal `(373223,818894)` optically judged apex over target pad, residual approximately (−2,−9) px.
- Evidence: sixteen +2 V/100 µA forming-as-approach trials from Z−34.5 to Z+40.5 in +5 increments. Peak current stayed 2.28–2.46 nA with no compliance hits or clean forming transition, while +10 mV pre-read remained pA/noise-like. Total estimated branch energy 2.146e−8 J. No RESET, recipe, or endurance run was justified.
- Operational cause: no credible electrical contact/coupling at the declared Z ceiling, or exceptionally high-HRS device; not a proven damaged DUT. Speculative mechanism: insulating film or contact geometry. Prevention: preserve optical-versus-electrical distinction and bounded ceiling; use paired-bias and/or probe-lifted controls before interpreting pA signals. Recovery: withheld additional Z/stress beyond ceiling; not attempted. Outcome: output off, 707B open/`nil`, lights off, stage retracted Z−84.5 at `(373223,818894)` and no runner, directly verified. Tally for this distinct no-forming/flat-current mode 0→1.

### 2026-09-29 — I56 re-approach lacked credible paired-bias contact

- Failure-mode label: weak/offset-dominated electrical coupling on revisit; no proven mechanical separation or irreversible device failure.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I56/recipe_B_repeats_20260929T014723Z/summary.json` and eleven per-Z five-bias raw batches. Prior C/B traces: `I56/multi_recipe01/`.
- Evidence: exact aligned XY `(347987,823808)` retained. After verified Z−84.5 preflight and guarded preapproach to −34.5, 0/±10/±50 mV reads at 1 µA compliance were acquired every +5 Z step through the previous contact limit +15.5. At +15.5, paired ±50 mV difference 0.199 nA, ±10 mV difference 0.102 nA, zero-bias 0.458 nA: same-sign, offset-dominated; none of eleven Z levels met the preregistered paired-coupling marker. No read clamp. The earlier single B trial's delayed/post-RESET 7.97× remains unreplicated, not discredited by a matched repeat because neither repeat was electrically eligible.
- Immediate classification: two recipe-B repeats **censored before stress** due to no credible coupling. Operational causes include probe contact change, altered device baseline, or read-path offset; speculative ionic relaxation cannot be distinguished. Avoid blind advance beyond previously contacted Z+15.5 or stronger electrical stress. Recovery attempted: bounded +5 Z step approach, failed to restore marker. Outcome: no new SET/RESET branches; fresh independent direct readback confirmed Keithley output-off command, 707B open/`nil`, light-off command, final Z−84.5 at unchanged XY. Tally weak/contact-edge 11→12; no-retention tally unchanged.

### 2026-09-29 — I54 formed; short-lived post-form conductance and inverted C/B reads

- Failure-mode label: no reproducible retained SET→RESET contrast; possible relaxation or contact/read-path offset, not a proven permanently failed DUT.
- Artifacts: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I54/` and `plots/I54_semilog_all_attempts.{png,svg}`. Thirteen forming sweeps and C/B paired branch/read CSV/JSON preserved; A not attempted after bounded time-budget stop.
- Evidence: nominal `(358223,823894)` optically accepted with probe over pad. Clean +2 V/100 µA forming on attempt 13 at Z+25.5; post-form +10/+50 mV medians 53.223/247.833 nA, both unclamped. Before C, +10 mV had relaxed to 0.597 nA; C pre/immediate/delayed SET/post-RESET medians = 0.597/0.136/0.466/0.771 nA. B = 0.533/0.317/0.362/0.732 nA. Delayed/post-RESET apparent ratios 0.61 and 0.49 (wrong direction/offset range), unqualified; no valid RESET recovery, baseline improvement or endurance claim.
- Operational cause unresolved: rapid post-form relaxation or changed contact/read offset. Ionic/volatile conduction is speculative. Prevention: matched fixed-bias delayed reads and repeated anchor, not forming current as qualification. Recovery attempted: two bounded same-site C/B recipes, neither retained. Stronger baseline-centered stress withheld because stable coupled read was absent. Outcome: output off, 707B open/`nil`, lamp off, stage Z−84.5, XY `(358223,823894)` directly verified and no runner. Tally no-retention 17→18.

### 2026-09-29 — I52 formed; +50 mV state read saturated at 1 µA

- Failure-mode label: post-forming read-compliance safety stop, not a validated SET/RESET cycle or proven permanent short.
- Artifacts: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I52/` (`forming_summary.json`, 16 forming CSV/raw JSON pairs, post-form read JSON, `all_attempts_semilog.{png,svg}`, `final_hardware_after_run.json`).
- Context/evidence: after user-confirmed route clearance, nominal `(368223,823894)` aligned to `(368352,823658)`. Bounded +2 V/100 µA forming reached clean sustained compliance on attempt 16 at stage Z+40.5, first sustained point at commanded +1.50 V; 42 points were compliance-limited on this sweep. Post-form +10 mV median `259.663 nA` was not clamped; +50 mV median `999.9937 nA` was pinned at the configured 1 µA read compliance. No RESET, C/B/A, stronger baseline-centered recipes, or endurance was attempted on I52.
- Immediate classification: low-bias read saturation makes resistance/retention ranking invalid. Operational cause could be strong contact or high conductance after forming; speculative filament/short mechanism is unproven by this one read. No evidence of a complete switching pair.
- Prevention: keep the fixed read-compliance site stop; do not increase read limit or RESET stress on this site. Recovery attempted: none; further stress withheld, with next fresh candidate only after a separately checked safe travel route. Outcome: output off, matrix open/`nil`, lamp off, stage retracted to Z−84.5 and aligned XY `(368352,823658)` by fresh direct preflight; no runner. Tally state-read compliance saturation 11→12.

### 2026-09-29 — I47 formed but B immediate SET current did not retain

- Failure-mode label: no retained state separation after switching-like branch; contact/offset remains an alternative, not proven permanent DUT damage.
- Artifacts: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I47/` (forming summary, nine sweep CSV/raw JSON pairs, `multi_recipe01` C/B/A branch CSV/raw/read JSON, `all_attempts_semilog.{png,svg}`, final hardware JSON).
- Evidence: bounded attempt 9 at Z+5.5 first sustained ~100 µA SET compliance near +1.25 V; immediate +10/+50 mV medians 1.398/0.765 nA, unclamped. C/B/A sequentially completed with fixed +10 mV pre/immediate/delayed SET/post-RESET medians in nA: C 0.337/0.215/0.440/0.471; B 0.589/419.456/0.461/0.670; A 0.658/0.647/1.805/0.530. B immediate rise vanished by 20 s; none is a qualified directional retained ON/OFF ratio.
- Operational cause unresolved: weak/variable contact or read offset could mimic sub-nA differences. Speculative ionic/volatile switching could account for the fleeting B current, but is not established.
- Prevention: use fixed-bias, fixed-delay and paired-polarity/zero-bias offset diagnostics before ranking ratios; no stress escalation on an offset-like read. Recovery attempted: bounded same-site C/B/A, no retained improvement; no endurance. Outcome: Keithley output-off transaction, 707B open/`nil`, lamp off (dark camera frame), stage Z−84.5 and XY (342707,828786) verified; no runner. Tally no-retention 16→17.

### 2026-09-29 — I46 transient SET current without retention

- Evidence: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I46/`, `plots/I46_semilog_all_attempts.{png,svg}`. Forming attempt 10 at Z+10.5, +10/+50 mV postreads 0.307/0.509 nA unclamped. Three C/B/A sequential recipes completed. Fixed +10 mV B pre/immediate/delayed SET/post-RESET `0.589/14.335/0.335/0.771 nA`; C `0.832/0.088/0.683/0.574 nA`; A `0.513/0.385/0.622/0.502 nA`. No retained directionally correct state.
- Class: transient switching-like current/no retention or changed coupling; not a proven permanently failed device. Contact change or rapid relaxation operationally possible, ionic transience mechanistically speculative. Prevention: compare fixed-time bias reads/zero-bias offsets rather than immediate peaks; recovery attempted: bounded C/B/A stress without retained improvement. No endurance. Output off, matrix open/`nil`, light off, Z−84.5 verified; proceed to next candidate.

### 2026-09-29 — I45 formed, transient SET-like current without retained contrast

- Evidence: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I45/`, `plots/I45_semilog_all_attempts.{png,svg}`. Forming attempt 11, Z+15.5; post-form +10/+50 mV medians 0.345/0.380 nA, not clamped. Three C/B/A same-device sweeps completed. At fixed +10 mV C pre/immediate/delayed SET/post-RESET = 0.649/0.365/0.463/0.519 nA; B = 0.406/4.012/0.186/0.778 nA; A = 0.477/0.501/0.470/0.594 nA. B's immediate rise did not retain for 20 s.
- Classification: transient conductivity/no retained direction; contact vs rapid relaxation unresolved, not permanent device failure. Operational cause uncertain; ionic/volatile contribution is speculative. Prevention: timed fixed-bias reads and zero-bias/paired diagnostics, reject offset-level ratio rankings. Recovery attempted: bounded C/B/A recipe changes without a qualified result. No endurance; site cleaned output off, 707B open/`nil`, lamp off, retracted Z−84.5; continue later user-verified sites.

### 2026-09-29 — I44 clean forming followed by +50 mV read saturation

- Failure-mode label: post-forming low-bias read compliance saturation; retained state or permanent short not established.
- Artifact paths: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I44/forming_summary.json`, `I44/` raw JSON and 12 sweep CSVs, `plots/I44_semilog_all_attempts.{png,svg}`.
- Evidence: nominal XY (358223,828894), aligned XY (358055,828839); bounded forming +2 V/100 µA from Z−34.5 to +20.5 (12 attempts). Attempt 12 first clean sustained compliance at +1.1 V, 3 points near 100 µA, no pre-compliance 10× collapse. Immediate +10 mV median +462.3719 nA; +50 mV median +999.9952 nA at 1 µA read compliance. RESET, C/B/A recipes, and endurance withheld.
- Classification: clamped read, not a valid retained ON/OFF metric. Operational cause: conduction changed after forming and/or contact advance. Speculative cause: filament or pressure-sensitive contact; neither confirmed.
- Prevention: obey 1 µA low-bias guard; do not rank clamped readings or escalate read compliance. Recovery: no additional electrical recovery attempted; Keithley output-off command and 707B open/`nil` verified via direct transactions, lamp turned off, Z retracted from +20.5 to −84.5, XY unchanged. Outcome: safely stopped on I44. Tally state-read compliance saturation during conditioning 10→11.

### 2026-09-29 — I43 clean forming followed by +50 mV read saturation

- Failure-mode label: post-forming state-read compliance saturation; not proven retained SET or permanent short.
- Artifact paths: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I43/forming_summary.json`, `I43/` raw/CSV, and `plots/I43_semilog_all_attempts.{png,svg}`.
- Context/evidence: nominal and actual XY (363223,828894); 15 bounded +2 V/100 µA attempts, Z−34.5 through +35.5. Attempt 14 had a >10× pre-compliance downward jump, not clean forming. Attempt 15 met clean sustained compliance near +0.7 V, peak 100.0022 µA. Its immediate +10 mV read median 871.826 nA (not clamped), while +50 mV read median 999.9929 nA hit 1 µA compliance with voltage delivery potentially collapsed. No RESET or C/B/A recipe was run after this guard.
- Immediate classification: saturated low-bias state read, unsafe/uninterpretable for retained-state optimization. Anecdotal/operational cause: conductance increased sharply after bounded forming/contact advance; contact pressure may contribute. Speculative mechanism: filament or over-contact, unconfirmed without independent diagnostics.
- Prevention: honor low-bias compliance guard and do not interpret clamped reads as precise resistance/ON-OFF. Recovery attempted: output off, 707B open/`nil`, light off, retract from Z+35.5 to −84.5, verified XY unchanged. No further electrical recovery attempted at I43. Outcome: safe hardware handoff, recipes and endurance withheld under compliance safety rule. Tally: state-read compliance saturation during conditioning 9→10.

### 2026-09-29 — I42 formed but C/B/A timed reads lacked retained state

- Evidence: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I42/` and `plots/I42_semilog_all_attempts.{png,svg}`. Formed at bounded attempt 15/Z+35.5. Fixed +10 mV pre/immediate/delayed SET/post-RESET reads (nA): C `0.684/0.402/0.683/0.480`; B `0.413/0.209/0.326/0.756`; A `0.671/0.518/0.404/0.551`. No repeated directionally correct retained SET→RESET. Contact change versus rapid relaxation unresolved; the numerically computed ratios are not valid ON/OFF.
- Immediate class: no-retention / weak offset-like reads, not proven permanent device failure. Operational cause may be contact/circuit baseline change; speculative ionic/volatile transient unproven. Prevention: fixed read timing and paired-bias baseline; do not rank sub-nA numerical ratios. Bounded same-device recipe changes C/B/A attempted without qualifying result. Recovery on this site not achieved; continue next user-verified candidate, no endurance at I42. Keithley off, matrix open/`nil`, light off, Z−84.5 verified.

### 2026-09-29 — I36 and I41: transient SET conduction, no retained contrast

- Evidence: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_opt_run2/I36/` and `I41/`; scatter semilog `plots/I36_semilog_all_attempts.{png,svg}`, `plots/I41_semilog_all_attempts.{png,svg}`.
- I36 formed at attempt 10 (Z+10.5). C SET immediate +10 mV 13.91 nA; 20-second read and RESET censored by worker timeout. Independent later +10 mV read 0.559 nA, offset-like. Fresh B recipe 41.75 nA immediately after SET, 0.303 nA at 20 s, 0.695 nA after RESET; A delayed 0.651 nA, post-RESET 0.330 nA, sub-nA/offset-like. C incomplete, B/A completed; no reproducible retained contrast.
- I41 formed at attempt 16 (Z+40.5), post-form +10 mV 0.502 nA vs post-RESET 0.972 nA (wrong direction). C/B/A same-device recipes complete: C 106.36 nA immediately after SET but 0.321 nA at 20 s; B delayed 0.331 nA/post-RESET 0.544 nA; A delayed 0.471 nA/post-RESET 0.307 nA, weak/offset-like.
- Classification: no-retention/uncertain contact; neither an optimized recipe nor a proven permanently failed DUT. Operational cause uncertain (contact change or rapid volatile conduction); speculative mechanism could include a fleeting filament or ionic/settling component, unproven. Prevention: fixed-timing delayed bias reads, paired-bias offset checks, no ranking on immediate peaks; recovery attempted: bounded same-device recipe changes. No reproducible retained state; stop endurance at these sites. Both finished output off, 707B open/`nil`, lights off, Z−84.5; proceed to further user-verified pristine candidates rather than halting campaign.

### 2026-09-29 — I34 repeatably timed reads weak; A final read censored by runner timeout

- Failure-mode label: apparent post-forming RESET contrast vanished before recipe screening; C/B delayed reads offset-dominated; A completed RESET trace but lacks fixed-time post-RESET read due control-plane timeout, **not** a device endurance failure.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I34/forming01/forming_summary.json`, `I34/multi_recipe01/summary.json`, `I34/multi_recipe01/interruption_recovery.json`, `plots/I34_semilog_all_attempts.{png,svg}`, late paired-bias check `runs/quick_resistance_check_20260928T180416Z/`.
- Evidence: at aligned Zaber `(357943,833679)`, Z+15.5, +2 V/100 µA forming attempt 11. Immediate +10 mV 32.87 nA after SET and 8.81 nA after RESET. Later C reads pre/post/delayed/postreset 0.697/1.791/0.619/0.585 nA; B 0.429/0.397/0.381/0.785 nA. A delayed SET 0.427 nA; its RESET CSV recorded 41 points, peak 57.7 nA, 4.79 nJ, no compliance hits, but the matching post-RESET read was not captured before the 600 s worker timeout. Late 0V/+10mV ~0.455/0.451 nA indicates offset, not a replacement fixed-timing read.
- Classification/cause: no reproducible retained state; possible contact drift or volatile state, neither proved. Runner interruption is censored operationally, not confirmed device failure.
- Prevention/recovery: preserve partial raw measurements, do not re-run A blindly. Parent checked no process, output off and matrix open/`nil`, retracted Z+15.5→−84.5, light off. Continue conservative trials on next site per user direction; no endurance. No-retention-like tally 10→11.

### 2026-09-29 — I32 transient high SET current without retained contrast

- Failure-mode label: forming and bounded same-device recipe SET branches showed immediate conductivity, but 20 s delayed SET reads became sub-nA, RESET sometimes raised rather than lowered current. Contact/volatile state unresolved; no confirmed material failure.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I32/forming_summary.json`, `I32/multi_recipe01/summary.json`, per-branch raw JSON/CSV and `plots/I32_semilog_all_attempts.{png,svg}`.
- Evidence: visible-apex aligned Zaber `(368102,833616)`, Z+25.5; +2 V/100 µA forming attempt 13 followed by +10 mV post-forming/post-RESET 72.69/0.965 nA. In sequential C/B/A comparisons at constant read bias/timing, B's immediate SET read 228.25 nA decayed to 0.239 nA at 20 s, then RESET read 152.71 nA (wrong direction); A's immediate 797.35 nA decayed to 0.470 nA. No valid delayed SET→RESET separation or optimum.
- Operational cause: unstable contact/coupling cannot be excluded. Speculative mechanism: volatile current path or relaxation, not established.
- Prevention/recovery: continue conservative bounded trials on other sites under user instruction, but exclude apparent compliance/immediate-only ratios from ranking and endurance. Parent confirmed no active runner after child timeout, output off and switch matrix open/`nil`, then retracted Z+25.5→−84.5 and verified light off. Outcome: no repeatable optimum; no-retention-like tally 9→10.

### 2026-09-29 — I23/I22/I21 same-device recipe sweeps lacked reproducible retention

- Failure-mode label: bounded forming/SET compliance with transient or offset-dominated +10 mV reads; apparent SET/RESET separation not repeatable. Do not classify any pad permanently failed.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I23/`, `I22/`, `I21/` (forming_summary.json, multi_recipe01/summary.json, I23 multi_recipe02/summary.json and recipe_E_repeats/summary.json, per-branch timestamped raw JSON/CSV); plots `plots/I2{1,2,3}_semilog_all_attempts.{png,svg}`.
- Evidence: optical alignment used the visible probe apex. I23 formed at Z+15.5, attempt 11; I22 Z+20.5, attempt 12; I21 Z+35.5, attempt 15, all +2 V/100 µA. Initial I22 and I21 +10 mV reads fell from 18.98 to 0.940 nA and 78.06 to 0.935 nA after RESET, but delayed paired-bias behavior did not corroborate retention. I23 initially had wrong-direction 0.312→0.925 nA. Exploratory same-site comparisons: I23 six recipes A–F plus E1/E2; I22 and I21 three recipes C/B/A each. I23 E once gave 156.18 nA delayed SET and 0.916 nA post-RESET (apparent 170.5×), but repeats E1/E2 gave delayed SET 0.386/0.199 nA and ratios 0.390×/0.192×. I22 A had only 0.280/0.063 nA near offset (apparent 4.41×); I21 all ratios <1. Bounded branches remained within configured compliance/energy guards, with raw timestamps and post-operation cleanup; no valid endurance candidate.
- Immediate classification: non-repeatable retained state or unstable contact/coupling; not a confirmed material or electrical short. Compliance hits are not ON states.
- Operational cause: possible probe coupling drift; one high ratio occurred in a delayed read without consistent immediate read and vanished on exact repetitions. Mechanistic alternative: volatile conduction/filament relaxation; cannot distinguish from contact instability.
- Prevention/recovery: obey user direction to continue testing on fresh sites with bounded, logged same-device recipes despite weak contact; require correct state direction, paired-bias coupling, delayed retention and replication before ranking/500-sweep endurance. If actual read compliance/hardware fault occurs, stop that site, cleanup and investigate. I21/I22/I23 output off, matrix open/`nil`, light off, safely retracted to Z−84.5.
- Outcome/tally: no reproducible optimum; no-retention-like events 6→9.

### 2026-09-29 — I24 visibly centered but immediate ON-like read relaxed before RESET

- Failure-mode label: forming compliance with rapidly lost read contrast and offset-dominated routed reads; possible volatile conduction or uncertain contact, not proven device failure.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I24/forming_summary.json`, `I24/postforming_contact_diagnostic01/summary.json`, `plots/I24_semilog_all_attempts.{png,svg}`; separate ±10/±50 mV checks `runs/quick_resistance_check_20260928T164055Z/` and `...164129Z/`.
- Evidence: unlike preceding sites, camera-1 pad was aligned to the **visible apex** `(746,680)` rather than the stale remembered `(720,656)`; inferred residual `(2.2,2.6)` px. Pre-forming differential resistance ~1.88 GΩ. At Z+15.75 forming attempt 12 hit sustained 100 µA, after attempt 11 had a 56× downward jump. Immediate 10 mV read 313.5 nA, 50 mV clamped at 1 µA. Later at the same Z: 10 mV 0.44 nA and 0 V 0.47 nA. +0.5 Z trim: 10 mV 0.53 nA, 0 V 0.58 nA. Matrix-open and routed controls showed open noise ~0.1 nA and routed same-sign ~0.6 nA, not a reliable retained state.
- Prevention/recovery: do not claim optimized ON/OFF when the apparent ON state vanishes before RESET and reads are dominated by zero-bias offset; do not declare device permanently failed. Per user's subsequent direction, **continue conservative trials on other pristine sites** despite weak contact, while preserving immediate hardware/read-compliance safety stops and labeling unqualified recipes honestly. Reassess earlier pad alignments to the visible apex, not stale target coordinates. Electrical output off/707B open-nil/light off and Z−83.75 after retract.
- Outcome/tally: no optimization/endurance on I24, recurrence 5→6.

### 2026-09-28 — Substrate 10 I25 lower-voltage forming did not produce retained SET/RESET

- Failure-mode label: forming-compliance event without retained contrast; weak/offset-dominated post-state despite optical pad alignment and small contact trim.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I25/forming_summary.json`, per-attempt CSVs, `plots/I25_semilog_all_attempts.{png,svg}`, low-bias checks `runs/quick_resistance_check_20260928T155058Z/`, `...155358Z/`, `...155439Z/`.
- Evidence: pristine candidate I25 at aligned Zaber `(353381,839257)` and Z+11 formed on attempt 12 with `0→+2→0 V` / 100 µA, 40/81 compliance hits, ~0.0622 mJ. Immediate +10/+50 mV post-forming reads were 0.434/0.508 nA, unclamped; one −2 V/1 mA RESET yielded 0.883/0.707 nA (higher, not HRS recovery). Delayed 0/±10/±50 mV read at Z+11 had ~0.584 nA zero-bias offset and +/−50 mV pair ~0.189 nA. At Z+11.5 after one +0.5 trim, zero-bias offset ~0.507 nA and ±50 pair ~0.175 nA, with no meaningful improvement.
- Classification: no repeatable retained SET/RESET; contact/coupling uncertain, not confirmed permanent failure or short.
- Cause: operationally, forming branch hit compliance but low-bias reads did not follow expected state direction; volatile conduction or changing contact are unproven alternatives.
- Prevention/recovery: do not treat `formed_reset_ready_for_optimization` label as authoritative if physical post-RESET read direction is inverted. Require stable paired-bias coupling and retention before applying multiple same-device recipes; one bounded trim was attempted, with no further electrical stress. Output off, matrix open/nil, light off, retracted to Z−88.5.
- Outcome/tally: same-device recipe sweep not eligible on I25; no endurance. No-retention-like recurrence 4→5.

### 2026-09-28 — Substrate 10 I27/I26 post-forming conductive read did not persist

- Failure-mode label: immediate read-compliance saturation after forming followed by same-site sub-nA/offset-dominated low-bias reads; retained conductive state and physical contact both unconfirmed.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I27/` (`forming_summary.json`, `reset_recovery01/summary.json`, `anchor01/summary.json`); `.../I26/forming_summary.json`; `runs/quick_resistance_check_20260928T153823Z/`, `...153905Z/`, `...153950Z/`.
- Evidence: I27 at Z+1 formed at attempt 10, +10 V/100 µA, 374/401 compliance points, ~0.327 mJ; immediate +10/+50 mV reads both clamped at 1 µA. Before one −2 V/1 mA RESET, +10 mV had relaxed to 0.061 nA median; after RESET 0.774 nA, and a +1.2 V SET yielded 0.217 nA post vs 0.336 nA pre, so RESET was withheld. I26 at Z+6 formed at attempt 11 using the lower +2 V/100 µA pilot (43/81 compliance points, ~0.0594 mJ), immediately clamped at +10/+50 mV 1 µA; subsequent 0/±10/±50 mV checks were same-sign and offset-dominated with ±10 mV pair ~0.13 nA and ±50 pair ~0.247 nA at Z+6. After bounded +0.25 and +0.5 Z checks, ±50 pair stayed ~0.245/0.242 nA with no improved coupling. No I26 RESET or additional SET was applied.
- Classification: no durable verified SET/RESET, possible volatile filament or contact/offset change. A forming compliance hit alone is not an endurance-ready device, and no confirmed permanent short is shown.
- Operational cause: full forming sweep continued after compliance onset; later contact/coupling was not corroborated. Mechanistic alternatives: volatile filament relaxation versus intermittent probe/cable contact; not distinguishable here.
- Prevention: use lower forming endpoint to limit post-onset energy (as tested on I26), then require delayed paired-bias contact/retention proof before RESET, factorial screening or endurance; do not repeat stress on offset-dominated reads.
- Recovery: I27 one bounded RESET then one low-amplitude SET, neither yielded repeatable retained state. I26 two small Z-sensitivity probes and dark low-bias checks without additional stress, then output-off/matrix-open/nil and Z retracted to −93.25, Zaber `(348393,839351)`.
- Outcome: no recipe optimized; both sites removed from factorial eligibility. Tally no-retention-like events 2→4; not counted as permanent DUT damage or confirmed contact loss.

### 2026-09-28 — Substrate 10 original-4×4 interstitial I12 anchor repeat lost retained SET state

- Failure-mode label: no retained low-bias SET response on the second bounded anchor SET; possible changing contact/coupling, not a confirmed permanent device failure.
- Artifacts: `data/pratap_samples/runs/substrate_10_opt_run2/I12/optimization_anchor_pair01/`, `optimization_anchor_pair02/`, and `postscreen_contact_diagnostic01/` (raw JSON, CSV, summary and semilog/voltage-collapse plots).
- Evidence: at unchanged tracked Z +21, first `0→+2→0 V` / 100 µA SET plus `0→−2→0 V` / 1 mA RESET yielded +50 mV reads 16.65 nA after SET and 0.906 nA after RESET (18.38×, both unclamped). Second same SET peaked at ~100 µA with measured-voltage collapse above ~1.0 V, but +50 mV read was 0.361 nA versus 0.438 nA before SET (0.82×); RESET was deliberately skipped. A dark 0/±10/±50 mV routed check showed ~0.3–0.5 nA same-sign offset-dominated currents across polarities; matrix-open reads were ~pA–0.2 nA noisy. Matrix-open is not a matched probe-lifted reference and cannot prove physical contact loss.
- Immediate classification: non-reproducible retained SET response / electrical coupling presently unconfirmed. Compliance-limited sweep alone is not proof of a usable LRS. No read-compliance hit or evidence of permanent stuck-SET.
- Anecdotal/operational cause: unchanged tracked Z/X/Y, but physical tip force/contact stability unverified; timed relaxation after SET also possible.
- Speculative mechanistic cause: volatile filament/ionic relaxation versus probe/contact drift; mechanism unresolved.
- Prevention strategy: pause additional high-voltage or higher-compliance recipe tiers after first failed replication; require a credible coupled low-bias signature or matched probe-lifted baseline before interpreting future stress.
- Recovery strategy: one bounded, non-stressing routed-versus-matrix-open diagnostic was attempted, without Z motion; further stress withheld pending contact/retention review. On an independently contacted next device, retain anchor replication and branch-by-branch safety gates.
- Outcome: inconclusive/no repeated optimum; output off, 707B open/nil, stage tracked Z +21. Tally update: no-retention after switching-like event +1 (1→2); not counted as confirmed open contact.

### 2026-09-28 — Substrate 10 Device 2 intermittent approach signal without retained contact

- Failure-mode label: open/weak contact or transient contact-edge response; no stable low-bias coupling after repeated guarded Z approach.
- Artifacts: `data/pratap_samples/runs/substrate_10_device02_handoff_20260928/` (`contact_edge_revisit.json`, `contact_edge_final.json`, `contact_edge_plus1.json`, `light_dark_contact_z45.json`, Camera-1 Z46); `runs/blunt_probe_slide_approach_20260928T085954Z/` and `runs/blunt_probe_slide_approach_20260928T091019Z/`; `runs/quick_resistance_check_20260928T091220Z/`.
- Evidence: At Z35 pre-approach, paired ±10/±50 mV read slope was ~1.75 GΩ with +10 mV ~48 pA. First illuminated +0.25-Z approach reached ~52 nA at Z44 and ~48 nA at Z45, but returned to Z35 because Camera-1 corrected forward slide was below 0.5 px. Dark re-approach to Z46 showed only ~44–48 pA at +10 mV. Alternating lamp off/on/off at Z45 changed +10 mV from ~46 to ~53 back to ~46 pA, not tens of nA; illumination alone does not explain the transient. A second guarded illuminated approach from Z46 briefly reached ~47–48 nA at Z48.75–49, again without corroborating optical slide and then returned to Z46. Final dark 0/±10/±50 mV check at Z46 gave +10 mV ~45.5 pA and paired ~1.71–1.76 GΩ, close to lifted/pre-approach baseline. No forming, RESET, or conditioning was attempted on Device 2. The tip appears over a partially occluded C pad, but neither optical overlap nor the fleeting current proves durable electrical contact.
- Immediate classification: contact-edge transient / no retained electrical coupling, **not** permanently SET and **not** a verified device short. No reproducible stress candidate yet.
- Anecdotal/operational cause: pad/probe alignment, contact force, contamination, or approach hysteresis unresolved; the slide-tracking sign/threshold did not corroborate the temporary current increase.
- Speculative mechanism: transient mechanical microcontact or stage-motion-induced artifact; cannot distinguish from brief DUT conduction without stable, independent dark paired reads at unchanged Z.
- Prevention: do not chase a migrating threshold with unbounded +Z or run high-voltage forming when returned-to-start read resembles the probe-lifted reference; inspect the actual probe tip and pad after each bounded approach. The Camera-2 scene was overexposed and could not certify a microgap.
- Recovery: two bounded optical+electrical approach passes and dark/light/dark differential reads attempted. Re-establish/confirm pad contact manually or use a newly calibrated contact method before stress; leave electrical outputs off, switch matrix open and light off.
- Outcome: unresolved; no permanently SET state. Recurrence tally: open/weak contact/contact edge +1 (10→11).

### 2026-09-28 — Substrate 10 Device 1 repeat-forming and RESET, residual read-compliance saturation

- Failure-mode label: repeat-forming-like transition followed by low-bias read-compliance saturation; RESET did not fully restore a safe higher-resistance state at +50 mV.
- Artifact paths: `data/pratap_samples/runs/substrate_10_device01_z45_pratap_sequence_20260928T080413Z/` (`forming.csv`, `summary.json`, `forming_reset_explicit_override/reset.csv`, reset summary); precursor Z+5 readback in `data/pratap_samples/runs/substrate_10_device01_zplus5_20260928T_current/move.json`.
- Context: user-authorized +5 Z from 40 to 45, then one non-virgin `0→+10→0 V` sweep at 100 µA, 50 mV steps, 16.6 ms commanded dwell; immediate low-bias read reached 1 µA at +10 mV. After review, the user explicitly authorized one Pratap `0→−2→0 V` RESET at 10 mA, 50 mV steps, 39.2 ms commanded dwell, despite that read hit.
- Evidence: forming onset of three consecutive near-100 µA points at commanded +8.85 V; at +8.95 V measured voltage collapsed to ~0.404 V. Forming peak 100.0015 µA, integrated ~0.297 mJ, 216 compliance points. The RESET delivered −1.999945 V, peak 0.8723 mA, no 10 mA compliance hits, integrated ~0.677 mJ. Post-RESET reads: +10 mV +0.2956 µA, −10 mV −0.2927 µA, +50 mV pinned at 1.000 µA; stopped before −50 mV and all conditioning DCIVs. Final Keithley output-off and 707B open/`nil` verified.
- Immediate classification: formed/strongly conductive after repeat stress, partial conductance reduction after RESET, but residual short-like/compliance-limited low-bias read; not proof of a clean reproducible SET/RESET pair.
- Anecdotal / operational cause: repeated high-voltage forming on a previously formed device at a manually advanced contact Z, followed by the standard Pratap RESET; contact area and current paths remain uncertain.
- Speculative mechanistic cause: persistent/overgrown conductive filament or geometry-sensitive probe shunt; neither mechanism is established by these data.
- Prevention strategy: retain immediate low-bias read gates after every stress branch; do not run +3 V/1 mA and −3/−4 V/10 mA conditioning while +50 mV read remains pinned at compliance. Avoid claiming a precise resistance from clamped reads.
- Recovery strategy: user-approved standard −2 V RESET was attempted once; reduced +10 mV current but did not clear +50 mV compliance. Further stress requires separate review of safer RESET/contact diagnostics.
- Outcome: conditioning withheld at post-RESET safety gate; no optimized DCIV recipe.
- Tally update: repeat-forming-like read saturation 1→2; post-forming RESET residual read saturation 0→1.

### 2026-09-26 — Device 40 repeat forming-like cycle, post-read saturation

- Failure-mode label: repeat high-voltage positive cycle caused a strongly conductive, compliance-limited low-bias post-state; not verified durable or recoverable.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_second_pass_device40_20260926T143453Z/repeat_forming_z40_20260926T155005Z/` (`forming.csv`, raw JSON, diagnostic plot, summary).
- Context: Device 40 was already formed at +8.2 V/100 µA on the first pass. A second-pass +35 versus +50 low-compliance DC-IV showed nearly unchanged ~1 nA peaks and ambiguous physical contact. User explicitly overrode no-repeat-forming and chose exactly one full `0→+10→0 V` cycle at Z +40, 100 µA limit, before inspection; no RESET/conditioning or other Z-height forming sweeps authorized.
- Evidence: fresh 0/±10/±50 mV precheck at Z +40 was pA/offset-dominated. The 401-point repeat cycle first sustained 100 µA at commanded +6.50 V; measured DUT voltage fell to ~0.204 V under compliance. There were 258 compliance points, including 187/200 return points. Measured-trace energy ~0.413 mJ. Post-read medians at +10/−10 mV were +326.4/−317.7 nA; +50 mV hit 1 µA read compliance and the −50 mV read was withheld.
- Immediate classification: strong forming/SET-like transition into a low-resistance, read-limited state; not virgin forming, and not proof of stable electrical contact or useful reversible switching. The +50 mV current is a cap, not an ohmic resistance.
- Operational cause: a full repeat positive sweep on an already formed device delivered extended 100 µA-limited stress after the +6.5 V command onset. The prior contact ambiguity was explicitly accepted for this one user-requested diagnostic; no software/routing malfunction is evidenced.
- Mechanistic alternatives: reactivated/overgrown conductive filament, contact change under electrical field, or pressure-dependent contact; data cannot isolate these mechanisms. The later same-Z read did not retain the initial high current; recoverability under RESET is untested.
- Prevention: do not repeat full forming at another Z or raise read compliance. Require user review of this trace, mechanical state, and a conservative post-state plan before any motion or RESET/conditioning; future high-voltage trials should avoid long post-onset exposure.
- Recovery: not attempted; user requested inspection before any further motion/stress. Keithley/Keysight outputs off, 707B `nil`, lamp off, stage at Z +40, Zaber `(399193,876405)`. No lateral travel at +40.
- Outcome: one repeat positive cycle completed; immediate post-read safety stop. A subsequent same-Z read found the conductive state did **not persist**: +10 mV fell from +326.4 nA to +0.0795 nA; ±50 mV were offset dominated ~0.11 nA. The user then inspected Camera 1, judged apparent contact okay, and explicitly requested DC-IV candidates. A bounded C01 ±1 V/1 µA, C02 +3 V/300 µA, C03 +3.5 V/300 µA screen at unchanged Z +40 had peaks 0.78, 10.44, and 11.02 nA, respectively, with no compliance and no retained post-SET read (C02 +50 mV −0.104 nA, C03 +50 mV +0.052 nA). No −4 V/10 mA RESET or 1 mA SET compliance escalation was run. Artifacts: `data/pratap_samples/runs/substrate_10_second_pass_device40_20260926T143453Z/postrepeat_dciv_eligibility_20260926T160000Z/` and `.../dciv_candidates_20260927T131022Z/`. Both SMUs off, 707B nil, lamp off, Z +40, Zaber `(399193,876405)`. Transient state could reflect relaxation or contact change; no proven persistent LRS. Tally repeat-forming/post-read-saturation +1 and no-retention-like event +1 for this single site (do not double-count candidate screen).

### 2026-09-26 — Device 49 short-like low-bias onset at +10 V segment

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_49_r7_c7_pratap_dciv_20260926T115259460867Z/`.
- Evidence: +9 V segment did not sustain onset, then the +10 V segment hit 100 µA at +0.35 V; cumulative measured trace energy 0.495 mJ at Z +35. No conditioning or DC-IV. Continuation to this fresh site was explicitly authorized after prior safety stops.
- Classification: low-bias short-like / possible latent partial activation, not clean new forming; mechanism unresolved and optical overlap alone does not prove contact.
- Prevention/recovery: existing hard stop, no replay or compliance increase. Add a non-stressing low-bias checkpoint between future forming segments and review raw traces before another campaign. Output off, matrix `nil`, light off, stage Z −65, encoder `(408693, 881405)` verified. Tally unstable forming +1.

### 2026-09-26 — Device 48 low-bias short-like in later forming segment

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_48_r7_c6_pratap_dciv_20260926T114624142804Z/`.
- Evidence: +8 V segment reached 30.10 µA without sustained forming; +9 V segment hit sustained 100 µA at +0.3 V. Cumulative trace energy 0.502 mJ, Z +35. User explicitly chose existing segmented recipe after Devices 46–47 safety stops.
- Classification: low-bias short-like / possible prior partial activation, not clean new forming. Contact-versus-device mechanism not resolved. No conditioning or DC-IV.
- Prevention/recovery: stop on existing hard gate, do not replay or increase compliance; future protocols should consider a low-bias health check between segments. Output off, matrix `nil`, light off, stage Z −65, encoder `(403693, 881405)` verified. Tally unstable forming +1.

### 2026-09-26 — Device 47 low-voltage short-like onset after prior near-compliance segment

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_47_r7_c5_pratap_dciv_20260926T113546151834Z/`.
- Evidence: +6 V segment peaked 52.61 µA without sustained onset; on the next +7 V segment, 100 µA sustained by +0.1 V. Z +35, optical apex over inferred C spine; cumulative measured trace energy 0.229 mJ. No conditioning or DC-IV.
- Classification: low-voltage short-like after possible partial activation in the prior segment; not clean new forming. Cause of transition may be device or contact-related and is unresolved.
- Prevention/recovery: safety gate stopped further stress; no retry or read-compliance escalation. Given consecutive Device 46/47 unsafe forming outcomes, pause before Devices 48–49 and review the checkpoint/partial-activation strategy. Output off, 707B `nil`, light off, Z −65, encoder `(398693, 881405)` verified. Tally unstable forming +1.

### 2026-09-26 — Device 46 pre-compliance down-jump in adaptive forming

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_46_r7_c4_pratap_dciv_20260926T112937175579Z/`.
- Evidence: +7 V segment reached sustained 100 µA at +3.5 V but had a preceding 14.89× downward current jump; trace energy across segments 0.427 mJ. Z +35, optical apex over inferred C spine; low-bias reads before forming remained pA/sub-nA. No conditioning or DC-IV.
- Classification: unstable forming / intermittent pre-compliance collapse. Cause could be transient device filament/contact or measurement-path instability; not resolved by the data.
- Prevention: fail-closed pre-compliance jump gate stopped further stress, no second forming attempt; verify trace and contact pathway independently before any future protocol revision. Recovery not attempted. Output off, 707B `nil`, light off, Z −65, encoder `(393693, 881405)` verified.

### 2026-09-26 — Device 45 conditioning SET-read saturation

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_45_r7_c3_pratap_dciv_20260926T112343193240Z/`.
- Evidence: Z +35, segmented forming reached sustained 100 µA at +5.4 V in +6 V segment, total 0.218 mJ; conditioning ratios 556.85 and 19.72, then pair 3 SET read saturated 100 µA. DC-IV withheld.
- Classification: recurrent invalid conditioning state read, not a validated LRS or DC-IV result. Operationally the Pratap +3 V/1 mA SET can exceed the 100 µA read gate; underlying device/contact mechanism uncertain.
- Prevention/recovery: stop on read saturation; no automatic read-compliance increase, second forming, or retry. Outcome: output off, 707B `nil`, light off, Z −65, encoder `(388693, 881405)` verified. Tally +1.

### 2026-09-26 — Device 44 near-compliance transient before segmented onset; conditioning read saturation

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_44_r7_c2_pratap_dciv_20260926T111656222161Z/`.
- Evidence: at Z +35, +5 V forming segment peaked at 84.8 µA but lacked sustained compliance; +6 V segment first sustained 100 µA at +1.85 V. Cumulative trace energy 0.543 mJ. Conditioning ON/OFF ratios 1.00, 0.789, 68085.1; pair 4 SET read saturated 100 µA. No DC-IV.
- Classification: invalid conditioning read and ambiguous segmented onset, not a verified DC-IV result. Operational possibility: previous segment partially activated the device. Mechanism remains speculative (filament/contact change cannot be distinguished).
- Prevention: tighten forming near-compliance transient stop from 90 to 80 µA, so a similar completed segment will not trigger a higher endpoint; verified runner offline tests 9/9. Recovery: no Device 44 retry or compliance escalation. Verified output off, 707B `nil`, lights off, Z −65, encoder `(383693, 881405)`; tally saturation +1.

### 2026-09-26 — Device 43 conditioning SET-read saturated after adaptive forming

- Failure-mode label: state-read compliance saturation during Pratap conditioning after clean adaptive forming.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_43_r7_c1_pratap_dciv_20260926T093717549320Z/`.
- Evidence: row-7 optical X correction −500 at Z −165; forming +2/+3 V segments no transition, +4 V segment onset +3.8 V/100 µA; total 0.337 mJ. Pair 1 ON/OFF 75.15; pair 2 SET read saturated at 100 µA. No DC-IV.
- Cause: SET state beyond read range or low-resistance/over-SET; whether intrinsic device or contact is unresolved. Do not infer a precise current from a capped read.
- Prevention/recovery: stop on the invalid read; do not automatically increase compliance. Keep remaining-site Pratap activation and DC-IV-only gate; no Device 43 repeat. Outcome: stopped with output off, 707B `nil`, light off, stage Z −65, Zaber `(378693, 881405)`; preflight passed. Tally saturation +1.

### 2026-09-26 — Device 36 adaptive early-stop forming; conditioning still unstable

- Failure-mode label: conditioning non-convergence despite minimized post-onset forming exposure.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_36_r6_c1_pratap_dciv_20260926T092938244888Z/`.
- Evidence: first output-off segment 0→+2→0 V at 100 µA formed cleanly at +1.9 V and stopped, 0.0580 mJ measured segment energy. Conditioning ON/OFF ratios 173.64, 58267.27, 1829.05, 0.707, 8539.27, 96.36; no three consecutive accepted. DC-IV never ran.
- Interpretation: post-onset exposure reduction did not by itself stabilize this site. Prior hypothesis of overforming as the sole cause is disfavored, but no material/contact mechanism is established.
- Prevention: retain per-segment energy and compliance gates; do not count planned +3.5 V DC-IV recipe as tested, and do not add recovery stress on this site. Fresh row-7 optical alignment/contact verification before continuation.
- Recovery/outcome: no recovery/replay; output off, matrix open/`nil`, light off, stage Z −65, live Zaber `(379193, 876405)` verified. Tally non-convergence +1.

### 2026-09-26 — Device 37 conditioning non-convergence and post-onset forming exposure concern

- Failure-mode label: repeated conditioning non-convergence after clean forming; **hypothesis**, not proof, of overforming from full +10 V sweep after early onset.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_37_r6_c2_pratap_dciv_20260926T091001375714Z/`.
- Evidence: sustained +100 µA forming at +2.65 V, no low-voltage short or precompliance collapse. Six conditioning ratios 25.60, 7.49, 39.29, 26554.84, 14421.78, 2.08; no three accepted pairs, DC-IV withheld. Offline integration of full forming sweep gave 0.509 mJ total and 0.505 mJ from onset onward; note current-clamped energy integration and instrumentation timing may vary. Across Devices 41/40/39/38/37 forming onset was 8.0/8.2/6.45/5.1/2.65 V, with 77.8–99.2% of integrated forming energy after onset.
- Classification/cause: switching activation but non-reproducible state reads; device heterogeneity/contact pressure and post-onset exposure are confounded. No causation established.
- Prevention: pause identical full +10 V sweeps before Device 36; evaluate bounded early-stop-at-compliance forming with +10 V/100 µA retained as ceiling, then resume only after an explicit recipe decision. No automatic DC-IV or read-compliance escalation.
- Recovery/outcome: no recovery/replay; outputs off, 707B open/`nil`, stage Z −65, Zaber `(384193, 876405)` confirmed. Tally conditioning non-convergence +1.

### 2026-09-26 — Device 38 Pratap conditioning non-convergence

- Failure-mode label: repeated conditioning non-convergence after clean forming.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_38_r6_c3_pratap_dciv_20260926T090335268375Z/`.
- Evidence: one +10 V/100 µA forming sweep at Z +35 transitioned at +5.1 V; six conditioning ratios 1.983, 0.0767, 1.315, 0.2046, 184.26, 6963.94; no accepted three-pair window. Planned DC-IV +3.5 V/300 µA was not run.
- Classification/cause: activation achieved but directionally inconsistent and highly variable state reads. Contact variability or device dynamics remain hypotheses, not proven mechanisms.
- Prevention: retain exact Pratap activation on fresh sites, withhold DC-IV until accepted conditioning. Do not count the planned contrast as tested or escalate/read compliance.
- Recovery/outcome: no recovery/replay; outputs off, matrix open/`nil`, stage Z −65, live Zaber `(389193, 876405)` verified. Tally non-convergence +1.

### 2026-09-26 — Device 39 Pratap conditioning non-convergence after forming

- Failure-mode label: conditioning ratios varied beyond the three-consecutive ≥5 and ≤2.5× spread gate.
- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_39_r6_c4_pratap_dciv/`.
- Evidence: one +10 V/100 µA forming sweep at Z +35 transitioned at +6.45 V, no pre-compliance downward jumps or low-voltage short. Six Pratap conditioning ON/OFF ratios: 32.39, 18.71, 488.84, 208.40, 1778.65, 31.50; no qualifying three-pair window. DC-IV never ran.
- Interpretation: clean activation but unstable state separation under the fixed conditioning schedule; mechanism and contact contribution unresolved.
- Prevention: preserve the Pratap activation recipe and withhold DC-IV until its stability gate passes. Do not mistake the untested +3.5 V/300 µA DC-IV assignment for a failed recipe.
- Recovery/outcome: no recovery/replay; outputs off, 707B open/`nil`, stage Z −65, live Zaber `(394193, 876405)`; preflight passed.
- Tally: conditioning non-convergence +1.

### 2026-09-26 — Device 40 Pratap DC-IV lost directionality on cycle 2

- Failure-mode label: directionally inverted second DC-IV characterization cycle after a valid first cycle.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_40_r6_c5_pratap_dciv/`.
- Evidence: formed at +8.2 V/100 µA; four conditioning pairs, final three ratios 10.43, 25.49, 25.38 met the stability gate. With DC-IV SET +3 V/300 µA, RESET −4 V/10 mA, cycle 1 independent LRS/HRS at +0.05 V were 37.68 µA / 175.06 nA (215.26×). Cycle 2 were 4.554 µA / 5.041 µA (0.903×); both reads below 100 µA compliance. RESET cycle 2 peak at −3.9 V was 0.795 mA, below its 10 mA ceiling. Plot: `device40_dciv_two_cycles_semilog.png`.
- Immediate classification: one valid cycle followed by non-retaining/inverted state separation; not a reproducible protocol or endurance claim.
- Operational cause hypothesis: +3 V/300 µA SET did not retain LRS in cycle 2; altered RESET state, contact drift, and device variability remain possible. No material mechanism established.
- Prevention: on a *fresh* site keep activation and RESET fixed, contrast SET endpoint +3.5 V at 300 µA; use independent unclamped reads and stop on first invalid cycle. Avoid raising read compliance or replaying Device 40.
- Recovery/outcome: no recovery attempted; outputs off, 707B open/`nil`, Stage Z −65, Zaber `(399193, 876405)` verified. New contrast pending.
- Tally update: DC-IV characterization inversion after initial valid cycle +1.

### 2026-09-26 — Device 41 Pratap-derived DC-IV cycle 2 SET-read saturation

- Failure-mode label: read-compliance-limited SET state during DC-IV characterization; not an endurance result.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_41_r6_c6_pratap_dciv/`.
- Evidence: one +10 V/100 µA forming sweep at Stage Z +35 formed cleanly at +8.0 V. Three Pratap conditioning ratios 30.06, 18.07, 42.19 passed ≥5 and ≤2.5× spread. DC-IV cycle 1 at +3 V/1 mA SET and −4 V/10 mA RESET produced independent +0.05 V LRS 63.50 µA and HRS 84.68 nA (749.86×), both below 100 µA read compliance. Cycle 2 SET read hit 100 µA read compliance; cycle-2 RESET withheld. Plot `device41_dciv_cycle1_semilog.png` labels partial cycle 2.
- Immediate classification: promising **single valid cycle** followed by invalid clamped read. The unclamped SET current is unknown; do not call repeated switching or endurance.
- Operational cause: DC-IV SET at 1 mA may over-SET relative to the 100 µA read ceiling; contact drift or device variability cannot be excluded. Mechanistic explanation unproven.
- Prevention: on the next *fresh* site, keep Pratap forming/conditioning and −4 V/10 mA RESET fixed, test DC-IV SET compliance 300 µA as one-factor contrast. Do not raise read compliance from a saturated read.
- Recovery/outcome: no recovery stress or replay; Keithley/Keysight outputs off, 707B open/`nil`, Stage Z −65, live Zaber `(404193, 876405)` verified. Contrast not yet tested.
- Tally update: DC-IV state-read saturation +1.

### 2026-09-26 — Device 42 CONF-03 no-transition after optical correction

- Failure-mode label: no forming transition with ambiguous contact-versus-high-HRS coupling; stronger-RESET recipe never executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_42_r6_c7_conf_03/`.
- Evidence: Camera 1 showed an inferred C-pad opening displaced from the apex; while Stage Z was −170, Zaber was corrected X −700/Y −500 native steps and recaptured. Twenty-five Tier-1 `+4 V / 10 µA` attempts from Stage Z −85 to +35 produced 2.077–2.262 nA peak, with no sustained forming or Tier-2 unlock. Across saved forward sweeps, the 1–4 V slope was 0.504–0.531 nA/V (first 0.5216; last 0.5231), with no clear Z-dependent contact step. The response was voltage-dependent but optical overlap and voltage scaling alone do not establish electrical contact. Plot/CSV: `contact_response_vs_z.png`, `contact_response_vs_z.csv` in the artifact folder.
- Immediate classification: DC-IV confirmation withheld; not a negative result for the proposed −3.5 V RESET. Operational cause unresolved (contact depth/edge, pristine high HRS, or routed-path leakage); device mechanism unproven.
- Prevention: stop repeating the same 25 forming sweeps. Matched same-setting reference now measured: matrix open Z −65 slope 0.030 nA/V, routed retracted Z −65 slope 0.509 nA/V, routed deepest Z +35 slope 0.523 nA/V. The nA signal is route-dependent but not appreciably Z-dependent; physical contact and route leakage remain unresolved. Inspect camera tip-slide and verify the electrical route/contact before advancing stress at another site. Comparative plot: `routed_vs_open_reference.png` in the artifact folder.
- Recovery/outcome: no further device stress attempted; output-off, 707B open/`nil`, light off verified after both references; Stage Z −65, Zaber `(409377, 876676)`. Physical contact diagnosis not yet completed.
- Tally update: no-transition/ambiguous-coupling: +1 (do not count as definitively open).

### 2026-09-26 — Device 35 CONF-02 withheld after no forming transition

- Failure-mode label: open/weak-contact-like activation failure; stronger-RESET confirmation recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_35_r5_c7_conf_02/`.
- Evidence: 25 Tier-1 forming attempts through Stage Z `+30` at `+4 V / 10 µA`; maximum peak current `2.446187 nA`, no sustained transition or tier unlock.
- Immediate classification: no meaningful coupling under the bounded test, not a measured failure of the proposed `−3.5 V` RESET recipe. Operational cause uncertain (high HRS/contact edge versus device variation); a mechanistic cause is not established.
- Prevention: preserve the low-current tier gate and avoid further stress on this site; compare future sites using non-stressing contact diagnostics where practical.
- Recovery/outcome: no recovery stress attempted. Outputs off, 707B open/`nil`, light off; Stage retracted Z `+30→−70`, live Zaber `(410077, 872176)`.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 33 PULSE-14 anchor withheld after activation-yield failure

- Failure-mode label: open/weak-contact-like activation failure; assigned pulse anchor not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_33_r5_c5_pulse_14/`.
- Evidence: 25 Tier-1 attempts through Z `+30` remained near `2 nA`; no tier unlock or forming transition.
- Immediate classification: activation-yield failure, not PULSE-14 performance; the anchor pair produced no reproducible pulse candidate.
- Recovery/outcome: outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−70`; stop before adaptive CONF-01 and review DOE evidence.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 32 PULSE-13 anchor withheld after conditioning non-convergence

- Failure-mode label: anchor-replicate conditioning non-convergence after clean forming; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_32_r5_c4_pulse_13/`.
- Evidence: clean Tier-2 forming at Z `+25`, onset `0.65 V`; conditioning ratios `0.000340`, `0.832`, `1.55`, `14.1`, `2.92`, `500.5`, with early inversion and extreme spread.
- Immediate classification: anchor failed before pulse execution; activation/conditioning remains non-reproducible.
- Prevention/recovery: unchanged gate; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−75`; continue replicate Device 33/PULSE-14.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 31 PULSE-12 withheld after pair-2 read compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_31_r5_c3_pulse_12/`.
- Evidence: clean Tier-1 forming at Z `+20`, onset `1.75 V`; pair 1 ratio `1.39`; pair-2 SET read hit compliance.
- Immediate classification: weak initial separation followed by invalid/clamped read; PULSE-12 remains unevaluated.
- Prevention/recovery: preserve partials and do not raise compliance automatically; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−80`; continue anchor Device 32/PULSE-13.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 30 PULSE-11 withheld after Tier-3 forming and inverted conditioning

- Failure-mode label: conditioning non-convergence after clean forming; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_30_r5_c2_pulse_11/`.
- Evidence: Tier-3 forming at Z `+15`, onset `3.30 V`, `50 µA` compliance; conditioning ratios `1.39`, `1.33`, `0.000860`, `0.859`, `0.849`, `2.11`, predominantly inverted.
- Immediate classification: non-converged state separation following higher-stress forming; PULSE-11 remains unevaluated.
- Prevention/recovery: unchanged gate and no further forming escalation; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−85`; continue Device 31/PULSE-12.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 29 PULSE-10 withheld after pair-2 read compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_29_r5_c1_pulse_10/`.
- Evidence: clean Tier-2 forming at Z `+25`, onset `1.20 V`; pair 1 ratio `210.8`; pair-2 SET read hit compliance.
- Immediate classification: promising but invalid/clamped conditioning partial; PULSE-10 remains unevaluated.
- Prevention/recovery: preserve partials and do not raise compliance automatically; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−75`; continue Device 30/PULSE-11.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 22 PULSE-09 characterization completed but directionally failed

- Failure-mode label: completed pulse characterization with systematic state inversion; no endurance attempted.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_22_r4_c1_pulse_09/`.
- Evidence: Tier-2 forming at Z `+20`, onset `5.15 V`; conditioning passed at pair 4. Five pulse ratios were `0.0194`, `0.00142`, `0.00319`, `0.00451`, `0.0371`, all inverted.
- Immediate classification: PULSE-09 rejected; pulse SET produced lower read current than pulse RESET in every cycle.
- Recovery/outcome: no endurance or retention; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−80`; continue Device 29/PULSE-10.

### 2026-09-25 — Device 23 PULSE-08 withheld on exact conditioning spread gate

- Failure-mode label: conditioning non-convergence after clean forming; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_23_r4_c2_pulse_08/`.
- Evidence: clean Tier-1 forming at Z `+20`, onset `1.70 V`; ratios `1.28`, `457`, `7.22`, `75.9`, `43.8`, `110.5`. Final-three spread was exactly `2.521855×`, narrowly above the `2.5×` gate.
- Immediate classification: near-miss, but non-converged by the prespecified exact criterion; PULSE-08 remains unevaluated.
- Prevention/recovery: do not round into acceptance; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−80`; continue Device 22/PULSE-09.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 24 PULSE-07 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_24_r4_c3_pulse_07/`.
- Evidence: clean Tier-1 forming at Z `+25`, onset `1.65 V`; ratios `1.96`, `0.00181`, `33.8`, `186`, `55.4`, `362`, including inversion and `6.54×` final-three spread.
- Immediate classification: non-converged state separation; PULSE-07 remains unevaluated.
- Prevention/recovery: unchanged gate; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−75`; continue Device 23/PULSE-08.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 25 PULSE-06 withheld on low-voltage short-like forming

- Failure-mode label: perma-SET/hard-short-like low-bias response; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_25_r4_c4_pulse_06/`.
- Evidence: Tier-2 forming at Z `+30` had low-bias median `5.10 µA`, sustained compliance onset `0.45 V`, and peak `25.0 µA`; low-voltage short gate true.
- Immediate classification: short-like response before valid forming; PULSE-06 remains unevaluated.
- Recovery/outcome: no conditioning or pulse execution; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−70`; continue Device 24/PULSE-07.
- Tally update: perma-SET/hard short-like low-bias compliance: +1.

### 2026-09-25 — Device 26 PULSE-05 withheld after pair-6 read compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_26_r4_c5_pulse_05/`.
- Evidence: clean Tier-2 forming at Z `+35`, onset `0.75 V`; ratios `1.00`, `133656`, `20567`, `738`, `15799`; pair-6 SET read hit compliance.
- Immediate classification: promising conditioning partial but invalid/clamped final state; PULSE-05 remains unevaluated.
- Prevention/recovery: preserve partials and do not raise compliance automatically; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−65`; continue Device 25/PULSE-06.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 27 PULSE-04 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_27_r4_c6_pulse_04/`.
- Evidence: clean Tier-2 forming at Z `+40`, onset `0.70 V`; ratios `55747`, `0.0826`, `0.301`, `79723`, `29373`, `381`, including two inverted pairs and approximately `209×` final-three spread.
- Immediate classification: non-converged state separation; PULSE-04 remains unevaluated.
- Prevention/recovery: unchanged gate; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−60`; continue Device 26/PULSE-05.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 28 PULSE-03 withheld after pair-6 read compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_28_r4_c7_pulse_03/`.
- Evidence: clean Tier-2 forming at Z `+50`, onset `0.75 V`; five directionally correct ratios `9333`, `2061`, `1461`, `60.7`, `219`; pair-6 SET read hit compliance.
- Immediate classification: promising conditioning partial but invalid/clamped final state; PULSE-03 remains unevaluated.
- Prevention/recovery: preserve partials and do not raise compliance automatically; outputs off, both SMUs off, matrix open/`nil`, light off, stage retracted to Z `−50`; continue Device 27/PULSE-04.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 21 PULSE-02 withheld after activation-yield failure

- Failure-mode label: open/weak-contact-like activation failure; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_21_r3_c7_pulse_02/`.
- Evidence: 25 Tier-1 attempts through Z `+50` remained near `2 nA`; no tier unlock or forming transition.
- Immediate classification: activation-yield failure, not PULSE-02 performance.
- Recovery/outcome: outputs off, matrix open/`nil`, light off, stage retracted to Z `−50`; continue Device 28/PULSE-03.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 20 PULSE-01 withheld after activation-yield failure

- Failure-mode label: open/weak-contact-like activation failure; assigned pulse recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_20_r3_c6_pulse_01/`.
- Evidence: 25 Tier-1 attempts through Z `+45` remained near `2 nA`; no tier unlock or forming transition.
- Immediate classification: activation-yield failure, not PULSE-01 performance.
- Recovery/outcome: outputs off, matrix open/`nil`, light off, stage retracted to Z `−55`; continue Device 21/PULSE-02.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 19 anchor DCIV-14 withheld after conditioning non-convergence

- Failure-mode label: anchor-replicate conditioning non-convergence after clean forming; assigned recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_19_r3_c5_dciv_14/`.
- Evidence: clean Tier-1 forming at Z `+40`, onset `1.90 V`; ratios `0.902`, `0.0159`, `0.0176`, `49.0`, `1279`, `57.2`; final-three spread `26.1×`.
- Immediate classification: second anchor replicate failed before recipe execution, confirming conditioning non-reproducibility.
- Recovery/outcome: outputs off, matrix open/`nil`, light off, stage retracted to Z `−60`.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 18 anchor DCIV-13 withheld after conditioning non-convergence

- Failure-mode label: anchor-replicate conditioning non-convergence after clean forming; assigned recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_18_r3_c4_dciv_13/`.
- Evidence: clean Tier-1 forming at Z `+35`, onset `1.55 V`; conditioning ratios `4.30`, `61765`, `50008`, `188`, `1047`, `30.6`, with `34.2×` final-three spread.
- Immediate classification: anchor replicate failed before recipe execution; activation/conditioning reproducibility remains the dominant bottleneck.
- Prevention/recovery: unchanged gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−65`; continue anchor replicate Device 19/DCIV-14.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 17 DCIV-12 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_17_r3_c3_dciv_12/`.
- Evidence: clean Tier-1 forming at Z `+30`, onset `1.85 V`; conditioning ratios `1.08`, `4.80`, `381`, `28829`, `100`, `9402`, with approximately `287×` final-three spread.
- Immediate classification: non-converged state separation; DCIV-12 remains unevaluated.
- Prevention/recovery: unchanged stability gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−70`; continue anchor replicate Device 18/DCIV-13.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 16 DCIV-11 withheld after inverted read and compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_16_r3_c2_dciv_11/`.
- Evidence: clean Tier-1 forming at Z `+25`, onset `1.85 V`; pair 1 ratio `0.754` was inverted, and pair-2 post-SET read hit compliance.
- Immediate classification: invalid/clamped conditioning state; DCIV-11 remains unevaluated.
- Prevention/recovery: preserve partials and do not raise compliance automatically; outputs off, matrix open/`nil`, light off, stage retracted to Z `−75`; continue Device 17/DCIV-12.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 15 DCIV-10 withheld after strongly inverted conditioning

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_15_r3_c1_dciv_10/`.
- Evidence: clean Tier-1 forming at Z `+20`, onset `1.70 V`; conditioning ratios `1.00`, `0.231`, `0.00123`, `0.000225`, `0.651`, `201`, with five of six pairs at or below unity.
- Immediate classification: strongly inverted/non-converged conditioning; DCIV-10 remains unevaluated.
- Prevention/recovery: unchanged stability gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−80`; continue to Device 16/DCIV-11.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 8 DCIV-09 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_08_r2_c1_dciv_09/`.
- Evidence: clean Tier-1 forming at Z `+25`, onset `2.45 V`; conditioning ratios `0.891`, `46.5`, `67.7`, `25078`, `434.6`, `157.8`, including inversion and approximately `159×` final-three spread.
- Immediate classification: non-converged state separation; DCIV-09 remains unevaluated.
- Prevention/recovery: unchanged stability gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−75`; continue to Device 15/DCIV-10.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 9 DCIV-08 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_09_r2_c2_dciv_08/`.
- Evidence: clean Tier-1 forming at Z `+30`, onset `1.85 V`; conditioning ratios `1.20`, `181`, `15.6`, `63044`, `61584`, `57.3`. Final-three spread was approximately `1099×`.
- Immediate classification: non-converged state separation; DCIV-08 remains unevaluated.
- Prevention/recovery: unchanged stability gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−70`; continue to Device 8/DCIV-09.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 10 DCIV-07 withheld after state-read compliance saturation

- Failure-mode label: state-read compliance saturation during conditioning; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_10_r2_c3_dciv_07/`.
- Evidence: clean Tier-2 forming at Z `+35`, onset `0.80 V`; conditioning pair 1 ratio `505`. Pair-2 post-SET read hit the configured read compliance, making that state value invalid.
- Immediate classification: conditioning interrupted on an invalid/clamped read; DCIV-07 remains unevaluated.
- Prevention/recovery: no automatic compliance escalation; preserve partials and review compliance tiers before any retest. Outputs off, matrix open/`nil`, light off, stage retracted to Z `−65`; continue to Device 9/DCIV-08.
- Tally update: state-read compliance saturation during conditioning: +1.

### 2026-09-25 — Device 11 DCIV-06 withheld after conditioning direction inversion

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_11_r2_c4_dciv_06/`.
- Evidence: clean Tier-1 forming at Z `+40`, onset `2.25 V`; conditioning ratios `1.09`, `172149`, `0.00329`, `189`, `4421`, `2258`, including direction inversion and extreme variability.
- Immediate classification: non-converged state separation; DCIV-06 remains unevaluated.
- Prevention/recovery: unchanged three-pair direction/stability gate; outputs off, matrix open/`nil`, light off, stage retracted to Z `−60`; continue to Device 10/DCIV-07.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 12 DCIV-05 withheld after conditioning non-convergence

- Failure-mode label: conditioning non-convergence after clean forming; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_12_r2_c5_dciv_05/`.
- Evidence: clean Tier-1 forming at Z `+45`, onset `1.80 V`; six conditioning ratios were `70476`, `48.7`, `26.6`, `81.2`, `11.3`, `255.6`. Final-three spread was `22.6×`, exceeding the `2.5×` gate.
- Immediate classification: formed device with non-converged state separation; DCIV-05 remains unevaluated.
- Prevention/recovery: do not apply DOE recipe until conditioning stability passes; outputs off, matrix open/`nil`, light off, stage retracted to Z `−55`; continue to Device 11/DCIV-06.
- Tally update: conditioning non-convergence after clean forming: +1.

### 2026-09-25 — Device 14 DCIV-03 withheld after unstable forming

- Failure-mode label: unstable forming / intermittent pre-compliance collapse; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_14_r2_c7_dciv_03/`.
- Evidence: Tier 4 at Z `+55` reached `100.1 µA` with apparent sustained onset at `2.95 V`, but five earlier current collapses ranged up to `5.88×10^4`-fold.
- Immediate classification: compliance-level intermittent response, not clean forming; DCIV-03 remains unevaluated.
- Prevention/recovery: keep no-collapse forming gate; no conditioning or DOE; outputs off, matrix open/`nil`, light off, stage retracted to Z `−45`; continue to Device 13/DCIV-04.
- Tally update: unstable forming/intermittent pre-compliance collapse: +1.

### 2026-09-25 — Device 7 DCIV-02 withheld after repeated activation-yield failure

- Failure-mode label: open/weak-contact-like activation failure; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_07_r1_c7_dciv_02/`.
- Evidence: 25 Tier-1 sweeps through Z `+60` remained near `2 nA`, without a `100 nA` unlock event or clean forming.
- Immediate classification: activation-yield failure; DCIV-02 remains unevaluated.
- Recovery/outcome: no further Device 7 stress; outputs off, matrix open/`nil`, light off, stage retracted to Z `−40`; continue to Device 14/DCIV-03.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 6 DCIV-01 withheld after activation-yield failure

- Failure-mode label: open/weak-contact-like activation failure; assigned DC-IV recipe not executed.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_06_r1_c6_dciv_01/`.
- Evidence: 25 Tier-1 forming/contact sweeps through Z `+55` remained near `2 nA`, never crossing the `100 nA` tier-unlock gate or producing clean forming.
- Immediate classification: activation-yield failure, not evidence that DCIV-01 is ineffective.
- Prevention strategy: preserve the requirement for clean forming and stable conditioning before applying a DOE recipe; do not contaminate recipe metrics with non-activated devices.
- Recovery strategy: no further stress on Device 6; advance to Device 7 and independent DCIV-02.
- Outcome: DCIV-01 withheld; outputs off, matrix open/`nil`, light off, stage retracted to Z `−45`.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 5 bounded search remained open/weak-contact-like

- Failure-mode label: open/weak contact or non-forming device; bounded forming-as-contact search exhausted.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_05_r1_c5_forming_pilot/`.
- Evidence: 25 Tier-1 `+4 V/10 µA` sweeps from OpenFlexure Z `−70` through `+50`; peak currents remained `1.89–2.06 nA`, with no sustained compliance and no `100 nA` tier-unlock event.
- Immediate classification: open/weak-contact-like or intrinsically non-forming site; no evidence of hard short or breakdown.
- Operational cause: no routing/cleanup failure; C-pad offset and exact X+5000 translation were preserved.
- Speculative mechanistic cause: weak probe coupling or high-resistance/non-forming DUT; not distinguishable from these data alone.
- Prevention strategy: retain the bounded 25-position window and do not escalate voltage/compliance while current remains below the meaningful-coupling gate.
- Recovery strategy: no further stress or Z advancement on Device 5; proceed to Device 6.
- Outcome: conditioning withheld; outputs off, matrix open/`nil`, light off, stage safely retracted to Z `−50`.
- Tally update: open/weak contact/contact edge: +1.

### 2026-09-25 — Device 4 unstable forming with intermittent pre-compliance collapses

- Failure-mode label: unstable forming / intermittent pre-compliance collapse; conditioning withheld.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_04_r1_c4_forming_pilot/`.
- Context: FORM-04 pilot using the verified C-pad row offset, Tier-1 low-stress Z search, and `100 nA` gate before higher-tier unlocking.
- Evidence: at OpenFlexure Z `+45`, tiers 1–4 reached peaks of `10.0`, `25.2`, `50.1`, and `100.2 µA`, but showed respectively `1`, `11`, `4`, and `2` pre-compliance current collapses. Maximum detected collapse exceeded `2×10^5`-fold. The clean-forming criterion therefore remained false despite compliance-level current.
- Immediate classification: intermittent contact/filament response; not clean forming, and compliance attainment was not accepted as success.
- Operational cause: no software or routing error found; exact 5,000-step row translation and C-pad capture were preserved. Intermittent mechanical/electrical coupling remains possible.
- Speculative mechanistic cause: unstable filament nucleation/rupture or contact intermittency; not distinguishable from these sweeps alone.
- Prevention strategy: preserve the no-down-jump clean-forming gate; do not use compliance alone as contact/forming proof; do not condition or run endurance after unstable forming.
- Recovery strategy: no retry on Device 4. Outputs disabled, matrix opened, light off, safe retract to Z `−55`; continue to the next pilot device.
- Outcome: Device 4 excluded before conditioning; raw sweeps and failure plot preserved.
- Tally update: unstable forming / intermittent pre-compliance collapse: +1.

### 2026-09-25 — Device 1 optimization pilot continued past unmet forming gate

- Failure-mode label: runner control-flow/parser incident causing post-gate unintended electrical stress; weak/open-like coupling, not demonstrated DUT breakdown.
- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/data/pratap_samples/runs/substrate_10_optimization_attempt1_20260925T133236Z/device_01_r1_c1_forming_pilot/`.
- Context: first Device 1 pilot for `optimization - attempt 1`; forming sweeps were also the contact detector. Four adaptive forming tiers were run at OpenFlexure Z `-75`: `+4 V/10 µA`, `+6 V/25 µA`, `+8 V/50 µA`, and `+10 V/100 µA`.
- Evidence: forming peaks were only `2.62`, `4.20`, `5.42`, and `6.65 nA`; no compliance hits or clean forming transition. The pA/nA traces had positive polarity and 4.3–7.0× high/low-bias slope, which the initial classifier labeled contact-like. The runner entered `forming_contacted_not_formed_waiting_review`, but a one-line nested-if/semicolon bug skipped the intended raise because status was no longer `running`. It then completed one `-2 V/10 mA` forming RESET (peak `82.6 nA`) and one `+3 V/1 mA` conditioning SET (peak `11.0 nA`), both with zero compliance hits. The following `+0.05 V` reads were `0.361`, `0.769`, and `0.361 nA`. Parsing stopped because `V_meas (V)` was `None` even though `I_meas (A)` and commanded voltage were valid.
- Immediate classification: no clean forming and no retained conductive state; weak/open-like or contact-edge coupling. The extra RESET and SET are uncertain unintended stress and are preserved, not silently repeated.
- Operational cause: control-flow bug after unmet forming gate plus a parser that incorrectly required measured voltage for constant-bias current reads.
- Speculative mechanistic cause: none established; pA/nA voltage response may be marginal physical coupling, routed leakage, or very-high-HRS conduction.
- Prevention strategy: make the unmet-forming stop unconditional; treat sub-100 nA response at the highest forming tier as weak/contact-edge rather than sufficient contact; advance bounded Z only after preserving the full tier result; parse constant-bias reads from `I_meas` with commanded-voltage provenance when measured voltage is absent; unit-test both branches before restart.
- Recovery strategy: cleanup and retract completed; Keithley/Keysight outputs off, 707B open/`nil`, light off, stage `[0,0,-175]`, Zaber `(379893,851405)`. Do not repeat completed operations. If continuation is authorized under the parent optimization request, restore to the next untested Z position (`-70`) and resume at the low forming tier with corrected gates.
- Outcome: initial runner stopped safely before further conditioning. The user explicitly authorized continuation on Device 1 while retaining the incident record. The corrected runner resumed from the next untested Z position, achieved clean forming at Z `+30` and `+1.90 V` on the `10 µA` tier, then completed six conditioning pairs without stable convergence. No further unintended operations occurred.
- Tally update: runner control-flow/parser incident causing post-gate unintended stress: +1.

### 2026-09-17 — excessive Zaber-X position damaged OpenFlexure Y axis

- Failure-mode label: mechanical coarse-stage collision / OpenFlexure Y-axis damage.
- Artifact paths:
  - Holder scan: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/runs/holder_calibration/right_edge_top_bottom_scan_20260917T075300Z/`
  - Emergency safe-state record: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/runs/holder_calibration/mechanical_incident_safe_state_20260917.json`
  - User-provided incident image: `/home/amdm/.hermes/cache/images/img_3b826b4e91b8.jpg`
- Context: holder-edge mapping was attempted with OpenFlexure tracked at `[0, 0, -200]`. The aligned coarse-stage reference was Zaber `X=769055`, `Y=712657`; subsequent automated scanning held X fixed and varied Y. The installed-system coarse-X clearance envelope had not been physically validated.
- Evidence: the user confirmed that excessive Zaber X travel drove the OpenFlexure assembly into a fixture underneath the probe-station platen; the resulting obstruction broke the OpenFlexure Y axis. The supplied camera image is severely defocused/occluded and does not independently resolve the fractured component; the user's direct physical observation establishes the collision and damage. No further motion was commanded after notification.
- Immediate classification: safety-critical mechanical collision/damage caused by an unmodeled under-platen fixture; not a DUT electrical failure.
- Confirmed operational cause: the installed fixture beneath the probe-station platen obstructed the motion envelope at excessive Zaber X. CAD-derived holder geometry and tracked Z retraction were incorrectly treated as sufficient clearance evidence, and the coarse X position was accepted without an under-platen inspection, installed-system collision check, or validated X hard limit.
- Speculative mechanistic cause: do not infer the exact failed flexure/actuator component from the blurred image; physical inspection is required.
- Prevention strategy: prohibit all Zaber/OpenFlexure motion until repair and recommissioning. After repair, establish conservative installed-system Zaber X/Y hard limits by physical dry-run, including the entire OpenFlexure/probe/cable envelope; enforce those limits in every runner before any move. Never extrapolate full-holder travel from CAD dimensions or assume tracked Z alone guarantees coarse-stage clearance.
- Recovery strategy: no automated recovery. De-energize motion hardware before manual inspection; do not home, zero, jog, or attempt an automatic return. Inspect/repair the OpenFlexure Y mechanism, then recommission with no-load low-speed tests and optical sign/magnitude validation before restoring holder scans.
- Outcome: motion frozen. Keithley output disabled, 707B opened with closed channels `nil`, light turned off; Keithley, matrix, light, stage, and Zaber reported idle with `run_id: null`. Mechanical repair pending.
- Tally update: mechanical coarse-stage collision / OpenFlexure-axis damage: +1.

### 2026-09-15 — third-left contact-gate identifiability and SCPI configuration warning

- Artifact: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/runs/pea_current_plus5_campaign_20260915/contact_method_iteration01/analysis.json`.
- Classification: protocol/contact-identifiability issue, NOT new device failure or proven open contact. Current device retained at Stage -90; no mechanical motion or stress during diagnostic.
- Evidence: three fixed-Z paired matrix-open/routed batches, 108 measured voltage/current/time records, 0/±10/±50 mV, requested 1 µA limit. Routed-minus-open conductance 531.9 pS (95% batch-t CI 480.3–583.4) at ±10 mV and 569.8 pS (559.2–580.4) at ±50 mV. Routed zero offset 24.01 pA; matrix-open -2.44 pA. No near-requested-compliance or voltage collapse.
- Operational cause: prior arbitrary 1 nA contact/initialization floor cannot identify high-HRS contact. A semicolon-delimited route readback caused one safe local parser stop, corrected after cleanup; one extra 18-point upstream reference preserved. Final instrument error query returned -113 Undefined SCPI header; offending configuration command not isolated, full settings acceptance not independently verified.
- Mechanistic alternatives: downstream cable/matrix/probe leakage or actual DUT/contact conductance; matrix-open alone does not separate these.
- Prevention: never use absolute pA/nA current alone as contact proof/failure; use batch-level paired slopes, actual buffer V/I/time, matched routed lifted-probe reference, and inspect instrument errors before stress.
- Recovery: completed low-bias differential diagnostic only; recommended parent-coordinated optically verified lift/reference/recontact A/B, not executed. Resolve SCPI configuration acceptance before stress.
- Outcome: upstream-only leakage insufficient to explain routed response, physical contact remains unproven. Both SMU-off acknowledged, matrix nil read back, lights off and all six idle/null. No edge restart or origin reset.
- Tally update: no DUT failure tally increment; one protocol/contact-diagnostic incident recorded separately here.

### 2026-09-15 — bounded resume confirms unstable RESET initialization, no persistent ON

- Artifact path: `/home/amdm/data/vipsa/legacy/windows-backup/vipsa-puda-project/runs/constrained_bo_resume_20260915T1147/REPORT.md` and `verified_metrics.json`; original history retained in linked gate/initialization runs and combined_records.csv.
- Context: approved no-motion resume at historically supplied Z=-135; RESET -2 V ×5, 100 µA; SET 0.4/0.6/0.8 V, shared SET/read 10 µA, read +0.1 V, nominal list dwell 50 ms.
- Evidence: prior marginal baseline rejection 25.26% was replaced successfully at 0.6 V (new trial 8 drift 6.71%). One valid 0.8 V trial followed; trials 10 and 11 baseline drift 31.41% and 29.77% exceeded unchanged 25% gate; SET withheld on both. Two consecutive new failures triggered stop. Totals 11/240 budget attempts, 7 valid SET/read trials, 3 rejections, 55 RESET pulses, 7 SET pulses; 0/7 persistent ON at >=3×, ratios 0.648–1.555; reads 48.476–172.972 nA, zero 9 µA read stops.
- Immediate classification: unstable initialized baseline and unvalidated persistent state separation; not hard-short or demonstrated permanent damage.
- Operational cause: original fixed-repeat loop incorrectly stopped a whole anchor after a single marginal rejection. Approved resume used valid-count targeting with bounded replacements and preserved all prior stress accounting. Remaining failure is measured repeat drift, not merely the old loop bug.
- Mechanistic cause: uncertain; time-dependent device/ionic response or coupling drift are hypotheses, not established diagnoses. No motion occurred.
- Prevention: distinguish data-acquired validity from persistent switching; no BO before reliable reset/separated states. When replacement is authorized, count every attempted RESET trial toward budget, skip completed anchors, allow bounded replacement without relaxing thresholds, stop repeated failures. Do not repeatedly retry the same device after this stop without fresh authorization.
- Recovery actually attempted: up to two replacements allowed for the missing 0.6 V trial (first succeeded); 0.8 V bounded at five attempts for three valid, but stopped after three attempts because two consecutive baselines failed.
- Timing: saved timestamps reanalyzed without extra calibration stress; persistence spacing 1.100147–1.100251 s; SET sample to first read 0.189846–0.189895 s. Exact physical width/RESET-end relaxation unverified; freeze waveform and exclude relaxation from optimization, never call host latency physical relaxation.
- Outcome: 0.6 V anchor completed, 0.8 V incomplete (1/3 valid), BO disabled. Tracked runner exited; both SMU-off and light-off acknowledged, 707B open-all then nil readback, all lifecycle states idle/null; independent follow-up state file saved.
- Tally update: unstable RESET initialization / no separated persistent pulse states = 1 campaign (continuation, not an additional damaged device).

### 2026-06-22 — contact-edge approach did not stabilize inside 0.5–1 nA gate

- Failure-mode label: open/weak contact edge; final guarded approach fell below lower current gate.
- Artifact paths:
  - `/home/vipsa/vipsa-puda-project/runs/approach_one_dciv_20260622T105924Z/summary.json`
  - `/home/vipsa/vipsa-puda-project/runs/approach_one_dciv_20260622T105924Z/approach_summary.json`
- Context:
  - Keithley-guided contact approach at `10 mV`.
  - Requested valid contact gate: `0.5–1.0 nA`.
  - Z step used in continuation: `1.0`, with final guard/trim behavior.
- Evidence:
  - Maximum observed current: `1.000232e-9 A`, just above upper gate.
  - Final guarded current: `2.520446e-10 A` = `0.252 nA`, below lower gate.
  - No logged read landed inside the strict `0.5–1.0 nA` window.
  - Final stage readback after continuation: `[0, 0, 202.75]`.
- Immediate classification:
  - Contact edge / weak contact, not stable valid contact under the strict gate.
- Anecdotal / operational cause:
  - Contact transition was sharper than the approach/guard step logic; current jumped just above the upper limit, then the minimum safe retraction left it below lower limit.
- Speculative mechanistic cause:
  - Probe/DUT contact likely has a steep mechanical/electrical turn-on near the pad/electrode interface; tiny Z changes modulate contact area/tunneling/filament access strongly.
- Prevention strategy:
  - Near the contact edge, use minimum supported Z trim increments (`0.25` steps) and bounded re-read after each trim.
  - Do not claim contact unless final low-bias current is inside the requested gate.
- Recovery strategy:
  - User authorized a single `+0.25` Z step followed by DCIV.
- Outcome:
  - `+0.25` Z step moved stage from `[0, 0, 202.75]` to `[0, 0, 203]` and DCIV was executed. Subsequent DCIV revealed a separate over-reset/breakdown-like failure mode below.
- Tally update:
  - Open / weak contact / contact edge: +1.

### 2026-06-22 — over-reset / negative-branch breakdown-like current surge around -1.35 to -1.40 V

- Failure-mode label: over-reset / negative-branch breakdown-like current surge; reset side over-stressed the device.
- Artifact paths:
  - Summary: `/home/vipsa/vipsa-puda-project/runs/z0p25_then_dciv/20260622T111639Z_z0p25_0_1_0_m15_0/summary.json`
  - CSV: `/home/vipsa/vipsa-puda-project/runs/z0p25_then_dciv/20260622T111639Z_z0p25_0_1_0_m15_0/z0p25_dciv_0_1_0_m15_0.csv`
  - Plot: `/home/vipsa/vipsa-puda-project/runs/z0p25_then_dciv/20260622T111639Z_z0p25_0_1_0_m15_0/z0p25_dciv_0_1_0_m15_0.png`
- Context:
  - User requested `+0.25` Z step to ensure contact, then DCIV `0 → +1 → 0 → -1.5 → 0`.
  - Positive/SET compliance: `1e-6 A`.
  - Negative/reset compliance: `1e-5 A`.
  - Stage moved from `[0, 0, 202.75]` to `[0, 0, 203]`.
- Evidence:
  - Negative branch current was roughly flat around `~2e-7 A` from `-1.0` to `-1.30 V`.
  - Abrupt surge:
    - `-1.30 V`: `2.350663e-7 A`
    - `-1.35 V`: `2.879402e-6 A`
    - `-1.40 V`: `7.721093e-6 A`
  - The jump from `-1.30` to `-1.35 V` was about `+1.09 log10`, i.e. >10×.
  - Return branch stayed in the µA range for many points.
  - Reset compliance was not technically reached (`1e-5 A`), but the current surge and sustained high return current are breakdown-like.
  - Post-read at `+10 mV`: `1.76855e-9 A`, so not an immediate hard short, but device/contact was altered.
- Immediate classification:
  - Over-reset / negative-side breakdown-like event, not clean RESET.
- Anecdotal / operational cause:
  - The reset side was too aggressive for this freshly nudged contact/device state: `-1.5 V` with `1e-5 A` allowed current to enter the µA range after a sudden jump around `-1.35 V`.
- Speculative mechanistic cause:
  - Negative bias likely caused runaway filament growth, electrode/ion migration, local Joule heating, or barrier breakdown rather than controlled filament rupture. The `+0.25` Z contact improvement may also have increased effective contact area/pressure, lowering the threshold for destructive negative-bias conduction.
- Prevention strategy:
  - Do not use `-1.5 V` / `1e-5 A` reset on this device class/contact state as a blind full branch.
  - Start reset recovery at lower stress: cap reset voltage at `-0.8` to `-1.0 V`, reset compliance `1e-6 A` or at most `3e-6 A`.
  - Use branch-by-branch execution with inspection gates.
  - Add hard stop criteria: stop reset if current jumps >3–5× in one voltage step, increases by >0.5–1 log10, or enters the µA range unexpectedly.
  - Use post-branch low-bias reads as the success criterion; do not treat a high-current reset branch as successful RESET.
- Recovery strategy:
  - First run only a low-bias health check: `0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`, with low compliance (`1e-7` to `1e-6 A`).
  - If short-like/over-contacted, stop electrical stress and consider `-0.25` Z retraction followed by another low-bias check.
  - If measurable but not shorted, attempt a bounded reset recovery capped before the observed breakdown onset, e.g. `0 → -0.8/−1.0 → 0`, `1e-6 A` reset compliance, with abrupt-jump stop.
  - If it does not recover, mark device as damaged/over-reset and move on.
- Outcome:
  - Recovery not yet attempted at time of entry. Proposed recovery communicated to user.
- Tally update:
  - Over-reset / negative-branch breakdown-like current surge: +1.

### 2026-07-24 — adjacent right-hand device is open/very-high-resistance-like after pre-approach

- Failure-mode label: open / weak contact / very-high-resistance-like.
- Artifact paths:
  - `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/quick_resistance_check_20260724T115119Z/summary.json`
- Context:
  - After moving one device right with Stage Z `-40`, Zaber X `+5000` native units, then Stage Z `+20` pre-approach.
  - Keithley low-bias diagnostic at `0 V`, `±10 mV`, and `±50 mV`; `1 µA` compliance; 3 reads per bias.
- Evidence:
  - Maximum absolute nonzero-bias mean current: `5.12e-11 A`.
  - Paired differential resistance: `1.65 GΩ` at `±10 mV` and `1.56 GΩ` at `±50 mV`; estimate `1.60 GΩ`.
  - No compliance hits; 707B cleanup verified open/`nil`.
- Immediate classification:
  - Open/very-high-resistance-like; insufficient evidence of robust electrical contact.
- Anecdotal / operational cause:
  - Pre-approach ended 20 Z steps short of the prior tracked position after the clearance move; no contact approach was requested or run.
- Speculative mechanistic cause:
  - Probe may remain above the electrode/contact edge, or the DUT may genuinely be in a very high HRS.
- Prevention strategy:
  - Require a live bounded low-bias contact approach before stress measurements on this device.
- Recovery strategy:
  - Run a bounded `+Z` contact approach at `10 mV` toward the active grid-policy `50–500 nA` target window, using `+0.5 Z` while open-like and `0.25 Z` guard trims near the contact edge.
- Outcome:
  - Recovery succeeded. The approach advanced from stage Z `43.25`, crossed abruptly into the `1 µA` read-compliance region, then used guarded retraction/final trim to finish at stage Z `70.5` and `187.537 nA` at `10 mV` (`in_window_after_final_guard`). Net Z displacement was `+27.25 steps`.
  - Approach summary: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/approach_current_device_50_500na_20260724T115346Z/approach_summary.json`
  - Step/current plot: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/approach_current_device_50_500na_20260724T115346Z/approach_step_vs_current.png`
  - Matching CSV: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/approach_current_device_50_500na_20260724T115346Z/approach_step_vs_current.csv`
  - Keithley output-off, 707B open/`nil`, lights off, and idle states were verified.
- Tally update:
  - Open / weak contact / contact edge: +1.

### 2026-07-24 — post-approach low-bias current drifted to compliance before DCIV

- Failure-mode label: over-contact / mechanical short-like contact; low-bias compliance hit.
- Artifact paths:
  - `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/dciv_after_approach_20260724T124311Z/summary.json`
  - `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/dciv_after_approach_20260724T124311Z/dciv_rows.csv`
- Context:
  - Bounded approach ended at `187.5 nA @ 10 mV`, stage Z `70.5`, within the `50–500 nA` target.
  - The default DCIV was gated by a fresh `10 mV`, `1 µA` precheck.
- Evidence:
  - Fresh precheck measured `9.999907e-7 A`, at read compliance.
  - DCIV aborted before stress (`0/121` sweep points).
  - Keithley output-off and 707B open/`nil` cleanup succeeded; machines ended idle.
- Immediate classification:
  - Short-like/over-contacted at low bias; apparent resistance is only a bound (`≤~10 kΩ`).
- Anecdotal / operational cause:
  - Contact conductance changed substantially after approach completion despite no commanded Z change, consistent with settling/contact creep.
- Speculative mechanistic cause:
  - Probe pressure/contact area may have increased during dwell, or a conductive pathway evolved under repeated approach reads.
- Prevention strategy:
  - Recheck low-bias current immediately before every DCIV and keep the compliance gate.
- Recovery strategy:
  - If authorized, retract `-0.25 Z` and repeat the low-bias diagnostic before reconsidering DCIV.
- Outcome:
  - Safety gate worked; no DCIV stress was applied.
- Tally update:
  - Over-contact / mechanical short-like contact: +1.

### 2026-07-25 — S9 device 5 contact edge jumped to read compliance and stayed high after bounded trim

- Failure-mode label: recurrent over-contact / mechanical short-like contact at a steep contact edge.
- Artifact paths:
  - `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/approach_step1_20260725T151730/summary.json`
- Context:
  - Standalone bounded approach at `10 mV`, `1 µA` read compliance, from stage Z `300` on the aligned S9 device-5 position.
  - Target used by the standalone approach was `10–100 nA`; the subsequent grid continuation uses the stricter stable `1–10 nA` gate.
- Evidence:
  - At Z `358`, current was `6.874139e-11 A`.
  - One `+1 Z` move to Z `359` produced `9.9999e-7 A`, pinned at read compliance.
  - Twenty guarded `-0.25 Z` trims retracted a total of `5 Z` to final Z `354`, but the final read remained `9.999906e-7 A`.
  - Cleanup left Keithley output off, 707B open/`nil`, lights off, and machines idle.
- Immediate classification:
  - Mechanical over-contact/contact-edge short-like recurrence; uncapped current and true resistance are unknown because the read was compliance-limited.
- Anecdotal / operational cause:
  - A `+1 Z` coarse step crossed an unusually abrupt contact transition; conductance then persisted during the bounded 5-step trim.
- Speculative mechanistic cause:
  - Contact settling/creep, pad deformation, or a pressure-sensitive conductive pathway may have made the contact hysteretic after crossing the edge.
- Prevention strategy:
  - Require three unchanged-Z reads inside `1–10 nA` before DCIV/pulses.
  - Preserve immediate over-current stop and guarded `-0.25 Z` retraction; do not treat a compliance-clamped reading as valid contact.
- Recovery strategy:
  - On overwrite continuation, start with a fresh `10 mV` read and bounded `-0.25 Z` retraction until the stable `1–10 nA` gate is met; otherwise use the configured three bounded attempts and skip stress if stability never passes.
- Outcome:
  - Standalone trim did not recover before its bound; fresh guarded recovery is being handed to the device-5 grid continuation.
- Tally update:
  - Over-contact / mechanical short-like contact: +1.

### 2026-09-12 — newly loaded PEA device remained open-like after bounded +60 Z approach

- Failure-mode label: open / weak contact after bounded approach.
- Artifact paths:
  - Interrupted first segment: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/vipsa_approach_pea_contact_approach_20260912T073006Z/`
  - Completed continuation: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/vipsa_approach_pea_contact_approach_continue_after_timeout_20260912T073922Z/approach_summary.json`
- Context:
  - Newly loaded PEA devices; user clarified these are not expected to have high pristine resistance.
  - Keithley-guided approach at `+10 mV`, target `1–10 nA`, `1 µA` compliance, `+0.5 Z` coarse steps, lights off.
  - The first runner was interrupted by the foreground tool timeout after 103 verified moves; cleanup was forced and verified before a bounded continuation to the original 120-move limit.
- Evidence:
  - Initial current: `3.106888e-11 A` at `+10 mV`.
  - After `+51.5 Z`: `2.664955e-11 A`.
  - Final stage readback: `[0, 0, 60]`, representing cumulative `+60 Z` from the run start.
  - Final current: `2.429722e-11 A`, far below the `1 nA` lower gate, with no meaningful rise across the approach.
  - Cleanup succeeded: both SMU outputs off, 707B open with closed channels `nil`, lights off, and stage/electrical/light machines idle with null run IDs.
- Immediate classification:
  - No electrical contact established within the bounded approach; open/weak-contact-like for this PEA device.
- Anecdotal / operational cause:
  - The newly loaded sample may not yet be at the expected probe height or the probe may not be over an electrically connected active pad.
- Speculative mechanistic cause:
  - A persistent physical gap, pad misalignment, or missing electrode coupling could keep the measured current at the leakage/offset floor.
- Prevention strategy:
  - Before extending Z travel beyond this bound, inspect Camera-1 alignment and confirm the visible probe tip is over the intended PEA pad; reconcile sample/loading height and stage reference.
- Recovery strategy:
  - Stop at the bounded limit and retain safe cleanup. Re-align or verify mechanical height before authorizing any further forward Z travel.
- Outcome:
  - No contact after cumulative `+60 Z`; no electrical stress beyond the `10 mV` approach reads.
- Tally update:
  - Open / weak contact / contact edge: +1.

### 2026-09-14 — PEA high-compliance DCIV produced a persistent short-like state

- Failure-mode label: perma-SET / electrically induced hard short-like state after high-compliance sweep.
- Artifact paths:
  - DCIV summary: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/pea_dciv_0_1_0_m2_0_step20mV_set1mA_reset10mA_20260914T110441Z/summary.json`
  - DCIV CSV: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/pea_dciv_0_1_0_m2_0_step20mV_set1mA_reset10mA_20260914T110441Z/dciv.csv`
  - Semilog plot: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/pea_dciv_0_1_0_m2_0_step20mV_set1mA_reset10mA_20260914T110441Z/dciv_semilog.png`
  - Confirmatory low-bias check: `/home/amdm/vipsa_windows_backup/vipsa-puda-project/runs/quick_resistance_check_20260914T110507Z/summary.json`
- Context:
  - One user-requested `0 → +1 → 0 → −2 → 0 V` sweep, `20 mV` steps, `1 ms` requested dwell.
  - SET compliance `10e-4 A = 1 mA`; RESET compliance `10e-3 A = 10 mA`.
  - Immediately before stress, the `+10 mV` median current was `3.442269e-11 A`.
- Evidence:
  - PF rose to `7.70e-7 A` at `+1 V`, but PB reached the `1 mA` SET compliance at `+0.90 V` and had 42 compliance-limited points.
  - NF/NB remained strongly conductive, peaking near `1.06 mA`; the negative branch never approached its `10 mA` compliance and showed no clean RESET.
  - The immediate `+10 mV` post-read was approximately `112 µA`, showing a several-order conductance increase.
  - A separate canonical `0 V`, `±10 mV`, `±50 mV` check reproducibly reached `1 µA` read compliance at every non-zero bias. At `10 mV`, resistance is therefore only bounded as `≤~10 kΩ`; nominal differential values are not precise because current was clamped.
  - No Z motion occurred between the high-resistance precheck and short-like postcheck.
- Immediate classification:
  - Persistent electrically induced short-like/perma-SET state; not a clean RESET or useful bipolar switching.
- Anecdotal / operational cause:
  - The requested compliance ceilings were 100× higher than the preceding `10 µA/100 µA` DCIV, allowing the conductive state to grow to approximately `1 mA` without recovery.
- Speculative mechanistic cause:
  - High-current filament overgrowth, electrode/ion migration, local Joule heating, or irreversible barrier breakdown may have formed a persistent conductive path.
- Prevention strategy:
  - Do not repeat `1 mA SET / 10 mA RESET` on this device as a default.
  - Retain the low-bias precheck and add branch-by-branch hard stops when return-branch current reaches SET compliance or the negative branch remains in the mA range without read-state recovery.
  - Decide RESET success from low-bias post-reads, not completion of the negative sweep.
- Recovery strategy:
  - Freeze further stress. If explicitly authorized, start with a bounded low-compliance reset-first probe and stop if low-bias reads remain compliance-limited; do not escalate blindly.
- Outcome:
  - Confirmatory check established a persistent short-like state. Keithley output-off, 707B open/`nil`, lights off, and idle states were verified. Recovery stress was not attempted.
- Tally update:
  - Perma-SET / hard short-like low-bias compliance: +1.

### 2026-09-30 — optimization_sub_2 device (1,2): RESET-recovery loss, not a proven short

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r1c2/summary.json`; raw ordered sweeps/read traces and `optimization_sub_2_r1c2_all_21_sweeps_semilog.png` in the same directory.
- Evidence: contact/forming at stage Z −70, +10 V / 100 µA commanded forming (sustained compliance; measured voltage only ~0.467 V at the commanded +10 V endpoint). After RESET to ~1 nA at +0.1 V, three +2 V / 200 µA exact SET trials gave delayed reads 8.08, 2.65, 27.75 µA; two +2 V / 150 µA trials gave 8.55 and 1.02 µA. Final 200 µA anchor shifted strongly upward; two −2 V / 100 µA RESET sweeps left an unclamped +0.1 V read ~7.85 µA, not earlier nA HRS.
- Classification: cumulative-stress-associated RESET-recovery failure / perma-SET-like conductive state; **not** a hard-short claim, because the read was far below 100 µA compliance.
- Operational cause: repeated SET sweeps with 150–200 µA ceilings and marked cycle-to-cycle drift preceded recovery loss. A specific threshold cannot be identified from this one site.
- Mechanism (speculative): filament growth/ionic redistribution or contact drift; unproven.
- Prevention: use the lower current tier on fresh sites, exact interleaved anchors and same-bias retention reads, and stop after failed bounded RESET rather than escalating into ambiguous conduction.
- Recovery: two identical −2 V / 100 µA RESET sweeps were attempted; full HRS did not return. Further site stress stopped and outputs-off/matrix-open (`nil`) verified.
- Outcome: site retired from optimization; zero endurance cycles. Tally +1 RESET-recovery loss with unclamped conductive read.

### 2026-09-30 — optimization_sub_2 device (1,4): retained SET disappeared at endurance entry

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r1c4/summary.json`; first endurance trial and verified cleanup in `r1c4/endurance_2V150uA_reset_m2V100uA/`.
- Evidence: stage Z −70, +10 V / 100 µA forming produced ~7 µA delayed +0.1 V read. Three exact +2 V / 150 µA SET trials retained 1.86, 3.26, 13.46 µA at 1 s; each recovered ~1 nA after one −2 V / 100 µA RESET. At the first endurance SET, commanded +2 V was delivered (measured 1.999958 V; peak ~9.73 µA), but immediate and 1 s +0.1 V reads were ~1 nA. There was no subsequent RESET and no complete endurance cycle; Keithley off and 707B open/`nil` were verified.
- Classification: loss of retained SET or contact-dependent coupling (unresolved), not confirmed permanent open/short. The apparently strong screening ratios did not survive the first endurance attempt.
- Operational cause: repeated preceding forming/SET/RESET may have changed the site or contact; no post-failure lifted-probe control was acquired.
- Mechanism (speculative): volatile/unstable filament or probe contact drift; not distinguishable here.
- Prevention: do not treat three directionally correct but widely varying current magnitudes as stable yield; gate endurance on every delayed SET read and stop at the first loss rather than counting a cycle.
- Recovery: no stress retry after failed retained SET; outputs-off/matrix-open verified and site retired. Outcome: zero complete endurance cycles; tally +1 no-retention after switching-like event.

### 2026-09-30 — optimization_sub_2 device (1,6): 125 µA SET failed exact retained repeat

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r1c6/summary.json`; raw ordered traces, 100-read files, cleanup logs, and `optimization_sub_2_r1c6_all_5_sweeps_semilog.png` in the same directory.
- Evidence: verified optical tip/pad alignment at stage Z −150, bounded pre-approach and Z −70 contact/forming. Forming +10 V / 100 µA had sustained compliance from commanded +2.25 V and measured only 0.384 V at commanded +10 V; delayed +0.1 V read was ~11.8 µA. One −2 V / 100 µA RESET recovered ~1.35 nA. First +2 V / 125 µA SET retained 17.8 µA at 1 s and 14.6 µA at read 100, then RESET recovered ~1.4 nA. Exact SET repeat hit stress compliance but produced ~1 nA at immediate, 1 s, and read 100; no second RESET or endurance was run. Low-bias reads were not compliance-clamped. Output-off and 707B open/`nil` were verified, then stage retracted from −70 to −150 with live position readback.
- Classification: non-repeatable retained SET / no-retention after switching-like event; contact-dependent coupling remains an alternative to intrinsic device failure. No confirmed hard short/open.
- Operational cause: site-specific instability after forming and one full SET/RESET pair despite reducing SET compliance from 150 to 125 µA; not a proof of compliance causality.
- Mechanism (speculative): volatile conduction, contact drift, or unstable filament.
- Prevention: require exact repeated same-bias retained reads and avoid interpreting the compliance plateau as a working SET; continue to a fresh eligible site rather than repeating stress on a nonretentive one.
- Recovery/outcome: no additional stress attempted after failed repeat; site retired, zero endurance cycles. Tally +1 no-retention after switching-like event.

### 2026-09-30 — optimization_sub_2 device (1,8): higher compliance, volatile negative-return conduction

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r1c8/summary.json`, ordered sweep/read traces, and `optimization_sub_2_r1c8_all_10_sweeps_semilog.png`.
- Evidence: +10 V / 100 µA forming at Z −70; initial −2 V / 100 µA RESET recovered ~1 nA. +2 V / 300 µA SET retained 25.1 µA at 1 s; −2 V / 100 µA RESET pinned current and left ~2.26 µA, then −2 V / 300 µA RESET recovered ~1.2 nA. Exact +2 V / 300 µA SET/RESET repeat retained 21.2 µA and recovered ~1.2 nA; a third exact SET reached full measured +2 V without reaching 300 µA yet failed to retain (~1.6 nA). +3 V / 300 µA SET retained 19.3 µA at 1 s, but −2 V / 300 µA RESET showed ~0.97 µA at −2 V on the forward branch and ~100 µA immediately on return; +0.1 V/1 s stayed ~4.1 µA before later relaxing to ~1.2 nA.
- Classification: nonrepeatable retained SET and volatile negative-return conductance; failed specified 1 s RESET-read gate, but later relaxation means not a proven permanent short. Contact change cannot be excluded.
- Prevention: inspect measured-voltage forward and return branches, not just RESET peak or compliance; do not raise RESET compliance after full-voltage recovery fails without clamping. No endurance; outputs off, matrix open/`nil`, and retract to Z −150 verified. Tally +1 volatile negative-return conductance.

### 2026-09-30 — optimization_sub_2 device (2,8): higher-compliance retained SET without RESET recovery

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c8/summary.json`, ordered sweep/read traces, and `optimization_sub_2_r2c8_all_7_sweeps_semilog.png`.
- Evidence: formed at Z −70 with +10 V / 100 µA; 100 µA RESET pinned at measured −1.01 V/commanded −2 V and left ~10 µA, 300 µA RESET pinned at measured −1.61 V and left ~49 nA, and 500 µA RESET reached −2 V and restored ~1.2 nA. +2 V / 500 µA SET retained 43.7 µA at 1 s and 39.3 µA at read 100 (same +0.1 V; below 100 µA read compliance). Two −2 V / 500 µA RESET sweeps reached full voltage without 500 µA clamping but left ~9.3 and ~8.9 µA at 1 s.
- Classification: RESET-recovery loss with unclamped conductive read, not a proven hard short; no qualified endurance. Repeating RESET without the HRS gate did not improve recovery. Contact change remains possible.
- Prevention/outcome: do not blindly increase compliance once RESET reaches full voltage without clamping; site retired, outputs off, matrix open/`nil`, and Z −150 retract verified. Tally +1 RESET-recovery loss.

### 2026-09-30 — optimization_sub_2 device (2,7): first contact at relative-height pre-approach; higher-SET RESET recovery loss

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c7/summary.json`, ordered sweep/read traces, and `optimization_sub_2_r2c7_all_5_sweeps_semilog.png`.
- Evidence: after prior device contact Z−70 and partial retract to −150, a further −20 reached Z−170; adjacent serpentine move/optical alignment, then +80 reached Z−90. First +10 V/100 µA forming at −90 had sustained compliance and post-forming +0.1/+0.2 V reads ~7.0/~13.3 µA; no +5 approach step was needed. Initial −2 V/100 µA RESET restored ~1.4 nA. +2 V/300 µA SET reached measured +2 V without hitting 300 µA and retained ~27.8 µA at 1 s, ~24.3 µA at read 100. Subsequent −2 V/100 µA RESET was current-clamped at ~−0.534 V and left ~21.6 µA. −2 V/300 µA RESET reached full measured voltage without 300 µA clamp but left ~1.21 µA at +0.1 V/1 s.
- Classification: incomplete RESET recovery with unclamped conductive read, not proven hard short. The formed contact-like response occurred already at the relative-height pre-approach, so the user-requested movement rule was exercised without further Z advance. Contact change still cannot be wholly excluded.
- Prevention/outcome: inspect commanded versus measured RESET endpoint; raise RESET compliance only after clamp-limited failure, then stop escalation if full voltage is reached but HRS remains unrecovered. Site retired; no endurance. Electrical output-off and matrix-open/`nil` were verified after each phase. Tally +1 RESET-recovery loss.

### 2026-09-30 — optimization_sub_2 device (2,6): approach found contact on fifth +5 step, initial RESET did not retain HRS

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c6/summary.json`, five ordered forming sweeps/read checks, three RESET traces/read checks, and `optimization_sub_2_r2c6_all_8_sweeps_semilog.png`.
- Evidence: from prior contact Z−90, verified −100 retract to Z−190; adjacent serpentine move/optical alignment; +80 pre-approach to Z−110. Forming at Z−110, −105, −100, −95 was full-voltage low-nA/open (~5–6 nA at +10 V; sub-nA at +0.1 V). At Z−90 on fifth forming cycle, sustained 100 µA compliance appeared and +0.1/+0.2 V delayed reads were ~29/~65 µA. Initial RESET at −2 V/100 µA was clamped at measured −0.658 V, left ~2.5 µA. RESET at −2 V/300 µA was clamped at −0.914 V, left ~37 µA. RESET at −2 V/500 µA reached full measured −2 V, but +0.1 V delayed reads rebounded from ~9.5 to ~21.8 µA; no retained HRS baseline.
- Classification: incomplete RESET recovery with unclamped conductive read after the 500 µA attempt, not proven hard short; no SET candidate or endurance was run because HRS did not recover. Volatile negative-bias state is possible.
- Prevention/outcome: retain the one-step-at-a-time +5 forming/contact gate and stop Z at the first credible contact response; do not escalate RESET further when a full-voltage trace still leaves a conductive read. Outputs off/matrix open with empty-channel readback after each phase. Tally +1 RESET-recovery loss.

### 2026-09-30 — optimization_sub_2 device (2,5): retained 300 µA SET not repeatable; +3 V SET left compliance-limited RESET branch

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c5/summary.json`, `approach_forming_gate.json`, all ordered traces and reads, `optimization_sub_2_r2c5_all_16_sweeps_semilog.png`.
- Evidence: from prior contact Z−90, verified −100 retract to −190; adjacent serpentine move, camera align, then +80 to −110. Forming at Z−110 through −90 stayed open; sixth forming at Z−85 gave sustained 100 µA compliance with ~22.5/~50.2 µA 0.1/0.2 V reads. −2 V / 100 µA RESET established ~1 nA HRS. +2 V / 150 µA SET was volatile (~12 µA immediately, ~1 nA at 1 s). +2 V / 300 µA SET retained ~35.8 µA at 1 s and ~32.3 µA by read 100; an intervening 100 µA RESET failed, but 300 µA RESET restored ~1 nA. Exact +2 V / 300 µA SET repeat failed (~1 nA). +2 V / 500 µA SET also failed to switch at full measured voltage. +3 V / 500 µA SET retained ~53 µA at 1 s and ~73 µA at read 100, then −2 V RESET at 300 and 500 µA was clamped to ~−0.538 and −0.745 V, with +0.1 V read increasing to ~57.5 µA.
- Classification: 300 µA candidate failed exact repeat; 3 V/500 µA candidate failed RESET recovery with compliance-limited negative branch and rising low-bias current. Not a proven hard short. No qualified endurance cycles.
- Prevention/outcome: stop electrical stress before read compliance, report SET/RESET/read compliance separately, never infer a qualified cycle from the isolated retained SET. Outputs off and matrix open/`nil`, Z−100 retract to −185 verified. Tally +1 compliance-limited RESET-recovery loss.

### 2026-09-30 — optimization_sub_2 device (2,4): two recoveries, third RESET compliance-limited

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c4/summary.json`, `approach_forming_gate.json`, ordered traces/reads, and `optimization_sub_2_r2c4_all_13_sweeps_semilog.png`.
- Evidence: contact-like forming response only at Z−80 on attempt six. A −2 V / 100 µA RESET restored ~1.4 nA baseline. At +2 V / 300 µA SET, the first two cycles retained ~26.0 and ~32.4 µA by read 100; −2 V / 300 µA RESET recovered ~1.29 and ~0.94 nA at 1 s, respectively. A third identical SET retained ~18.8 µA by read 100, but RESET clamped at measured −0.956 V / 300 µA and the delayed +0.1 V read remained ~10.9 µA. No read reached 100 µA compliance. Measured full SET voltage varied between cycles, so identical commands do not imply identical physical stress.
- Classification: exact same-device repeatability failed at third RESET; compliant negative branch with conductive post-read, not a proven permanent hard short. No recipe qualification or endurance.
- Cause: operationally cumulative stress/state dependence across cycles; filament dynamics or contact evolution remain hypotheses, not established mechanisms.
- Prevention/outcome: stop RESET escalation when recovery fails; gate qualification on multiple full cycles and delayed unclamped reads, then reproduce on held-out pads. Both SMU outputs off, 707B open/`nil`, and verified Z−100 retract from contact −80 to −180. Tally +1 compliance-limited RESET-recovery loss.

### 2026-09-30 — optimization_sub_2 device (2,3): no contact within bounded approach

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c3/summary.json`, `approach_forming_gate.json`, Camera 1 nominal/alignment frames, and five-sweep semilog plot.
- Evidence: optical same-pad alignment at safe Z−180, +80 pre-approach to −100, then forming/contact checks at Z−100, −95, −90, −85, −80. All five +10 V traces reached full measured voltage with ~5.7–6.0 nA and no 100 µA compliance events; 0.1/0.2 V reads remained ~0.5–0.7 nA without bias scaling. No SET/RESET attempted.
- Classification: no electrical contact established inside the declared Z bound; not evidence that the pristine DUT is intrinsically open or damaged. Physical contact vs very high HRS is unresolved.
- Cause: optical overlap alone does not prove Z contact; local pad height/contact variation is plausible but unverified.
- Prevention/outcome: do not push +5 beyond the bound or form repeatedly without contact-dependent evidence. Both outputs off, matrix open/`nil`, Z−100 retract to −180 verified; site skipped/retired for this pass. Tally +1 open/weak contact/contact edge.

### 2026-09-30 — optimization_sub_2 device (2,2): second adjacent pad without contact within bound

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c2/summary.json`, `approach_forming_gate.json`, Camera 1 alignment frames, and five-sweep semilog plot.
- Evidence: verified same-pad optical alignment at Z−180, +80 pre-approach and five forming/contact checks Z−100 through −80. All +10 V traces reached full voltage at ~5.7–6.0 nA with no 100 µA compliance events; 0.1/0.2 V reads ~0.5–0.8 nA without a contact-dependent transition. No SET/RESET attempted. This repeats (2,3)'s bounded no-contact outcome.
- Classification: no contact established inside declared Z range; not proven intrinsic open DUT. Two consecutive adjacent pads motivate review of contact-height policy rather than extending forward Z autonomously.
- Cause: surface-height variation or optical/physical contact mismatch plausible; unresolved without a safer differential contact diagnostic.
- Prevention/outcome: pause campaign after cleanup instead of more blind +10 V forming or wider Z search. Both outputs off, matrix open/`nil`, Z−100 retract to −180 verified. Tally +1 open/weak contact/contact edge.

### 2026-10-01 — optimization_sub_2 device (2,1): third adjacent no-contact pad after bounded search

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r2c1/summary.json`, `approach_forming_gate.json`, nominal Camera 1 frame, and `optimization_sub_2_r2c1_all_5_sweeps_semilog.png`.
- Evidence: actual probe apex optically over intact pad; Z−180 live travel readback, then +80 to −100 and five checks at −100, −95, −90, −85, −80. Full measured +10 V at ~5.72–6.12 nA, no 100 µA compliance; 0.1/0.2 V reads ~0.48–0.77 nA without contact-dependent response. No SET/RESET.
- Classification: contact not established by bounded Z−80, not proof of intrinsic device open. Repeated near-identical response across (2,3), (2,2), (2,1) suggests a common contact path or height issue, not confirmed.
- Cause: operationally the preapproach/search height may not reach the electrode; optical overlap does not establish vertical contact. Probe path or high-HRS response remain alternative hypotheses.
- Prevention/outcome: do not increase Z limit without a live clearance/contact diagnostic; retract by −100 to Z−180, outputs off, matrix open/`nil`. Tally +1 open/weak contact/contact edge.

### 2026-10-01 — optimization_sub_2 device (3,2): fourth aligned site with same open-like signature

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r3c2/summary.json`, `approach_forming_gate.json`, nominal Camera 1 frame, and `optimization_sub_2_r3c2_all_5_sweeps_semilog.png`.
- Evidence: fresh Stage/Zaber readback and same-pad optical overlap; +80 preapproach from verified Z−180, five checks through Z−80. Full measured +10 V at ~5.66–6.01 nA, no 100 µA compliance; 0.1/0.2 V reads ~0.48–0.77 nA without Z-dependent transition. No SET/RESET.
- Classification: no contact-dependent electrical coupling within bound, not proven intrinsically open. Identical behavior in next row increases suspicion of common probe-height/routing issue.
- Cause: probe physical standoff, shared path leakage, or high-HRS response are hypotheses; optical images alone cannot distinguish them.
- Prevention/outcome: stop site consumption and diagnose the contact path using non-stressing low-bias routed/matrix-open/probe-lifted comparisons and visible height/clearance; do not widen Z autonomously. Light and both SMUs off, 707B open/`nil`, Z−100 retract to −180 verified. Tally +1 open/weak contact/contact edge.

### 2026-10-01 — optimization_sub_2 (3,2) manual Z−60 contact correction and third-SET delayed instability

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r3c2/summary.json`, `manual_contact_*_trace.json`, `manual_contact_*_reads.json`, and `optimization_sub_2_r3c2_all_14_sweeps_semilog.png`.
- Evidence: user physically confirmed contact after moving from the prior Z−180 safe retract to live Stage Z−60 at unchanged Zaber (375791,830008). A single +10 V / 100 µA forming check then measured only +0.290 V at 100 µA, with ~0.6–0.8 µA +0.1 V postreads, versus the earlier five full-voltage ~6 nA traces at Z−100 to −80. Initial −2 V / 100 µA RESET reached full voltage, leaving ~1 nA read. +2 V / 150 µA SET did not retain. +2 V / 300 µA SET gave ~2.21 and ~2.57 µA at read 100 on the first two repeats, each followed by full-voltage −2 V / 100 µA RESET and ~1 nA read. Third identical SET had reads 1–78 near nA and reads 79–100 near 3.7 µA at the same +0.1 V; third RESET again restored ~1 nA without compliance.
- Classification: old absolute Z−80 ceiling was too shallow for this site, not evidence of a failed electrical path or intrinsic DUT open. Two recovered cycles, then delayed/unstable state on the third SET; no reproducible retention qualification or endurance authorization. A mechanism such as intermittent filament/contact evolution remains speculative.
- Prevention/outcome: preserve the manual Z−60 contact as this site's reference, retract −100 relative to it for Z−160 travel (verified dark Camera 2 visible gap), start the next site's +80 pre-approach at Z−80 and bound +5 search through Z−60 with fresh optical/readback checks. Stop stress on unstable read series rather than declaring a successful third cycle; outputs and light off, matrix open/`nil`, Stage Z−160 verified. This corrects the earlier (3,2) no-contact interpretation without adding a separate new open-contact tally.

### 2026-10-01 — optimization_sub_2 (3,4) contact at Z−75; RESET-tier dependence and volatile third SET

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r3c4/summary.json`, all ordered trace/read JSON, and `optimization_sub_2_r3c4_all_9_sweeps_semilog.png`.
- Evidence: after verified Z−160 travel from manually confirmed (3,2) Z−60 contact, Camera 1 showed probe apex over intact pad. +80 preapproach to −80 gave full +10 V/~6 nA; next +5 to Z−75 produced 341 forming compliance hits at 100 µA, measured +0.198 V at commanded +10 V, and +0.1/+0.2 V postreads of ~21.5/~59.7 µA. Initial −2 V/100 µA RESET reached full voltage and ~1–2 nA HRS. +2 V/150 µA SET first pass grew from ~0.6 to ~2.6 µA during 100 reads; 100 µA RESET recovered ~1 nA. Exact command repeat SET retained ~8–9 µA; 100 µA RESET then clamped at measured −0.717 V and left ~8.4 µA; one −2 V/300 µA recovery nearly reached compliance at measured −1.929 V but restored ~1 nA. Third +2 V/150 µA SET gave ~1.5 µA immediately but returned to ~1 nA by delayed read and stayed there for 100 reads. No final 300 µA RESET was applied because no LRS remained.
- Classification: first two passes were not an exact SET/RESET recipe because RESET compliance changed; third SET lacked retention. No qualified recipe/endurance. Not proven permanent short; RESET recovery succeeded once at higher compliance.
- Cause: cumulative stress/filament state or contact evolution possible; not established. Optical alignment and manually corrected contact height mattered, but no mechanism proven.
- Prevention/outcome: keep SET at 150 µA only as candidate; require consistent delayed same-bias retention and exact repeat plus RESET and held-out device before endurance. Stop after volatile third SET; lights and both SMUs off, 707B open/`nil`, relative −100 retract from contact Z−75 to verified Z−175. Tally +1 no-retention after switching-like event.

### 2026-10-01 — optimization_sub_2 (3,6) contact at Z−90; initial RESET failed independent readback

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r3c6/summary.json`, two forming sweeps and one RESET trace with independent postreads, `optimization_sub_2_r3c6_all_3_sweeps_semilog.png`.
- Evidence: from (3,4) contact Z−75, verified relative −100 to travel Z−175; camera-confirmed intact (3,6) pad, then +80 to Z−95. First +10 V forming response ~6 nA full-voltage; +5 to Z−90 gave 100 µA compliance (measured +0.367 V at commanded +10 V), +0.1/+0.2 V reads ~22.2/~51.9 µA. Initial −2 V/100 µA RESET clamped at measured −0.609 V, with immediate +0.1 V reads 2.21 µA, 8.1 nA, 2.0 nA. A separate 10-read +0.1 V verification returned mostly 2.4–2.6 µA, so the apparent HRS in the last two immediate reads was transient.
- Classification: failed RESET/read recovery after contact; no SET, no conditioning, no endurance. A permanently hard short or permanent damage is not established from this test.
- Prevention/outcome: inspect independent same-bias readback after transient apparent RESET; stop stress when RESET clamps and conductive reads recur. Both SMUs/light off, matrix open/`nil`, relative −100 retract from contact Z−90 to Z−190 verified. No new no-retention tally (no SET was run).

### 2026-10-01 — optimization_sub_2 (3,8) camera Y correction, contact Z−100, delayed SET

- Artifacts: `data/pratap_samples/runs/optimization_sub_2/r3c8/summary.json`, Camera 1 nominal/aligned frames, all sweep/read traces, `optimization_sub_2_r3c8_all_6_sweeps_semilog.png`.
- Evidence: at XY (345791,830008), Camera 1 apex was just below intact pad; Y−1000 native correction at Z−190 moved pad under apex, with post-image verification and final XY (345791,829008). +80 from Z−190 to −110 then +5 checks: −110/−105 full 10 V/~6 nA, −100 compliance-limited at +0.414 V and +0.1/+0.2 V postreads ~0.885/~8.89 µA. Initial −2 V/100 µA RESET clamped at −1.025 V but independent ten +0.1 V reads stayed ~0.7–1.4 nA. +2 V/150 µA SET immediate ~6.7 µA, delayed ~1.1 µA; first six of 100 reads under 10 nA, later 83 above 0.5 µA, final ~0.875 µA. Single −2 V/100 µA RESET reached full voltage; independent ten reads returned ~1 nA.
- Classification: delayed/unstable SET retention, RESET recovered HRS; no exact repeat or held-out reproduction, no qualified recipe/endurance. Avoid inferring retention from compliance-limited sweep alone.
- Prevention/outcome: alignment must use actual apex, not frame center; preserve site-specific contact Z (row-3 contact heights −60, −75, −90, −100). Stop stress after unstable read series. Both SMUs/light off, 707B open/`nil`, relative −100 retract from contact Z−100 to verified Z−200 at aligned XY.

# Irreversible device-grid optimization with activation history

Use for RRAM/memristor grids where each device requires contact/forming/conditioning before DC-IV or pulse optimization, and stress history makes repeated recipes on one device non-exchangeable.

## Experimental hierarchy

Model and log:

```text
substrate → grid device → contact/forming history → conditioning history → assigned recipe → cycle/read
```

A device is the prospective experimental unit. Cycles estimate within-device stability; they are not independent recipe replicates. Forming and conditioning are irreversible covariates and must accompany every objective vector.

## Staged allocation

Reserve devices before starting for:

- activation/contact pilots;
- discrete space-filling DC-IV recipes;
- discrete space-filling pulse recipes;
- Pareto confirmation on fresh devices; and
- long endurance/retention plus recovery reserve.

Do not consume confirmation/reserve devices merely because an early runner can continue. Reassign only at documented safe decision boundaries.

## Activation as a constrained adaptive phase

- Begin with the least stressful approved forming tier.
- If forming is also the contact detector, separate weak/no coupling from meaningful coupling and clean forming.
- Advance mechanics only within bounded, verified increments while weak; unlock higher electrical tiers only after meaningful coupling without forming.
- Stop on the first clean forming event and record its voltage, compliance, mechanical Z, energy, and trace quality.
- Conditioning is successful only when repeated low-bias state reads meet a predeclared directional separation and stability gate. Large isolated ON/OFF ratios do not establish convergence.
- Preserve all unintended or partial operations in cumulative stress; never silently repeat them.

## Objective vector and feasibility

Keep separate objectives for:

- valid switching yield;
- median and lower-quantile ON/OFF;
- valid endurance survival;
- retention drift/time-to-threshold;
- multilevel linearity, distinguishable levels, gain symmetry;
- energy and voltage stress; and
- device-to-device variability.

Use hard feasibility labels for open/weak contact, short-like, stuck state, inverted state direction, compliance-limited read, malformed trace, non-converged conditioning, and cleanup/mechanical failures. Do not let a scalar score hide these classes.

## Sequential adaptation

1. Preassign a reproducible discrete maximin or D-optimal DOE plus spatially separated anchors.
2. After each device, write its complete record before changing policy.
3. Adapt only at device boundaries and within approved bounds.
4. Prefer interpretable rule updates during pilots (for example, reducing unnecessary forming stress) over Bayesian optimization.
5. Activate constrained multi-objective BO only after fresh held-out performance and feasibility calibration are adequate.

## Per-device knowledge record

Append after every device:

- absolute/actual location and alignment method;
- contact/forming tiers and mechanical history;
- conditioning pairs and convergence result;
- assigned DC-IV/pulse recipe and actual timing;
- ON/OFF, endurance, retention, multilevel metrics;
- compliance/energy/failure labels;
- raw data and focused plot paths;
- interpretation and exact next-device change;
- cleanup and final positions.

For unattended optimization, continue across routine devices without conversational pauses, but retain all hard safety stops. Report successful or scientifically interesting devices with focused plots and explanations; keep routine failures and learning in the durable knowledge record.

## Plot design

Avoid unreadable all-sweep overlays. A useful activation figure has four panels:

1. peak current versus mechanical position/forming tier;
2. the successful forming sweep with threshold and compliance;
3. post-SET/post-RESET read currents by conditioning pair; and
4. ON/OFF ratio by pair with directional/stability gates.

Label non-convergence honestly even when some individual ratios are very large.

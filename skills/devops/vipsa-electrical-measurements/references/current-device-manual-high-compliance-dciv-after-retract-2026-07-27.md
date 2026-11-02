# Current-device manual split-compliance DCIV after safe Z retract (2026-07-27)

## Trigger

Use this when the user explicitly requests a one-off DCIV on the current manually positioned device, especially after a grid run was stopped and the stage has been safely retracted. Example request:

```text
run a DCIV on the current device, 0->1->0->-1.5->0, set compliance 10mA and reset compliance 100mA, 0.05 step size
```

## Workflow

1. Verify no grid runner is active and all electrical machines are idle/null.
2. Turn lights off and run a non-stressing Keithley precheck before the high-compliance sweep:
   - route DUT to Keithley via 707B
   - read `+10 mV` at `1 µA` compliance
   - force Keithley output off, open 707B, verify `get_closed_channels == nil`
3. If the precheck is short-like / near read compliance, abort and report the high-compliance DCIV as not run unless the user explicitly overrides the safety gate.
4. If the precheck is pA/sub-nA/open-like but the user explicitly requested the DCIV, proceed and record the open-like precondition.
5. Build a non-duplicated row-order-preserving sweep:
   - PF: `0 -> +Vmax` inclusive
   - PB: `+Vmax-step -> 0`
   - NF: `-step -> -Vreset`
   - NB: `-Vreset+step -> 0`
   For `0 -> +1 -> 0 -> -1.5 -> 0` with `0.05 V`, this yields `101` points.
6. Apply positive/PF+PB compliance as the SET compliance and negative/NF+NB compliance as the RESET compliance.
7. Save CSV with `point_index, segment, voltage_v, current_a, abs_current_a, compliance_a`; plot row-order DCIV (`V` vs log `|I|`) plus point-index voltage path. Use `MPLBACKEND=Agg` in the plotting-capable venv for headless rendering; if plotting fails after hardware completes, regenerate from the saved CSV rather than rerunning the sweep.
8. Always cleanup: Keithley output off, Keysight output off, 707B open/nil, light off, final six-machine states.

## Stale-state pitfall

If a stopped grid/direct runner left `light`, `stage`, or `zaber` with `idle` but non-null stale `run_id`, protocol precheck may fail at START before any stress occurs. Follow `vipsa-machine-operations/references/stale-shared-run-id-after-grid-stop-recovery-2026-07-27.md`, then rerun the precheck/DCIV. Report the blocked attempt separately from the successful retry.

## Interpretation note

High requested compliance does not imply compliance was reached. In the observed cases, backed-off/manual-Z-position sweeps remained mostly pA–nA and did not show robust SET/RESET:

- After a large safe Stage-Z retreat, the precheck was `~2.8e-11 A`; the completed 101-point sweep had no SET/RESET compliance hits and currents mostly pA–nA with a single positive-branch µA-scale spike (`max |I| ~2.8e-6 A`).
- After a subsequent `+5` Stage-Z move and repeat of the same `0→+1→0→-1.5→0 V` high-compliance sweep, the precheck was `~3.4e-11 A`, all 101 points completed, no compliance hits occurred, and the maximum current stayed sub-nA (`~9.9e-10 A`).

Report this class of result as weak/open-like/high-HRS/no robust SET-RESET unless the curve clearly shows retained low-resistance state separation.

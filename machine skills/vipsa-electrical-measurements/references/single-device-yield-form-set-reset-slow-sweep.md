# Single-device yield: forming → SET → RESET slow-sweep workflow

Use for a separate device-yield side project when testing one currently probed device with user-specified forming, SET, and RESET cycles at a slow voltage sweep rate.

## Prerequisite gate

1. Treat this as a separate campaign; write artifacts under a dedicated yield-project run directory rather than an unrelated substrate/grid run.
2. Turn illumination off before routing electrical hardware unless the user explicitly latched it on.
3. Verify SMU/switch states, force outputs off, run 707B `open_all`, and confirm closed channels are `nil` before routing.
4. Run the canonical low-bias `0, ±10 mV, ±50 mV` diagnostic before high-voltage forming.
   - Abort on read-compliance-limited/short-like contact unless the user explicitly overrides.
   - Do not reject a very-high-HRS candidate solely because it is sub-nA: paired-bias voltage scaling and consistent differential resistance can distinguish a plausible HRS device from an offset-dominated open contact.
   - Record the precheck artifact and interpretation in the yield-run summary.

## Building a slow stepped sweep

For requested rate `r` and voltage step `ΔV`, use commanded dwell `Δt = |ΔV| / r`. Example: `ΔV=0.05 V`, `r=0.05 V/s` gives `1 s/point`.

**No-dwell priority rule:** if the user subsequently says `no dwell`, that explicit correction supersedes the earlier nominal sweep-rate timing. Set the native-list inter-point delay to exactly `0.0`, remove extra per-point sleeps and unrequested postcheck dwell, and describe timing as **zero commanded dwell**—not as `0.05 V/s`. Instrument integration, autoranging, command overhead, and device dynamics still create nonzero elapsed time; preserve buffer timestamps rather than calling that time dwell.

Prefer a Keithley native voltage-list sweep with current autoranging and low NPLC when nA sensitivity is required. Preserve both commanded dwell/rate and instrument timestamps; call the rate *nominal/commanded* unless timestamps verify the physical point spacing.

### Critical endpoint rule

When compliance changes between polarity or operation, execute each **complete zero-return cycle** as one list:

- `0 → +VFORM → 0` at positive-forming compliance
- `0 → −VFORM → 0` at negative-forming compliance
- `0 → +VSET → 0` at SET compliance
- `0 → −VRESET → 0` at RESET compliance

Do **not** split a cycle into separate forward/backward native lists that begin at the endpoint. Since output is turned off between list calls, starting the return list at `+Vmax` or `−Vmax` can re-enable output as an abrupt zero-to-endpoint step rather than a slow sweep.

### Keithley 2450 SCPI list-command length pitfall

Keep source-list write chunks at **50 points or fewer**, especially for negative voltages. A 100-point negative-voltage `:SOUR:LIST:VOLT` payload can exceed the instrument parser/input limit and be silently rejected while a shorter following `:SOUR:LIST:VOLT:APP` succeeds. The resulting sweep then executes only the tail of the intended list and may enable at a large nonzero voltage. Always verify returned record count **and actual measured/source-voltage endpoints** against the intended path before accepting a cycle. If this occurs, stop, keep outputs off, reduce chunk size, restart the edge to load the driver fix, and rerun only the missing cycle unless the user explicitly authorizes repeating the full electrical history.

### Very-high-HRS autorange timeout pitfall

Keithley native-list duration can substantially exceed `point_count × commanded_dwell`, especially on open/very-high-HRS paths with current autoranging:

- A 401-point **zero-dwell** `0 → +10 → 0 V` sweep took about **187 s**, while a conductive/compliance-limited run finished in about 18 s.
- A 401-point sweep with `1 s/point` commanded dwell timed out after about **431 s** when the VISA budget was only `401 s + 30 s`; `*OPC?` returned no trace records.

Use a timeout budget that includes autorange/integration overhead, not merely programmed dwell. For this class of slow sweep, a proven conservative driver rule is:

```python
timeout_ms = max(600_000, int((delay_s * point_count + 300.0) * 1000))
```

Set the PUDA/orchestration command timeout above the driver budget. Restart the Keithley edge after changing driver code, then verify correct identity, empty error queue, output off, and idle state before retrying into a fresh run directory.

A VISA timeout at `*OPC?` means **records were not recovered**, not that no voltage stress occurred. The instrument may have traversed part or all of the list before the query expired. Record the cycle as `outcome_unknown_after_possible_stress`; do not count it as completed, but also do not call it zero-point/no-stress. Before repeating the cycle, force output off, open/verify the 707B, inspect instrument state/errors, and require explicit retry authorization when repeating may add electrical history. Accept a successful cycle only after exact record count, ordered path, measured endpoints, and cleanup are verified.

## Artifact contract

Save:

- one raw response JSON and normalized CSV per complete cycle;
- one combined ordered CSV with operation/cycle, forward-vs-return branch, commanded/measured voltage, measured current, compliance, and compliance-hit flag;
- partial summary after every cycle so interruption preserves completed data;
- requested and measured timing fields;
- a connected-line DCIV plot with no point markers, preserving acquisition order and branch/operation identity, plus compliance references;
- a low-bias post-test health check unless the user explicitly requested a strict no-dwell/no-extra-measurement sequence;
- final output-off, `open_all`, closed-channels-`nil`, light-off, and idle-state verification.

Never sort sweep rows by voltage: operation order carries the hysteresis history.

## Interpretation

- Compare forming HRS current and SET current against the user's expected scales, but report observed values rather than forcing a yield pass.
- Compliance hits are outcomes, not precise resistance values.
- A SET-like increase without a RESET-like recovery is not a passing reversible device.
- High negative compliance can permanently alter fragile devices; preserve the explicit user authorization and exact compliance per cycle in metadata.

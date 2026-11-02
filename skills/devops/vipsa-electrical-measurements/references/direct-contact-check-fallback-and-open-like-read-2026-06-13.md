# Direct contact-check fallback and open-like read — 2026-06-13

## Trigger

Use this reference when the user asks “is the device in contact?” and the standard low-bias PUDA protocol cannot run because the protocol runner/707B path reports a duplicate START / `RUN_ID_MISMATCH` before commands execute.

Machine-control fallback details live in `vipsa-machine-operations/references/direct-contact-check-protocol-runner-duplicate-start-2026-06-13.md`.

## Measurement recipe

Electrical command sequence remains the standard low-bias contact check:

1. `keithley-2450.set_output(enabled=false)`
2. `keithley-707b.connect_keithley_smu()`
3. `keithley-2450.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=3, reset=True)`
4. `keithley-2450.set_output(enabled=false)`
5. `keithley-707b.open_all()`
6. `keithley-707b.get_closed_channels()`

If the protocol runner cannot start but direct fallback is justified, execute those methods under a direct PUDA/NATS run and verify cleanup.

## Observed interpretation pattern

A 10 mV contact check returned:

```text
I ≈ 6.87e-11 A = 68.7 pA
R_apparent ≈ 146 MΩ
closed channels after cleanup: nil
```

Report this as:

```text
not in contact / very weak contact
far below the 10–100 nA contact target
```

Do not report it as a healthy high-resistance device contact from a single 10 mV read. If the user wants to distinguish open contact from true high-HRS, follow the multi-bias diagnostic in `references/open-vs-high-hrs-contact-diagnostic-2026-06-06.md`.

## Reporting checklist

- Bias voltage and current in A plus pA/nA human units.
- Apparent resistance if nonzero current, but label it as apparent.
- Compare explicitly with the current contact target window.
- Cleanup: Keithley output off, 707B open all, closed channels `nil`.
- Electrical machine states (`keithley-2450`, `keithley-707b`) idle with `run_id: null`.
- If non-electrical machines (`stage`, `light`) are in `error`, report separately and do not let that obscure that the electrical path was cleaned up.

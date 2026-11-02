# Approach-to-DCIV no-contact gate (2026-06-18)

## Trigger

Use this when the user asks for a chained sequence like **“perform approach and run one DCIV sweep”** after optical alignment or device navigation.

## Lesson

A combined approach→DCIV request authorizes the DCIV only after the approach establishes safe electrical contact. If the approach remains open/weak-contact, do **not** run the DCIV at the old/no-contact state just because the user asked for the chain.

## Proven pattern

1. Start `stage`, `keithley-2450`, and `keithley-707b` in one run context.
2. Route DUT to Keithley conservatively:
   - `keithley-2450.set_output(enabled=false)`
   - `keithley-707b.connect_keithley_smu()`
3. Approach with established defaults unless the user supplied overrides:
   - test voltage: `0.01 V`
   - target window: `10 nA <= |I| <= 100 nA`
   - read compliance: `1 µA`
   - forward Z step: `+0.5` with minimum trim step `0.25`
   - bounded max attempts sized to the preceding retraction/pre-move.
4. If final current remains below the lower threshold after the bounded approach, classify as `no_contact_after_max` / weak-open contact and **skip DCIV**.
5. Cleanup regardless of success/failure:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should return `nil`
   - complete the run and verify machine states idle.
6. Report concise facts:
   - final current and threshold comparison
   - net Z motion and stage readback
   - whether DCIV was run or skipped
   - cleanup and idle verification.

## Example outcome

A chained request after alignment moved forward `+60` Z steps but final current stayed around `6.7e-11 A` at `10 mV`, far below the `10 nA` lower threshold. The DCIV was correctly skipped, Keithley output was turned off, 707B was opened, closed channels returned `nil`, and all machines were verified idle.

## Reporting template

```text
👇 Approach attempted, but contact was not established, so I did not run the DCIV sweep.

- Approach target: 10–100 nA at 10 mV
- Z moved forward: +<net_z> steps
- Final current: <I> A, below threshold
- Final stage readback: <position>
- DCIV: skipped for safety because the device is still open/weak-contact
- Cleanup verified: Keithley output off; 707B open_all; closed channels nil; relevant machines idle
```

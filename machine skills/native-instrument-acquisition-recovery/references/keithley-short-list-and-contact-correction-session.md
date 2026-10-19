# Keithley short-list and contact-correction recovery

## Short-list defect and verified fix

A valid five-point RESET waveform was rejected with Keithley error 4920 because the driver configured trace-buffer capacity to the source-list length. The instrument requires buffer capacity of at least 10 readings.

Correct implementation:

```python
smu.write(f':TRAC:POIN {max(10, len(voltage_values))}, "defbuffer1"')
```

Do not modify the five-point voltage array. Continue to validate exactly five returned measurements. Regression tests covered 5→10 capacity and 89→89 capacity. After deployment, output-OFF proofs validated both the 89-point SET and five-point RESET arrays.

## Wire-journal precedence

The ledger's final `error_envelope` contained a later `RUN_ID_MISMATCH` from lifecycle completion, not the useful native command failure. The raw wire journal retained the earlier `source_voltage_measure_current` reply with:

- native verification failure;
- `output_before: 0`;
- expected count 5;
- no returned measurement rows;
- buffer-capacity error before output enable.

Therefore recovery keyed the wire record by exact run ID and command name. This is safer than taking the final ledger exception at face value.

## Zero-exposure reconciliation

The failed RESET was reconciled at 0 J only after all were true:

- failure was before `OUTP ON`;
- output was already OFF;
- no rows existed;
- operation cleanup verified output 0 and matrix nil;
- controller final cleanup independently verified OFF/open;
- all other device operations were resolved.

The failed attempt remained in history with `zero_exposure=true` and `no_replay=true`; cumulative energy was unchanged. The continuation reused the completed SET and due health-read receipts, executed RESET only, computed cycle-1 metrics from old SET + new RESET, and started normal execution at cycle 2.

## Completed sweep with cleanup acknowledgement timeout

A separate reconditioning sweep returned all 121 rows, finite energy was already charged, output readback was 0, matrix readback was nil, but one redundant `set_output(False)` acknowledgement timed out. Independent final cleanup again proved OFF/open. Reconciliation changed only cleanup resolution; it did not replay the sweep or charge energy twice.

## Contact-correction sequence

For an operator-confirmed contact concern during an initial-screen campaign:

1. Reconcile every in-flight operation first.
2. Verify OFF/open and read back the exact pose.
3. Apply the exact authorized Z increment without XY motion.
4. Run only the requested tail of conditioning with fresh operation IDs.
5. Preserve pre-correction candidate history separately.
6. Restart candidate cycle numbering at 1 under the unchanged recipe.
7. Enforce the full minimum-cycle rule on the restarted run.
8. Advance only after terminal cleanup and ledger UNKNOWN checks pass.

Do not infer irreversible DUT failure from poor contrast before or after contact correction; report failure as recipe-specific unless stronger evidence exists.

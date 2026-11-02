# Output-OFF native-list proof with stale measurement range

Use this recovery pattern when a native voltage-list verifier rejects a new high-compliance sweep before output enable because the instrument retains a smaller current measurement range from the previous operation.

## Classification

If the raw response proves output remained OFF and no acquisition rows or reservation energy exist, classify the attempt as `failed_before_hardware_action` / zero exposure. Preserve it; do not label the DUT failed and do not replay completed stress.

## Proven correction

1. Require output OFF and switch matrix open/nil.
2. Make the OFF-only verifier accept the sweep's `current_range` as an explicit parameter.
3. Validate that range is finite and positive.
4. Program `:SENS:CURR:RANG:AUTO OFF` and `:SENS:CURR:RANG <current_range>` before setting `:SOUR:VOLT:ILIM <current_compliance>` and uploading the list.
5. Preserve exact upload tokens/counts, per-index source configuration, error queue, final-zero restoration, and output-OFF proof.
6. Unit-test the command ordering with a stub session, compile, commit/push, deploy the exact edge branch, and verify the live driver fingerprint.
7. Rerun every frozen branch proof. Do not dispatch stress until all branch proofs pass and final output/matrix cleanup is verified.

Observed 2450 failure signature: error 5077, `Cannot change source Limit for measure Range 0.01 A`, when the prior operation left a 10 mA measure range and the next RESET requested about 100 mA source compliance. The correct response is range setup—not weakening compliance/list equality or bypassing the proof.

# Forecasting serial measurement campaigns

## Trigger
A user asks how long earlier sampling/optimization stages took and how long a new multi-device campaign will take.

## Audit before estimating
1. Freeze stage/site scope; exclude later rounds, supplementary re-probes and fresh-substrate retests. Allocated sites, attempted sites, terminal dispositions and successful devices are different counts.
2. Recover first/last execution timestamps from saved command envelopes or operation journals, not file mtimes. State whether boundaries include navigation, final cleanup, verification, administrative closure or final plots.
3. Report summed stage windows separately from first-to-last wall-clock span including interstage gaps.
4. Match wire requests/replies by machine, run, step and command, retaining unmatched requests and errors. Include command names such as `source_voltage_measure_current_continuous_segments`, `source_voltage_measure_current` and `hold_voltage_measure_current` in electrical classification; a substring test for `native` misses these.
5. Union parent/child operation intervals and copied wire logs before summing. Saved electrical snapshots alone do not measure full motion/alignment or all active work. Residual time remains unclassified, not automatically idle or human waiting.
6. Distinguish failed-command duration from full troubleshooting duration. Error counts do not equal unique interruptions.

## Forecast
- Do not promise a speedup simply because procedures improved. Fixed acquisition physics remains; software may reduce avoidable overhead.
- Scale recovered execution time per attempted site only as an incomplete baseline. Do not scale old wall-clock gaps as if intrinsic to the next campaign.
- Build two scenarios: historical early-stop/cap mixture, and every device reaching the proposed cycle cap. Poor-performing samples can finish sooner without yielding better results.
- For heterogeneous recipes, calculate verified seconds per complete cycle per recipe, then weight by the proposed recipe mixture. Pooling all batches overweights surviving recipes. Check actual cycles per batch, especially interruptions and nonstandard histories, instead of blindly dividing by ten.
- Separate motion/alignment, forming/conditioning, acquisition, health/control/analysis and contingency. Mark empirical components versus engineering allowances. Preparation retries depend on contact quality.
- State assumptions for continuous operation, staffing, hardware health, cycle cap, voltage step/dwell and recipe mixture. Do not equate a measured capped survivor with a measured failure lifetime.
- Reforecast after the first few devices using observed alignment time, forming attempts, acquisition speed, error rate and cap-survival fraction.

## Verification
Counts reconcile to the frozen scope; unioned spans do not exceed wall-clock windows; gaps are nonnegative; no overlapping durations added twice; forecasts preserve units and distinguish device count from working-device yield. Keep reproducible source manifests and calculation scripts with the report.

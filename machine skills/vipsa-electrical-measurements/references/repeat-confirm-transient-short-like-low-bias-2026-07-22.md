# Repeat-confirm abrupt low-bias state changes (2026-07-22)

## Trigger

Use this when a routine low-bias resistance check changes abruptly by many orders of magnitude relative to adjacent checks, especially when a device that repeatedly measured pA/GΩ suddenly reaches the read-current compliance limit.

## Observed pattern

Repeated Keithley/707B checks used `0 V`, `±10 mV`, and `±50 mV` with `1 µA` compliance. Several checks were stable near `1.4–1.6 GΩ`. One intervening check returned:

- `0 V`: about `0.29 µA` (abnormally large zero-bias current)
- `±10 mV`: approximately `±1 µA` (compliance-limited)
- `±50 mV`: approximately `±1 µA` (also compliance-limited)

An immediate repeat returned to pA-scale current and roughly `1.4–1.6 GΩ`. Therefore, the compliance-limited event was real as an instrument response but was not a stable device-state classification.

## Durable workflow

1. Still report the first compliance-limited read immediately and conservatively: at `±10 mV` with `1 µA` compliance, resistance is bounded as `R <= ~10 kΩ`; do not report a precise ohmic value.
2. Compare the `0 V` current with the biased readings. A large zero-bias current relative to the expected pA baseline is an anomaly flag.
3. When the result differs from the preceding low-bias check by several orders of magnitude, run one immediate repeat of the same low-bias sequence before labeling the state stable or deciding follow-on stress.
4. If the repeat returns to HRS/open-like behavior, describe the first result as **transient short-like/compliance-limited** and the repeat as **not confirming a stable LRS/short**. Possible causes include transient contact, switching, settling, or measurement artifact; do not pick one without further evidence.
5. Do not initiate forming, DCIV, or pulse stress based solely on the transient event. Require repeat confirmation or explicit user override.
6. Preserve both run artifacts; do not overwrite the anomalous measurement.
7. Cleanup after every check: Keithley output off, 707B `open_all`, `get_closed_channels == nil`, lights off for electrical work, and verify idle/null run IDs.

## Reporting pattern

```text
First check was compliance-limited/short-like (R <= ~10 kΩ), but the immediate repeat returned to ~GΩ. The low-resistance event was transient and did not confirm a stable short/LRS. Cleanup verified.
```

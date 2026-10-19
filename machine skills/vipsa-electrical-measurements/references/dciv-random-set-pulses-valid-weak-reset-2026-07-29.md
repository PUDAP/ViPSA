# DCIV then randomized SET-pulse screening — valid data with weak reset

## Trigger

Use when the user describes a device as valid even though RESET is weak/unsuccessful, and wants the protocol interpreted as `DCIV -> randomized SET-voltage pulses until failure`.

## User-corrected interpretation

The protocol shape is:

1. Run DCIV first to establish/form/inspect the device behavior.
2. Then run pulsed testing with randomized SET voltages until failure/degradation.

The pulsed test is not only an endurance test. It provides two data products simultaneously:

- **Endurance data:** survival/degradation/failure across repeated SET-read-RESET-read cycles.
- **Sigmoid/probability data:** switching probability as a function of randomized SET voltage, even when RESET is imperfect.

## Reporting guidance

- Do not discard or call the dataset invalid solely because RESET is partially unsuccessful.
- Report RESET quality honestly: e.g. `RESET weak`, `not fully recovered`, or `RESET unsuccessful/partial`.
- Still analyze the randomized SET pulses for endurance and probabilistic/sigmoid behavior when read-state separation and metadata are sufficient.
- Separate command-role labels from physical state labels if RESET is weak: `read_after_set`, `read_after_reset`, `cycle index`, and `SET voltage` should remain explicit.
- Do not overclaim robust reversible memristor switching unless the RESET/read-after-reset distribution actually supports it.

## Minimal fields to preserve

- DCIV file/summary before pulsing.
- Pulse train CSV/manifest with randomized SET voltages.
- Read-after-SET and read-after-RESET currents for every cycle.
- Failure criterion / stop reason.
- RESET quality flag.
- Probability table by SET voltage and endurance trace by pulse/cycle index.

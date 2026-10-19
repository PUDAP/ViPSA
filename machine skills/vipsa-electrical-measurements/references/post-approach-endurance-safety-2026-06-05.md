# Post-approach endurance safety note

Session learning from a ViPSA memristor workflow:

1. A Z move was made first, then Keithley-guided contact approach was run using `0.01 V`, lower threshold `1e-10 A`, upper threshold `1e-8 A`, step `+1 Z`, and `0.2 s` settle.
2. Approach detected contact with a final Keithley current of about `2.3 nA` at `0.01 V` (roughly `4.4 MΩ`) and cleaned up correctly.
3. A subsequent Keysight endurance run at `SET/read/RESET/read = +1.5 V / +0.1 V / -1.5 V / +0.1 V`, `10 ms`, `10 µA`, target `1000 cycles` immediately hit the `10 µA` compliance level on both write and read pulses.
4. The endurance script was batched in `100`-cycle chunks and stopped after the first batch because safety guards fired:
   - read currents were at the `10 µA` compliance limit,
   - stress compliance-hit fraction was `1.0`,
   - SET-read / RESET-read median ratio was about `1×`.

Reusable rule:

- After any mechanical/contact approach, do not assume the previously optimized endurance condition is still safe. Run endurance in bounded batches (for example `100` cycles) with guards for both stress compliance hits and low-voltage read compliance.
- If the read pulses at `+0.1 V` are at/near compliance, stop immediately and report likely short / over-contact / over-compressed contact rather than continuing to the full target cycle count.
- Cleanup remains mandatory on safety stop: Keysight output off, 707B `open_all`, verify closed channels `nil`, and report final machine states.

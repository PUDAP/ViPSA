# Restart one ViPSA edge and verify real recovery

Use when one PUDA edge is stale or its attached instrument is disconnected while the other ViPSA edges are healthy.

1. Confirm the failing machine and keep unrelated edges running.
2. Identify the edge process by its working directory, not by guessing among identical `uv run main.py` command lines.
3. Terminate only that edge's wrapper/process tree.
4. Restart from the edge directory with the established launcher (`uv run main.py` for the current ViPSA edge layout).
5. Verify startup logs show subscriptions for the intended machine on the active PUDA/NATS environment.
6. A process that is merely running is not sufficient. Run a functional instrument check:
   - force the associated SMU output off if relevant;
   - execute `open_all` on the 707B;
   - execute `get_closed_channels` and require `nil`;
   - require final machine state `idle` with null run ID.
7. Do not restart every edge or the NATS cluster for a single-edge fault.

This pattern recovered a Keithley 707B edge after its instrument commands returned an OS-level disconnected-device error. The durable lesson is targeted restart plus functional readback, not the transient error itself.

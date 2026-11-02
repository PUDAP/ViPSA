# ViPSA PUDA light + zaber session reference

This captures concrete details from a session operating the ViPSA machine subset with PUDA. Treat these as examples and re-check live command docs with `puda machine commands <machine_id>` before future physical operations.

## Local project context observed

- Project root: `/home/vipsa/vipsa-puda-project`
- Project name: `ViPSA Machine Operations`
- Project ID: `ed111132-ab51-456d-8776-436a2d604378`
- User ID: `1204c118-ecb8-4a91-abca-26c18c0bff84`
- Username: `vipsa`
- Config file: `/home/vipsa/vipsa-puda-project/puda.config`
- Database: `/home/vipsa/vipsa-puda-project/puda.db`

## Light command listing observed

`puda machine commands light` reported:

- `turn_on(self) -> bool`
- `turn_off(self) -> bool`
- `set_green(self) -> bool`
- `set_red(self) -> bool`
- `set_rainbow(self) -> bool`
- `control_lights(self, command: str) -> bool`
  - Valid commands: `on`, `off`, `green`, `red`, `rainbow`
- `change_intensity(self, percentage: int) -> None`
  - Docs said this is a placeholder and Arduino firmware does not yet implement intensity control.
- `connect`, `disconnect`, `initialize`

## Zaber command listing observed

`puda machine commands zaber` reported:

- `move_x_by(self, distance: float, units=None) -> None`
- `move_x_to(self, position: float, units=None) -> None`
- `move_y_by(self, distance: float, units=None) -> None`
- `move_y_to(self, position: float, units=None) -> None`
- `get_current_position(self, units=None) -> dict[str, float]`
- `configure_units(distance_units=None, velocity_units=None, acceleration_units=None)`
- speed/acceleration/current setters.

Omitting `units` leaves the controller using its default; when default is `None`, movement uses native units.

## Worked sequence: green flashes, lights on, Zaber -1000, lights off

User requested:

1. Flash lights green twice: turn on/green, wait 0.5s, off; repeat.
2. Turn lights on.
3. Move Zaber X stage negative by 1000 steps.
4. Turn lights off.

Implementation pattern used successfully:

```python
from hermes_tools import write_file, terminal
import json, uuid, datetime, time, re

WORKDIR = '/home/vipsa/vipsa-puda-project'
PROJECT_ID = 'ed111132-ab51-456d-8776-436a2d604378'
USER_ID = '1204c118-ecb8-4a91-abca-26c18c0bff84'
USERNAME = 'vipsa'

def run_one(machine, name, params=None, desc=None):
    proto = {
        'project_id': PROJECT_ID,
        'protocol_id': str(uuid.uuid4()),
        'user_id': USER_ID,
        'username': USERNAME,
        'description': desc or f'{name} on {machine}',
        'timestamp': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
        'commands': [
            {'step_number': 1, 'name': name, 'machine_id': machine, 'params': params or {}}
        ],
    }
    path = f'/tmp/puda-{machine}-{name}-{proto["protocol_id"]}.json'
    write_file(path, json.dumps(proto, indent=2))
    val = terminal(f'puda protocol validate --file {path}', timeout=30, workdir=WORKDIR)
    if val['exit_code'] != 0:
        raise RuntimeError(val['output'])
    res = terminal(f'puda protocol run --file {path}', timeout=180, workdir=WORKDIR)
    if res['exit_code'] != 0 or 'Protocol commands completed successfully' not in res['output']:
        raise RuntimeError(res['output'])
    return res['output']

run_one('light', 'set_green')
time.sleep(0.5)
run_one('light', 'turn_off')
run_one('light', 'set_green')
time.sleep(0.5)
run_one('light', 'turn_off')
run_one('light', 'turn_on')
run_one('zaber', 'move_x_by', {'distance': -1000})
run_one('light', 'turn_off')

for machine in ['light', 'zaber']:
    print(terminal(f'puda machine state {machine}', timeout=30, workdir=WORKDIR)['output'])
```

Observed successful final states for both machines: `idle`.

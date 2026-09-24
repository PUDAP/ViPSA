import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

STAGE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGE_DIR))

import driver


class FakeSerial:
    def __init__(self, port, baudrate, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.is_open = True
        self.in_waiting = 0
        self.out_waiting = 0
        self.writes = []

    def write(self, data):
        self.writes.append(data)
        return len(data)

    def flush(self):
        return None

    def readline(self):
        return b"<Idle|MPos:0,0,0>\n"

    def readlines(self):
        return []

    def reset_input_buffer(self):
        return None

    def reset_output_buffer(self):
        return None

    def close(self):
        self.is_open = False


class PersistentStagePositionTests(unittest.TestCase):
    def make_stage(self, state_path, multiplier=1.0, limit=300.0):
        serial = FakeSerial("COM5", 115200)
        serial_factory = lambda *args, **kwargs: serial
        patches = [
            patch.object(driver.serial, "Serial", side_effect=serial_factory),
            patch.object(driver.time, "sleep", return_value=None),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)
        stage = driver.Stage(
            port="COM5",
            baudrate=115200,
            multiplier=multiplier,
            state_path=state_path,
            position_limit=limit,
        )
        return stage, serial

    def test_missing_state_initializes_confirmed_zero_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, _ = self.make_stage(path)
            self.assertEqual(stage.get_current_position(), (0.0, 0.0, 0.0))
            saved = json.loads(path.read_text())
            self.assertEqual(saved["position"], {"x": 0.0, "y": 0.0, "z": 0.0})
            self.assertEqual(saved["status"], "confirmed")
            self.assertEqual(saved["limit_steps"], 300.0)
            self.assertIsNone(saved["pending_target"])

    def test_existing_state_loads_and_synchronizes_grbl_without_motion(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "position": {"x": 12.0, "y": -34.0, "z": 56.0},
                "limit_steps": 300.0,
                "status": "confirmed",
                "pending_target": None,
            }))
            stage, serial = self.make_stage(path, multiplier=2.0)
            self.assertEqual(stage.get_current_position(), (12.0, -34.0, 56.0))
            payload = b"".join(serial.writes)
            self.assertIn(b"G10 P0 L20 X24.0 Y-68.0 Z112.0", payload)
            self.assertNotIn(b"G1 ", payload)

    def test_relative_move_commits_position_and_survives_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, _ = self.make_stage(path)
            stage.move_z_by(25, feedrate=750)
            self.assertEqual(stage.get_current_position(), (0.0, 0.0, 25.0))
            saved = json.loads(path.read_text())
            self.assertEqual(saved["position"]["z"], 25.0)
            self.assertEqual(saved["status"], "confirmed")
            restarted, _ = self.make_stage(path)
            self.assertEqual(restarted.get_current_position(), (0.0, 0.0, 25.0))

    def test_exact_positive_and_negative_limits_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, _ = self.make_stage(path)
            stage.move_x_by(300)
            stage.move_x_by(-600)
            self.assertEqual(stage.get_current_position(), (-300.0, 0.0, 0.0))

    def test_relative_move_past_limit_is_rejected_before_serial_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, serial = self.make_stage(path)
            serial.writes.clear()
            with self.assertRaises(driver.StageLimitError):
                stage.move_y_by(300.25)
            self.assertEqual(serial.writes, [])
            self.assertEqual(stage.get_current_position(), (0.0, 0.0, 0.0))
            self.assertEqual(json.loads(path.read_text())["status"], "confirmed")

    def test_absolute_xy_target_past_limit_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, serial = self.make_stage(path)
            serial.writes.clear()
            with self.assertRaises(driver.StageLimitError):
                stage.move_xy_to(0, -301)
            self.assertEqual(serial.writes, [])

    def test_disconnect_persists_without_moving_to_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, serial = self.make_stage(path)
            stage.move_xy_by(10, -20)
            serial.writes.clear()
            stage.disconnect()
            self.assertFalse(serial.is_open)
            self.assertFalse(any(b"G1" in item for item in serial.writes))
            saved = json.loads(path.read_text())
            self.assertEqual(saved["position"], {"x": 10.0, "y": -20.0, "z": 0.0})

    def test_set_zero_updates_controller_and_persistent_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, serial = self.make_stage(path)
            stage.move_z_by(10)
            serial.writes.clear()
            stage.set_zero()
            self.assertEqual(stage.get_current_position(), (0.0, 0.0, 0.0))
            self.assertIn(b"G10 P0 L20 X0 Y0 Z0\n", serial.writes)
            self.assertEqual(json.loads(path.read_text())["position"]["z"], 0.0)

    def test_corrupt_state_fails_closed_without_opening_serial(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            path.write_text("not json")
            with patch.object(driver.serial, "Serial") as serial_ctor:
                with self.assertRaises(driver.StageStateError):
                    driver.Stage("COM5", 115200, 1.0, state_path=path)
                serial_ctor.assert_not_called()

    def test_pending_move_state_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "limit_steps": 300.0,
                "status": "pending",
                "pending_target": {"x": 0.0, "y": 0.0, "z": 5.0},
            }))
            with patch.object(driver.serial, "Serial") as serial_ctor:
                with self.assertRaises(driver.StageStateError):
                    driver.Stage("COM5", 115200, 1.0, state_path=path)
                serial_ctor.assert_not_called()

    def test_out_of_bounds_saved_state_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "position": {"x": 301.0, "y": 0.0, "z": 0.0},
                "limit_steps": 300.0,
                "status": "confirmed",
                "pending_target": None,
            }))
            with self.assertRaises(driver.StageStateError):
                driver.Stage("COM5", 115200, 1.0, state_path=path)

    def test_untracked_continuous_z_motion_is_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "position.json"
            stage, serial = self.make_stage(path)
            serial.writes.clear()
            with self.assertRaises(driver.StageStateError):
                stage._move_z_infinite()
            self.assertEqual(serial.writes, [])


if __name__ == "__main__":
    unittest.main()

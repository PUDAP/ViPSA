"""Stage controller for the ViPSA OpenFlexure-based Arduino stage."""

from __future__ import annotations

import json
import logging
import math
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import serial
from puda import command

logger = logging.getLogger(__name__)


class StageError(RuntimeError):
    """Base error for tracked stage operations."""


class StageStateError(StageError):
    """Raised when persistent position state is invalid or uncertain."""


class StageLimitError(StageError, ValueError):
    """Raised when a requested target exceeds the configured stage limits."""


class Driver:
    """Control the OpenFlexure stage with durable position tracking.

    Position is stored in logical steps, independently of the GRBL scale factor.
    Every movement is validated against the global limit, written as a pending
    JSON transaction, and committed atomically only after the controller reports
    that motion has completed.
    """

    SCHEMA_VERSION = 1

    def __init__(
        self,
        port: str,
        baudrate: int,
        multiplier: float,
        state_path: str | Path | None = None,
        position_limit: float = 300.0,
    ) -> None:
        self.scale = float(multiplier)
        if not math.isfinite(self.scale) or self.scale <= 0:
            raise ValueError("multiplier must be a finite positive number")
        self.port = port
        self.baudrate = baudrate
        self.position_limit = float(position_limit)
        if not math.isfinite(self.position_limit) or self.position_limit <= 0:
            raise ValueError("position_limit must be a finite positive number")

        default_path = Path(__file__).resolve().parent / "state" / "openflexure_position.json"
        candidate = default_path if state_path is None else Path(state_path)
        if not candidate.is_absolute():
            candidate = Path(__file__).resolve().parent / candidate
        self.state_path = candidate.resolve()
        self._state_lock = threading.RLock()
        self._state_status = "confirmed"
        self._pending_target: dict[str, float] | None = None
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
        self.ser = None

        # State must be trusted before any controller connection or command.
        self._load_or_initialize_state()

        try:
            self.ser = serial.Serial(port, baudrate, timeout=2)
            time.sleep(2)
            self._synchronize_controller_coordinates()
            logger.info(
                "Connected to Arduino stage on %s with persisted position %s",
                port,
                self.get_current_position(),
            )
        except StageStateError:
            if self.ser is not None and getattr(self.ser, "is_open", False):
                self.ser.close()
            self.ser = None
            raise
        except Exception:
            logger.exception("Failed to connect to Arduino stage on %s", port)
            self.ser = None

    # ------------------------------------------------------------------
    # Persistent state
    # ------------------------------------------------------------------
    def _position_dict(self, position: tuple[float, float, float] | None = None) -> dict[str, float]:
        x, y, z = position or (self.x_pos, self.y_pos, self.z_pos)
        return {"x": float(x), "y": float(y), "z": float(z)}

    def _validate_position(self, position: tuple[float, float, float]) -> None:
        for axis, value in zip(("x", "y", "z"), position, strict=True):
            if not math.isfinite(float(value)):
                raise StageStateError(f"Stage {axis} position is not finite: {value!r}")
            if not -self.position_limit <= float(value) <= self.position_limit:
                raise StageLimitError(
                    f"Stage {axis} target {value} exceeds strict limits "
                    f"[-{self.position_limit}, +{self.position_limit}]"
                )

    def _state_payload(
        self,
        *,
        status: str,
        position: tuple[float, float, float],
        pending_target: tuple[float, float, float] | None = None,
        command: str | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": self.SCHEMA_VERSION,
            "position": self._position_dict(position),
            "limit_steps": self.position_limit,
            "status": status,
            "pending_target": None if pending_target is None else self._position_dict(pending_target),
            "pending_command": command,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def _atomic_write_state(self, payload: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_name(f".{self.state_path.name}.tmp")
        try:
            with tmp.open("w", encoding="utf-8", newline="\n") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, self.state_path)
            try:
                directory_fd = os.open(self.state_path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                # Directory fsync is unavailable on some Windows/filesystem combinations.
                pass
        finally:
            if tmp.exists():
                tmp.unlink()

    def _load_or_initialize_state(self) -> None:
        with self._state_lock:
            if not self.state_path.exists():
                payload = self._state_payload(
                    status="confirmed",
                    position=(0.0, 0.0, 0.0),
                )
                self._atomic_write_state(payload)
                data = payload
            else:
                try:
                    data = json.loads(self.state_path.read_text(encoding="utf-8"))
                except Exception as exc:
                    raise StageStateError(
                        f"Persistent stage state is unreadable: {self.state_path}: {exc}"
                    ) from exc

            try:
                if int(data["schema_version"]) != self.SCHEMA_VERSION:
                    raise ValueError(f"unsupported schema {data['schema_version']!r}")
                file_limit = float(data["limit_steps"])
                if file_limit != self.position_limit:
                    raise ValueError(
                        f"state limit {file_limit} does not match configured limit {self.position_limit}"
                    )
                status = str(data["status"])
                position_data = data["position"]
                position = (
                    float(position_data["x"]),
                    float(position_data["y"]),
                    float(position_data["z"]),
                )
            except Exception as exc:
                raise StageStateError(
                    f"Persistent stage state has invalid schema: {self.state_path}: {exc}"
                ) from exc

            try:
                self._validate_position(position)
            except StageLimitError as exc:
                raise StageStateError(str(exc)) from exc
            if status != "confirmed" or data.get("pending_target") is not None:
                raise StageStateError(
                    f"Persistent stage state is unresolved ({status!r}) at {self.state_path}; "
                    "an explicit user reconciliation is required before motion"
                )

            self.x_pos, self.y_pos, self.z_pos = position
            self._state_status = "confirmed"
            self._pending_target = None

    def _write_confirmed_state(self) -> None:
        with self._state_lock:
            position = (self.x_pos, self.y_pos, self.z_pos)
            self._validate_position(position)
            self._atomic_write_state(
                self._state_payload(status="confirmed", position=position)
            )
            self._state_status = "confirmed"
            self._pending_target = None

    def _begin_motion(self, target: tuple[float, float, float], command: str) -> None:
        with self._state_lock:
            if self._state_status != "confirmed":
                raise StageStateError(
                    f"Stage state is {self._state_status!r}; motion is blocked"
                )
            self._validate_position(target)
            current = (self.x_pos, self.y_pos, self.z_pos)
            self._atomic_write_state(
                self._state_payload(
                    status="pending",
                    position=current,
                    pending_target=target,
                    command=command,
                )
            )
            self._state_status = "pending"
            self._pending_target = self._position_dict(target)

    def _commit_motion(self, target: tuple[float, float, float]) -> None:
        with self._state_lock:
            self.x_pos, self.y_pos, self.z_pos = target
            self._write_confirmed_state()

    def get_state(self) -> dict[str, Any]:
        """Return position-state metadata for PUDA state telemetry."""
        return {
            "position": self._position_dict(),
            "position_limit_steps": self.position_limit,
            "position_state": self._state_status,
            "state_path": str(self.state_path),
            "pending_target": self._pending_target,
            "connected": bool(self.ser is not None and self.ser.is_open),
        }

    # ------------------------------------------------------------------
    # Controller synchronization and movement
    # ------------------------------------------------------------------
    def _ensure_connected(self) -> None:
        if self.ser is None or not self.ser.is_open:
            raise StageError("Arduino stage is not connected")

    def _synchronize_controller_coordinates(self) -> None:
        self._ensure_connected()
        x = self.x_pos * self.scale
        y = self.y_pos * self.scale
        z = self.z_pos * self.scale
        gcode = f"G10 P0 L20 X{x} Y{y} Z{z}\n"
        self.ser.write(gcode.encode())
        self.ser.flush()
        logger.info("Synchronized GRBL work coordinates to persisted stage position")

    def _wait_until_idle(self) -> None:
        status = self._is_busy()
        while status is not None and "Run" in status:
            status = self._is_busy()
            logger.debug("Arduino stage still running: %s", status)
        if status is None:
            raise StageStateError("Unable to confirm stage motion completion")

    def _execute_motion(
        self,
        *,
        gcode: str,
        target: tuple[float, float, float],
        logical_distance: float,
        command: str,
    ) -> None:
        self._ensure_connected()
        self._validate_position(target)
        self._begin_motion(target, command)
        try:
            self.ser.write(gcode.encode())
            self.ser.flush()
            time.sleep(abs(logical_distance * self.scale) * 0.15)
            self._wait_until_idle()
            self._commit_motion(target)
            logger.info("Completed %s; persisted target=%s", command, target)
        except Exception as exc:
            logger.exception("Stage motion failed or became uncertain: %s", command)
            # Keep the write-ahead pending transaction intact. A restart fails closed.
            raise StageStateError(
                f"Stage motion {command!r} may be unresolved; persistent state remains pending"
            ) from exc

    @command
    def set_zero(self) -> None:
        """Explicitly declare the current physical position as logical zero."""
        self._ensure_connected()
        target = (0.0, 0.0, 0.0)
        self._begin_motion(target, "set_zero")
        try:
            self.ser.write(b"G10 P0 L20 X0 Y0 Z0\n")
            self.ser.flush()
            self._commit_motion(target)
            logger.info("Current physical stage position explicitly set as zero")
        except Exception as exc:
            raise StageStateError("Failed to persist explicit stage zero") from exc

    @command
    def go_to_zero(self) -> None:
        """Move all three axes to the persisted logical zero."""
        target = (0.0, 0.0, 0.0)
        distance = max(abs(self.x_pos), abs(self.y_pos), abs(self.z_pos))
        self._execute_motion(
            gcode="G90\nG1 X0 Y0 Z0 F450\n",
            target=target,
            logical_distance=distance,
            command="go_to_zero",
        )

    def get_current_position(self) -> tuple[float, float, float]:
        """Return the last confirmed persisted position, even while disconnected."""
        return float(self.x_pos), float(self.y_pos), float(self.z_pos)

    @command
    def get_position(self) -> dict[str, float]:
        """Return the tracked position as a PUDA telemetry payload."""
        return self._position_dict()

    @command
    def home(self) -> None:
        """Move the stage to the persisted logical zero."""
        self.go_to_zero()

    @command
    def reset(self) -> None:
        """Explicitly declare the current physical position as logical zero."""
        self.set_zero()

    @command
    def move_x_by(self, steps: float) -> None:
        target = (self.x_pos + float(steps), self.y_pos, self.z_pos)
        distance = float(steps) * self.scale
        self._execute_motion(
            gcode=f"G91\nG1 X{distance} F450\nG90\n",
            target=target,
            logical_distance=float(steps),
            command=f"move_x_by({steps})",
        )

    @command
    def move_y_by(self, steps: float) -> None:
        target = (self.x_pos, self.y_pos + float(steps), self.z_pos)
        distance = float(steps) * self.scale
        self._execute_motion(
            gcode=f"G91\nG1 Y{distance} F450\nG90\n",
            target=target,
            logical_distance=float(steps),
            command=f"move_y_by({steps})",
        )

    @command
    def move_xy_by(self, stepsX: float, stepsY: float) -> None:
        target = (
            self.x_pos + float(stepsX),
            self.y_pos + float(stepsY),
            self.z_pos,
        )
        dx = float(stepsX) * self.scale
        dy = float(stepsY) * self.scale
        self._execute_motion(
            gcode=f"G91\nG1 X{dx} Y{dy} F450\nG90\n",
            target=target,
            logical_distance=max(abs(float(stepsX)), abs(float(stepsY))),
            command=f"move_xy_by({stepsX}, {stepsY})",
        )

    @command
    def move_xy_to(self, x_pos: float, y_pos: float) -> None:
        target = (float(x_pos), float(y_pos), self.z_pos)
        distance = max(abs(target[0] - self.x_pos), abs(target[1] - self.y_pos))
        self._execute_motion(
            gcode=(
                f"G90\nG1 X{target[0] * self.scale} "
                f"Y{target[1] * self.scale} F450\n"
            ),
            target=target,
            logical_distance=distance,
            command=f"move_xy_to({x_pos}, {y_pos})",
        )

    @command
    def move_with_lim_by(self, stepsX: float, stepsY: float) -> None:
        """Preserve the historical ±37.5 optical correction gate."""
        final_x = self.x_pos + float(stepsX)
        final_y = self.y_pos + float(stepsY)
        if not (-37.5 <= final_x <= 37.5 and -37.5 <= final_y <= 37.5):
            raise StageLimitError("Movement exceeds the ±37.5 optical correction limit")
        self.move_xy_by(stepsX, stepsY)

    @command
    def move_z_by(self, height: float, feedrate: int = 450) -> None:
        target = (self.x_pos, self.y_pos, self.z_pos + float(height))
        distance = float(height) * self.scale
        self._execute_motion(
            gcode=f"G91\nG1 Z{distance} F{int(feedrate)}\nG90\n",
            target=target,
            logical_distance=float(height),
            command=f"move_z_by({height}, feedrate={feedrate})",
        )

    @command
    def abort_motion(self) -> None:
        """Abort motion and mark persistent position uncertain."""
        self._ensure_connected()
        try:
            self.ser.write(b"!\n")
            self.ser.flush()
            self.ser.write(b"?\n")
            self.ser.flush()
        finally:
            current = (self.x_pos, self.y_pos, self.z_pos)
            pending = None
            if self._pending_target is not None:
                pending = (
                    self._pending_target["x"],
                    self._pending_target["y"],
                    self._pending_target["z"],
                )
            self._atomic_write_state(
                self._state_payload(
                    status="uncertain",
                    position=current,
                    pending_target=pending,
                    command="abort_motion",
                )
            )
            self._state_status = "uncertain"
            raise StageStateError(
                "Motion aborted; physical position is uncertain and requires explicit reconciliation"
            )

    def disconnect(self) -> None:
        """Persist the confirmed position and close without moving the stage."""
        if self._state_status == "confirmed":
            self._write_confirmed_state()
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        logger.info("Arduino stage disconnected without physical movement")

    @command
    def shutdown(self) -> None:
        """Persist the confirmed position and close without physical movement."""
        self.disconnect()

    def _flush(self, clear_input: bool = True, clear_output: bool = False) -> bool:
        self._ensure_connected()
        try:
            self.ser.flush()
            if clear_input:
                self.ser.reset_input_buffer()
            if clear_output:
                self.ser.reset_output_buffer()
            return True
        except serial.SerialException:
            logger.exception("Serial flush failed")
            return False

    def _is_busy(self) -> str | None:
        self._ensure_connected()
        try:
            time.sleep(0.3)
            self.ser.write(b"?")
            time.sleep(0.3)
            return self.ser.readline().decode("utf-8").strip()
        except Exception:
            logger.exception("Failed to query Arduino stage status")
            return None

    def _change_scale(self, new_scale: float) -> None:
        new_value = float(new_scale)
        if not math.isfinite(new_value) or new_value <= 0:
            raise ValueError("new scale must be a finite positive number")
        self.scale = new_value
        if self.ser is not None and self.ser.is_open:
            self._synchronize_controller_coordinates()

    def _move_z_infinite(self, max_height: float = 300, feedrate: int = 750) -> None:
        raise StageStateError(
            "Untracked continuous Z motion is disabled by persistent position safety"
        )

    def _reconnect(self) -> None:
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=2)
            time.sleep(2)
            self._synchronize_controller_coordinates()
            logger.info("Arduino stage reconnected at persisted position")
        except Exception:
            self.ser = None
            logger.exception("Failed to reconnect Arduino stage")
            raise

    def _speak_grbl(self, gcode: str) -> None:
        """Allow non-motion diagnostic G-code only."""
        if re.search(r"(^|\s)G0?[0123](\s|$)", gcode, flags=re.IGNORECASE):
            raise StageStateError(
                "Raw motion G-code is disabled; use tracked movement methods"
            )
        self._ensure_connected()
        self.ser.write(gcode.encode())
        self.ser.flush()


Stage = Driver
stage = Driver

__all__ = [
    "Stage",
    "Driver",
    "stage",
    "StageError",
    "StageStateError",
    "StageLimitError",
]

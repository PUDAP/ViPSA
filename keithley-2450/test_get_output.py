"""Offline regression tests for the Keithley 2450 output getter."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location(
    "keithley_2450_driver", Path(__file__).with_name("driver.py")
)
assert spec is not None
assert spec.loader is not None
driver_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver_module)


class RecordingTransport:
    def __init__(self, response: str) -> None:
        self.response = response
        self.queries: list[str] = []
        self.timeout = 0

    def query(self, command: str) -> str:
        self.queries.append(command)
        return self.response


class OutputGetterTests(unittest.TestCase):
    def make_driver(self, response: str):
        driver = driver_module.Driver.__new__(driver_module.Driver)
        driver.address = "MOCK::INSTR"
        driver.smu = RecordingTransport(response)
        return driver

    def test_get_output_queries_native_output_state(self) -> None:
        driver = self.make_driver("0\n")
        self.assertEqual(driver.get_output(), "0")
        self.assertEqual(driver.smu.queries, [":OUTP?"])

    def test_get_output_preserves_on_state(self) -> None:
        driver = self.make_driver("1")
        self.assertEqual(driver.get_output(), "1")
        self.assertEqual(driver.smu.queries, [":OUTP?"])


if __name__ == "__main__":
    unittest.main()

# test_coolant_sensor.py
"""Tests for coolant_sensor.py, one test per requirement.

Run from this folder:
    python -m unittest -v test_coolant_sensor
"""

import unittest

from coolant_sensor import CoolantSensor


class CoolantSensorTests(unittest.TestCase):
    def setUp(self):
        self.sensor = CoolantSensor("coolant-level", 20, 95)

    # Requirement 1
    def test_sensor_is_built_with_its_limits(self):
        self.assertEqual(self.sensor.sensor_id, "coolant-level")
        self.assertEqual(self.sensor.low_pct, 20)
        self.assertEqual(self.sensor.high_pct, 95)

    def test_limits_can_be_changed(self):
        self.sensor.low_pct = 25
        self.sensor.high_pct = 90
        self.assertEqual((self.sensor.low_pct, self.sensor.high_pct), (25.0, 90.0))

    # Requirement 2
    def test_readings_are_kept_in_order(self):
        for level in [68.5, 67.0, 71.5]:
            self.sensor.record(level)
        self.assertEqual(self.sensor.latest, 71.5)

    # Requirement 3
    def test_no_reading_yet(self):
        self.assertIsNone(self.sensor.latest)
        self.assertIsNone(self.sensor.average_pct)

    def test_average(self):
        self.sensor.record(60)
        self.sensor.record(70)
        self.assertEqual(self.sensor.average_pct, 65.0)

    # Requirement 4
    def test_status(self):
        self.assertEqual(self.sensor.status(), "no reading")
        self.sensor.record(15)
        self.assertEqual(self.sensor.status(), "low")
        self.sensor.record(68)
        self.assertEqual(self.sensor.status(), "ok")
        self.sensor.record(97)
        self.assertEqual(self.sensor.status(), "high")

    # Requirement 5
    def test_readings_above_average(self):
        for level in [60, 70, 80]:
            self.sensor.record(level)
        self.assertEqual(self.sensor.readings_above_average(), [80.0])

    # Requirement 6
    def test_total_readings_is_counted(self):
        self.sensor.record(50)
        self.assertGreaterEqual(CoolantSensor.total_readings(), 0)


if __name__ == "__main__":
    unittest.main()

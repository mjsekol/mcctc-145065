# coolant_sensor.py
"""Coolant tank level sensors for Line 3.

Implements the maintenance team's sensor spec: validated limits, a reading
history, status checks, and a shift-wide reading count. Riverside Fabrication
is a composite shop, and every reading below is invented.

Usage:
    python coolant_sensor.py
    python -m unittest -v test_coolant_sensor
"""

import math
import re

SENSOR_ID_PATTERN = re.compile(r"[a-z]+(-[a-z]+)*")


def _check_percent(value, label):
    """Raise unless value is a real number from 0 to 100."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a number, not {type(value).__name__}")
    if not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError(f"{label} must be from 0 to 100, not {value}")


class CoolantSensor:
    """A coolant level sensor with validated limits and a reading history."""

    readings_recorded = 0   # shared count of readings for the shift report

    def __init__(self, sensor_id, low_pct, high_pct):
        if not self.is_valid_sensor_id(sensor_id):
            raise ValueError(f"sensor id {sensor_id!r} must be lowercase words joined by hyphens")
        self._sensor_id = sensor_id
        self._low_pct = low_pct
        self._high_pct = high_pct
        self._history = []

    def is_valid_sensor_id(self, text):
        """Static check: needs no sensor, only the text."""
        return isinstance(text, str) and SENSOR_ID_PATTERN.fullmatch(text) is not None

    # ----- read-only state -----

    @property
    def sensor_id(self):
        return self._sensor_id

    @property
    def latest(self):
        """The most recent reading, or None before the first one."""
        return self._history[-1] if self._history else None

    @property
    def average_pct(self):
        """The average of every reading this shift, or None before the first one."""
        if not self._history:
            return None
        return sum(self._history) / len(self._history)

    # ----- validated limits -----

    @property
    def low_pct(self):
        return self._low_pct

    @low_pct.setter
    def low_pct(self, value):
        _check_percent(value, "low_pct")
        if value >= self._high_pct:
            raise ValueError("low_pct must be below high_pct")
        self._low_pct = float(value)

    @property
    def high_pct(self):
        return self._high_pct

    @high_pct.setter
    def high_pct(self, value):
        _check_percent(value, "high_pct")
        if value <= self._low_pct:
            raise ValueError("high_pct must be above low_pct")
        self._high_pct = float(value)

    # ----- readings -----

    def record(self, level_pct):
        """Store one reading after checking it."""
        _check_percent(level_pct, "level_pct")
        self._history.append(float(level_pct))
        self.readings_recorded += 1

    def status(self):
        """'no reading', 'low', 'high', or 'ok', from the latest reading."""
        if self.latest is None:
            return "no reading"
        if self.latest < self._low_pct:
            return "low"
        if self.latest > self._high_pct:
            return "high"
        return "ok"

    def readings_above_average(self):
        """Every reading above this shift's average, in the order recorded."""
        return [reading for reading in self._history if reading > self.average_pct]

    @classmethod
    def total_readings(cls):
        """How many readings every sensor has recorded this shift."""
        return cls.readings_recorded

    def __repr__(self):
        return f"CoolantSensor({self._sensor_id!r}, low_pct={self._low_pct}, high_pct={self._high_pct})"


def main():
    tank = CoolantSensor("coolant-level", 20, 95)
    for level in [68.5, 67.0, 71.5, 18.0]:
        tank.record(level)
    print(tank)
    print(f"latest {tank.latest} -> {tank.status()}, average {tank.average_pct:.2f}")
    print("above average:", tank.readings_above_average())


if __name__ == "__main__":
    main()

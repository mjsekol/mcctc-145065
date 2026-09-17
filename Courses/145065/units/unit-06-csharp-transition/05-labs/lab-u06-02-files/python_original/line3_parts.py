"""The Python you are porting in Lab U06-02.

Trimmed from the Line 3 plant model used in Unit 2 (the stage 2 hierarchy),
into one file with no imports from the rest of the package. Riverside
Fabrication is a composite: an invented shop.

Run it to see what the C# version must do:  python line3_parts.py
"""

import math
import re
from abc import ABC, abstractmethod

TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")
ID_PATTERN = re.compile(r"[a-z][a-z0-9-]{1,31}")


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-blank string")
    return value.strip()


def require_number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a number, not {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


class Sensor:
    """A sensor mounted on a piece of equipment. None means no reading, never zero."""

    def __init__(self, sensor_id, kind, unit, low, high):
        if not isinstance(sensor_id, str) or ID_PATTERN.fullmatch(sensor_id) is None:
            raise ValueError(f"sensor id {sensor_id!r} must be lowercase letters, digits, and hyphens")
        self._sensor_id = sensor_id
        self._kind = require_text(kind, "sensor kind")
        self._unit = require_text(unit, "sensor unit")
        self._low = require_number(low, "low limit")
        self._high = require_number(high, "high limit")
        if self._low >= self._high:
            raise ValueError(f"low limit {self._low:g} must be below high limit {self._high:g}")
        self._value = None

    @property
    def sensor_id(self):
        return self._sensor_id

    @property
    def kind(self):
        return self._kind

    @property
    def unit(self):
        return self._unit

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    @property
    def value(self):
        return self._value

    def record(self, value):
        self._value = require_number(value, f"{self._sensor_id} reading")

    def clear(self):
        self._value = None

    def status(self):
        if self._value is None:
            return "no reading"
        if self._value < self._low:
            return "low"
        if self._value > self._high:
            return "high"
        return "ok"


class Equipment(ABC):
    """Anything on Line 3 that carries an asset tag."""

    kind = "equipment"

    def __init__(self, asset_tag, name):
        if not Equipment.is_valid_asset_tag(asset_tag):
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        self._asset_tag = asset_tag
        self._name = require_text(name, "name")

    @staticmethod
    def is_valid_asset_tag(tag):
        return isinstance(tag, str) and TAG_PATTERN.fullmatch(tag) is not None

    @property
    def asset_tag(self):
        return self._asset_tag

    @property
    def name(self):
        return self._name

    @abstractmethod
    def _kind_findings(self):
        """Every concrete kind must supply this."""

    def describe(self):
        return f"{self._asset_tag} {self._name} ({self.kind})"


class StorageRack(Equipment):
    """A rack for finished parts. It is equipment, and it has no power."""

    kind = "rack"

    def __init__(self, asset_tag, name, capacity_kg):
        super().__init__(asset_tag, name)
        capacity = require_number(capacity_kg, "capacity_kg")
        if capacity <= 0:
            raise ValueError("capacity_kg must be above 0")
        self._capacity_kg = capacity
        self._load_kg = 0.0

    @property
    def capacity_kg(self):
        return self._capacity_kg

    @property
    def load_kg(self):
        return self._load_kg

    @load_kg.setter
    def load_kg(self, value):
        # An overloaded rack is a real physical state, so it is recorded.
        # A negative weight is impossible, so it is refused.
        load = require_number(value, "load_kg")
        if load < 0:
            raise ValueError("load_kg cannot be negative")
        self._load_kg = load

    def _kind_findings(self):
        return []

    def describe(self):
        percent = round(self._load_kg * 100 / self._capacity_kg)
        return f"{super().describe()}, {percent}% full"


if __name__ == "__main__":
    temp = Sensor("oven-temp", "temperature", "C", low=0, high=240)
    print(temp.sensor_id, temp.value, temp.status())
    temp.record(212.4)
    print(temp.sensor_id, temp.value, temp.status())
    temp.record(251)
    print(temp.sensor_id, temp.value, temp.status())
    temp.clear()
    print(temp.sensor_id, temp.value, temp.status())

    rack = StorageRack("L3-RCK-01", "Finished Goods Rack", capacity_kg=1200)
    rack.load_kg = 1150
    print(rack.describe())
    rack.load_kg = 1500
    print(rack.describe())
    print(Equipment.is_valid_asset_tag("L3-RCK-01"), Equipment.is_valid_asset_tag("l3-rck-01"))
    try:
        rack.load_kg = -5
    except ValueError as error:
        print("refused:", error)

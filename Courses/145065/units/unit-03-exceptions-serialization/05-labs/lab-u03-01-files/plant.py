# plant.py
# The Line 3 model for Unit 3, at Riverside Fabrication, a composite shop
# invented for this course. STARTER FILE for Lab U03-01. It runs.
#
# Every refusal in this file raises a built-in exception: ValueError,
# RuntimeError, or KeyError. Code that catches them cannot tell a locked-out
# press from a typo. Step 3 changes each raise to a class from errors.py.

import math
import re
from abc import ABC

TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-blank string")
    return value.strip()


def require_positive(value, label, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a number, not {type(value).__name__}")
    if not math.isfinite(value) or value <= 0 or (maximum is not None and value > maximum):
        limit = "" if maximum is None else f" and at most {maximum:g}"
        raise ValueError(f"{label} must be above 0{limit}")
    return float(value)


def require_count(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a whole number of at least 0")
    return value


class Equipment(ABC):
    kind = "equipment"

    def __init__(self, asset_tag, name):
        if not isinstance(asset_tag, str) or TAG_PATTERN.fullmatch(asset_tag) is None:
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        self._asset_tag = asset_tag
        self._name = require_text(name, "name")

    @property
    def asset_tag(self):
        return self._asset_tag

    @property
    def name(self):
        return self._name

    def describe(self):
        return f"{self._asset_tag} {self._name} ({self.kind})"


class PoweredEquipment(Equipment):
    kind = "powered"

    def __init__(self, asset_tag, name, rated_kw):
        super().__init__(asset_tag, name)
        self._rated_kw = require_positive(rated_kw, "rated_kw", 500)
        self._running = False
        self._lockout_holder = None

    @property
    def rated_kw(self):
        return self._rated_kw

    @property
    def is_running(self):
        return self._running

    @property
    def locked_out_by(self):
        return self._lockout_holder

    def start(self):
        if self._lockout_holder is not None:
            raise RuntimeError(f"{self._asset_tag}: locked out by {self._lockout_holder}; cannot start")
        self._running = True

    def stop(self):
        self._running = False

    def lock_out(self, badge):
        badge = require_text(badge, "badge")
        if self._lockout_holder not in (None, badge):
            raise RuntimeError(f"{self._asset_tag}: already locked out by {self._lockout_holder}")
        self.stop()
        self._lockout_holder = badge

    def release_lockout(self, badge):
        if self._lockout_holder is None:
            raise RuntimeError(f"{self._asset_tag}: is not locked out")
        if badge != self._lockout_holder:
            raise RuntimeError(f"{self._asset_tag}: only {self._lockout_holder} can release this lockout")
        self._lockout_holder = None

    def describe(self):
        state = "running" if self._running else "stopped"
        return f"{super().describe()} {self._rated_kw:g} kW, {state}"


class Press(PoweredEquipment):
    kind = "press"

    def __init__(self, asset_tag, name, rated_kw, tonnage, service_interval=20000):
        super().__init__(asset_tag, name, rated_kw)
        self._tonnage = require_positive(tonnage, "tonnage", 2000)
        self._service_interval = require_count(service_interval, "service_interval")
        self._strokes_since_service = 0
        self._guard_closed = False  # unknown counts as open

    @property
    def tonnage(self):
        return self._tonnage

    @property
    def service_interval(self):
        return self._service_interval

    @property
    def strokes_since_service(self):
        return self._strokes_since_service

    @property
    def guard_closed(self):
        return self._guard_closed

    def close_guard(self):
        self._guard_closed = True

    def open_guard(self):
        self._guard_closed = False
        self.stop()

    def start(self):
        if not self._guard_closed:
            raise RuntimeError(f"{self.asset_tag}: guard is open; close it before starting")
        super().start()

    def record_strokes(self, count):
        if not self._running:
            raise RuntimeError(f"{self.asset_tag}: is not running, so it cannot record strokes")
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ValueError("stroke count must be a whole number of at least 1")
        self._strokes_since_service += count


class Oven(PoweredEquipment):
    kind = "oven"

    def __init__(self, asset_tag, name, rated_kw, setpoint_c, max_c):
        super().__init__(asset_tag, name, rated_kw)
        self._max_c = require_positive(max_c, "max_c")
        self.setpoint_c = setpoint_c

    @property
    def max_c(self):
        return self._max_c

    @property
    def setpoint_c(self):
        return self._setpoint_c

    @setpoint_c.setter
    def setpoint_c(self, value):
        self._setpoint_c = require_positive(value, "setpoint_c", self._max_c)


class Conveyor(PoweredEquipment):
    kind = "conveyor"

    def __init__(self, asset_tag, name, rated_kw, max_speed_mps):
        super().__init__(asset_tag, name, rated_kw)
        self._max_speed_mps = require_positive(max_speed_mps, "max_speed_mps")
        self._speed_mps = 0.0

    @property
    def max_speed_mps(self):
        return self._max_speed_mps

    @property
    def speed_mps(self):
        return self._speed_mps

    @speed_mps.setter
    def speed_mps(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"speed_mps must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or not 0 <= value <= self._max_speed_mps:
            raise ValueError(f"speed must be from 0 to {self._max_speed_mps:g} m/s")
        self._speed_mps = float(value)


class StorageRack(Equipment):
    kind = "rack"

    def __init__(self, asset_tag, name, capacity_kg):
        super().__init__(asset_tag, name)
        self._capacity_kg = require_positive(capacity_kg, "capacity_kg")
        self._load_kg = 0.0

    @property
    def capacity_kg(self):
        return self._capacity_kg

    @property
    def load_kg(self):
        return self._load_kg

    @load_kg.setter
    def load_kg(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"load_kg must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or value < 0:
            raise ValueError("load_kg must be a finite number of at least 0")
        self._load_kg = float(value)


class Cell:
    def __init__(self, name):
        self._name = require_text(name, "cell name")
        self._items = []

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return tuple(self._items)

    def add(self, item):
        if not isinstance(item, (Equipment, Cell)):
            raise TypeError(f"a cell holds Equipment and Cell objects, not {type(item).__name__}")
        self._items.append(item)
        return item


class Line:
    def __init__(self, name):
        self._name = require_text(name, "line name")
        self._cells = []

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return tuple(self._cells)

    def add_cell(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError(f"a line holds Cell objects, not {type(cell).__name__}")
        self._cells.append(cell)
        return cell

    def equipment(self):
        found = []

        def collect(node):
            for item in node.items:
                if isinstance(item, Cell):
                    collect(item)
                else:
                    found.append(item)

        collect(self)
        return found

    def get(self, asset_tag):
        """The equipment with this tag. Raises KeyError if none."""
        for item in self.equipment():
            if item.asset_tag == asset_tag:
                return item
        raise KeyError(f"{asset_tag}: not on this line")


def build_sample_line():
    line = Line("Line 3")
    forming = line.add_cell(Cell("Forming"))
    forming.add(Press("L3-PRS-01", "Press 1", rated_kw=15, tonnage=60))
    forming.add(Press("L3-PRS-02", "Press 2", rated_kw=22, tonnage=100))
    finishing = line.add_cell(Cell("Finishing"))
    finishing.add(Oven("L3-OVN-01", "Cure Oven", rated_kw=45, setpoint_c=200, max_c=240))
    transfer = finishing.add(Cell("Transfer"))
    transfer.add(Conveyor("L3-CNV-01", "Transfer Conveyor", rated_kw=3, max_speed_mps=1.5))
    staging = line.add_cell(Cell("Staging"))
    staging.add(StorageRack("L3-RCK-01", "Finished Goods Rack", capacity_kg=1200))
    return line

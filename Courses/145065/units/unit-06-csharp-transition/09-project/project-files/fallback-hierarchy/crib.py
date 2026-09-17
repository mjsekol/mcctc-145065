"""Riverside Fabrication tool crib: a Unit 2 style class hierarchy.

The fallback hierarchy for the Unit 6 port project. Port this only if your
own Unit 2 hierarchy is unusable and your instructor has approved the switch.
Riverside Fabrication is a composite: an invented shop. Badge ids are invented.

    CribItem (abstract)            level 1: anything with a crib tag
    ├── PoweredTool (abstract)     level 2: runs, needs service, can be checked out
    │   ├── Drill                  level 3: has a Battery (composition)
    │   └── Grinder                level 3: has a guard
    └── HandTool                   level 2: needs calibration

    Battery                        not a CribItem: a drill HAS a battery
    Kit                            a named group of items and smaller kits
"""

import re
from abc import ABC, abstractmethod

TAG_PATTERN = re.compile(r"CRIB-[0-9]{3}")


class CribItem(ABC):
    kind = "item"

    def __init__(self, tag, name):
        if not CribItem.is_valid_tag(tag):
            raise ValueError(f"tag {tag!r} does not match CRIB-000")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-blank string")
        self._tag = tag
        self._name = name.strip()

    @staticmethod
    def is_valid_tag(tag):
        return isinstance(tag, str) and TAG_PATTERN.fullmatch(tag) is not None

    @property
    def tag(self):
        return self._tag

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return f"{self._tag} {self._name}"

    @abstractmethod
    def issues(self):
        """A list of strings. Empty when nothing is wrong."""

    def describe(self):
        return f"{self.label} ({self.kind})"


class PoweredTool(CribItem):
    kind = "powered"
    service_every_hours = 100

    def __init__(self, tag, name):
        super().__init__(tag, name)
        self._hours_since_service = 0.0
        self._checked_out_to = None

    @property
    def hours_since_service(self):
        return self._hours_since_service

    @property
    def checked_out_to(self):
        return self._checked_out_to

    def log_hours(self, hours):
        if isinstance(hours, bool) or not isinstance(hours, (int, float)) or hours <= 0:
            raise ValueError("hours must be a number above 0")
        self._hours_since_service += hours

    def service_done(self):
        self._hours_since_service = 0.0

    def check_out(self, badge):
        if self._checked_out_to is not None:
            raise RuntimeError(f"{self._tag} is already checked out to {self._checked_out_to}")
        self._checked_out_to = badge

    def check_in(self):
        self._checked_out_to = None

    def issues(self):
        found = []
        if self._hours_since_service >= self.service_every_hours:
            found.append(f"{self.label}: service due ({self._hours_since_service:g} h)")
        return found


class Battery:
    def __init__(self, charge_percent=100):
        self.charge_percent = charge_percent

    @property
    def charge_percent(self):
        return self._charge_percent

    @charge_percent.setter
    def charge_percent(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
            raise ValueError("charge must be a number from 0 to 100")
        self._charge_percent = value

    @property
    def label(self):
        return "battery"

    def issues(self):
        if self._charge_percent < 20:
            return [f"battery low ({self._charge_percent:g}%)"]
        return []


class Drill(PoweredTool):
    kind = "drill"
    service_every_hours = 50

    def __init__(self, tag, name, battery=None):
        super().__init__(tag, name)
        self._battery = battery if battery is not None else Battery()

    @property
    def battery(self):
        return self._battery

    def issues(self):
        found = super().issues()
        found.extend(f"{self.label}: {issue}" for issue in self._battery.issues())
        return found


class Grinder(PoweredTool):
    kind = "grinder"

    def __init__(self, tag, name, guard_fitted=True):
        super().__init__(tag, name)
        self.guard_fitted = guard_fitted

    def issues(self):
        found = super().issues()
        if not self.guard_fitted:
            found.append(f"{self.label}: guard missing, do not issue")
        return found


class HandTool(CribItem):
    kind = "hand"

    def __init__(self, tag, name, calibration_days_left):
        super().__init__(tag, name)
        self.calibration_days_left = calibration_days_left

    def issues(self):
        if self.calibration_days_left <= 0:
            return [f"{self.label}: calibration expired"]
        return []


class Kit:
    def __init__(self, name):
        self.name = name
        self.items = []

    @property
    def label(self):
        return f"kit {self.name}"

    def add(self, item):
        self.items.append(item)
        return item

    def issues(self):
        found = []
        for item in self.items:
            found.extend(item.issues())
        return found

    def count_tools(self):
        total = 0
        for item in self.items:
            total += item.count_tools() if isinstance(item, Kit) else 1
        return total


def crib_report(things):
    """The polymorphic loop that replaced an if/elif chain on kind."""
    lines = []
    for thing in things:
        lines.extend(thing.issues())
    return lines


def build_sample_crib():
    weak = Battery(charge_percent=12)
    drill = Drill("CRIB-001", "Cordless Drill", battery=weak)
    drill.log_hours(52)
    grinder = Grinder("CRIB-002", "Angle Grinder", guard_fitted=False)
    wrench = HandTool("CRIB-003", "Torque Wrench", calibration_days_left=0)
    spare = Drill("CRIB-004", "Spare Drill")

    setup = Kit("setup")
    setup.add(wrench)
    inner = setup.add(Kit("drilling"))
    inner.add(spare)
    return [drill, grinder, setup]

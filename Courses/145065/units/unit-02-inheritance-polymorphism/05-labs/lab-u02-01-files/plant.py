# plant.py
# Line 3 equipment at Riverside Fabrication, a composite shop invented for
# this course. STARTER FILE for Lab U02-01. It runs.
#
#     python plant.py
#
# Three classes, written one after another by copying. Look at how much of
# Press and Oven is the same code typed twice. Your job this week is to move
# the shared parts into parent classes so each rule lives in exactly one place.
#
# Do not change main() until the lab tells you to. The self-check expects the
# names used here: Press, Oven, StorageRack, and their methods.

import re

# Asset tags look like L3-PRS-01. [0-9], not \d: \d also matches digits from
# other writing systems.
TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")


class Press:
    """A stamping press."""

    kind = "press"

    def __init__(self, asset_tag, name, rated_kw, tonnage):
        # ---- the same checks appear in all three classes ----
        if not isinstance(asset_tag, str) or TAG_PATTERN.fullmatch(asset_tag) is None:
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-blank string")
        self._asset_tag = asset_tag
        self._name = name.strip()
        # ---- the same power and lockout state appears in Press and Oven ----
        if isinstance(rated_kw, bool) or not isinstance(rated_kw, (int, float)) or rated_kw <= 0:
            raise ValueError("rated_kw must be a number above 0")
        self._rated_kw = float(rated_kw)
        self._running = False
        self._lockout_holder = None
        # ---- press only ----
        if isinstance(tonnage, bool) or not isinstance(tonnage, (int, float)) or tonnage <= 0:
            raise ValueError("tonnage must be a number above 0")
        self._tonnage = float(tonnage)
        self._guard_closed = False  # unknown counts as open

    @property
    def asset_tag(self):
        return self._asset_tag

    @property
    def name(self):
        return self._name

    @property
    def is_running(self):
        return self._running

    @property
    def is_locked_out(self):
        return self._lockout_holder is not None

    @property
    def guard_closed(self):
        return self._guard_closed

    def start(self):
        if self._lockout_holder is not None:
            raise RuntimeError(f"{self._asset_tag} is locked out by {self._lockout_holder}")
        if not self._guard_closed:
            raise RuntimeError(f"{self._asset_tag} guard is open; close it before starting")
        self._running = True

    def stop(self):
        self._running = False

    def lock_out(self, badge):
        if not isinstance(badge, str) or not badge.strip():
            raise ValueError("badge must be a non-blank string")
        if self._lockout_holder is not None and self._lockout_holder != badge:
            raise RuntimeError(f"{self._asset_tag} is already locked out by {self._lockout_holder}")
        self.stop()
        self._lockout_holder = badge

    def release_lockout(self, badge):
        if self._lockout_holder is None:
            raise RuntimeError(f"{self._asset_tag} is not locked out")
        if badge != self._lockout_holder:
            raise RuntimeError(f"only {self._lockout_holder} can release {self._asset_tag}")
        self._lockout_holder = None

    def close_guard(self):
        self._guard_closed = True

    def open_guard(self):
        self._guard_closed = False
        self._running = False

    def describe(self):
        state = "running" if self._running else "stopped"
        return f"{self._asset_tag} {self._name} (press) {self._rated_kw:g} kW, {state}"

    def problems(self):
        found = []
        if self._lockout_holder is not None:
            found.append(f"{self._asset_tag}: locked out by {self._lockout_holder}")
        if not self._guard_closed:
            found.append(f"{self._asset_tag}: guard is open; press cannot run")
        return found


class Oven:
    """A curing oven."""

    kind = "oven"
    TOLERANCE_C = 10.0

    def __init__(self, asset_tag, name, rated_kw, setpoint_c, max_c):
        if not isinstance(asset_tag, str) or TAG_PATTERN.fullmatch(asset_tag) is None:
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-blank string")
        self._asset_tag = asset_tag
        self._name = name.strip()
        if isinstance(rated_kw, bool) or not isinstance(rated_kw, (int, float)) or rated_kw <= 0:
            raise ValueError("rated_kw must be a number above 0")
        self._rated_kw = float(rated_kw)
        self._running = False
        self._lockout_holder = None
        # ---- oven only ----
        if not 0 < setpoint_c <= max_c:
            raise ValueError("setpoint_c must be above 0 and at most max_c")
        self._setpoint_c = float(setpoint_c)
        self._max_c = float(max_c)
        self._temperature_c = None  # None means no reading, never zero

    @property
    def asset_tag(self):
        return self._asset_tag

    @property
    def name(self):
        return self._name

    @property
    def is_running(self):
        return self._running

    @property
    def is_locked_out(self):
        return self._lockout_holder is not None

    @property
    def temperature_c(self):
        return self._temperature_c

    def start(self):
        if self._lockout_holder is not None:
            raise RuntimeError(f"{self._asset_tag} is locked out by {self._lockout_holder}")
        self._running = True

    def stop(self):
        self._running = False

    def lock_out(self, badge):
        if not isinstance(badge, str) or not badge.strip():
            raise ValueError("badge must be a non-blank string")
        if self._lockout_holder is not None and self._lockout_holder != badge:
            raise RuntimeError(f"{self._asset_tag} is already locked out by {self._lockout_holder}")
        self._lockout_holder = badge

    def release_lockout(self, badge):
        if self._lockout_holder is None:
            raise RuntimeError(f"{self._asset_tag} is not locked out")
        if badge != self._lockout_holder:
            raise RuntimeError(f"only {self._lockout_holder} can release {self._asset_tag}")
        self._lockout_holder = None

    def record_temperature(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("temperature must be a number")
        self._temperature_c = float(value)

    def describe(self):
        state = "running" if self._running else "stopped"
        return f"{self._asset_tag} {self._name} (oven) {self._rated_kw:g} kW, {state}"

    def problems(self):
        found = []
        if self._lockout_holder is not None:
            found.append(f"{self._asset_tag}: locked out by {self._lockout_holder}")
        value = self._temperature_c
        if value is None:
            found.append(f"{self._asset_tag}: no temperature reading")
            return found
        if value > self._max_c:
            found.append(f"{self._asset_tag}: {value:g} C is above the maximum {self._max_c:g} C")
        drift = abs(value - self._setpoint_c)
        if self._running and drift > Oven.TOLERANCE_C:
            found.append(f"{self._asset_tag}: {value:g} C is {drift:g} C from setpoint {self._setpoint_c:g} C")
        return found


class StorageRack:
    """A rack for finished parts. It has no power."""

    kind = "rack"

    def __init__(self, asset_tag, name, capacity_kg):
        if not isinstance(asset_tag, str) or TAG_PATTERN.fullmatch(asset_tag) is None:
            raise ValueError(f"asset tag {asset_tag!r} does not match the L3-ABC-00 pattern")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-blank string")
        self._asset_tag = asset_tag
        self._name = name.strip()
        # ---- rack only ----
        if isinstance(capacity_kg, bool) or not isinstance(capacity_kg, (int, float)) or capacity_kg <= 0:
            raise ValueError("capacity_kg must be a number above 0")
        self._capacity_kg = float(capacity_kg)
        self._load_kg = 0.0

    @property
    def asset_tag(self):
        return self._asset_tag

    @property
    def name(self):
        return self._name

    @property
    def load_kg(self):
        return self._load_kg

    @load_kg.setter
    def load_kg(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("load_kg must be a number of at least 0")
        self._load_kg = float(value)

    def describe(self):
        return f"{self._asset_tag} {self._name} (rack)"

    def problems(self):
        if self._load_kg > self._capacity_kg:
            return [f"{self._asset_tag}: overloaded: {self._load_kg:g} kg on a {self._capacity_kg:g} kg rack"]
        if self._load_kg >= self._capacity_kg * 0.9:
            return [f"{self._asset_tag}: at {self._load_kg / self._capacity_kg:.0%} of capacity"]
        return []


def build_sample():
    press1 = Press("L3-PRS-01", "Press 1", 15, 60)
    press2 = Press("L3-PRS-02", "Press 2", 22, 100)
    oven = Oven("L3-OVN-01", "Cure Oven", 45, 200, 240)
    rack = StorageRack("L3-RCK-01", "Finished Goods Rack", 1200)
    return [press1, press2, oven, rack]


def main():
    press1, press2, oven, rack = build_sample()
    press1.close_guard()
    press1.start()
    press2.lock_out("tech-07")
    oven.start()
    oven.record_temperature(228)
    rack.load_kg = 1150

    for item in (press1, press2, oven, rack):
        print(item.describe())
    print()
    print("Problems:")
    for item in (press1, press2, oven, rack):
        for problem in item.problems():
            print(f"  {problem}")


if __name__ == "__main__":
    main()

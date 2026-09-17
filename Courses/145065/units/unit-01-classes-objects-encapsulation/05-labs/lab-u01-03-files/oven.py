# oven.py
# Lab U01-03: Guard the State. STARTER.
#
# The Line 3 cure oven, written the Week 2 way: every attribute is public,
# and the rules live in the methods. It works, as long as everyone calls the
# methods. rogue_script.py shows what happens when someone does not.
#
# Riverside Fabrication is a composite shop. Everything here is invented.
#
#     python oven.py
#     python rogue_script.py
#     python selfcheck_oven.py part1
#     python selfcheck_oven.py part2
#
# This file runs. Part 1 (Monday) guards its state with underscores and
# properties. Part 2 (Tuesday) adds a static method and two class methods.

MIN_READING_C = -40.0     # the sensor cannot read below this
MAX_READING_C = 1200.0    # or above this
MAX_OVEN_C = 400.0        # no oven on Line 3 is rated above this


class Oven:
    """A cure oven on Line 3."""

    def __init__(self, asset_tag, name, setpoint_c, max_c):
        self.asset_tag = asset_tag
        self.name = name
        self.max_c = max_c
        self.setpoint_c = setpoint_c
        self.temperature_c = None     # None means "never read", which is not 0
        self.heating = False
        self.door_open = False
        self.last_opened_by = None    # the badge of whoever last opened the door

    def record_temperature(self, celsius):
        self.temperature_c = celsius

    def start_heating(self):
        if self.door_open:
            raise RuntimeError(f"{self.asset_tag} door is open; close it before heating")
        self.heating = True

    def stop_heating(self):
        self.heating = False

    def open_door(self, badge):
        # Opening the door always stops the heat. A person may reach inside.
        self.stop_heating()
        self.door_open = True
        self.last_opened_by = badge

    def close_door(self):
        self.door_open = False

    def status_text(self):
        if self.door_open:
            state = f"DOOR OPEN ({self.last_opened_by})"
        elif self.heating:
            state = "HEATING"
        else:
            state = "IDLE"
        if self.temperature_c is None:
            reading = "no reading"
        else:
            reading = f"reads {self.temperature_c:.1f} C"
        return f"{self.asset_tag} {self.name}: {state}, setpoint {self.setpoint_c:g} C, {reading}"

    def __repr__(self):
        return (f"Oven(asset_tag={self.asset_tag!r}, name={self.name!r}, "
                f"setpoint_c={self.setpoint_c!r}, max_c={self.max_c!r})")


if __name__ == "__main__":
    oven = Oven("L3-OVN-01", "Cure Oven", 200.0, 240.0)
    oven.start_heating()
    oven.record_temperature(185.5)
    print(oven.status_text())
    oven.open_door("tech-07")
    print(oven.status_text())
    print(repr(oven))

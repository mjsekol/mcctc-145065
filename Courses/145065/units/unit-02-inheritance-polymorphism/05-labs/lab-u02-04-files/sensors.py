# sensors.py
# Line 3 equipment and the sensors mounted on it, at Riverside Fabrication,
# a composite shop invented for this course.
# STARTER FILE for Lab U02-04. It runs.
#
#     python sensors.py
#
# Last year someone added readings to the model by inheritance. Every
# combination of readings became its own subclass: a press with vibration, a
# press with coolant, a press with both. Look at VibrationCoolantPress. It is
# two classes pasted together, because Python had no clean way to say
# "a press that has these two sensors".
#
# The Sensor class below is complete and nothing uses it yet. Your job is to
# make equipment HAVE sensors, and delete the four reading subclasses.

import re
from dataclasses import dataclass

SEVERITIES = ("info", "warning", "stop")
_ID_PATTERN = re.compile(r"[a-z][a-z0-9-]{1,31}")


@dataclass(frozen=True)
class Finding:
    asset_tag: str
    severity: str
    message: str

    def __post_init__(self):
        if self.severity not in SEVERITIES:
            raise ValueError(f"severity must be one of {SEVERITIES}, not {self.severity!r}")

    def __str__(self):
        return f"[{self.severity.upper()}] {self.asset_tag}: {self.message}"


class Sensor:
    """A sensor mounted on one piece of equipment. GIVEN. Do not change it."""

    def __init__(self, sensor_id, kind, unit, low, high):
        if not isinstance(sensor_id, str) or _ID_PATTERN.fullmatch(sensor_id) is None:
            raise ValueError(f"sensor id {sensor_id!r} must be lowercase letters, digits, and hyphens")
        if low >= high:
            raise ValueError(f"low limit {low:g} must be below high limit {high:g}")
        self._sensor_id = sensor_id
        self._kind = kind
        self._unit = unit
        self._low = low
        self._high = high
        self._value = None  # None means no current reading. It never means zero.
        self._owner_tag = None

    @property
    def sensor_id(self):
        return self._sensor_id

    @property
    def kind(self):
        return self._kind

    @property
    def value(self):
        return self._value

    @property
    def owner_tag(self):
        return self._owner_tag

    def record(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value != value:
            raise ValueError(f"{self._sensor_id} reading must be a real number")
        self._value = float(value)

    def clear(self):
        """The reading is gone: sensor fault, cable pulled. Missing, not zero."""
        self._value = None

    def status(self):
        if self._value is None:
            return "no reading"
        if self._value < self._low:
            return "low"
        if self._value > self._high:
            return "high"
        return "ok"

    def inspect(self):
        tag = self._owner_tag or "unmounted"
        status = self.status()
        if status == "ok":
            return []
        if status == "no reading":
            return [Finding(tag, "info", f"{self._sensor_id} has no reading")]
        side, limit = ("below", self._low) if status == "low" else ("above", self._high)
        return [Finding(tag, "warning",
                        f"{self._sensor_id} reads {self._value:g} {self._unit}, {side} {limit:g}")]

    def _mount(self, owner_tag):
        """Called by PoweredEquipment.attach_sensor(). A sensor has one owner."""
        if self._owner_tag is not None and self._owner_tag != owner_tag:
            raise ValueError(f"{self._sensor_id} is already mounted on {self._owner_tag}")
        self._owner_tag = owner_tag


class Equipment:
    kind = "equipment"

    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    def inspect(self):
        return self.common_findings() + self._kind_findings()

    def common_findings(self):
        return []

    def _kind_findings(self):
        return []


class PoweredEquipment(Equipment):
    kind = "powered"

    def __init__(self, asset_tag, name):
        super().__init__(asset_tag, name)
        self.is_running = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False


class Press(PoweredEquipment):
    kind = "press"


class VibrationPress(Press):
    """A press with a vibration reading."""

    def __init__(self, asset_tag, name):
        super().__init__(asset_tag, name)
        self.vibration = None
        self.vibration_high = 8.0

    def record_vibration(self, value):
        self.vibration = float(value)

    def clear_vibration(self):
        self.vibration = None

    def _kind_findings(self):
        findings = super()._kind_findings()
        if self.vibration is None:
            findings.append(Finding(self.asset_tag, "info", "press-vibration has no reading"))
        elif self.vibration > self.vibration_high:
            findings.append(Finding(self.asset_tag, "warning",
                                    f"press-vibration reads {self.vibration:g} mm/s, above {self.vibration_high:g}"))
        return findings


class CoolantPress(Press):
    """A press with a coolant level reading."""

    def __init__(self, asset_tag, name):
        super().__init__(asset_tag, name)
        self.coolant = None
        self.coolant_low = 20.0

    def record_coolant(self, value):
        self.coolant = float(value)

    def _kind_findings(self):
        findings = super()._kind_findings()
        if self.coolant is None:
            findings.append(Finding(self.asset_tag, "info", "coolant-level has no reading"))
        elif self.coolant < self.coolant_low:
            findings.append(Finding(self.asset_tag, "warning",
                                    f"coolant-level reads {self.coolant:g} %, below {self.coolant_low:g}"))
        return findings


class VibrationCoolantPress(Press):
    """A press with both readings. Press 1 is one of these.

    Both parent classes above would each need to be a parent here, and both
    define _kind_findings(). So both readings were pasted in by hand.
    """

    def __init__(self, asset_tag, name):
        super().__init__(asset_tag, name)
        self.vibration = None
        self.vibration_high = 8.0
        self.coolant = None
        self.coolant_low = 20.0

    def record_vibration(self, value):
        self.vibration = float(value)

    def clear_vibration(self):
        self.vibration = None

    def record_coolant(self, value):
        self.coolant = float(value)

    def _kind_findings(self):
        findings = super()._kind_findings()
        if self.vibration is None:
            findings.append(Finding(self.asset_tag, "info", "press-vibration has no reading"))
        elif self.vibration > self.vibration_high:
            findings.append(Finding(self.asset_tag, "warning",
                                    f"press-vibration reads {self.vibration:g} mm/s, above {self.vibration_high:g}"))
        if self.coolant is None:
            findings.append(Finding(self.asset_tag, "info", "coolant-level has no reading"))
        elif self.coolant < self.coolant_low:
            findings.append(Finding(self.asset_tag, "warning",
                                    f"coolant-level reads {self.coolant:g} %, below {self.coolant_low:g}"))
        return findings


class Oven(PoweredEquipment):
    kind = "oven"
    TOLERANCE_C = 10.0

    def __init__(self, asset_tag, name, setpoint_c, max_c):
        super().__init__(asset_tag, name)
        self.setpoint_c = setpoint_c
        self.max_c = max_c

    def _kind_findings(self):
        return [Finding(self.asset_tag, "warning", "no temperature sensor mounted")]


class MonitoredOven(Oven):
    """An oven with a temperature reading."""

    def __init__(self, asset_tag, name, setpoint_c, max_c):
        super().__init__(asset_tag, name, setpoint_c, max_c)
        self.temperature = None

    def record_temperature(self, value):
        self.temperature = float(value)

    def _kind_findings(self):
        value = self.temperature
        if value is None:
            return [Finding(self.asset_tag, "info", "oven-temp has no reading")]
        findings = []
        if value > 240:
            findings.append(Finding(self.asset_tag, "warning", f"oven-temp reads {value:g} C, above 240"))
        if value > self.max_c:
            findings.append(Finding(self.asset_tag, "stop",
                                    f"{value:g} C is above the oven maximum {self.max_c:g} C"))
        drift = abs(value - self.setpoint_c)
        if self.is_running and drift > Oven.TOLERANCE_C:
            findings.append(Finding(self.asset_tag, "warning",
                                    f"{value:g} C is {drift:g} C from setpoint {self.setpoint_c:g} C"))
        return findings


def build_sample():
    press1 = VibrationCoolantPress("L3-PRS-01", "Press 1")
    press2 = VibrationPress("L3-PRS-02", "Press 2")
    oven = MonitoredOven("L3-OVN-01", "Cure Oven", setpoint_c=200, max_c=240)
    return [press1, press2, oven]


def record_sample_readings(press1, press2, oven):
    press1.record_vibration(3.1)
    press1.record_coolant(14)
    press2.record_vibration(9.2)
    oven.start()
    oven.record_temperature(228)


def main():
    press1, press2, oven = build_sample()
    record_sample_readings(press1, press2, oven)
    print("Findings:")
    for item in (press1, press2, oven):
        for finding in item.inspect():
            print(f"  {finding}")
    press2.clear_vibration()
    print()
    print("After the Press 2 cable is pulled:")
    for finding in press2.inspect():
        print(f"  {finding}")


if __name__ == "__main__":
    main()

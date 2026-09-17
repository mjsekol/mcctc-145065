"""Polymorphic inspection for Riverside Fabrication, Line 3.

Every machine answers inspect() for itself, so the line never branches on
equipment type. Sensors are composed into powered equipment rather than
inherited, which lets one machine carry any mix of sensors.

Riverside Fabrication is a composite shop invented for this course.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

SEVERITIES = ("info", "warning", "stop")


@dataclass(frozen=True)
class Finding:
    asset_tag: str
    severity: str
    message: str

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"unknown severity {self.severity!r}")

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.asset_tag}: {self.message}"


class Sensor:
    """One sensor. It reports against its own low and high limits."""

    def __init__(self, sensor_id: str, unit: str, low: float, high: float) -> None:
        self.sensor_id = sensor_id
        self.unit = unit
        self.low = low
        self.high = high
        self.value = None
        self.owner_tag = None

    def record(self, value: float) -> None:
        self.value = float(value)

    def inspect(self) -> list:
        tag = self.owner_tag or "unmounted"
        if self.value is None:
            return [Finding(tag, "info", f"{self.sensor_id} has no reading")]
        if self.value < self.low:
            return [Finding(tag, "warning", f"{self.sensor_id} reads {self.value:g} {self.unit}, below {self.low:g}")]
        if self.value > self.high:
            return [Finding(tag, "warning", f"{self.sensor_id} reads {self.value:g} {self.unit}, above {self.high:g}")]
        return []


class Equipment(ABC):
    """Anything on the line with an asset tag."""

    kind = "equipment"

    def __init__(self, asset_tag: str, name: str) -> None:
        self.asset_tag = asset_tag
        self.name = name

    def inspect(self) -> list:
        """Shared findings first, then this kind's own findings."""
        if not self.common_findings():
            return self._kind_findings()
        return self.common_findings() + self._kind_findings()

    def common_findings(self) -> list:
        return []

    @abstractmethod
    def _kind_findings(self) -> list:
        """Findings only this kind of equipment knows how to make."""


class PoweredEquipment(Equipment):
    """Equipment that runs, can be locked out, and has sensors."""

    kind = "powered"

    def __init__(self, asset_tag: str, name: str) -> None:
        super().__init__(asset_tag, name)
        self.is_running = False
        self.locked_by = None
        self._sensors = {}

    def start(self) -> None:
        if self.locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self.locked_by}")
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def lock_out(self, badge: str) -> None:
        self.stop()
        self.locked_by = badge

    def attach_sensor(self, sensor: Sensor) -> Sensor:
        """Mount a sensor. Sensor ids are unique per machine."""
        if not isinstance(sensor, Sensor):
            raise TypeError(f"expected a Sensor, not {type(sensor).__name__}")
        if sensor.sensor_id in self._sensors:
            raise ValueError(f"{self.asset_tag} already has a sensor named {sensor.sensor_id}")
        sensor.owner_tag = self.asset_tag
        self._sensors[sensor.sensor_id] = sensor
        return sensor

    @property
    def sensors(self) -> dict:
        """The sensors mounted on this machine, by id."""
        return self._sensors

    def common_findings(self) -> list:
        findings = []
        if self.locked_by is not None:
            findings.append(Finding(self.asset_tag, "info", f"locked out by {self.locked_by}"))
        for sensor in self._sensors.values():
            findings.extend(sensor.inspect())
        return findings


class Press(PoweredEquipment):
    kind = "press"

    def __init__(self, asset_tag: str, name: str) -> None:
        super().__init__(asset_tag, name)
        self.guard_closed = False

    def _kind_findings(self) -> list:
        if not self.guard_closed:
            return [Finding(self.asset_tag, "stop", "guard is open; press cannot run")]
        return []


class Conveyor(PoweredEquipment):
    kind = "conveyor"

    def __init__(self, asset_tag: str, name: str, max_speed_mps: float) -> None:
        super().__init__(asset_tag, name)
        self.max_speed_mps = max_speed_mps
        self.speed_mps = 0.0

    def common_findings(self) -> list:
        # A running belt at zero speed is a stall, which matters on every conveyor.
        if self.is_running and self.speed_mps == 0:
            return [Finding(self.asset_tag, "warning", "running with belt speed 0 m/s; check for a stall")]
        return []

    def _kind_findings(self) -> list:
        if self.speed_mps > self.max_speed_mps:
            return [Finding(self.asset_tag, "stop", f"belt at {self.speed_mps:g} m/s, above {self.max_speed_mps:g}")]
        return []


class Oven(PoweredEquipment):
    kind = "oven"

    def __init__(self, asset_tag: str, name: str, setpoint_c: float, tolerance_c: float = 10.0) -> None:
        super().__init__(asset_tag, name)
        self.setpoint_c = setpoint_c
        self.tolerance_c = tolerance_c

    def _kind_findings(self) -> list:
        sensor = self.sensors.get("oven-temp")
        if sensor is None or sensor.value is None or not self.is_running:
            return []
        drift = abs(sensor.value - self.setpoint_c)
        if drift > self.tolerance_c:
            return [Finding(self.asset_tag, "warning",
                            f"{sensor.value:g} C is {drift:g} C from setpoint {self.setpoint_c:g} C")]
        return []


class Cell:
    """A named group of machines and smaller cells."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items = []

    @property
    def items(self) -> tuple:
        return tuple(self._items)

    def add(self, item):
        if not isinstance(item, (Equipment, Cell)):
            raise TypeError(f"a cell holds equipment and cells, not {type(item).__name__}")
        self._items.append(item)
        return item


def iter_equipment(node):
    for item in node.items:
        if isinstance(item, Cell):
            yield from iter_equipment(item)
        else:
            yield item


class Line(Cell):
    """The top of the layout. A line is a named group of cells."""

    def add_cell(self, cell: Cell) -> Cell:
        if not isinstance(cell, Cell):
            raise TypeError(f"a line holds cells, not {type(cell).__name__}")
        return self.add(cell)

    def equipment(self) -> list:
        return list(iter_equipment(self))

    def inspect_all(self) -> list:
        """Inspect every machine on the line. Findings come back most severe first."""
        findings = []
        for item in self.equipment():
            findings.extend(item.inspect())
        # stop outranks warning, and warning outranks info
        return sorted(findings, key=lambda finding: finding.severity, reverse=True)


def build_sample_line() -> Line:
    line = Line("Line 3")
    forming = line.add_cell(Cell("Forming"))
    press1 = forming.add(Press("L3-PRS-01", "Press 1"))
    press1.attach_sensor(Sensor("press-vibration", "mm/s", 0, 8))
    press1.attach_sensor(Sensor("coolant-level", "%", 20, 100))
    press2 = forming.add(Press("L3-PRS-02", "Press 2"))
    press2.attach_sensor(Sensor("press-vibration", "mm/s", 0, 8))

    finishing = line.add_cell(Cell("Finishing"))
    oven = finishing.add(Oven("L3-OVN-01", "Cure Oven", setpoint_c=200))
    oven.attach_sensor(Sensor("oven-temp", "C", 0, 240))
    transfer = finishing.add(Cell("Transfer"))
    conveyor = transfer.add(Conveyor("L3-CNV-01", "Transfer Conveyor", max_speed_mps=1.5))
    conveyor.attach_sensor(Sensor("belt-temp", "C", 0, 80))
    return line


def main() -> None:
    line = build_sample_line()
    by_tag = {item.asset_tag: item for item in line.equipment()}

    by_tag["L3-PRS-01"].guard_closed = True
    by_tag["L3-PRS-01"].start()
    by_tag["L3-PRS-01"].sensors["press-vibration"].record(3.1)
    by_tag["L3-PRS-01"].sensors["coolant-level"].record(14)
    by_tag["L3-PRS-02"].lock_out("tech-07")
    by_tag["L3-PRS-02"].sensors["press-vibration"].record(0.0)
    by_tag["L3-OVN-01"].start()
    by_tag["L3-OVN-01"].sensors["oven-temp"].record(228)
    by_tag["L3-CNV-01"].start()
    by_tag["L3-CNV-01"].speed_mps = 0.8
    by_tag["L3-CNV-01"].sensors["belt-temp"].record(41)

    print(f"{len(by_tag)} machines inspected")
    for finding in line.inspect_all():
        print(f"  {finding}")


if __name__ == "__main__":
    main()

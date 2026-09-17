# inspection.py
# Inspecting every machine on Line 3 at Riverside Fabrication, a composite
# shop invented for this course. STARTER FILE for Lab U02-03. It runs.
#
#     python inspection.py
#
# Right now one function, inspect_by_kind(), inspects every machine by asking
# what kind it is. It works. Your job is to move each kind's rules into its
# own class, so the loop that inspects the line never has to ask.
#
# Leave inspect_by_kind() and inspect_line_by_kind() exactly as they are.
# They are how you will prove your refactor changed nothing.

from dataclasses import dataclass

SEVERITIES = ("info", "warning", "stop")


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


class Equipment:
    kind = "equipment"

    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    # TODO Step 5: inspect() and an abstract _kind_findings() go here.


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

    def __init__(self, asset_tag, name, service_interval=20000):
        super().__init__(asset_tag, name)
        self.guard_closed = False
        self.strokes_since_service = 0
        self.service_interval = service_interval


class Conveyor(PoweredEquipment):
    kind = "conveyor"

    def __init__(self, asset_tag, name, max_speed_mps):
        super().__init__(asset_tag, name)
        self.max_speed_mps = max_speed_mps
        self.speed_mps = 0.0


class Oven(PoweredEquipment):
    kind = "oven"
    TOLERANCE_C = 10.0

    def __init__(self, asset_tag, name, setpoint_c, max_c):
        super().__init__(asset_tag, name)
        self.setpoint_c = setpoint_c
        self.max_c = max_c
        self.temperature_c = None  # None means no reading, never zero


class StorageRack(Equipment):
    kind = "rack"
    WARN_FRACTION = 0.9

    def __init__(self, asset_tag, name, capacity_kg):
        super().__init__(asset_tag, name)
        self.capacity_kg = capacity_kg
        self.load_kg = 0.0


# ---------- the if/elif chain, kept only to prove the refactor changed nothing ----------

def inspect_by_kind(item):
    """The old way: ask what kind each item is. Do not add new kinds here."""
    findings = []
    if item.kind == "press":
        if not item.guard_closed:
            findings.append(Finding(item.asset_tag, "stop", "guard is open; press cannot run"))
        if item.strokes_since_service >= item.service_interval:
            findings.append(Finding(
                item.asset_tag, "warning",
                f"service due: {item.strokes_since_service} strokes since service "
                f"(interval {item.service_interval})"))
    elif item.kind == "conveyor":
        if item.is_running and item.speed_mps == 0:
            findings.append(Finding(item.asset_tag, "warning",
                                    "running with belt speed 0 m/s; check for a stall or a missing setpoint"))
    elif item.kind == "oven":
        value = item.temperature_c
        if value is None:
            findings.append(Finding(item.asset_tag, "warning", "no temperature reading"))
        else:
            if value > item.max_c:
                findings.append(Finding(item.asset_tag, "stop",
                                        f"{value:g} C is above the oven maximum {item.max_c:g} C"))
            drift = abs(value - item.setpoint_c)
            if item.is_running and drift > 10.0:
                findings.append(Finding(item.asset_tag, "warning",
                                        f"{value:g} C is {drift:g} C from setpoint {item.setpoint_c:g} C"))
    elif item.kind == "rack":
        if item.load_kg > item.capacity_kg:
            findings.append(Finding(item.asset_tag, "stop",
                                    f"overloaded: {item.load_kg:g} kg on a {item.capacity_kg:g} kg rack"))
        elif item.load_kg >= item.capacity_kg * 0.9:
            findings.append(Finding(item.asset_tag, "warning",
                                    f"at {item.load_kg / item.capacity_kg:.0%} of capacity"))
    else:
        raise ValueError(f"no inspection rule for kind {item.kind!r}")
    return findings


def inspect_line_by_kind(items):
    findings = []
    for item in items:
        findings.extend(inspect_by_kind(item))
    return findings


# ---------- the polymorphic loop ----------

def inspect_all(items):
    """The polymorphic version of inspect_line_by_kind()."""
    # TODO Step 6
    return []


def build_sample():
    press1 = Press("L3-PRS-01", "Press 1")
    press1.guard_closed = True
    press1.strokes_since_service = 20150
    press2 = Press("L3-PRS-02", "Press 2")
    oven = Oven("L3-OVN-01", "Cure Oven", setpoint_c=200, max_c=240)
    oven.start()
    oven.temperature_c = 228
    conveyor = Conveyor("L3-CNV-01", "Transfer Conveyor", max_speed_mps=1.5)
    conveyor.start()
    rack = StorageRack("L3-RCK-01", "Finished Goods Rack", capacity_kg=1200)
    rack.load_kg = 1150
    return [press1, press2, oven, conveyor, rack]


def main():
    items = build_sample()
    print("Findings, from the if/elif chain:")
    for finding in inspect_line_by_kind(items):
        print(f"  {finding}")
    print()
    print(f"Findings, asked polymorphically: {len(inspect_all(items))}")


if __name__ == "__main__":
    main()

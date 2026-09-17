# selfcheck_hierarchy.py
# Checks your plant.py against the three parts of Lab U02-01.
#
# Put this file next to plant.py and run:
#     python selfcheck_hierarchy.py
#
# NOT YET means a name the check needs does not exist yet. That is expected
# until you reach that part. FAIL means the name exists and the behavior is wrong.

import dataclasses
import importlib

plant = importlib.import_module("plant")

results = []


def check(part, label, test):
    """Run one check. test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except (AttributeError, NameError) as error:
        results.append((part, "NOT YET", label, str(error)))
        return
    except Exception as error:  # a self-check reports every failure, whatever its type
        results.append((part, "FAIL", label, f"{type(error).__name__}: {error}"))
        return
    if problem is None:
        results.append((part, "PASS", label, ""))
    else:
        results.append((part, "FAIL", label, problem))


def raises(error_type, action):
    try:
        action()
    except error_type:
        return True
    return False


def sample():
    return plant.build_sample()


# ---------------- Part 1 - Monday - the shared parts move up ----------------

def t_equipment_exists():
    plant.Equipment
    plant.PoweredEquipment
    if not issubclass(plant.PoweredEquipment, plant.Equipment):
        return "PoweredEquipment must inherit from Equipment"


def t_three_levels():
    if not issubclass(plant.Press, plant.PoweredEquipment):
        return "Press must inherit from PoweredEquipment"
    if not issubclass(plant.Oven, plant.PoweredEquipment):
        return "Oven must inherit from PoweredEquipment"


def t_rack_level_two():
    if not issubclass(plant.StorageRack, plant.Equipment):
        return "StorageRack must inherit from Equipment"
    if issubclass(plant.StorageRack, plant.PoweredEquipment):
        return "a rack has no power, so it must not inherit from PoweredEquipment"
    if hasattr(plant.StorageRack, "start"):
        return "StorageRack has a start() method; a rack cannot start"


def t_no_copies():
    plant.Equipment
    copied = []
    for cls in (plant.Press, plant.Oven):
        for method in ("lock_out", "release_lockout", "stop", "is_locked_out"):
            if method in vars(cls):
                copied.append(f"{cls.__name__}.{method}")
    for cls in (plant.Press, plant.Oven, plant.StorageRack):
        for member in ("asset_tag", "name"):
            if member in vars(cls):
                copied.append(f"{cls.__name__}.{member}")
    if copied:
        return "still defined in a subclass instead of a parent: " + ", ".join(copied)


def t_tag_check_once():
    plant.Equipment
    for build in (
        lambda: plant.Press("PRS-1", "Press 1", 15, 60),
        lambda: plant.Oven("L3-OVN-1", "Cure Oven", 45, 200, 240),
        lambda: plant.StorageRack("l3-rck-01", "Rack", 1200),
    ):
        if not raises(ValueError, build):
            return "a bad asset tag was accepted"
    inits = []
    original = plant.Equipment.__init__

    def spy(self, *args, **kwargs):
        inits.append(type(self).__name__)
        return original(self, *args, **kwargs)

    plant.Equipment.__init__ = spy
    try:
        sample()
    finally:
        plant.Equipment.__init__ = original
    if sorted(inits) != ["Oven", "Press", "Press", "StorageRack"]:
        return f"Equipment.__init__ ran for {sorted(inits)}; every kind must reach it through super().__init__()"


def t_oven_lockout_stops():
    plant.Equipment
    oven = plant.Oven("L3-OVN-01", "Cure Oven", 45, 200, 240)
    oven.start()
    oven.lock_out("tech-12")
    if oven.is_running:
        return "an oven that is locked out is still running"


def t_lockout_rules():
    plant.Equipment
    press = plant.Press("L3-PRS-02", "Press 2", 22, 100)
    press.lock_out("tech-07")
    if not raises(RuntimeError, lambda: press.release_lockout("tech-12")):
        return "a different badge released the lockout"
    press.release_lockout("tech-07")
    if press.is_locked_out:
        return "the right badge did not release the lockout"


# ---------------- Part 2 - Tuesday - extend, do not copy ----------------

def t_press_start_extends():
    plant.Equipment
    if "start" not in vars(plant.Press):
        return "Press needs its own start() that adds the guard rule"
    parent_calls = []
    original = plant.PoweredEquipment.start

    def spy(self):
        parent_calls.append(self)
        return original(self)

    plant.PoweredEquipment.start = spy
    try:
        spied = plant.Press("L3-PRS-09", "Spy Press", 5, 10)
        spied.close_guard()
        spied.start()
    finally:
        plant.PoweredEquipment.start = original
    if not parent_calls:
        return "Press.start() never called super().start(), so the parent's rule is a copy, not a reuse"
    press = plant.Press("L3-PRS-01", "Press 1", 15, 60)
    if not raises(RuntimeError, press.start):
        return "a press with its guard open started"
    press.close_guard()
    press.lock_out("tech-07")
    try:
        press.start()
    except RuntimeError as error:
        if "locked out" not in str(error):
            return f"wrong refusal for a locked-out press: {error}"
    else:
        return "a locked-out press with its guard closed started"
    press.release_lockout("tech-07")
    press.start()
    if not press.is_running:
        return "a press with its guard closed and no lockout did not start"


def t_open_guard_stops():
    plant.Equipment
    press = plant.Press("L3-PRS-01", "Press 1", 15, 60)
    press.close_guard()
    press.start()
    press.open_guard()
    if press.is_running:
        return "opening the guard left the press running"
    stops = []

    class SpyPress(plant.Press):
        kind = "press"

        def stop(self):
            stops.append(self)
            super().stop()

    spied = SpyPress("L3-PRS-09", "Spy Press", 5, 10)
    spied.close_guard()
    spied.start()
    spied.open_guard()
    if not stops:
        return "open_guard() changed the running state itself; call self.stop() so stop() stays the one rule"


def t_describe_extends():
    plant.Equipment
    press1, press2, oven, rack = sample()
    press1.close_guard()
    press1.start()
    want = {
        press1: "L3-PRS-01 Press 1 (press) 15 kW, running",
        oven: "L3-OVN-01 Cure Oven (oven) 45 kW, stopped",
        rack: "L3-RCK-01 Finished Goods Rack (rack)",
    }
    for item, text in want.items():
        if item.describe() != text:
            return f"describe() gave {item.describe()!r}, want {text!r}"
    for cls in (plant.Press, plant.Oven, plant.StorageRack):
        if "describe" in vars(cls):
            return f"{cls.__name__} has its own describe(); the parents already build it"
    if "describe" not in vars(plant.PoweredEquipment):
        return "PoweredEquipment needs a describe() that adds power and state"
    original = plant.Equipment.describe
    plant.Equipment.describe = lambda self: "PARENT"
    try:
        extended = press1.describe()
    finally:
        plant.Equipment.describe = original
    if not extended.startswith("PARENT"):
        return "PoweredEquipment.describe() repeats the parent's text; build on super().describe()"


# ---------------- Part 3 - Wednesday - the standard library helps ----------------

def t_equipment_abstract():
    if not raises(TypeError, lambda: plant.Equipment("L3-ABC-01", "Anything")):
        return "Equipment can be created directly; make it an abstract base class"
    if not raises(TypeError, lambda: plant.PoweredEquipment("L3-ABC-02", "Anything", 5)):
        return "PoweredEquipment can be created directly; it should stay abstract"


def t_forgetful_subclass_refused():
    class Grinder(plant.PoweredEquipment):
        kind = "grinder"

    if not raises(TypeError, lambda: Grinder("L3-GRD-01", "Grinder", 4)):
        return "a subclass with no _kind_findings() was allowed; mark it @abstractmethod"


def t_finding_dataclass():
    finding = plant.Finding("L3-PRS-01", "stop", "guard is open; press cannot run")
    if not dataclasses.is_dataclass(plant.Finding):
        return "Finding must be a dataclass"
    if not raises(dataclasses.FrozenInstanceError, lambda: setattr(finding, "severity", "info")):
        return "a Finding could be edited; use frozen=True"
    if not raises(ValueError, lambda: plant.Finding("L3-PRS-01", "urgent", "x")):
        return "a severity outside info, warning, stop was accepted"
    if str(finding) != "[STOP] L3-PRS-01: guard is open; press cannot run":
        return f"str(finding) gave {str(finding)!r}"
    if finding != plant.Finding("L3-PRS-01", "stop", "guard is open; press cannot run"):
        return "two identical findings are not equal"


def t_inspect_template():
    press1, press2, oven, rack = sample()
    press1.close_guard()
    press1.start()
    press2.lock_out("tech-07")
    oven.start()
    oven.record_temperature(228)
    rack.load_kg = 1150
    got = [str(f) for item in (press1, press2, oven, rack) for f in item.inspect()]
    want = [
        "[INFO] L3-PRS-02: locked out by tech-07",
        "[STOP] L3-PRS-02: guard is open; press cannot run",
        "[WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C",
        "[WARNING] L3-RCK-01: at 96% of capacity",
    ]
    if got != want:
        return f"inspect() findings were {got}, want {want}"
    if "inspect" in vars(plant.Press) or "inspect" in vars(plant.Oven):
        return "inspect() is written once, in Equipment; subclasses supply _kind_findings()"


check(1, "Equipment and PoweredEquipment exist, in that order", t_equipment_exists)
check(1, "Press and Oven are level 3", t_three_levels)
check(1, "StorageRack is level 2 and cannot start", t_rack_level_two)
check(1, "no shared method is copied into a subclass", t_no_copies)
check(1, "every kind refuses a bad asset tag, and super() carries it", t_tag_check_once)
check(1, "locking out an oven stops it", t_oven_lockout_stops)
check(1, "only the badge that locked can release", t_lockout_rules)
check(2, "Press.start() adds the guard rule and keeps the lockout rule", t_press_start_extends)
check(2, "opening the guard stops the press through stop()", t_open_guard_stops)
check(2, "describe() is built once per level with super()", t_describe_extends)
check(3, "Equipment and PoweredEquipment are abstract", t_equipment_abstract)
check(3, "a kind that forgets _kind_findings() cannot be built", t_forgetful_subclass_refused)
check(3, "Finding is a frozen dataclass that checks severity", t_finding_dataclass)
check(3, "inspect() is one template method and gives the right findings", t_inspect_template)

passed = 0
for part, status, label, detail in results:
    line = f"{status:<8} Part {part}  {label}"
    if detail:
        line += f"\n           {detail}"
    print(line)
    passed += status == "PASS"
print(f"\n{passed} of {len(results)} self-checks passed")

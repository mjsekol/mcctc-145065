# selfcheck_inspection.py
# Checks your inspection.py against Lab U02-03.
#
# Put this file next to inspection.py and run:
#     python selfcheck_inspection.py

import inspection as ins

results = []


def check(label, test):
    """test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except Exception as error:  # a self-check reports every failure, whatever its type
        problem = f"{type(error).__name__}: {error}"
    results.append((label, problem))


def texts(findings):
    return [str(finding) for finding in findings]


def t_rules_moved():
    missing = [cls.__name__ for cls in (ins.Press, ins.Conveyor, ins.Oven, ins.StorageRack)
               if "_kind_findings" not in vars(cls)]
    if missing:
        return "no _kind_findings() of its own yet: " + ", ".join(missing)


def t_each_kind_alone():
    press = ins.Press("L3-PRS-01", "Press 1")
    press.guard_closed = True
    press.strokes_since_service = 20000
    rack = ins.StorageRack("L3-RCK-01", "Rack", capacity_kg=1000)
    rack.load_kg = 1000
    oven = ins.Oven("L3-OVN-01", "Cure Oven", setpoint_c=200, max_c=240)
    oven.start()
    oven.temperature_c = 210
    conveyor = ins.Conveyor("L3-CNV-01", "Conveyor", max_speed_mps=1.5)
    conveyor.start()
    conveyor.speed_mps = 0.4
    for item in (press, rack, oven, conveyor):
        mine = texts(item._kind_findings())
        chain = texts(ins.inspect_by_kind(item))
        if mine != chain:
            return f"{item.kind} at a boundary value: yours gave {mine}, the chain gave {chain}"


def t_template():
    if "inspect" not in vars(ins.Equipment):
        return "Equipment needs inspect()"
    for cls in (ins.Press, ins.Conveyor, ins.Oven, ins.StorageRack):
        if "inspect" in vars(cls):
            return f"{cls.__name__} overrides inspect(); only _kind_findings() belongs in a subclass"


def t_abstract():
    try:
        ins.Equipment("L3-ABC-01", "Anything")
    except TypeError:
        pass
    else:
        return "Equipment can be created directly; make it abstract with abc"

    class Forgetful(ins.PoweredEquipment):
        kind = "forgetful"

    try:
        Forgetful("L3-FGT-01", "Forgetful")
    except TypeError:
        return None
    return "a kind with no _kind_findings() could be created; mark it @abstractmethod"


def t_same_answers():
    items = ins.build_sample()
    mine = texts(ins.inspect_all(items))
    chain = texts(ins.inspect_line_by_kind(items))
    if not mine:
        return "inspect_all() returned nothing"
    if mine != chain:
        return f"inspect_all() gave {mine}, the chain gave {chain}"


def t_never_asks():
    class Grinder(ins.PoweredEquipment):
        kind = "grinder"

        def _kind_findings(self):
            return [ins.Finding(self.asset_tag, "info", "grinder checked")]

    items = ins.build_sample() + [Grinder("L3-GRD-01", "Bench Grinder")]
    got = texts(ins.inspect_all(items))
    if got[-1:] != ["[INFO] L3-GRD-01: grinder checked"]:
        return f"inspect_all() did not ask the new kind; last findings were {got[-2:]}"


def t_welder():
    welder = ins.Welder("L3-WLD-01", "MIG Welder A", wire_kg=1.5)
    if not issubclass(ins.Welder, ins.PoweredEquipment) or welder.kind != "welder":
        return "Welder must be powered equipment with kind 'welder'"
    if texts(welder.inspect()) != []:
        return "a stopped welder should have no findings"
    welder.start()
    if texts(welder.inspect()) != ["[WARNING] L3-WLD-01: wire low: 1.5 kg left"]:
        return f"a running welder with 1.5 kg of wire gave {texts(welder.inspect())}"
    welder.wire_kg = 2.0
    if texts(welder.inspect()) != []:
        return "2.0 kg is not below the 2.0 kg limit, so no finding"


def t_chain_untouched():
    welder = ins.Welder("L3-WLD-01", "MIG Welder A", wire_kg=1.5)
    try:
        ins.inspect_by_kind(welder)
    except ValueError:
        return None
    return "inspect_by_kind() now handles welders; leave the chain as it was, it is the 'before' picture"


check("Step 2-4  every kind has its own _kind_findings()", t_rules_moved)
check("Step 2-4  each kind matches the chain at its boundary values", t_each_kind_alone)
check("Step 5    inspect() lives once, in Equipment", t_template)
check("Step 5    Equipment is abstract and demands _kind_findings()", t_abstract)
check("Step 6    inspect_all() gives exactly the chain's findings", t_same_answers)
check("Step 6    inspect_all() never asks what kind an item is", t_never_asks)
check("Step 8    Welder warns when running with under 2 kg of wire", t_welder)
check("Step 8    the if/elif chain was left alone", t_chain_untouched)

passed = 0
for label, problem in results:
    if problem is None:
        print(f"PASS  {label}")
        passed += 1
    else:
        print(f"FAIL  {label}")
        print(f"        {problem}")
print(f"\n{passed} of {len(results)} self-checks passed")

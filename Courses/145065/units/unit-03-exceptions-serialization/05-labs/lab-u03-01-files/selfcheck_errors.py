# selfcheck_errors.py
# Checks errors.py, plant.py, and shift_start.py against Lab U03-01.
#
# Put this file next to the three files and run:
#     python selfcheck_errors.py

import errors
import plant
import shift_start

results = []

EXPECTED_REPORT = [
    "step 1 SKIPPED, needs attention: L3-PRS-01: guard is open; close it before starting",
    "step 2 SKIPPED, locked out: L3-PRS-02: locked out by tech-07; cannot start",
    "step 3 done: L3-CNV-01 start",
    "step 4 done: L3-OVN-01 setpoint 205",
    "step 5 SKIPPED, not on this line: L3-PRS-07: not on this line",
    "step 6 STOPPED, the plan is wrong: setpoint '2O5' is not a number",
    "steps not run: 1",
]


def check(label, test):
    """test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except Exception as error:  # a self-check reports every failure, whatever its type
        problem = f"{type(error).__name__}: {error}"
    results.append((label, problem))


def raised(action):
    """Run action and return the exception it raised, or None."""
    try:
        action()
    except Exception as error:  # the caller inspects the type
        return error
    return None


def prepared_line():
    line = plant.build_sample_line()
    press2 = line.get("L3-PRS-02")
    press2.close_guard()
    press2.lock_out("tech-07")
    return line


def t_family():
    e = errors
    pairs = [
        (e.PlantError, Exception),
        (e.ConfigurationError, e.PlantError),
        (e.ConfigurationError, ValueError),
        (e.EquipmentError, e.PlantError),
        (e.LockoutError, e.EquipmentError),
        (e.EquipmentStateError, e.EquipmentError),
        (e.UnknownEquipmentError, e.EquipmentError),
    ]
    for child, parent in pairs:
        if not issubclass(child, parent):
            return f"{child.__name__} must inherit from {parent.__name__}"
    if issubclass(e.LockoutError, e.EquipmentStateError) or issubclass(e.EquipmentStateError, e.LockoutError):
        return "LockoutError and EquipmentStateError are siblings; neither inherits the other"


def t_carries_tag():
    error = errors.LockoutError("L3-PRS-02", "locked out by tech-07")
    if getattr(error, "asset_tag", None) != "L3-PRS-02":
        return "EquipmentError must store the tag in an asset_tag attribute"
    if str(error) != "L3-PRS-02: locked out by tech-07":
        return f"str(error) should be 'L3-PRS-02: locked out by tech-07', got {str(error)!r}"


def t_model_raises_family():
    line = prepared_line()
    press1, press2 = line.get("L3-PRS-01"), line.get("L3-PRS-02")
    cases = [
        ("a press with its guard open", press1.start, errors.EquipmentStateError),
        ("a locked-out press", press2.start, errors.LockoutError),
        ("the wrong badge", lambda: press2.release_lockout("tech-12"), errors.LockoutError),
        ("a tag not on the line", lambda: line.get("L3-PRS-07"), errors.UnknownEquipmentError),
        ("a negative rating", lambda: plant.Press("L3-PRS-09", "x", -5, 60), errors.ConfigurationError),
        ("a bad tag", lambda: plant.StorageRack("RCK-1", "x", 100), errors.ConfigurationError),
        ("strokes on a stopped press", lambda: press1.record_strokes(5), errors.EquipmentStateError),
    ]
    for what, action, wanted in cases:
        error = raised(action)
        if type(error) is not wanted:
            got = "nothing" if error is None else type(error).__name__
            return f"{what} should raise {wanted.__name__}, raised {got}"


def t_old_callers_still_work():
    error = raised(lambda: plant.Oven("L3-OVN-09", "x", 45, setpoint_c=300, max_c=240))
    if not isinstance(error, ValueError):
        return "a bad setpoint must still be caught by `except ValueError`"
    error = raised(lambda: plant.Press("L3-PRS-09", "x", "fifteen", 60))
    if type(error) is not TypeError:
        return "a wrong type is a programming mistake and should stay TypeError"


def t_chained():
    error = raised(lambda: shift_start.parse_number("2O5", "setpoint"))
    if type(error) is not errors.ConfigurationError:
        return f"parse_number('2O5') should raise ConfigurationError, raised {type(error).__name__}"
    if not isinstance(error.__cause__, ValueError):
        return "the ConfigurationError must be raised `from` the ValueError, so __cause__ keeps it"
    if shift_start.parse_number("205", "setpoint") != 205.0:
        return "parse_number('205') should return 205.0"


def t_report():
    got = shift_start.run_plan(prepared_line(), shift_start.PLAN)
    if got != EXPECTED_REPORT:
        return "the report does not match. It was:\n" + "\n".join(got)


def t_oven_not_started():
    line = prepared_line()
    shift_start.run_plan(line, shift_start.PLAN)
    if line.get("L3-OVN-01").is_running:
        return "the oven started after the plan was found to be wrong"


def t_bugs_not_swallowed():
    line = prepared_line()

    def broken_start():
        return 1 / 0  # a real bug nobody planned for

    line.get("L3-CNV-01").start = broken_start
    error = raised(lambda: shift_start.run_plan(line, ["L3-CNV-01 start"]))
    if not isinstance(error, ZeroDivisionError):
        return "run_plan() hid a ZeroDivisionError; never catch Exception"


check("Step 1  the six classes form the right family", t_family)
check("Step 2  EquipmentError carries the asset tag", t_carries_tag)
check("Step 3  the model raises the family, not built-ins", t_model_raises_family)
check("Step 3  old `except ValueError` callers still work", t_old_callers_still_work)
check("Step 4  parse_number() chains its error with `from`", t_chained)
check("Step 5  run_plan() reports each failure its own way", t_report)
check("Step 6  a wrong plan stops before the oven starts", t_oven_not_started)
check("Step 7  a real bug is not swallowed", t_bugs_not_swallowed)

passed = 0
for label, problem in results:
    if problem is None:
        print(f"PASS  {label}")
        passed += 1
    else:
        print(f"FAIL  {label}")
        for line in problem.splitlines():
            print(f"        {line}")
print(f"\n{passed} of {len(results)} self-checks passed")

# selfcheck_layout.py
# Checks your layout.py against Lab U02-02.
#
# Put this file next to layout.py and line3_parts.py, then run:
#     python selfcheck_layout.py

import sys

import layout
from line3_parts import Machine

results = []


def check(label, test):
    """test() returns None when it passes, or a string saying why not."""
    try:
        problem = test()
    except RecursionError:
        problem = "RecursionError: the recursion never reached a base case"
    except Exception as error:  # a self-check reports every failure, whatever its type
        problem = f"{type(error).__name__}: {error}"
    results.append((label, problem))


def nested(depth):
    """A line whose single machine sits inside `depth` cells, one inside the next."""
    line = layout.Line("Deep Line")
    cell = line.add_cell(layout.Cell("Level 1"))
    for level in range(2, depth + 1):
        cell = cell.add(layout.Cell(f"Level {level}"))
    cell.add(Machine("L3-TST-01", "Test Stand", "test", 2))
    return line


EXPECTED_OUTLINE = """Line 3
  Forming
    L3-PRS-01 Press 1 (press)
    L3-PRS-02 Press 2 (press)
  Finishing
    L3-OVN-01 Cure Oven (oven)
    Transfer
      L3-CNV-01 Transfer Conveyor (conveyor)
  Staging
    L3-RCK-01 Finished Goods Rack (rack)"""


def t_base_case():
    machine = Machine("L3-PRS-01", "Press 1", "press", 15)
    if layout.count_equipment(machine) != 1:
        return f"one machine should count 1, got {layout.count_equipment(machine)}"
    if layout.count_equipment(layout.Cell("Empty")) != 0:
        return "an empty cell should count 0"


def t_count_line():
    got = layout.count_equipment(layout.build_sample_line())
    if got != 5:
        return f"the sample line has 5 machines, got {got}"


def t_walk():
    got = [(depth, getattr(item, "asset_tag", None) or item.name)
           for depth, item in layout.walk(layout.build_sample_line())]
    want = [(0, "Forming"), (1, "L3-PRS-01"), (1, "L3-PRS-02"), (0, "Finishing"),
            (1, "L3-OVN-01"), (1, "Transfer"), (2, "L3-CNV-01"), (0, "Staging"),
            (1, "L3-RCK-01")]
    if got != want:
        return f"walk() gave {got}"


def t_outline():
    got = layout.build_sample_line().outline()
    if got != EXPECTED_OUTLINE:
        return "outline() does not match. It printed:\n" + got


def t_total_kw():
    got = layout.total_rated_kw(layout.build_sample_line())
    if got != 85:
        return f"15 + 22 + 45 + 3 + 0 is 85 kW, got {got}"


def t_find_deep():
    line = layout.build_sample_line()
    found = line.find("L3-CNV-01")
    if found is None or found.name != "Transfer Conveyor":
        return "find() did not reach the conveyor two levels down"
    if line.find("L3-PRS-99") is not None:
        return "find() returned something for a tag that is not on the line"


def t_no_fixed_depth():
    for depth in (1, 5, 50):
        line = nested(depth)
        if layout.count_equipment(line) != 1:
            return f"with {depth} nested cells, count_equipment gave {layout.count_equipment(line)}"
        deepest = list(layout.walk(line))[-1][0]
        if deepest != depth:
            return f"with {depth} nested cells, the machine should be at depth {depth}, got {deepest}"


def t_contains_cell():
    line = layout.build_sample_line()
    forming, finishing, _staging = line.items
    transfer = finishing.items[1]
    if not finishing.contains_cell(transfer):
        return "Finishing contains Transfer, but contains_cell said False"
    if forming.contains_cell(transfer):
        return "Forming does not contain Transfer, but contains_cell said True"
    deep = nested(6)
    top = deep.items[0]
    bottom = list(layout.walk(deep))[-2][1]
    if not top.contains_cell(bottom):
        return "a cell five levels down was not found"
    if bottom.contains_cell(top):
        return "contains_cell looked upward; it should only look below"


def t_loop_refused():
    line = layout.build_sample_line()
    finishing = line.items[1]
    transfer = finishing.items[1]
    try:
        transfer.add(finishing)
    except ValueError:
        pass
    else:
        return "Transfer accepted Finishing, its own parent, which makes a loop"
    try:
        transfer.add(transfer)
    except ValueError:
        pass
    else:
        return "a cell accepted itself"
    if layout.count_equipment(line) != 5:
        return "the refused add still changed the line"


check("Step 1  count_equipment has a base case", t_base_case)
check("Step 1  count_equipment counts the sample line", t_count_line)
check("Step 2  walk() visits every item depth first, with its depth", t_walk)
check("Step 3  outline() indents by depth", t_outline)
check("Step 4  total_rated_kw adds power at every level", t_total_kw)
check("Step 4  find() reaches any depth", t_find_deep)
check("Step 4  nothing limits the depth", t_no_fixed_depth)
check("Step 5  contains_cell searches every level below", t_contains_cell)
check("Step 6  add() refuses a loop", t_loop_refused)

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
sys.exit(0)

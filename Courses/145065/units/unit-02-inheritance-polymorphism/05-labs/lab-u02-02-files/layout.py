# layout.py
# How Line 3 is laid out: a line holds cells, and a cell holds machines and
# smaller cells. STARTER FILE for Lab U02-02. It runs, and it finds nothing yet.
#
#     python layout.py
#
# Riverside Fabrication is a composite shop invented for this course.
# Five functions are stubs marked TODO. Each one returns a harmless value so
# the program runs. The lab tells you which step fills in which stub.
#
#     Line 3
#     |-- Forming              (cell)
#     |   |-- L3-PRS-01        (press)
#     |   `-- L3-PRS-02        (press)
#     |-- Finishing            (cell)
#     |   |-- L3-OVN-01        (oven)
#     |   `-- Transfer         (a cell inside a cell)
#     |       `-- L3-CNV-01    (conveyor)
#     `-- Staging              (cell)
#         `-- L3-RCK-01        (rack)

from line3_parts import Machine


class Cell:
    """A named group of machines and smaller cells. Nothing limits the depth."""

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("cell name must be a non-blank string")
        self._name = name.strip()
        self._items = []

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        # A tuple: callers can read the items but cannot append around add().
        return tuple(self._items)

    def add(self, item):
        if not isinstance(item, (Machine, Cell)):
            raise TypeError(f"a cell holds Machine and Cell objects, not {type(item).__name__}")
        if any(existing is item for existing in self._items):
            raise ValueError(f"{item!r} is already in cell {self._name}")
        # TODO Step 6: refuse a cell that would create a loop.
        self._items.append(item)
        return item

    def contains_cell(self, target):
        """True if target is anywhere below this cell, at any depth."""
        # TODO Step 5
        return False

    def __repr__(self):
        return f"Cell({self._name!r}, items={len(self._items)})"


class Line:
    """A production line: the top of the layout. It holds cells only."""

    def __init__(self, name):
        self._name = name
        self._cells = []

    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return tuple(self._cells)

    def add_cell(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError(f"a line holds Cell objects, not {type(cell).__name__}")
        self._cells.append(cell)
        return cell

    def equipment(self):
        return iter_equipment(self)

    def find(self, asset_tag):
        for machine in iter_equipment(self):
            if machine.asset_tag == asset_tag:
                return machine
        return None

    def outline(self):
        # TODO Step 3: one line per item from walk(), indented two spaces per level.
        return self._name


def count_equipment(node):
    """Count the machines at or below node. Textbook recursion."""
    # TODO Step 1: a base case and a recursive case.
    return 0


def total_rated_kw(node):
    """The total rated_kw of every machine at or below node."""
    # TODO Step 4
    return 0


def walk(node, depth=0):
    """Return (depth, item) for everything below node, depth first."""
    # TODO Step 2
    return []


def iter_equipment(node):
    return [item for _depth, item in walk(node) if isinstance(item, Machine)]


def build_sample_line():
    line = Line("Line 3")

    forming = line.add_cell(Cell("Forming"))
    forming.add(Machine("L3-PRS-01", "Press 1", "press", 15))
    forming.add(Machine("L3-PRS-02", "Press 2", "press", 22))

    finishing = line.add_cell(Cell("Finishing"))
    finishing.add(Machine("L3-OVN-01", "Cure Oven", "oven", 45))
    transfer = finishing.add(Cell("Transfer"))
    transfer.add(Machine("L3-CNV-01", "Transfer Conveyor", "conveyor", 3))

    staging = line.add_cell(Cell("Staging"))
    staging.add(Machine("L3-RCK-01", "Finished Goods Rack", "rack"))

    return line


def main():
    line = build_sample_line()
    print(line.outline())
    print()
    print(f"Machines on the line: {count_equipment(line)}")
    print(f"Rated power on the line: {total_rated_kw(line)} kW")
    conveyor = line.find("L3-CNV-01")
    print(f"Found two levels down: {conveyor.describe() if conveyor else 'nothing'}")


if __name__ == "__main__":
    main()

"""A work cell: a group of machines that work together on Line 3.

Collection choice (Unit 1, Week 3): the cell stores machines in a dict keyed by
asset tag. You look machines up by tag constantly, a dict finds one without
scanning the whole group, and a duplicate tag is caught with one membership
test. Since Python 3.7 a dict also keeps insertion order, so the cell still
lists machines in the order they were installed. A list would keep order but
make every lookup and duplicate check a full scan.
"""

from line3.machine import Machine


class WorkCell:
    """A named group of machines, looked up by asset tag."""

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("cell name must be a non-blank string")
        self._name = name.strip()
        self._machines = {}

    @property
    def name(self):
        return self._name

    @property
    def machines(self):
        """A tuple copy. Callers can read the machines but cannot add or remove
        them behind the cell's back."""
        return tuple(self._machines.values())

    def add(self, machine):
        if not isinstance(machine, Machine):
            raise TypeError(f"a cell holds Machine objects, not {type(machine).__name__}")
        if machine.asset_tag in self._machines:
            raise ValueError(f"{machine.asset_tag} is already in cell {self._name}")
        self._machines[machine.asset_tag] = machine
        return machine

    def get(self, asset_tag):
        """The machine with this tag, or None if the cell does not have it."""
        return self._machines.get(asset_tag)

    def remove(self, asset_tag):
        """Remove and return a machine. Refuses to remove a running machine."""
        machine = self._machines.get(asset_tag)
        if machine is None:
            raise KeyError(asset_tag)
        if machine.is_running:
            raise RuntimeError(f"stop {asset_tag} before removing it from the cell")
        return self._machines.pop(asset_tag)

    def running(self):
        return [m for m in self._machines.values() if m.is_running]

    def total_rated_kw(self):
        return sum(m.rated_kw for m in self._machines.values())

    def __contains__(self, asset_tag):
        return asset_tag in self._machines

    def __len__(self):
        return len(self._machines)

    def __iter__(self):
        return iter(self.machines)

    def __repr__(self):
        return f"WorkCell(name={self._name!r}, machines={len(self._machines)})"

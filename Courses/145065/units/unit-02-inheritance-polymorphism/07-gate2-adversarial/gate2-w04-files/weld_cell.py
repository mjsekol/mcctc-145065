"""Weld cell asset model for Riverside Fabrication, Line 3.

Implements the asset hierarchy for the new weld cell:

    Asset (abstract)
    |-- PoweredAsset
    |   |-- Welder
    |   `-- FumeExtractor
    `-- WeldCart

Cells can be nested to any depth. Counting and lookup are recursive.

Riverside Fabrication is a composite shop invented for this course.
"""

import re
from abc import ABC, abstractmethod

TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")


class Asset(ABC):
    """Base class for every asset in the weld cell."""

    kind = "asset"

    def __init__(self, asset_tag: str, name: str) -> None:
        if not isinstance(asset_tag, str) or not TAG_PATTERN.fullmatch(asset_tag):
            raise ValueError(f"invalid asset tag: {asset_tag!r}")
        self.asset_tag = asset_tag
        self.name = name

    @abstractmethod
    def start(self) -> None:
        """Start the asset."""

    def describe(self) -> str:
        """Return a one-line summary. Each subclass supplies its own details."""
        line = f"{self.asset_tag} {self.name} ({self.kind})"
        if isinstance(self, Welder):
            line += ", arc on" if self.arc_on else ", arc off"
        elif isinstance(self, FumeExtractor):
            line += f", {self.airflow_m3h:g} m3/h"
        if isinstance(self, PoweredAsset):
            line += ", running" if self.is_running else ", stopped"
        return line


class PoweredAsset(Asset):
    """An asset that draws power. It can run, stop, and be locked out."""

    kind = "powered"

    def __init__(self, asset_tag: str, name: str, rated_kw: float) -> None:
        super().__init__(asset_tag, name)
        self.rated_kw = rated_kw
        self._running = False
        self._locked_by = None

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def is_locked_out(self) -> bool:
        return self._locked_by is not None

    @property
    def locked_by(self):
        return self._locked_by

    def start(self) -> None:
        if self.is_locked_out:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self._locked_by}")
        self._running = True

    def stop(self) -> None:
        self._running = False

    def lock_out(self, badge: str) -> None:
        """Apply a lockout for this badge. The asset is stopped first."""
        if not badge:
            raise ValueError("a lockout needs a badge id")
        if self._locked_by is not None and self._locked_by != badge:
            raise RuntimeError(f"{self.asset_tag} is already locked out by {self._locked_by}")
        self.stop()
        self._locked_by = badge

    def release_lockout(self, badge: str) -> None:
        """Release the lockout held by this badge."""
        if not self.is_locked_out:
            raise RuntimeError(f"{self.asset_tag} is not locked out")
        self._locked_by = None


class Welder(PoweredAsset):
    """A MIG welder. The arc is on only while the welder runs."""

    kind = "welder"

    def __init__(self, asset_tag: str, name: str, rated_kw: float, max_amps: int) -> None:
        super().__init__(asset_tag, name, rated_kw)
        self.max_amps = max_amps
        self.arc_on = False

    def start(self) -> None:
        super().start()
        self.arc_on = True

    def stop(self) -> None:
        # The arc is the hazard, so it goes off first.
        self.arc_on = False


class FumeExtractor(PoweredAsset):
    """Pulls welding fumes out of the booth."""

    kind = "extractor"

    def __init__(self, asset_tag: str, name: str, rated_kw: float, airflow_m3h: float) -> None:
        super().__init__(asset_tag, name, rated_kw)
        self.airflow_m3h = airflow_m3h


class WeldCart(Asset):
    """A cart for filler wire and gas bottles. It has no power."""

    kind = "cart"

    def __init__(self, asset_tag: str, name: str, capacity_kg: float) -> None:
        super().__init__(asset_tag, name)
        self.capacity_kg = capacity_kg

    def start(self) -> None:
        # A cart has no power, so there is nothing to start.
        pass


class WeldCell:
    """A named group of assets and nested cells."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items = []

    def add(self, item):
        if not isinstance(item, (Asset, WeldCell)):
            raise TypeError(f"a weld cell holds assets and cells, not {type(item).__name__}")
        self._items.append(item)
        return item

    def all_assets(self) -> list:
        """Every asset in this cell and its sub-cells, depth first."""
        found = []
        for item in self._items:
            if isinstance(item, WeldCell):
                found.extend(item.all_assets())
            else:
                found.append(item)
        return found

    def count_assets(self) -> int:
        return len(self.all_assets())

    def find(self, asset_tag: str):
        """Return the asset with this tag at any depth, or None."""
        for asset in self.all_assets():
            if asset.asset_tag == asset_tag:
                return asset
        return None

    def start_all(self, tags: list) -> list:
        """Start each listed asset. Returns the tags that were started."""
        started = []
        for tag in tags:
            asset = self.find(tag)
            if asset is not None:
                asset.start()
                started.append(tag)
        return started


def build_weld_cell() -> WeldCell:
    cell = WeldCell("Weld Cell")
    booth = cell.add(WeldCell("Booth A"))
    booth.add(Welder("L3-WLD-01", "MIG Welder A", 12, 250))
    booth.add(FumeExtractor("L3-FEX-01", "Extractor A", 1.5, 1200))
    cell.add(WeldCart("L3-CRT-01", "Wire Cart", 150))
    return cell


def main() -> None:
    cell = build_weld_cell()
    started = cell.start_all(["L3-FEX-01", "L3-WLD-01", "L3-CRT-01"])
    print(f"Started: {', '.join(started)}")
    print(f"Assets in cell: {cell.count_assets()}")
    for asset in cell.all_assets():
        print(asset.describe())


if __name__ == "__main__":
    main()

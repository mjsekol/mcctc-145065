"""Save and load the Line 3 equipment register as JSON.

The register is written with a backup of the previous save, and loading is
generic: each saved item names its class, and the loader rebuilds it and
restores its saved state, so new equipment types need no loader changes.

Riverside Fabrication is a composite shop invented for this course.

    python line_store.py
"""

import json
import shutil
import tempfile
from pathlib import Path

FORMAT_VERSION = 2


class PlantFileError(Exception):
    """Raised when a plant file cannot be used."""


class Press:
    FIELDS = ("tag", "name", "rated_kw")

    def __init__(self, tag: str, name: str, rated_kw: float) -> None:
        if isinstance(rated_kw, bool) or not isinstance(rated_kw, (int, float)) or rated_kw <= 0:
            raise ValueError("rated_kw must be a number above 0")
        self.tag = tag
        self.name = name
        self.rated_kw = float(rated_kw)
        self.locked_by = None
        self._running = False
        self._guard_closed = False  # unknown counts as open

    def close_guard(self) -> None:
        self._guard_closed = True

    def lock_out(self, badge: str) -> None:
        self._running = False
        self.locked_by = badge

    def start(self) -> None:
        if self.locked_by is not None:
            raise RuntimeError(f"{self.tag} is locked out by {self.locked_by}")
        if not self._guard_closed:
            raise RuntimeError(f"{self.tag} guard is open")
        self._running = True

    def to_dict(self) -> dict:
        return {"kind": "Press", "tag": self.tag, "name": self.name, "rated_kw": self.rated_kw}

    def describe(self) -> str:
        state = "running" if self._running else "stopped"
        lock = f"locked out by {self.locked_by}" if self.locked_by else "not locked out"
        return f"{self.tag} {self.name} {self.rated_kw:g} kW, {state}, {lock}"


class Rack:
    FIELDS = ("tag", "name", "capacity_kg")

    def __init__(self, tag: str, name: str, capacity_kg: float) -> None:
        if isinstance(capacity_kg, bool) or not isinstance(capacity_kg, (int, float)) or capacity_kg <= 0:
            raise ValueError("capacity_kg must be a number above 0")
        self.tag = tag
        self.name = name
        self.capacity_kg = float(capacity_kg)
        self._load_kg = 0.0

    @property
    def load_kg(self) -> float:
        return self._load_kg

    @load_kg.setter
    def load_kg(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("load_kg must be a number of at least 0")
        self._load_kg = float(value)

    def to_dict(self) -> dict:
        return {"kind": "Rack", "tag": self.tag, "name": self.name,
                "capacity_kg": self.capacity_kg, "_load_kg": self._load_kg}

    def describe(self) -> str:
        return f"{self.tag} {self.name} {self._load_kg:g} of {self.capacity_kg:g} kg"


class Register:
    """Every machine on the line, in the order it was added."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.items = []

    def add(self, item):
        self.items.append(item)
        return item

    def get(self, tag: str):
        for item in self.items:
            if item.tag == tag:
                return item
        raise KeyError(tag)


def _document(register: Register) -> dict:
    return {"version": FORMAT_VERSION, "name": register.name,
            "items": [item.to_dict() for item in register.items]}


def save(register: Register, path) -> None:
    """Save the register. The previous save is kept as <name>.bak."""
    path = Path(path)
    if path.exists():
        shutil.copy2(path, path.with_suffix(".bak"))
    with open(path, "w", encoding="utf-8") as handle:
        # ensure_ascii keeps non-English names readable in the saved file
        json.dump(_document(register), handle, indent=2, ensure_ascii=True)


def _check_duplicates(document: dict) -> None:
    """Refuse a register that lists the same tag twice."""
    for item in document["items"]:
        occurrences = json.dumps(document["items"]).count(f'"tag": "{item["tag"]}"')
        if occurrences > 1:
            raise PlantFileError(f"duplicate tag {item['tag']}")


def _rebuild(data: dict):
    """Recreate an item from its saved fields, whatever its class."""
    cls = globals()[data["kind"]]
    item = cls(*[data[name] for name in cls.FIELDS])
    # Restore the rest of the saved state.
    item.__dict__.update({key: value for key, value in data.items() if key != "kind"})
    return item


def load(path) -> Register:
    """Load a register written by save(). Raises PlantFileError if the file is unusable."""
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PlantFileError(f"cannot read {path}: {error}") from error
    if document.get("version") != FORMAT_VERSION:
        raise PlantFileError(f"unsupported format version {document.get('version')}")
    _check_duplicates(document)
    register = Register(document["name"])
    for data in document["items"]:
        register.add(_rebuild(data))
    return register


def build_sample() -> Register:
    register = Register("Line 3")
    press1 = register.add(Press("L3-PRS-01", "Press 1", 15))
    press1.close_guard()
    press1.start()
    register.add(Press("L3-PRS-02", "Press 2", 22)).lock_out("tech-07")
    register.add(Rack("L3-RCK-01", "Rack, Área de Soldadura", 1200)).load_kg = 640
    return register


def main() -> None:
    register = build_sample()
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "register.json"
        save(register, path)
        print(f"Saved {path.stat().st_size} bytes")
        loaded = load(path)
    print("Loaded:")
    for item in loaded.items:
        print(f"  {item.describe()}")


if __name__ == "__main__":
    main()

# storage.py
# Save and load Line 3 as JSON, at Riverside Fabrication, a composite shop
# invented for this course. STARTER FILE for Lab U03-02. It runs.
#
#     python storage.py
#
# This file grows across three days:
#   Part 1, Tuesday     the round trip: dumps, loads, save_line, load_line
#   Part 2, Wednesday   a file is untrusted input: check everything
#   Part 3, Thursday    survive a crash and an upgrade: backup, replace, migrate
#
# Every stub raises NotImplementedError with its step number, so main() can
# tell you what is still to do. Never use pickle in this file.

import json
import os
import shutil
import tempfile
from pathlib import Path

from errors import (
    ConfigurationError,
    PlantFileError,
    PlantFileFormatError,
    PlantFileMissingError,
    UnsupportedVersionError,
)
from plant import Cell, Conveyor, Line, Oven, Press, StorageRack, build_sample_line

FORMAT_NAME = "line3-plant"
CURRENT_VERSION = 2
MAX_FILE_BYTES = 1_000_000
MAX_CELL_DEPTH = 20


# ================= Part 1 - Tuesday - the round trip =================

def line_to_document(line):
    """GIVEN. The whole file as one dict: format, version, and the line."""
    return {"format": FORMAT_NAME, "version": CURRENT_VERSION, "line": line.to_dict()}


def dumps(line):
    """Step 3. Return the JSON text for line: indent=2, readable non-ASCII, a final newline."""
    raise NotImplementedError("Step 3: dumps()")


# GIVEN for Tuesday only. It trusts the document completely. Wednesday
# replaces it with line_from_document(), which trusts nothing.
KINDS = {"press": Press, "oven": Oven, "conveyor": Conveyor, "rack": StorageRack}


def build_line(document):
    def build_cell(data):
        cell = Cell(data["name"])
        for item in data["items"]:
            if item["kind"] == "cell":
                cell.add(build_cell(item))
            else:
                cell.add(KINDS[item["kind"]].from_dict(item))
        return cell

    line = Line(document["line"]["name"])
    for cell_data in document["line"]["cells"]:
        line.add_cell(build_cell(cell_data))
    return line


def loads(text, source="<string>"):
    """Step 4 (Tuesday), then Step 8 (Wednesday). Turn JSON text back into a Line."""
    raise NotImplementedError("Step 4: loads()")


def load_line(path):
    """Step 5 (Tuesday), then Step 9 (Wednesday). Read a file and return the Line."""
    raise NotImplementedError("Step 5: load_line()")


def save_line(line, path, keep_backup=True):
    """Step 5 (Tuesday), then Step 11 (Thursday). Write line to path.

    Returns the backup path, or None. Tuesday's version makes no backup.
    """
    raise NotImplementedError("Step 5: save_line()")


# ================= Part 2 - Wednesday - a file is untrusted input =================
# The helpers below are GIVEN. Each checker raises PlantFileFormatError with
# a "where" that says exactly which field in the file is wrong.

def _fail(source, where, problem):
    raise PlantFileFormatError(source, where, problem)


def _json_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true/false"
    if isinstance(value, (int, float)):
        return "a number"
    if isinstance(value, str):
        return "a string"
    if isinstance(value, list):
        return "a list"
    return "an object"


def _text(value, source, where):
    if not isinstance(value, str) or not value.strip():
        _fail(source, where, "must be a non-blank string")


def _optional_text(value, source, where):
    if value is not None:
        _text(value, source, where)


def _number(value, source, where):
    # bool is a subclass of int in Python. true is not 15 kW.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(source, where, f"must be a number, not {_json_type(value)}")


def _whole(value, source, where):
    if isinstance(value, bool) or not isinstance(value, int):
        _fail(source, where, f"must be a whole number, not {_json_type(value)}")


def _any(value, source, where):
    """No check here. The value is checked later, where its meaning is known."""


def _list(value, source, where):
    if not isinstance(value, list):
        _fail(source, where, f"must be a list, not {_json_type(value)}")


def _check_fields(value, source, where, fields):
    """value must be an object with exactly these fields, each passing its checker."""
    if not isinstance(value, dict):
        _fail(source, where, f"must be an object, not {_json_type(value)}")
    missing = [name for name in fields if name not in value]
    if missing:
        _fail(source, where, f"missing field {', '.join(missing)}")
    unknown = sorted(set(value) - set(fields))
    if unknown:
        _fail(source, where, f"unknown field {', '.join(unknown)}")
    for name, checker in fields.items():
        checker(value[name], source, f"{where}.{name}")


_BASE = {"kind": _text, "tag": _text, "name": _text}
_POWERED = {**_BASE, "rated_kw": _number}

# The only kinds a file may name, and the class each one builds.
EQUIPMENT_KINDS = {
    "press": (Press, {**_POWERED, "tonnage": _number, "service_interval": _whole,
                      "strokes_since_service": _whole, "locked_out_by": _optional_text}),
    # TODO Step 7: oven, conveyor, and rack. Every field to_dict() writes, and nothing else.
}


def _build_equipment(data, source, where):
    """GIVEN. Look the kind up in the table. A kind not in the table is refused."""
    kind = data.get("kind") if isinstance(data, dict) else None
    entry = EQUIPMENT_KINDS.get(kind) if isinstance(kind, str) else None
    if entry is None:
        _fail(source, f"{where}.kind", f"unknown equipment kind {kind!r}")
    cls, fields = entry
    _check_fields(data, source, where, fields)
    try:
        return cls.from_dict(data)
    except ConfigurationError as error:
        raise PlantFileFormatError(source, where, str(error)) from error


def _build_cell(data, source, where, depth):
    """GIVEN. Recursive, with a depth limit."""
    if depth > MAX_CELL_DEPTH:
        _fail(source, where, f"cells are nested deeper than {MAX_CELL_DEPTH} levels")
    _check_fields(data, source, where, {"kind": _text, "name": _text, "items": _list})
    if data["kind"] != "cell":
        _fail(source, f"{where}.kind", f"expected 'cell', found {data['kind']!r}")
    cell = Cell(data["name"])
    for index, item in enumerate(data["items"]):
        item_where = f"{where}.items[{index}]"
        if isinstance(item, dict) and item.get("kind") == "cell":
            cell.add(_build_cell(item, source, item_where, depth + 1))
        else:
            cell.add(_build_equipment(item, source, item_where))
    return cell


def line_from_document(document, source="<document>"):
    """GIVEN. Check a version 2 document and build the Line it describes."""
    _check_fields(document, source, "document", {"format": _text, "version": _whole, "line": _any})
    data = document["line"]
    _check_fields(data, source, "line", {"name": _text, "cells": _list})
    line = Line(data["name"])
    for index, cell_data in enumerate(data["cells"]):
        line.add_cell(_build_cell(cell_data, source, f"line.cells[{index}]", depth=1))
    duplicates = line.duplicate_tags()
    if duplicates:
        _fail(source, "line", f"duplicate asset tag {', '.join(duplicates)}")
    return line


# ================= Part 3 - Thursday - surviving a crash and an upgrade =================

V1_FIELDS = {
    "press": ("type", "tag", "name", "cell", "power_kw", "tonnage"),
    "oven": ("type", "tag", "name", "cell", "power_kw", "setpoint_c", "max_c"),
    "conveyor": ("type", "tag", "name", "cell", "power_kw", "max_speed_mps"),
    "rack": ("type", "tag", "name", "cell", "capacity_kg", "load_kg"),
}
V1_COPIED = {
    "press": ("tonnage",),
    "oven": ("setpoint_c", "max_c"),
    "conveyor": ("max_speed_mps",),
    "rack": ("capacity_kg", "load_kg"),
}
# Values version 1 never recorded. Step 13 asks which ones a person must review.
V1_DEFAULTS = {
    "press": {"service_interval": 20000, "strokes_since_service": 0},
    "oven": {},
    "conveyor": {"speed_mps": 0.0},
    "rack": {},
}


def migrate_v1_to_v2(document, source="<document>"):
    """GIVEN except one line. Return a new version 2 document; never change the old one."""
    _check_fields(document, source, "document",
                  {"format": _text, "version": _whole, "line_name": _text, "equipment": _list})
    cells = {}  # cell name -> cell dict; a dict keeps first-seen order
    for index, old in enumerate(document["equipment"]):
        where = f"equipment[{index}]"
        kind = old.get("type") if isinstance(old, dict) else None
        if not isinstance(kind, str) or kind not in V1_FIELDS:
            _fail(source, f"{where}.type", f"unknown version 1 equipment type {kind!r}")
        _check_fields(old, source, where, {name: _any for name in V1_FIELDS[kind]})
        new = {"kind": kind, "tag": old["tag"], "name": old["name"]}
        if kind != "rack":
            pass  # TODO Step 12: version 1 called it power_kw. Version 2 calls it rated_kw.
        for field in V1_COPIED[kind]:
            new[field] = old[field]
        new.update(V1_DEFAULTS[kind])
        if kind != "rack":
            new["locked_out_by"] = None  # version 1 never recorded lockouts
        _text(old["cell"], source, f"{where}.cell")
        cell = cells.setdefault(old["cell"], {"kind": "cell", "name": old["cell"], "items": []})
        cell["items"].append(new)
    return {"format": FORMAT_NAME, "version": 2,
            "line": {"name": document["line_name"], "cells": list(cells.values())}}


MIGRATIONS = {1: migrate_v1_to_v2}


def migrate(document, source="<document>"):
    """GIVEN. Bring any supported version up to CURRENT_VERSION, one step at a time."""
    if not isinstance(document, dict):
        _fail(source, "document", f"must be an object, not {_json_type(document)}")
    if document.get("format") != FORMAT_NAME:
        _fail(source, "format", f"expected {FORMAT_NAME!r}, found {document.get('format')!r}")
    version = document.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        _fail(source, "version", f"must be a whole number, not {_json_type(version)}")
    if version > CURRENT_VERSION:
        raise UnsupportedVersionError(source, version, CURRENT_VERSION)
    if version < 1:
        _fail(source, "version", f"version {version} does not exist")
    while version < CURRENT_VERSION:
        document = MIGRATIONS[version](document, source)
        version = document["version"]
    return document


def backup_path(path):
    """GIVEN. line3.json -> line3.json.bak"""
    path = Path(path)
    return path.with_name(path.name + ".bak")


def restore_backup(path):
    """Step 11. Put the .bak back, but only if it loads cleanly. Return the Line."""
    raise NotImplementedError("Step 11: restore_backup()")


# ================= try it =================

def main():
    """Runs whatever is written so far, in a temporary folder."""
    samples = Path(__file__).parent / "sample_data"
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder) / "line3.json"
        line = build_sample_line()
        line.get("L3-RCK-01").load_kg = 640
        try:
            save_line(line, target)
            print(f"Saved {target.name}: {target.stat().st_size} bytes")
            again = load_line(target)
            print(f"Round trip identical: {dumps(again) == dumps(line)}")
        except NotImplementedError as error:
            print(f"Not written yet: {error}")
        except AttributeError as error:
            # Until Step 2 is done, some classes have no from_dict() yet.
            print(f"Not written yet: {error}")
    try:
        old = load_line(samples / "line3_v1.json")
        print(f"Version 1 sample loaded: {len(old.equipment())} machines")
    except (NotImplementedError, AttributeError) as error:
        print(f"Not written yet: {error}")
    except KeyError as error:
        # Tuesday's build_line() cannot read a version 1 file. Step 12 fixes that.
        print(f"Version 1 sample not readable yet: KeyError {error}")
    except PlantFileError as error:
        print(f"Version 1 sample refused: {error}")


if __name__ == "__main__":
    main()

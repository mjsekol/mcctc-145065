# Lecture Notes: The Data Outlives the Program
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W06_TheDataOutlivesTheProgram.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-03-exceptions-serialization/04-slides/MCCTC_145065_Slides_W06_TheDataOutlivesTheProgram.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 3.2.8 identify the need for disaster recovery policies and procedures. 5.5.3
develop programs using operating system calls. 5.5.6 preserve, convert, or migrate data to a new
format.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop.

---

## Why this exists

The line's data file will outlive the program that writes it. It will be there after a power cut in
the middle of a save. It will be there when next year's version of the program, with a new file
format, opens it for the first time. And one day it will be gone, and someone will need to know what
to do.

Each of those is a disaster only if nobody planned for it.

---

## The concept in plain language

### A save that cannot destroy the last good copy

Opening a file with `open(path, "w")` empties it **immediately**. If anything fails between that
moment and the end of the write, the old data is gone and the new data is incomplete. The safe save
has four steps:

1. **Build the whole text in memory.** If the model cannot be written, no file has been touched.
2. **Copy the current file to a backup** (`shutil.copy2`).
3. **Write the new text to a temporary file**, then `flush()` and `os.fsync()`, which asks the
   operating system to actually put the bytes on the disk before continuing.
4. **Swap it in with `os.replace()`.** On one drive this is **atomic**: it either happens completely
   or not at all. A crash leaves the old file or the new one, never half of each.

If step 3 or 4 fails, delete the temporary file and raise your family's file error. The real file is
untouched.

### A restore that checks first

Restoring means copying the backup over the file. Load and fully check the backup **before** you
copy. Restoring a damaged backup over the last good file destroys the only good copy you had.

### Old files, new program

A **versioned** file says which format it uses (`"version": 2`). When the format changes, the program
keeps a **migration**: a function that turns a version 1 document into a version 2 document, filling
in anything the old version never recorded. Migrations never change their input. A file from a
**newer** program is refused, because the old program cannot know what the new fields mean.

Some values filled in by a migration are guesses. A person must review them before the data is
trusted, and the migration's documentation says which ones.

### A recovery plan, written before it is needed

A **disaster recovery plan** is the written procedure for the day the data store is lost or damaged.
Writing it forces the questions nobody asks until it is too late: What exactly is lost? Who notices,
and how? Where are the backups, and how old can they be? What must a person check by hand before the
line runs again? When was the plan last tested? A backup nobody has ever restored is a hope, not a
plan.

---

## Worked example 1: the unsafe save, failing

```python
# save_in_place.py
import json
import tempfile
from pathlib import Path


def save(document, path):
    with open(path, "w", encoding="utf-8") as handle:   # the old file is empty from here
        json.dump(document, handle, indent=2)


with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "line3.json"
    save({"version": 2, "racks": [{"tag": "L3-RCK-01", "load_kg": 640}]}, path)
    print("first save:", path.stat().st_size, "bytes, loads:", json.loads(path.read_text(encoding="utf-8"))["version"])
    try:
        save({"version": 2, "racks": [{"tag": "L3-RCK-01", "load_kg": {640}}]}, path)
    except TypeError as error:
        print("second save failed:", error)
    text = path.read_text(encoding="utf-8")
    print("file now holds", len(text), "characters:", repr(text[-20:]))
    try:
        json.loads(text)
    except json.JSONDecodeError as error:
        print("JSONDecodeError:", error)
```

Output:

```
first save: 103 bytes, loads: 2
second save failed: Object of type set is not JSON serializable
file now holds 80 characters: '",\n      "load_kg": '
JSONDecodeError: Expecting value: line 6 column 18 (char 80)
```

The second save failed partway through, because a Python `set` cannot be written as JSON. By then
`open(path, "w")` had already emptied the file, and `json.dump()` had written the first 80 characters
in pieces. The good first save is gone, and what is left will not load.

---

## Worked example 2: the safe save, failing the same way

```python
# save_safely.py
import json
import os
import shutil
import tempfile
from pathlib import Path


def save(document, path):
    path = Path(path)
    text = json.dumps(document, indent=2) + "\n"          # 1. build it all in memory
    temp = path.with_name(path.name + ".tmp")
    try:
        if path.exists():
            shutil.copy2(path, path.with_name(path.name + ".bak"))   # 2. keep the old one
        with open(temp, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)                              # 3. write somewhere else
            handle.flush()
            os.fsync(handle.fileno())                       #    and make the disk hold it
        os.replace(temp, path)                              # 4. swap, in one step
    except OSError:
        temp.unlink(missing_ok=True)
        raise


with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "line3.json"
    save({"version": 2, "load_kg": 640}, path)
    save({"version": 2, "load_kg": 950}, path)
    try:
        save({"version": 2, "load_kg": {950}}, path)
    except TypeError as error:
        print("third save failed:", error)
    print(sorted(p.name for p in Path(folder).iterdir()))
    print("file:  ", json.loads(path.read_text(encoding="utf-8")))
    print("backup:", json.loads((Path(folder) / "line3.json.bak").read_text(encoding="utf-8")))
```

Output:

```
third save failed: Object of type set is not JSON serializable
['line3.json', 'line3.json.bak']
file:   {'version': 2, 'load_kg': 950}
backup: {'version': 2, 'load_kg': 640}
```

The third save failed at step 1, in memory, before any file was opened. The folder holds the second
save and a backup of the first, and both load. There is no `.tmp` left behind.

---

## Worked example 3: migrating an old file

```python
# migrate_v1.py
import copy
import json


def migrate_v1_to_v2(old):
    """Return a new document. Never change the one you were given."""
    cells = {}
    for item in old["equipment"]:
        new = {"kind": item["type"], "tag": item["tag"], "name": item["name"]}
        if item["type"] != "rack":
            new["rated_kw"] = item["power_kw"]          # renamed in version 2
            new["locked_out_by"] = None                  # version 1 never recorded it
        cell = cells.setdefault(item["cell"], {"kind": "cell", "name": item["cell"], "items": []})
        cell["items"].append(new)
    return {"format": old["format"], "version": 2,
            "line": {"name": old["line_name"], "cells": list(cells.values())}}


v1 = {"format": "line3-plant", "version": 1, "line_name": "Line 3", "equipment": [
    {"type": "press", "tag": "L3-PRS-01", "name": "Press 1", "cell": "Forming", "power_kw": 15},
    {"type": "press", "tag": "L3-PRS-02", "name": "Press 2", "cell": "Forming", "power_kw": 22},
]}
before = copy.deepcopy(v1)
v2 = migrate_v1_to_v2(v1)
print(json.dumps(v2["line"]["cells"][0]["items"][0]))
print("version 1 unchanged:", v1 == before)
```

Output:

```
{"kind": "press", "tag": "L3-PRS-01", "name": "Press 1", "rated_kw": 15, "locked_out_by": null}
version 1 unchanged: True
```

Version 1 called the rating `power_kw` and never recorded lockouts. The migration renames the field
and fills `locked_out_by` with `null`, and the old document is unchanged. That filled-in `null` is
exactly the kind of value a person must review: version 1 did not record lockouts, so `null` means
"unknown," and someone has to walk the line.

---

## The wrong version: a restore that trusts the backup

The safe restore loads the backup first. Here the backup is damaged, and the check saves the file:

```python
# restore_checked.py
import json
import shutil
import tempfile
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def restore_backup(path):
    backup = Path(str(path) + ".bak")
    document = load(backup)            # if the backup is bad, this raises first
    shutil.copy2(backup, path)
    return document


with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "line3.json"
    path.write_text('{"version": 2, "load_kg": 640}', encoding="utf-8")
    Path(str(path) + ".bak").write_text('{"version": 2, "load_', encoding="utf-8")
    try:
        restore_backup(path)
    except json.JSONDecodeError as error:
        print("backup refused:", error)
    print("file still:", load(path))
```

Output:

```
backup refused: Unterminated string starting at: line 1 column 16 (char 15)
file still: {'version': 2, 'load_kg': 640}
```

Now imagine the version without `load(backup)` first: it would copy the damaged backup over the good
file, and **both** copies would be damaged. That wrong version produces no error at all during the
restore. The error arrives the next time anyone loads the file, and by then there is nothing left to
restore from.

---

## Why the wrong version is tempting

`open(path, "w")` then `json.dump()` is the first save everyone writes, and it works every time the
program is healthy, which is every time you test it. The failure needs a crash at the wrong moment.

A restore that does not check is tempting because a backup feels safe by definition. It is only as
good as the moment it was taken. A backup job that runs after the damage copies the damage.

The habits that prevent both: **never write over the only copy**, and **check a backup before you
trust it.**

---

## Vocabulary

| Term | What it means |
|---|---|
| **Atomic** | an operation that happens completely or not at all |
| **`os.replace()`** | an operating system call that swaps one file into another's place, atomically on one drive |
| **`os.fsync()`** | an operating system call that asks for written bytes to reach the disk now |
| **Backup** | a copy of data kept to restore from |
| **Restore** | putting a backup back in place of damaged or lost data |
| **Versioned format** | a file that records which version of its format it uses |
| **Migration** | code that converts data from an old format to a new one |
| **Disaster recovery plan** | the written procedure for when a data store is lost or damaged |

---

## Self-check

**Question 1.** The power fails between steps 3 and 4 of the safe save. What is on disk?

**Question 2.** Why is a file written by a **newer** version refused instead of loaded with the fields
the old program knows?

**Question 3.** A backup job copies the data file to a USB stick at midnight. The file was damaged at
6 p.m. Write the one sentence your recovery plan needs because of this.

---

### Answers

**1.** The real file, unchanged from the last successful save; a backup copy of it; and a complete
`.tmp` file with the new text that was never swapped in. Nothing is half-written.

**2.** The newer version may have added fields that change the meaning of the old ones, such as a unit
field. Loading only the fields you know would silently drop or misread data. Refusing tells the person
to use the newer program.

**3.** Any sentence to this effect: "Before restoring from the stick, check that the backup loads and
predates the damage; keep more than one dated backup so a damaged copy never replaces the last good
one."

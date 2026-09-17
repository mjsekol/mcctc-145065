# Lab U3-02: Save, Load, Recover
## 145065 Object-Oriented Programming · Unit 3 · Week 6

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** three Build 1 blocks. Tuesday is
Part 1 (steps 1-6), Wednesday is Part 2 (steps 7-10), and Thursday is Part 3 (steps 11-13).
**Competencies:** 5.5.6 (format output for data files, and migrate data to a new format), 2.3.1
(character encoding), 5.5.1 (data validation), 3.2.1 (data and application security), 5.5.3
(operating system calls), 3.2.8 (the need for disaster recovery procedures).

Files: `lab-u03-02-files/`: `errors.py`, `plant.py`, `storage.py`, `selfcheck_storage.py`, and
`sample_data/` with two good files and twelve files in `sample_data/bad/`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every tag, name, and badge id in this lab is invented. No hardware is used.

---

## The scenario

Line 3's model forgets everything when the program closes. The supervisor wants it saved: the
machines, their settings, how many strokes each press has run since service, and, above all, which
machines are locked out. A program that restarts and forgets a lockout leaves a technician inside a
machine with nobody protecting them.

Saving is where quiet mistakes hide. The file will be opened by other programs,
edited by hand, copied to a USB stick, cut off by a power failure, and read by next year's version of
this program. Each of those is a day in this lab.

## What you will build

- **Tuesday:** a round trip. The line becomes JSON text and comes back identical.
- **Wednesday:** a loader that refuses any damaged, hand-edited, or hostile file, and says exactly
  where the problem is.
- **Thursday:** a save that a crash cannot turn into half a file, a restore that checks the backup
  before trusting it, and a migration that reads last year's file format.

---

## Before you start

Copy the whole `lab-u03-02-files/` folder into `unit-03-lab/` in your repository and run:

```
python storage.py
python selfcheck_storage.py
```

`storage.py` prints:

```
Not written yet: Step 5: save_line()
Not written yet: Step 5: load_line()
```

The self-check ends with `1 of 17 self-checks passed`. The one that passes says there is no pickle
in `storage.py`. Keep it that way. Commit.

**`storage.py` grows across three days.** Every function you write is a stub now, and every stub
names its step. The functions marked GIVEN are written for you. Read them. You will need them.

---

## Part 1 · Tuesday · Objects become text

### Step 1. Read the worked example

Open `plant.py` and read, in this order:

1. `Equipment.to_dict()` and `_state_fields()`. One method builds the dict for every kind, and each
   level adds its own fields. This is the Unit 2 template method again.
2. `PoweredEquipment.to_dict()`, which adds `locked_out_by`, and `_restore_lockout()`.
3. `Press._state_fields()` and `Press.from_dict()`.
4. `Cell.to_dict()` and `Line.to_dict()`.

In your README, under `## What a restart remembers`, answer three questions:

- Why does `from_dict()` build the press through its constructor instead of setting attributes?
- A running press is saved. What is it when it loads, and why?
- Why is the lockout saved when the running state is not?

### Step 2. `to_dict()` and `from_dict()` for the other three kinds

In `plant.py`, write `_state_fields()` and a `from_dict()` class method for `Oven`, `Conveyor`, and
`StorageRack`. Follow `Press`. Save only what a restart must remember:

| Kind | Saved fields beyond `kind`, `tag`, `name` |
|---|---|
| `Oven` | `rated_kw`, `setpoint_c`, `max_c`, `locked_out_by` |
| `Conveyor` | `rated_kw`, `max_speed_mps`, `speed_mps`, `locked_out_by` |
| `StorageRack` | `capacity_kg`, `load_kg` |

`from_dict()` must go through the rules. Set the conveyor's speed and the rack's load **through
their properties**, so a file with a conveyor at 9 m/s is refused, not obeyed.

`from_dict()` needs `@classmethod` and `cls` as its first parameter. Forget the decorator and the
self-check shows why in "If it breaks."

**Observable result:** `3 of 17`. Both `Step 2` lines pass.

### Step 3. `dumps()`

In `storage.py`, `dumps(line)` returns the text of the whole file:
`json.dumps(line_to_document(line), indent=2, ensure_ascii=False)` followed by one `"\n"`.

`indent=2` makes the file readable and lets you compare two saves line by line. `ensure_ascii=False` is
step 6's subject.

**Observable result:** still `3 of 17`. Nothing can load yet.

### Step 4. `loads()`, the trusting version

For today, `loads(text, source)` returns `build_line(json.loads(text))`. `build_line()` is GIVEN, and
it trusts the file completely. Wednesday replaces it.

Now test the round trip at a Python prompt:

```python
>>> import storage, plant
>>> line = plant.build_sample_line()
>>> storage.dumps(storage.loads(storage.dumps(line))) == storage.dumps(line)
True
```

**Observable result:** `5 of 17`. Both `Step 4` lines pass: the text round trip is identical, and a
reloaded press is stopped, has its guard treated as open, and keeps its lockout.

### Step 5. `save_line()` and `load_line()`, the plain versions

- `save_line(line, path, keep_backup=True)`: write `dumps(line)` to the path with
  `encoding="utf-8"` and return `None`. Thursday makes it safe.
- `load_line(path)`: read the file with `encoding="utf-8"` and return
  `loads(text, source=str(path))`. Wednesday makes it careful.

**Observable result:** `8 of 17 self-checks passed`, and `python storage.py` prints:

```
Saved line3.json: 1901 bytes
Round trip identical: True
Version 1 sample not readable yet: KeyError 'line'
```

On Windows the size is 1901 bytes. On macOS or Linux it is 1823. `write_text()` turns each of the
file's 78 line endings into two bytes on Windows. Thursday's save writes the same bytes everywhere.
The last line is expected. Step 12 fixes it. Commit.

### Step 6. What the bytes actually are

A text file is bytes. The encoding is the rule that turns characters into bytes and back.

At a Python prompt, fill in this table in your README under `## Bytes`:

| Character | `ord()` | `.encode("utf-8")` | Bytes | `json.dumps()` with the default `ensure_ascii=True` |
|---|---|---|---|---|
| `A` | | | | |
| `é` | | | | |
| `Á` | | | | |
| `Ł` | | | | |
| `€` | | | | |

Then answer:

1. ASCII has 128 characters. Which rows are ASCII, and how many UTF-8 bytes does each ASCII
   character take?
2. `"Área de Soldadura"` is 17 characters. How many bytes is it in UTF-8, and why?
3. Save a line with a cell named `Área de Soldadura` using `open(path, "w")` with **no** encoding,
   then load it with `encoding="utf-8"`. Paste the last line of the error. Try again with a cell
   named `Łódź`. Paste that error too. What is the program's default encoding on this computer?

The self-check's `Step 6` line already passes if steps 3 and 5 used `ensure_ascii=False` and
`encoding="utf-8"`.

**Observable result:** still `8 of 17`, and the README table is complete. Commit and push.

---

## Part 2 · Wednesday · A file is untrusted input

**Why today exists.** A file can be damaged by a crash, edited by hand, or written by someone who
wants your program to misbehave. The moment you load it is the moment your program trusts outside
data. Every check today happens before any object is built from the file.

Try Tuesday's loader on two bad files first:

```python
>>> storage.load_line("sample_data/bad/unknown_kind.json")
```

It ends `KeyError: 'Line'`. The file asked for a kind named `Line`, and the dictionary did not have
one. Now imagine a loader that looked the kind up with `globals()[item["kind"]]`. `Line` exists
there. So do `Path`, `json`, and everything else the module imported. The file would be choosing
which of your code runs.

### Step 7. The allowlist

`EQUIPMENT_KINDS` in `storage.py` maps the only kind names a file may use to the class each one
builds, with the exact fields each kind must have. `press` is written. Add `oven`, `conveyor`, and
`rack`, with every field their `to_dict()` writes, and nothing else. Use the GIVEN checkers:
`_text`, `_optional_text`, `_number`, `_whole`.

Read `_check_fields()` and `_build_equipment()` before you write. A missing field, an extra field,
and a field of the wrong JSON type are all refused, and every refusal names its `where`: a path
into the file such as `line.cells[1].items[0].rated_kw`.

**Observable result:** still `8 of 17`. `loads()` does not use the table yet.

### Step 8. `loads()`, the careful version

Replace today's one-line `loads()`. The new version:

1. Calls `json.loads(text, parse_constant=...)` with a function that raises `ValueError` for `NaN`,
   `Infinity`, and `-Infinity`. Python's `json` module accepts those words, and they are not valid
   JSON. A `NaN` load passes every check, because `NaN > 1200` and `NaN <= 1200` are both `False`.
2. Turns a `json.JSONDecodeError` into
   `PlantFileFormatError(source, "document", f"not valid JSON: {error.msg} (line {error.lineno}, column {error.colno})")`,
   raised `from` the original.
3. Turns any other `ValueError` from step 1 into a `PlantFileFormatError` at `"document"`, and a
   `RecursionError` into one that says the JSON is nested too deeply.
4. Returns `line_from_document(migrate(document, source), source)`. Both are GIVEN.

`JSONDecodeError` is a kind of `ValueError`. Which `except` goes first?

**Observable result:** `9 of 17`. The `Step 8` line passes: Infinity is refused and named.

### Step 9. `load_line()`, the careful version

Replace today's `load_line()`. The new version asks the operating system before it reads:

1. `path.stat().st_size` gives the size without reading the file. A missing file raises
   `FileNotFoundError` here. Turn it into `PlantFileMissingError(path, "file does not exist")`.
2. If the size is over `MAX_FILE_BYTES`, raise `PlantFileFormatError` at `"document"` with a problem
   that names the size and the limit. A 4 GB "plant file" is not read into memory to find out.
3. Read the bytes with `read_bytes()`, and decode them with `"utf-8-sig"`. That codec accepts UTF-8
   and also the invisible byte order mark some Windows editors put at the start of a file.
4. A `UnicodeDecodeError` becomes `PlantFileFormatError` at `"document"`:
   `not UTF-8 text (bad byte at position N)`.
5. Return `loads(text, source=str(path))`.

`PlantFileMissingError` inherits from `FileNotFoundError` too. Look at `errors.py`: it is the same
two-parent idea as Monday's `ConfigurationError`.

**Observable result:** `13 of 17 self-checks passed`. Every `Part 2` line passes. Then, at a
prompt, load every file in `sample_data/bad/` and print what each one raises. Ten are refused.
`bom_but_valid.json` loads, correctly. So does `lockout_erased.json`.

### Step 10. What validation cannot do, and why never pickle

Read worked example 4 in the Wednesday notes, `pickle_runs_code.py`. Then open
`sample_data/bad/lockout_erased.json` and compare it with `sample_data/line3_v2.json`.

In your README, under `## Untrusted input`, answer:

1. What does `lockout_erased.json` change, and why does every check pass?
2. What can a pickle file do while it is being **loaded** that a JSON file cannot?
3. `_build_equipment()` chooses a class from a four-row table. What could a file do if the loader
   used `globals()` instead?
4. Name one check from steps 8 and 9 that runs **before** any object is built, and say what it
   protects against.

**Observable result:** still `13 of 17`, and the four answers are in the README. Commit and push.

---

## Part 3 · Thursday · The data outlives the program

### Step 11. A save a crash cannot break, and a restore that checks first

Tuesday's `save_line()` opens the real file for writing, which empties it, and then writes. A crash
in between leaves a cut-off file, and the last good save is already gone.

Rewrite `save_line()` in this order:

1. Build the whole text first: `text = dumps(line)`. If the model cannot be written, nothing on disk
   has been touched.
2. If `keep_backup` is true and the file exists, copy it to `backup_path(path)` with
   `shutil.copy2()`. Remember the backup path to return.
3. Write the text to a temporary file beside the real one, `<name>.tmp`, with `encoding="utf-8"` and
   `newline="\n"`. Before closing it, call `handle.flush()` and then `os.fsync(handle.fileno())`.
   The first hands Python's buffer to the operating system. The second asks the operating system to
   put it on the disk.
4. `os.replace(temp, path)`. On one drive, this swaps the new file in as one step. A crash leaves the
   old file or the new one, never half of each.
5. Wrap steps 2 through 4 in `try`. On any `OSError`, delete the `.tmp` file with
   `temp.unlink(missing_ok=True)` and raise `PlantFileError(path, ...)` from the original error.
6. Return the backup path, or `None`.

Then write `restore_backup(path)`. It loads the backup with `load_line()` **first**. Only if that
succeeds does it copy the backup over the file. Return the line. A corrupt backup copied over the
file would destroy the last good copy.

**Observable result:** `16 of 17`. The self-check simulated a power cut in `os.replace()` and found
the real file whole and no `.tmp` left behind. `python storage.py` now reports `1823 bytes` on every
computer.

### Step 12. Read last year's files

Version 1 of this program saved a flat list of machines, and it called the power rating
`power_kw`. Read `sample_data/line3_v1.json` and the GIVEN `migrate_v1_to_v2()`. One line is
missing. Where the TODO is, copy `power_kw` into the new document as `rated_kw`.

`loads()` already calls `migrate()`, so a version 1 file now loads as version 2. The version 1
document itself is never changed.

**Observable result:** `17 of 17 self-checks passed`, and `python storage.py` prints:

```
Saved line3.json: 1823 bytes
Round trip identical: True
Version 1 sample loaded: 5 machines
```

### Step 13. What a person must check

A migration can only copy what the old file had. Everything else is a default. Read `V1_DEFAULTS`
and the line that sets `locked_out_by`.

In your README, under `## After a migration`, write a table with one row per value the migration
invents: the field, the value it gets, and whether a person must check it before the line runs, with
a reason. At least one of them is a safety question. Commit and push.

---

## Acceptance criteria, full lab

- [ ] `python selfcheck_storage.py` prints `17 of 17 self-checks passed`
- [ ] `python storage.py` prints the three lines in step 12
- [ ] Ten of the twelve files in `sample_data/bad/` are refused, each with a `where`
- [ ] `storage.py` imports no pickle, and no class is looked up by a name from the file
- [ ] The README has the sections from steps 1, 6, 10, and 13
- [ ] Committed at the end of Tuesday, Wednesday, and Thursday

---

## If it breaks

### 1. JSON does not know your object

```
TypeError: Object of type Press is not JSON serializable
```

**Cause:** a `to_dict()` put an object in the dict instead of that object's dict, most often
`Cell.to_dict()` returning `self._items`. JSON holds dicts, lists, strings, numbers, true, false,
and null. Call `item.to_dict()` for each item.

### 2. `from_dict()` without `@classmethod`

```
TypeError: Oven.from_dict() missing 1 required positional argument: 'data'
```

**Cause:** `Oven.from_dict(data)` passed `data` as `self`. Add `@classmethod` and name the first
parameter `cls`.

### 3. A field the file does not have

```
KeyError: 'tonnage'
```

**Cause:** Tuesday's trusting loader read `typo_field.json`, which spells it `tonage`. Wednesday's
loader turns this into `line.cells[0].items[1]: missing field tonnage`.

### 4. The byte order mark

```
json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

**Cause:** the file starts with the three bytes some editors add. Step 9 decodes with `utf-8-sig`.

### 5. The default encoding

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc1 in position 1928: invalid start byte
```

```
UnicodeEncodeError: 'charmap' codec can't encode character 'Ł' in position 1928: character maps to <undefined>
```

**Cause:** a file opened without `encoding=`. On this Windows computer the default was cp1252, which
wrote `Á` as the single byte `0xc1` and cannot write `Ł` at all. Always pass `encoding="utf-8"`.

### 6. Something JSON cannot hold

```
TypeError: Object of type set is not JSON serializable
```

**Cause:** a value in the model is a Python `set`. With step 11's save, this happens while building
the text, so no file is touched. With Tuesday's save it happens while writing, and a file opened
with `open(path, "w")` has already been emptied.

### 7. A version 1 file before step 12

```
PlantFileFormatError: ...line3_v1.json: line.cells[0].items[0]: missing field rated_kw
```

**Cause:** the migration built the press without its rating. Finish step 12.

### Not an error, and the one that matters most: a file that passes every check

`lockout_erased.json` loads without complaint, and Press 2 is no longer locked out. Validation
proves a file is well formed. It cannot prove the file is true. That is why step 13 and the recovery
plan in your project name the checks only a person can do.

**Error wording was captured on Python 3.13.7 on Windows.** Confirm it on the lab's Python 3.14. The
default encoding in error 5 depends on the computer [VERIFY].

---

## Stretch goal

Add `save_line(..., keep_backups=3)`, which keeps the last three saves as `.bak1`, `.bak2`, and
`.bak3`, oldest last. Write a test that saves five times and checks that exactly three backups exist
and that `.bak1` holds the fourth save. Then write two sentences: why is one backup not enough if a
bad save is not noticed until the next day?

---

## Submission checklist

- [ ] Self-check 17 of 17
- [ ] README sections: what a restart remembers, bytes, untrusted input, after a migration
- [ ] No `line3.json`, `.bak`, or `.tmp` files committed; the program writes only to a temporary
      folder
- [ ] Committed and pushed at the end of each day
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.5.6, 2.3.1, 5.5.1, 3.2.1, 5.5.3, 3.2.8) and grade
on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 15 of Tuesday Build 1, step 2 has not started, or `from_dict()` is still a mystery | SCAFFOLDED |
| Steady progress, and questions about which checker fits which field | STANDARD |
| 8 of 17 before Tuesday Build 1 is half over | EXTENDED |
| The student asks what saving a factory model has to do with anything they will build | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out a different `plant.py`, with `Oven` written as a second
  worked example, and a different `storage.py`, with Tuesday's plain `dumps()`, `loads()`,
  `save_line()`, and `load_line()` already written. The self-check starts at `2 of 17`.
- **Steps:** Tuesday is steps 1, 2 (conveyor and rack only), and 6. Skip steps 3, 4, and 5, and
  read the four written functions instead.
- **Checkpoints:** show the self-check to the instructor at the end of each Build 1: `8 of 17`,
  `13 of 17`, `17 of 17`.
- **Keep steps 6, 10, and 13.** The written answers are the lesson.

**Acceptance criteria:** 17 of 17 and the four README sections.

**Grading:** same 100-point scale. Full completion earns the same grade as full completion of
STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one problem the lab has not taught.

**Added requirement.** `lockout_erased.json` passes every check. Make the program notice when a
saved file has been changed by anything other than `save_line()`. Write
`save_line_with_checksum()`, which saves and then writes a fingerprint of the file's bytes beside
it, and `load_line_verified()`, which refuses a file whose fingerprint does not match, or that has
none. Demonstrate it: save, change `"tech-07"` to `null` by hand, and show the plain load accepting
the file and the verified load refusing it.

**Hint, not the answer.** Python's standard library has a module for secure hashes. Read the
`hashlib` page in the library reference, `https://docs.python.org/3/library/hashlib.html`, and use
SHA-256.

**Acceptance criteria:** all STANDARD criteria; the demonstration output in the README; a
paragraph saying who a checksum stops and who it does not, since anyone who can edit the file can
also recompute the fingerprint; a decision log entry naming the rejected alternative.

**Grading:** same scale.

---

## APPLIED

**For the student who asks when they would use this.** The same skill in a game's save file.

**Changed scenario.** A game saves a player's progress: the character, the inventory, and the
unlocked levels. Players edit save files, crashes cut them off, and next month's update changes the
format. Write `to_dict()` and `from_dict()` for your character and items, a loader that refuses a
file with an unknown item type, a negative gold count, or `NaN` health, and names where the problem
is, a save that keeps one backup and replaces the file atomically, and a migration from a version 1
format that stored the inventory as a comma-separated string. Invent every name and number. No real
game's content.

**What you build.** The above, twelve bad save files of your own, and a self-check of at least ten
checks modeled on `selfcheck_storage.py`, including the simulated power cut.

**Acceptance criteria:** your self-check passes; your README has the bytes table, the untrusted
input answers for your own format, and the after-a-migration table.

**Grading:** same scale. Security is judged on whether any field in the file can make the loader
build a class you did not list.

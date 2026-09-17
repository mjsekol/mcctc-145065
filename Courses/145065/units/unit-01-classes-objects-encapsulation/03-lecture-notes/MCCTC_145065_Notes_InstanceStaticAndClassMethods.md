# Lecture Notes: Instance, Static, and Class Methods
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W03_InstanceStaticAndClassMethods.md). There is no
exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W03_InstanceStaticAndClassMethods.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competency:** 5.3.12 write code to create classes, objects, and methods.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop.

---

## Why this exists

Last Wednesday you learned two homes for behavior. Code that needs this object's data is a method.
Code that needs no object is a function. Some code falls between the two.

Checking whether `"L3-OVN-01"` is a valid asset tag needs no machine. It is still clearly about
machines, and you want it next to the `Machine` class, not in a loose file of helpers. Counting how
many machines the program has built needs no single machine either. It needs the class. And building
a machine from a row in a file needs to run the class's own rules.

Python gives you a method kind for each of these. Choosing the right one is a design decision, and
your refactor project asks you to make at least one of them on purpose and say why.

---

## The concept in plain language

**Choose the kind by what the method needs.**

| The method needs | Kind | First parameter | Decorator |
|---|---|---|---|
| this one object | instance method | `self` | none |
| the class, not one object | class method | `cls` | `@classmethod` |
| neither | static method | none | `@staticmethod` |

- An **instance method** is what you have written all along. It reads or changes one object.
- A **class method** receives the class itself as `cls`. It can read data shared by the whole class,
  and it can build new objects by calling `cls(...)`.
- A **static method** receives nothing automatically. It is a plain function that lives inside the
  class because it belongs with that class. You can call it on the class or on an object.

### Class attributes, briefly

A class method usually reads a **class attribute**: a variable assigned in the class body, outside any
method. There is one copy, shared by every object. `_machines_created = 0` in the example below is one.
Tomorrow's lesson is all about where names like that live and how they go wrong. Today you only need
to know that the class method reads it through `cls`, and `__init__` updates it through the class name.

### Alternative constructors

A class method that builds and returns an object is called an **alternative constructor**. Its name
usually starts with `from_`. `Machine.from_record(row)` reads a row from a file, cleans it up, and
calls `cls(...)`. Because it calls the normal constructor, every rule in `__init__` still runs. You
will want one in your refactor project, where your 145060 data arrives as rows.

---

## Worked example 1: all three kinds in one class

```python
# method_kinds.py
import re

_TAG_PATTERN = re.compile(r"L3-[A-Z]{3}-[0-9]{2}")


class Machine:
    _machines_created = 0                       # class attribute: one shared count

    def __init__(self, asset_tag, rated_kw):
        if not Machine.is_valid_asset_tag(asset_tag):
            raise ValueError(f"asset tag {asset_tag!r} does not match L3-ABC-00")
        self.asset_tag = asset_tag
        self.rated_kw = float(rated_kw)
        Machine._machines_created += 1

    @staticmethod
    def is_valid_asset_tag(tag):
        """Needs no machine and no class data. Lives here because it is about machines."""
        return isinstance(tag, str) and _TAG_PATTERN.fullmatch(tag) is not None

    @classmethod
    def machines_created(cls):
        """Needs the class, not one machine."""
        return cls._machines_created

    @classmethod
    def from_record(cls, record):
        """A second way to build a machine: from a row read out of a file."""
        return cls(record["tag"].strip().upper(), float(record["kw"]))

    def describe(self):
        """Needs this machine."""
        return f"{self.asset_tag}: {self.rated_kw:g} kW"


print(Machine.is_valid_asset_tag("L3-OVN-01"), Machine.is_valid_asset_tag("oven"))
press = Machine("L3-PRS-01", 15)
rack_row = {"tag": " l3-cnv-01 ", "kw": "3"}
conveyor = Machine.from_record(rack_row)
print(press.describe(), "|", conveyor.describe())
print("Machines built:", Machine.machines_created())
print(press.is_valid_asset_tag("L3-PRS-02"))   # works on an object too
```

Output:

```
True False
L3-PRS-01: 15 kW | L3-CNV-01: 3 kW
Machines built: 2
True
```

Read each docstring. It states what the method needs, and the kind follows from that. The pattern uses
`[0-9]` rather than `\d`, because in Python 3 `\d` also matches digits from other writing systems.

`from_record` cleaned up a messy row: extra spaces, lower case, and a rating stored as text. Then it
called `cls(...)`, so the tag check in `__init__` ran on the cleaned value.

---

## Worked example 2: building machines from a file

Your refactor project reads rows from a file. `csv.DictReader` turns each line into a dictionary keyed
by the header, which is exactly what `from_record` expects. This file imports the `Machine` class from
example 1, saved without its demo lines as `machines.py`.

```python
# load_machines.py
import csv
import io

from machines import Machine

# In the refactor project this text comes from a file. Here it is inline.
RACK_FILE = """tag,kw
 l3-cnv-01 ,3
L3-PRS-02,22
press three,15
"""

loaded = []
for row in csv.DictReader(io.StringIO(RACK_FILE)):
    try:
        loaded.append(Machine.from_record(row))
    except ValueError as error:
        print("Skipped a row:", error)

for machine in loaded:
    print(machine.describe())
print("Machines built:", Machine.machines_created())
```

Output:

```
Skipped a row: asset tag 'PRESS THREE' does not match L3-ABC-00
L3-CNV-01: 3 kW
L3-PRS-02: 22 kW
Machines built: 2
```

The bad row was refused by the rules in `__init__`, not by extra code in the loader. The count is 2,
not 3, because the counter only goes up after every check has passed. `io.StringIO` makes a string
behave like an open file, so you can test a loader without creating one.

---

## Worked example 3: the same choice outside the shop

```python
# playlist.py
class Playlist:
    MAX_SONGS = 100

    def __init__(self, title):
        self.title = title
        self._songs = []

    @staticmethod
    def seconds_to_clock(seconds):
        """Needs no playlist at all. It formats a number."""
        return f"{seconds // 60}:{seconds % 60:02d}"

    @classmethod
    def from_line(cls, line):
        """A second constructor: builds a playlist from 'title;song;song'."""
        title, *songs = [part.strip() for part in line.split(";")]
        playlist = cls(title)
        for song in songs:
            playlist.add(song)
        return playlist

    def add(self, song):
        """Needs this playlist."""
        if len(self._songs) >= self.MAX_SONGS:
            raise ValueError(f"{self.title} is full")
        self._songs.append(song)

    def summary(self):
        return f"{self.title}: {len(self._songs)} songs"


print(Playlist.seconds_to_clock(215))
road_trip = Playlist.from_line("Road Trip; Song A; Song B; Song C")
print(road_trip.summary())
```

Output:

```
3:35
Road Trip: 3 songs
```

`from_line` builds the playlist with `cls(title)` and then fills it through `add`, so the 100-song
limit applies to playlists built from text too. An alternative constructor should never sneak around
the normal rules.

Is `seconds_to_clock` better as a static method or as a plain function? Honest answer: it could be
either. It lives here because every caller who needs it is already using playlists. If a second class
needed it, a module-level function would be the better home.

---

## The wrong version, and the error it produces

Leave off `@staticmethod`:

```python
class Machine:
    def is_valid_asset_tag(tag):          # the deliberate mistake: no @staticmethod
        return tag.startswith("L3-")

press = Machine()
print(Machine.is_valid_asset_tag("L3-PRS-01"))
print(press.is_valid_asset_tag("L3-PRS-01"))
```

Output:

```
True
Traceback (most recent call last):
  File "...\static_forgot.py", line 7, in <module>
    print(press.is_valid_asset_tag("L3-PRS-01"))
          ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
TypeError: Machine.is_valid_asset_tag() takes 1 positional argument but 2 were given
```

Called on the class, it works, because nothing is passed automatically. Called on an object, Python
passes the object first, as it does for every normal method. Now there are two arguments, the object
and the tag, and the method only has room for one. `@staticmethod` is the instruction "do not pass
the object".

---

## Why the wrong version is tempting

The first call worked. If you only ever test through the class, you never see the bug, and it waits
for the first teammate who calls it on an object. That is the thread again: the dangerous design is
the one that works today.

The other temptation is to skip the choice entirely and make everything an instance method, with a
`self` that is never used. It runs. It also hides what the method needs, and anyone reading it has
to check the whole body to learn that it ignores the object. The decorator is documentation Python
enforces.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Instance method** | a method that receives one object as `self` |
| **Class method** | a method marked `@classmethod` that receives the class as `cls` |
| **Static method** | a method marked `@staticmethod` that receives nothing automatically |
| **Decorator** | a line starting with `@` that changes how the next function works |
| **`cls`** | the name used for the class passed to a class method |
| **Class attribute** | a variable in the class body, shared by every object |
| **Alternative constructor** | a class method, often named `from_...`, that builds and returns an object |
| **`csv.DictReader`** | reads CSV text and gives each row as a dictionary keyed by the header |

---

## Self-check

**Question 1.** For each method in a `ToolCrib` class, name the kind: (a) `overdue_tools(now)`, which
lists this crib's overdue tools; (b) `is_valid_tool_tag(tag)`, which checks the `TC-014` pattern;
(c) `from_csv_row(row)`, which builds a crib from one line of a file.

**Question 2.** Why should `from_record` call `cls(...)` instead of creating the object and setting
its attributes directly?

**Question 3.** A method is written `def total_built(): return Machine._built` with no decorator and
no parameters. What happens when you call `Machine.total_built()`? What happens with
`press.total_built()`?

---

### Answers

**1.** (a) Instance method, because it needs this crib's tools. (b) Static method, because it needs
no crib and no class data. (c) Class method, because it builds a new object and should call `cls`.

**2.** `cls(...)` runs `__init__`, so every validation rule and the counter still apply. Setting
attributes directly would skip them, which is the same silent bypass as Monday's `__init__` mistake.

**3.** `Machine.total_built()` works and returns the count, because nothing is passed automatically
through the class. `press.total_built()` raises `TypeError`, because Python passes `press` and the
method takes no arguments. The message says it takes 0 positional arguments but 1 was given.

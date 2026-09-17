# Lecture Notes: A File Is Untrusted Input
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W06_AFileIsUntrustedInput.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-03-exceptions-serialization/04-slides/MCCTC_145065_Slides_W06_AFileIsUntrustedInput.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 3.2.1 identify and implement data and application security. 5.5.1 develop programs
using data validation techniques. 5.5.3 develop programs using operating system calls.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop.

---

## Why this exists

"My program wrote this file, so my program can trust it." Every part of that sentence fails on a
real shop floor. Files get edited by hand in Notepad. They get copied from another machine running an
older version. They get cut off when the power goes out mid-save. Occasionally someone edits one on
purpose, to make the program do something it should not.

The moment a program loads a file is the moment it trusts outside data. That makes loading the place
where **application security** lives for this program.

---

## The concept in plain language

A guarded loader checks the file in layers, cheapest first, and refuses at the first problem, saying
exactly where it is.

1. **Size, before reading.** Ask the operating system how big the file is (`Path.stat()`), and refuse
   a file far bigger than any real one. Reading a 3 GB file to find out it is wrong is a failure too.
2. **Encoding.** Decode as UTF-8. Use `utf-8-sig`, which also accepts the invisible byte order mark
   some Windows editors put at the front.
3. **Syntax.** Parse the JSON, and refuse `NaN` and `Infinity`. They are not valid JSON, Python
   accepts them anyway, and a `NaN` compares `False` against every limit, so it passes every check.
4. **Shape.** Every object has exactly the fields it should: none missing, none extra. A typo such as
   `"tonage"` is refused, not ignored.
5. **Types.** A number is a number. `true` is not 15 kW, even though Python counts `True` as an
   integer.
6. **Kind.** The file picks a class **from an allowlist**, a table of the only kinds allowed. It never
   names a class for Python to look up.
7. **Values.** Build every object through its constructor, so a negative rating is refused by the
   same rule that refuses it everywhere else.

Every refusal raises your family's format error with a **where**, a path into the document such as
`line.cells[1].items[0].rated_kw`, so the person fixing the file knows where to look.

**Never load a pickle you did not make.** Python's `pickle` format can store "call this function"
instead of data, and `pickle.loads()` makes the call while it loads. JSON can only hold data. That is
the reason this course never uses pickle.

---

## Worked example 1: NaN passes every check

```python
# nan_passes.py
import json

rack = json.loads('{"tag": "L3-RCK-01", "load_kg": NaN, "capacity_kg": 1200}')
load = rack["load_kg"]
print(load)
print("overloaded:", load > rack["capacity_kg"])
print("within capacity:", load <= rack["capacity_kg"])


def refuse(name):
    raise ValueError(f"{name} is not allowed in a plant file")


try:
    json.loads('{"load_kg": NaN}', parse_constant=refuse)
except ValueError as error:
    print("refused:", error)
```

Output:

```
nan
overloaded: False
within capacity: False
refused: NaN is not allowed in a plant file
```

The rack is neither overloaded nor within capacity. Any check written as "if load > capacity, warn"
stays silent forever. `parse_constant` is the hook `json.loads` calls for `NaN`, `Infinity`, and
`-Infinity`, and raising there refuses them.

---

## Worked example 2: an allowlist, field checks, and a where

```python
# allowlist_loader.py
import json


class LoadError(Exception):
    def __init__(self, where, problem):
        self.where = where
        super().__init__(f"{where}: {problem}")


class Press:
    def __init__(self, tag, rated_kw):
        self.tag, self.rated_kw = tag, rated_kw


class Rack:
    def __init__(self, tag, capacity_kg):
        self.tag, self.capacity_kg = tag, capacity_kg


def number(value, where):
    # True is an int in Python. A file that says "rated_kw": true is wrong.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LoadError(where, f"must be a number, not {type(value).__name__}")
    return value


KINDS = {  # the file may pick one of these, and nothing else
    "press": (Press, {"kind", "tag", "rated_kw"}),
    "rack": (Rack, {"kind", "tag", "capacity_kg"}),
}


def build(data, where):
    entry = KINDS.get(data.get("kind"))
    if entry is None:
        raise LoadError(f"{where}.kind", f"unknown kind {data.get('kind')!r}")
    cls, fields = entry
    if set(data) != fields:
        raise LoadError(where, f"fields must be exactly {sorted(fields)}")
    if cls is Press:
        return Press(data["tag"], number(data["rated_kw"], f"{where}.rated_kw"))
    return Rack(data["tag"], number(data["capacity_kg"], f"{where}.capacity_kg"))


items = json.loads("""[
  {"kind": "press", "tag": "L3-PRS-01", "rated_kw": 15},
  {"kind": "press", "tag": "L3-PRS-02", "rated_kw": true},
  {"kind": "Line", "tag": "L3-LIN-01"},
  {"kind": "rack", "tag": "L3-RCK-01", "capacity_kg": 1200, "tonage": 60}
]""")
for index, data in enumerate(items):
    try:
        item = build(data, f"items[{index}]")
        print("built", type(item).__name__, item.tag)
    except LoadError as error:
        print("refused", error)
```

Output:

```
built Press L3-PRS-01
refused items[1].rated_kw: must be a number, not bool
refused items[2].kind: unknown kind 'Line'
refused items[3]: fields must be exactly ['capacity_kg', 'kind', 'tag']
```

Three bad items, three refusals, each with the exact place: a `true` where a number belongs, a kind
that is not on the list, and a misspelled extra field.

---

## Worked example 3: asking the operating system first

```python
# size_first.py
import tempfile
from pathlib import Path

MAX_FILE_BYTES = 1_000_000

with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "line3.json"
    path.write_bytes(b" " * 3_000_000)
    size = path.stat().st_size                  # an operating system call: no reading yet
    print(f"{size} bytes on disk")
    if size > MAX_FILE_BYTES:
        print(f"refused before reading: the limit is {MAX_FILE_BYTES}")
    bom = Path(folder) / "bom.json"
    bom.write_bytes(b'\xef\xbb\xbf{"version": 2}')
    print(bom.read_bytes()[:3])
    print(bom.read_bytes().decode("utf-8-sig"))
```

Output:

```
3000000 bytes on disk
refused before reading: the limit is 1000000
b'\xef\xbb\xbf'
{"version": 2}
```

`path.stat().st_size` asks the file system for the size without reading a byte of the file. The last
two lines show a byte order mark: three bytes, `ef bb bf`, and `utf-8-sig` removes them. Here is what
plain UTF-8 does with the same file:

```python
# bom_refused.py
import json
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as folder:
    bom = Path(folder) / "bom.json"
    bom.write_bytes(b'\xef\xbb\xbf{"version": 2}')
    print(json.loads(bom.read_text(encoding="utf-8")))
```

Output:

```
Traceback (most recent call last):
  File "...\bom_refused.py", line 9, in <module>
    print(json.loads(bom.read_text(encoding="utf-8")))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "...\Lib\json\__init__.py", line 335, in loads
    raise JSONDecodeError("Unexpected UTF-8 BOM (decode using utf-8-sig)",
                          s, 0)
json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

---

## Worked example 4: why pickle is never used here

This demonstration is harmless: the only thing it does is print. It shows the idea without the
danger.

```python
# pickle_runs_code.py
# A harmless demonstration. The only thing this "attack" does is print.
import pickle


class Surprise:
    def __reduce__(self):
        # pickle stores "call print with this text" instead of the object.
        return (print, ("this line ran while the file was being LOADED",))


data = pickle.dumps(Surprise())
print(len(data), "bytes of pickle")
result = pickle.loads(data)
print("loads() returned", result)
```

Output:

```
85 bytes of pickle
this line ran while the file was being LOADED
loads() returned None
```

The printed line came from **loading**. The program only asked to read data. If the stored call had
been something other than `print`, it would have run the same way. Python's own documentation for
the `pickle` module warns about this at the top of the page.

---

## The wrong version: a loader that lets the file choose

```python
# globals_loader.py
import json


class Press:
    def __init__(self, tag, rated_kw):
        if rated_kw <= 0:
            raise ValueError("rated_kw must be above 0")
        self.tag, self.rated_kw = tag, rated_kw
        self._guard_closed = False


def build(data):
    cls = globals()[data.pop("kind")]          # the file names the class
    item = cls.__new__(cls)                    # skip __init__ and its checks
    item.__dict__.update(data)                 # the file writes any attribute
    return item


press = build(json.loads('{"kind": "Press", "tag": "L3-PRS-01", "rated_kw": -15, "_guard_closed": true}'))
print(press.tag, press.rated_kw, press._guard_closed)
build(json.loads('{"kind": "json", "tag": "x"}'))
```

Output:

```
L3-PRS-01 -15 True
Traceback (most recent call last):
  File "...\globals_loader.py", line 22, in <module>
    build(json.loads('{"kind": "json", "tag": "x"}'))
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "...\globals_loader.py", line 15, in build
    item = cls.__new__(cls)                    # skip __init__ and its checks
TypeError: module.__new__(X): X is not a type object (module)
```

Look at the first line of output. The file named the class, skipped the constructor, set a
**negative** rating the constructor would have refused, and set the private `_guard_closed` to
`True`. A press loaded from this file believes its guard is closed. Then a file that named `json`, a
module, crashed the loader with an error nobody planned for.

**The fix** is worked example 2: an allowlist of kinds, exact fields, and construction through
`__init__`.

---

## Why the wrong version is tempting

The generic loader is short, and it "handles new classes automatically." Every file your own program
writes loads perfectly, so every test you think to write passes. The attacker, the power cut, and the
person with Notepad were not in the tests.

The habit that prevents it: **treat every file as if a stranger wrote it**, and write at least one test
per layer with a file that is wrong in exactly that way.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Untrusted input** | any data from outside the running program, including its own saved files |
| **Deserialization** | turning stored data back into objects; the moment trust is extended |
| **Allowlist** | a list of the only values allowed; anything else is refused |
| **Validation** | checking data against rules before using it |
| **Byte order mark (BOM)** | three invisible bytes some editors add to the front of a UTF-8 file |
| **`NaN`** | "not a number," a float that compares false with everything, itself included |
| **Operating system call** | asking the OS for something, such as a file's size with `stat()` |
| **Pickle** | Python's own object format; loading one can run code |

---

## Self-check

**Question 1.** A file has `"load_kg": -5`. Which layer refuses it, and why is that layer the right
one?

**Question 2.** Why check the size with `stat()` before reading the file?

**Question 3.** A classmate says: "My loader uses `pickle`, but only for files my program saved." Give
the strongest version of their argument, then the reason this course still says no.

---

### Answers

**1.** The values layer: the object is built through its constructor or setter, whose rule refuses a
negative load. The shape and type layers pass it, because it is a correctly named number. Putting the
rule in the class means files, forms, and code all hit the same rule.

**2.** Reading costs memory and time proportional to the file. A size check costs almost nothing and
refuses a file that could not be real before any of it is read.

**3.** For: if only this program ever writes the file, and nobody else can reach the folder, the file
contains only what the program put there, and pickle saves a lot of code. Against: files get copied,
emailed, restored from backups, and edited, and the program cannot tell a file it wrote from one that
only looks like it. With JSON, a changed file can at worst be wrong data, which validation catches.
With pickle, a changed file can run code.

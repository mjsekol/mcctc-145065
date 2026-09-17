# Lecture Notes: Objects That Hold Objects
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W02_ObjectsThatHoldObjects.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W02_ObjectsThatHoldObjects.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competency:** 5.3.12 write code to create classes, objects, and methods. This lesson also previews
5.1.2, explain how algorithms and data structures are used in information processing, which you earn
in Week 3's lab.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop.

---

## Why this exists

One press is one object. A shop floor is many. Line 3 groups machines into work cells, and a cell has
rules of its own: no two machines with the same asset tag, and nothing in the cell that is not a
machine.

You could keep the machines in a plain list and let every part of the program append to it. You know
where that goes. It is Monday's dictionary problem again, one level up. Any line can put a duplicate
in, or a string, and nothing notices until much later.

The fix is the same idea as Monday. An object that holds a collection **owns the rules for that
collection**. It checks every member on the way in, and it never hands out the real collection.

---

## The concept in plain language

A **container object** keeps its members in an internal collection and gives the rest of the program
controlled ways in and out:

- **One way in.** An `add` method that refuses bad members.
- **Read-only ways out.** A method that returns a **copy**, here a tuple, so a caller can read the
  machines but cannot add or remove any behind the cell's back.
- **Python's built-in questions.** Three special methods let your object answer the questions Python
  already knows how to ask:

| You write | Python calls | Your method answers |
|---|---|---|
| `len(forming)` | `forming.__len__()` | how many members |
| `"L3-PRS-02" in forming` | `forming.__contains__("L3-PRS-02")` | is this tag here |
| `for machine in forming:` | `forming.__iter__()` | here is something to loop over |

In the class diagram from Tuesday, this is **aggregation**: `WorkCell "1" o-- "0..*" Machine`. A cell
holds zero or more machines, and a machine can exist outside any cell.

### Which collection goes inside

This part is review, not new. In 145060 Unit 5 you chose collections on purpose: a list for order, a
set for membership, a dictionary for lookup by key. A cell looks machines up by asset tag constantly,
and it must reject a duplicate tag. So the cell keeps a **dictionary keyed by asset tag**. Finding a
tag is one lookup, not a scan, and Python dictionaries keep insertion order, so the cell still lists
machines in the order they were added. Week 3, Thursday's lab measures that choice against a list.

---

## Worked example 1: the cell refuses bad members

```python
# work_cell.py, with lookup and iteration added
class Machine:
    def __init__(self, asset_tag, rated_kw):
        self.asset_tag = asset_tag
        self.rated_kw = float(rated_kw)
        self._running = False

    def start(self):
        self._running = True

    def is_running(self):
        return self._running


class WorkCell:
    """A named group of machines. The cell owns the rules for its collection."""

    def __init__(self, name):
        self.name = name
        self._machines = {}              # keyed by asset tag

    def add(self, machine):
        if not isinstance(machine, Machine):
            raise TypeError(f"a cell holds Machine objects, not {type(machine).__name__}")
        if machine.asset_tag in self._machines:
            raise ValueError(f"{machine.asset_tag} is already in cell {self.name}")
        self._machines[machine.asset_tag] = machine
        return machine

    def get(self, asset_tag):
        return self._machines.get(asset_tag)

    def machines(self):
        return tuple(self._machines.values())   # a copy: read it, cannot change the cell

    def running(self):
        return [m for m in self._machines.values() if m.is_running()]

    def total_rated_kw(self):
        return sum(m.rated_kw for m in self._machines.values())

    def __len__(self):
        return len(self._machines)

    def __contains__(self, asset_tag):
        return asset_tag in self._machines

    def __iter__(self):
        return iter(self.machines())
```

```python
from work_cell import Machine, WorkCell

forming = WorkCell("Forming")
forming.add(Machine("L3-PRS-01", 15)).start()
forming.add(Machine("L3-PRS-02", 22))
print(len(forming), "machines,", forming.total_rated_kw(), "kW")
print("L3-PRS-02" in forming, [m.asset_tag for m in forming.running()])
for bad in [Machine("L3-PRS-01", 10), "L3-PRS-03"]:
    try:
        forming.add(bad)
    except (ValueError, TypeError) as error:
        print("Refused:", error)
```

Output:

```
2 machines, 37.0 kW
True ['L3-PRS-01']
Refused: L3-PRS-01 is already in cell Forming
Refused: a cell holds Machine objects, not str
```

`add` returns the machine, so `forming.add(...).start()` adds and starts in one line. The duplicate is
refused even though it is a different object with a different rating. The tag is what makes a machine
unique on this line.

---

## Worked example 2: len, in, lookup, and a loop

```python
from work_cell import Machine, WorkCell

forming = WorkCell("Forming")
forming.add(Machine("L3-PRS-01", 15))
forming.add(Machine("L3-PRS-02", 22))
for machine in forming:
    print(machine.asset_tag, machine.rated_kw)
print(len(forming), "L3-PRS-02" in forming, "L3-OVN-01" in forming)
print(forming.get("L3-PRS-02").rated_kw, forming.get("L3-OVN-01"))
```

Output:

```
L3-PRS-01 15.0
L3-PRS-02 22.0
2 True False
22.0 None
```

The loop runs in the order the machines were added. `in` checks tags, because that is what
`__contains__` was written to check. `get` returns `None` for a tag the cell does not have, instead of
crashing, which is the same choice a dictionary's `get` makes.

---

## Worked example 3: the copy protects the cell

```python
from work_cell import Machine, WorkCell

forming = WorkCell("Forming")
forming.add(Machine("L3-PRS-01", 15))
snapshot = forming.machines()
print(type(snapshot).__name__, len(snapshot))
try:
    snapshot[0] = "Press 3"
except TypeError as error:
    print("Refused:", error)
try:
    snapshot.append("Press 3")
except AttributeError as error:
    print("Refused:", error)
snapshot[0].start()                      # the machines inside are the real ones
print(forming.get("L3-PRS-01").is_running(), len(forming))
```

Output:

```
tuple 1
Refused: 'tuple' object does not support item assignment
Refused: 'tuple' object has no attribute 'append'
True 1
```

A tuple cannot be changed, so the caller cannot add or swap members. Be precise about what the copy
protects. It protects **the collection**. The machines inside are the same objects, so
`snapshot[0].start()` really starts the press. That is fine, because `Machine` guards its own rules.
Each object guards its own level.

---

## The wrong version, and what it produces

Return the real dictionary instead of a copy. This run uses a shorter copy of the class, saved as
`leaky_cell.py`, with the same `add` type check and this one change:

```python
    def machines(self):
        return self._machines            # the deliberate mistake: the real dict
```

Then any caller can go around `add`:

```python
forming = WorkCell("Forming")
forming.add(Machine("L3-PRS-01", 15))
forming.machines()["L3-PRS-03"] = "Press 3"   # no add(), no checks
print(len(forming), "machines")
print(forming.total_rated_kw())
```

Output:

```
2 machines
Traceback (most recent call last):
  File "...\leaky_cell.py", line 31, in <module>
    print(forming.total_rated_kw())
          ~~~~~~~~~~~~~~~~~~~~~~^^
  File "...\leaky_cell.py", line 21, in total_rated_kw
    return sum(m.rated_kw for m in self._machines.values())
  File "...\leaky_cell.py", line 21, in <genexpr>
    return sum(m.rated_kw for m in self._machines.values())
               ^^^^^^^^^^
AttributeError: 'str' object has no attribute 'rated_kw'
```

Read where the error is. The bad line was the one that put a string in. The crash is in
`total_rated_kw`, a method that did nothing wrong, one call later. In a real program it could be a
thousand lines and a day later. That distance is what makes a leak expensive.

A second mistake: forgetting `__iter__` and then looping over the cell. In `no_iter.py` the class has
`__len__` and no `__iter__`:

```python
forming = WorkCell("Forming")
print(len(forming))
for machine in forming:
    print(machine)
```

```
0
Traceback (most recent call last):
  File "...\no_iter.py", line 12, in <module>
    for machine in forming:
                   ^^^^^^^
TypeError: 'WorkCell' object is not iterable
```

`len` worked in that same file, because the class had `__len__`. Python asks for each ability
separately.

---

## Why the wrong version is tempting

`return self._machines` is shorter than `return tuple(self._machines.values())`, and in your own test
it works perfectly. You only read from what it returns, so you never see the problem. The person who
writes to it is someone else, later, who did not know the rule.

The habit: a method that hands out a collection hands out a copy. If a caller needs to change the
collection, give them a method that checks, like `add` or `remove`.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Container object** | an object whose job includes holding other objects |
| **Aggregation** | a "holds" relationship where the parts can exist on their own |
| **Defensive copy** | a copy returned so the caller cannot change the original |
| **Tuple** | an ordered collection that cannot be changed after it is made |
| **`__len__`** | the method `len()` calls |
| **`__contains__`** | the method the `in` operator calls |
| **`__iter__`** | the method a `for` loop calls to get something to loop over |
| **Special method** | a method with two underscores on each side that Python calls for you |

---

## Self-check

**Question 1.** A `Playlist` class keeps songs in `self._songs`, a list, and has
`def songs(self): return self._songs`. Name one thing a caller can now do that the playlist cannot
stop, and give the one-line fix.

**Question 2.** `print("L3-PRS-01" in forming)` prints `True`, but
`print(forming.get("L3-PRS-01") in forming)` prints `False`. Why?

**Question 3.** Why does the cell keep a dictionary keyed by asset tag instead of a list of machines?
Give two reasons.

---

### Answers

**1.** The caller can append a duplicate song, or anything that is not a song, or clear the whole
list, with no check. The fix is `return tuple(self._songs)`.

**2.** `__contains__` checks whether the value is a key in `self._machines`, and the keys are tags.
The second line asks about a `Machine` object, which is not a tag, so the answer is `False`. The class
decides what `in` means.

**3.** Finding a machine by tag is one dictionary lookup instead of a scan of the whole list. A
duplicate tag is caught with one membership test. The dictionary also keeps the order machines were
added, so nothing is lost.

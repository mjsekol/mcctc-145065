# Lab U2-01: Line Hierarchy
## 145065 Object-Oriented Programming · Unit 2 · Week 4

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1 and Build 2 (Part 1),
Tuesday Build 1 and the first half of Build 2 (Part 2), Wednesday Build 1 (Part 3).
**Competencies:** 5.3.12 (create classes, objects, and methods), 5.1.4 (object-oriented compared with
procedural), 5.5.2 (programs that use reuse libraries: `abc` and `dataclasses`).

Files: `lab-u02-01-files/plant.py` (starter) and `lab-u02-01-files/selfcheck_hierarchy.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every tag, name, and badge id in this lab is invented. No hardware is used.

---

## The scenario

Line 3's equipment model was written in a hurry, one class at a time, by copying the previous class
and editing it. It runs and it prints the right report today. Last month the lockout rule changed,
and the change reached one copy and not the other, so a locked-out oven in the model keeps running.

## What you will build

A three-level class hierarchy where every shared rule lives in exactly one class, enforced by the
standard library.

---

## The hierarchy you are building

```
Equipment (abstract)              level 1: asset tag, name, kind, describe, inspect
|-- PoweredEquipment (abstract)   level 2: rating, running, lockout
|   |-- Press                     level 3: guard, tonnage
|   `-- Oven                      level 3: setpoint, maximum, temperature
`-- StorageRack                   level 2: capacity, load. No power.
```

---

## Starter code

Copy both files into a folder in your `oop-semester` repository and run them:

```
python plant.py
python selfcheck_hierarchy.py
```

The starter prints:

```
L3-PRS-01 Press 1 (press) 15 kW, running
L3-PRS-02 Press 2 (press) 22 kW, stopped
L3-OVN-01 Cure Oven (oven) 45 kW, running
L3-RCK-01 Finished Goods Rack (rack)

Problems:
  L3-PRS-02: locked out by tech-07
  L3-PRS-02: guard is open; press cannot run
  L3-OVN-01: 228 C is 28 C from setpoint 200 C
  L3-RCK-01: at 96% of capacity
```

The self-check ends with `0 of 14 self-checks passed`, and every line says `NOT YET`. **NOT YET**
means a name the check needs does not exist yet. **FAIL** means the name exists and the behavior is
wrong. Checks for Part 2 and Part 3 stay NOT YET or FAIL until you reach those parts. That is
expected.

Read all of `plant.py` before you change anything. `Press`, `Oven`, and `StorageRack` are three
separate classes. Count the lines that appear in more than one of them.

---

## Part 1 · Monday · Move the shared parts up

### Step 1. Run the starter and the self-check, and commit

**Observable result:** the output above, and `0 of 14 self-checks passed`. Commit the two files with
a message that says what they are.

### Step 2. Find the copy that drifted

`Press.lock_out()` and `Oven.lock_out()` were supposed to be identical. Compare them line by line.
Then prove what the difference does:

```
python -c "import plant; oven = plant.Oven('L3-OVN-01', 'Cure Oven', 45, 200, 240); oven.start(); oven.lock_out('tech-12'); print('locked out by', oven._lockout_holder, '| running:', oven.is_running)"
```

**Observable result:** `locked out by tech-12 | running: True`. In your lab README, under
`## The copy that drifted`, write which line is missing, and one sentence about what that means for a
technician.

### Step 3. Write `Equipment`, and make the rack inherit from it

Above `Press`, write `class Equipment:` with a class attribute `kind = "equipment"`, an `__init__`
that takes `asset_tag` and `name` and holds the tag and name checks, and the `asset_tag` and `name`
properties. Then change `class StorageRack:` to `class StorageRack(Equipment):`, replace its tag and
name checks with `super().__init__(asset_tag, name)`, and delete its own `asset_tag` and `name`
properties.

**Observable result:** `python plant.py` prints exactly what it printed in step 1. The self-check
shows `1 of 14`, with a mix of FAIL and NOT YET. That is expected: most checks need
`PoweredEquipment`, which step 4 writes.

### Step 4. Write `PoweredEquipment(Equipment)`

Between `Equipment` and `Press`, write `class PoweredEquipment(Equipment):` with `kind = "powered"`.
Its `__init__` takes `asset_tag, name, rated_kw`, calls `super().__init__(asset_tag, name)`, checks
the rating, and sets `_running` and `_lockout_holder`. Move these into it from `Press`, unchanged:
the `rated_kw`, `is_running`, `is_locked_out`, and `locked_out_by` properties (write `rated_kw` and
`locked_out_by` if the copy you started from lacks them), and the `stop()`, `lock_out()`, and
`release_lockout()` methods. Give it a `start()` that refuses a locked-out machine and sets
`_running`.

**Observable result:** `python plant.py` still prints the step 1 output. Nothing uses the new class
yet.

### Step 5. Make `Press` and `Oven` inherit, and delete every copy

Change both class lines to inherit from `PoweredEquipment`. In each `__init__`, replace the tag,
name, and rating code with `super().__init__(asset_tag, name, rated_kw)`. Delete every property and
method that `PoweredEquipment` or `Equipment` now provides. `Press` keeps its own `start()` for now,
with both of its checks. `Oven` needs no `start()` of its own at all.

**Observable result:** `python plant.py` prints the step 1 output. Run step 2's command again. It
now prints `locked out by tech-12 | running: False`.

### Step 6. Run the self-check, and explain the fix nobody wrote

**Observable result:** `7 of 14 self-checks passed`, and every Part 1 line says PASS. In your README,
under the step 2 heading, add one sentence: which step fixed the oven, and why nobody had to write a
fix for it. Commit.

---

## Part 2 · Tuesday · Extend, do not copy

### Step 7. Rewrite `Press.start()` to extend the parent

`Press.start()` should check the guard, then call `super().start()`. Delete its lockout check: the
parent already has one.

**Observable result:** a locked-out press with its guard closed still refuses to start, with the
parent's message, `L3-PRS-01 is locked out by tech-07`.

### Step 8. Make `open_guard()` call `self.stop()`

Replace the line that sets `_running` with `self.stop()`.

**Observable result:** `python plant.py` prints the step 1 output.

### Step 9. Build `describe()` once per level

Give `Equipment` a `describe()` that returns the tag, the name, and `(kind)` in the step 1 format.
Give `PoweredEquipment` a `describe()` that starts with `super().describe()` and adds the rating and
`running` or `stopped`. Delete `describe()` from `Press`, `Oven`, and `StorageRack`.

**Observable result:** `python plant.py` prints the step 1 output. `self.kind` gives each class its
own word, because Python finds `kind` on the object's own class first.

### Step 10. Run the self-check

**Observable result:** `10 of 14 self-checks passed`. All Part 1 and Part 2 lines say PASS.

### Step 11. Break a promise on purpose, and write down what happened

Add this method to `Press`, anywhere in the class:

```python
    def stop(self):
        pass
```

Then run:

```
python -c "import plant; p = plant.Press('L3-PRS-01', 'Press 1', 15, 60); p.close_guard(); p.start(); p.open_guard(); print('guard closed:', p.guard_closed, '| running:', p.is_running); p.lock_out('tech-07'); print('locked out by:', p.locked_out_by, '| running:', p.is_running)"
```

**Observable result:** no error at all, and these two lines:

```
guard closed: False | running: True
locked out by: tech-07 | running: True
```

The self-check drops to `8 of 14`. Copy the two lines into your README under
`## The override that broke a promise`, and write two sentences: what a technician would believe, and
what was true. Then delete the `stop()` you added and confirm `10 of 14` again. Commit.

---

## Part 3 · Wednesday · Let the standard library enforce it

### Step 12. Write `Finding` as a frozen dataclass

At the top of the file, add `from dataclasses import dataclass` and
`SEVERITIES = ("info", "warning", "stop")`. Write:

```python
@dataclass(frozen=True)
class Finding:
    asset_tag: str
    severity: str
    message: str
```

Add `__post_init__` to refuse a severity that is not in `SEVERITIES` with `ValueError`, and
`__str__` to return text like `[STOP] L3-PRS-02: guard is open; press cannot run`.

**Observable result:** the self-check's `Finding is a frozen dataclass` line says PASS.

### Step 13. Make `Equipment` an abstract base class with a template method

Add `from abc import ABC, abstractmethod`. Change the class line to `class Equipment(ABC):`. Add:

- `inspect()`, which returns `self.common_findings() + self._kind_findings()`
- `common_findings()`, which returns an empty list
- `_kind_findings()`, marked `@abstractmethod`, with only a docstring

**Observable result:** `python plant.py` now fails with a `TypeError` about an abstract method. That
is correct: no class has written `_kind_findings()` yet.

### Step 14. Move the findings into the classes that own them

- Give `PoweredEquipment` a `common_findings()` that starts from `super().common_findings()` and adds
  an `info` finding `locked out by <badge>` when the machine is locked out.
- Rename `problems()` in `Press`, `Oven`, and `StorageRack` to `_kind_findings()`. Each returns a
  list of `Finding` objects instead of strings, and none of them reports the lockout any more.
  Severities: an open guard and an overload are `stop`; a temperature above the maximum is `stop`; a
  drift from setpoint and a rack at 90 percent are `warning`; an oven with no reading is `info`.

### Step 15. Update `main()` and run everything

In `main()`, print `Findings:` and loop over `item.inspect()` instead of `item.problems()`.

**Observable result:** `python plant.py` prints the four `describe()` lines, then:

```
Findings:
  [INFO] L3-PRS-02: locked out by tech-07
  [STOP] L3-PRS-02: guard is open; press cannot run
  [WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C
  [WARNING] L3-RCK-01: at 96% of capacity
```

and `python selfcheck_hierarchy.py` prints `14 of 14 self-checks passed`.

### Step 16. Break it on purpose

Rename `Oven._kind_findings` back to `problems`. Run `python plant.py`.

**Observable result:** the program refuses to start:

```
TypeError: Can't instantiate abstract class Oven without an implementation for abstract method '_kind_findings'
```

Write one sentence in your README under `## What abc caught`: what would the oven's inspection have
returned without `abc`? Restore the name, confirm 14 of 14, and commit.

---

## Acceptance criteria, full lab

- [ ] `python selfcheck_hierarchy.py` prints `14 of 14 self-checks passed`
- [ ] `python plant.py` prints the four description lines and the four findings in step 15
- [ ] No method or property is written in more than one class
- [ ] `StorageRack` has no `start()`
- [ ] Every child `__init__` calls `super().__init__(...)`
- [ ] The README has the step 2, step 11, and step 16 sections
- [ ] Committed at the end of Monday, Tuesday, and Wednesday

---

## If it breaks

### 1. A child that skipped the parent's setup

```
AttributeError: 'Press' object has no attribute '_lockout_holder'
```

**Cause:** `Press.__init__` never called `super().__init__(...)`, so the parent's attributes were
never created. The error appears later, in whatever method first reads one of them. Put
`super().__init__(asset_tag, name, rated_kw)` first in the child's `__init__`.

### 2. The wrong arguments to the parent

```
TypeError: PoweredEquipment.__init__() missing 1 required positional argument: 'rated_kw'
```

**Cause:** `Press` called `super().__init__(asset_tag, name)`, the grandparent's arguments. Pass
exactly what the direct parent's `__init__` asks for.

### 3. `super` without its parentheses

```
TypeError: descriptor '__init__' requires a 'super' object but received a 'str'
```

**Cause:** `super.__init__(...)` instead of `super().__init__(...)`. `super` is called like a
function first.

### 4. A child written above its parent

```
NameError: name 'PoweredEquipment' is not defined
```

**Cause:** Python runs the file top to bottom. A class line can only name a parent that already
exists. Move the parent above every class that inherits from it.

### 5. A concrete class with an abstract method left unwritten

```
TypeError: Can't instantiate abstract class Press without an implementation for abstract method '_kind_findings'
```

**Cause:** that class has no `_kind_findings()`, often because it is still called `problems()`. Step
13 shows this on purpose. Finish step 14.

### 6. Changing a frozen record

```
dataclasses.FrozenInstanceError: cannot assign to field 'severity'
```

**Cause:** code tried to change a `Finding` after creating it. Create a new `Finding` instead.

### Not an error, and the one that matters most: an override that drops the parent

A `Press.start()` that never calls `super().start()` starts a locked-out press, and a `stop()` that
does nothing leaves a press running with its guard open. Nothing prints an error. The self-check
catches both. The shop floor would not.

**Error wording was captured on Python 3.13.7.** Confirm it on the lab's Python 3.14.

---

## Stretch goal

Add a `Welder(PoweredEquipment)` with an `arc_on` attribute. Its `start()` extends the parent and
turns the arc on. Its `stop()` turns the arc off and then calls `super().stop()`. Its
`_kind_findings()` returns a `warning` when the arc is on and the welder is not running. Lock a
running welder out and prove both the arc and the machine stopped. Write down which parent methods you
did not have to touch.

---

## Submission checklist

- [ ] Self-check 14 of 14
- [ ] README sections: the copy that drifted, the override that broke a promise, what abc caught
- [ ] Temporary break code from steps 11 and 16 removed
- [ ] Committed and pushed at the end of each day
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.3.12, 5.1.4, 5.5.2) and grade on the same
100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 20 of Monday Build 1, step 3 is not done, or the student is editing `selfcheck_hierarchy.py` | SCAFFOLDED |
| Steady progress, and questions about which lines to delete | STANDARD |
| 7 of 14 before Monday Build 2 is half over | EXTENDED |
| The student asks what equipment classes have to do with anything they will build | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out a different `plant.py`, in which `Equipment` and
  `PoweredEquipment` are already written above `Press` and nothing uses them yet. Part 2 and Part 3
  locations are marked with comments.
- **Steps:** skip steps 3 and 4. Step 5 becomes "make all three classes inherit from the right parent
  and delete what the parents already do."
- **Checkpoints:** show the self-check to the instructor after step 5, step 10, and step 15.
- **Keep steps 2, 11, and 16.** The breaks are the lesson.

**Acceptance criteria:** 14 of 14, the three README sections.

**Grading:** same 100-point scale. Full completion earns the same grade as full completion of
STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one problem the lab has not taught.

**Added requirement.** A subclass that forgets to set its own `kind` inherits its parent's and
labels itself wrongly in every report. Make Python refuse such a class **when the class statement
runs**, before any object exists. `PoweredEquipment` and every concrete class must still work.

**Hint, not the answer.** Python calls a special class method on a parent each time a subclass is
created. Read the entry for `object.__init_subclass__` in the Python language reference's data model
chapter, `https://docs.python.org/3/reference/datamodel.html`. `vars(cls)` shows only the names a
class defines itself.

**Acceptance criteria:** all STANDARD criteria; `class Grinder(PoweredEquipment): ...` with no `kind`
raises `TypeError` at the class line; a decision log entry names the rejected alternative (for
example, an abstract property).

**Grading:** same scale.

---

## APPLIED

**For the student who asks when they would use this.** The same skill in a game.

**Changed scenario.** A game's inventory has swords, shields, and potions. They were written by
copying, and a durability rule reached the sword and not the shield. Write `Item` (name, weight,
abstract `describe_effect()`), `Equipable(Item)` (durability, `equip()`, `unequip()`, a `break_()`
that unequips), `Weapon(Equipable)` and `Armor(Equipable)`, and `Consumable(Item)` at level 2, which
cannot be equipped. Invent every name and number. No real game's content.

**What you build.** The hierarchy, a frozen `ItemReport` dataclass, and an `inspect()` template
method. Write a self-check of at least eight checks modeled on `selfcheck_hierarchy.py`, including
"a consumable has no `equip()`" and "breaking an item always unequips it."

**Acceptance criteria:** your self-check passes; your README has a "copy that drifted" section for your
own starter and an "override that broke a promise" section.

**Grading:** same scale. Requirements Fit is judged on whether each "is a" passes the sentence test.

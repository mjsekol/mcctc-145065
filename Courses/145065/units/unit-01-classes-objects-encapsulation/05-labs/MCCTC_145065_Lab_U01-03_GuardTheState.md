# Lab U01-03: Guard the State
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Monday and Tuesday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Part 1 on Monday, Build 1 and the
first 20 minutes of Build 2. Part 2 on Tuesday, Build 1.
**Competencies:** 5.3.12 (write code to create classes, objects, and methods: encapsulation,
properties, instance, static, and class methods), 5.5.1 (data validation), 5.5.7 (read inputs: a
spreadsheet row), 5.5.5 (naming conventions and comments), 5.4.2 (write and edit code in the IDE).

Files: `lab-u01-03-files/oven.py` (your starter), `lab-u01-03-files/rogue_script.py`, and
`lab-u01-03-files/selfcheck_oven.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag, badge,
and temperature here is invented. No hardware is used.

---

## The scenario

Line 3's cure oven is modeled by a class whose attributes are all public. It behaves as long as every
program calls its methods, but a maintenance script last week set the setpoint to 900 C on an oven
rated for 240 C, and another turned the heat on with the door open, and the class never saw either
one. The shop also keeps its ovens in a spreadsheet, and someone has to turn those rows of text into
oven objects without skipping the rules.

## What you will build

An oven that controls every change to its own state through properties and methods, a written proof
of what Python's underscores do not stop, and a class method that builds an oven from a spreadsheet
row.

---

## Say it before you start

**Python has no real `private`.** A single leading underscore is a convention: a sign to other
programmers. Two leading underscores make Python rename the attribute, which is called name mangling.
It makes accidental access harder. It does not make access impossible. **Nothing enforces either one
until Unit 6**, where C# turns `private` into a compiler error. In this lab you guard every public way
in, and then you prove, in writing, the ways that remain.

---

## Starter code

Copy the three files into `unit-01-labs/lab-u01-03/` in your `oop-semester` repository.

```
python oven.py
python rogue_script.py
python selfcheck_oven.py part1
```

`oven.py` prints a heating line, a door-open line, and the oven's `repr`.

---

## Part 1: Monday, steps 1 through 11

### Step 1. Watch the rogue lines get in

Run `python rogue_script.py`.

**Observable result:**

```
1. set the setpoint to 900 C on a 240 C oven: ACCEPTED
2. turn the heat on while the door is open: ACCEPTED
3. type a word where a reading goes: ACCEPTED
4. repaint the asset tag: ACCEPTED

status_text() crashed: ValueError: Unknown format code 'f' for object of type 'str'
4 of 4 rogue lines were accepted
```

In your lab README, under `## What public attributes allowed`, write one sentence for each accepted
line: what a person on the floor would see or suffer. Then one sentence on the crash: which line
caused it, and which line reported it.

### Step 2. The starting score

```
python selfcheck_oven.py part1
```

**Observable result:** `2 of 9 self-checks passed`. Commit.

### Step 3. Underscore the state, and make it readable but not writable

Rename every attribute `__init__` creates so it starts with an underscore, **except** the badge, which
gets two underscores: `self.__last_opened_by`. Update every method to use the new names. Leave
`setpoint_c` alone for now.

Then add a read-only property for each of `asset_tag`, `name`, `max_c`, `temperature_c`, `heating`,
`door_open`, and `last_opened_by`: a `@property` getter that returns the internal value, and no
setter.

**Observable result:** `rogue_script.py` reports `1 of 4 rogue lines were accepted`, and each refusal
reads like `property 'heating' of 'Oven' object has no setter`. `part1` reports `3 of 9`.

### Step 4. A property that checks

Make `setpoint_c` a property with a getter and a setter. The setter raises `TypeError` unless the
value is an `int` or `float` and not a `bool`, then raises `ValueError` unless the value is finite
(`math.isfinite`) and above 0 and at most this oven's `max_c`. Then it stores `float(value)` in
`self._setpoint_c`.

**The setter must store into `self._setpoint_c`, with the underscore.** Read the first "If it breaks"
entry before you run it.

**Observable result:** `0 of 4 rogue lines were accepted`. P1-3 passes.

### Step 5. A new oven gets the same checks

In `__init__`, before storing anything, refuse a blank or non-string tag or name (`ValueError`) and a
bad `max_c` (the same `TypeError` and `ValueError` checks, with `MAX_OVEN_C` as the limit). Store
`self._max_c` **before** the setpoint. Then write `self.setpoint_c = setpoint_c`, **with no
underscore**, so the setter runs.

**Observable result:** P1-1 and P1-4 pass.

### Step 6. A reading the sensor could produce

`record_temperature(celsius)` raises `TypeError` for a non-number or a `bool`, and `ValueError` for a
value that is not finite or is outside `MIN_READING_C` to `MAX_READING_C`. A refused reading leaves
the last good one in place.

**Observable result:** P1-5 passes.

### Step 7. A badge before the door opens

`open_door(badge)` raises `ValueError` for a blank or non-string badge **before it changes anything**,
then stops the heat, opens the door, and records the trimmed badge.

**Observable result:** P1-6 passes.

### Step 8. Nothing public left

`status_text()` and `__repr__` read the internal names. Every attribute in `vars(oven)` starts with an
underscore, and the badge shows up as `_Oven__last_opened_by`.

**Observable result:** `9 of 9 self-checks passed` on `part1`. Commit.

### Step 9. Prove what the underscores do not stop

Create `prove_bypass.py`. Build an oven, open its door as `tech-07`, and then:

1. Turn the heat on by writing the single-underscore attribute directly. Print `door_open` and
   `heating`.
2. Try to print `oven.__last_opened_by` inside a `try`, and print the error.
3. Write the badge through its mangled name, `_Oven__last_opened_by`, and print `last_opened_by` and
   `status_text()`.

**Observable result:** four lines that show the door open with the heat on, the `AttributeError`, and
the badge changed to whatever you wrote.

### Step 10. Say it in writing

In your README, under `## What the underscore does not stop`, write three sentences: what the single
underscore did not stop, what name mangling did not stop, and what does stop both. The third
sentence names Unit 6.

**Observable result:** three sentences, and none of them claims the attributes are private.

### Step 11. Commit

**Observable result:** `prove_bypass.py` and the README are pushed.

---

## Part 2: Tuesday, steps 12 through 16

### Step 12. A static method for the tag rule

Add a module-level pattern: `re.compile(r"L3-[A-Z]{3}-[0-9]{2}")`. Add
`@staticmethod is_valid_asset_tag(tag)` that returns `True` only when `tag` is a string that fully
matches it. **It needs no oven and no class data**, which is why it is static.

```
python selfcheck_oven.py part2
```

**Observable result:** P2-1 passes.

### Step 13. The constructor uses it

Replace the non-blank tag check in `__init__` with `Oven.is_valid_asset_tag(asset_tag)`.

**Observable result:** P2-2 passes.

### Step 14. A class method for a class-wide count

Add a class attribute, `_ovens_created = 0`, in the class body. At the **end** of `__init__`, after
every check has passed, write `Oven._ovens_created += 1`. Add `@classmethod ovens_created(cls)` that
returns `cls._ovens_created`.

**Observable result:** P2-3 passes.

### Step 15. A class method that builds an oven from a spreadsheet row

The equipment spreadsheet gives you rows like this, every value as text:

```python
{"asset_tag": " l3-ovn-02 ", "name": " Paint Oven ", "setpoint_c": "180", "max_c": "220.0"}
```

Add `@classmethod from_record(cls, record)`. It raises `ValueError` naming any missing key, trims and
upper-cases the tag, converts both numbers with `float()`, and returns `cls(...)`. **It calls the
constructor, so every rule still runs.** It never builds an oven any other way.

**Observable result:** `13 of 13 self-checks passed`.

### Step 16. Show it

In `oven.py`'s `if __name__ == "__main__":` block, build the paint oven from the row above and print
its `repr` and `Oven.ovens_created()`. Commit and push.

**Observable result:**

```
Oven(asset_tag='L3-OVN-02', name='Paint Oven', setpoint_c=180.0, max_c=220.0)
Ovens built: 2
```

### Acceptance criteria, full lab

- [ ] `python selfcheck_oven.py` prints `13 of 13 self-checks passed`
- [ ] `python rogue_script.py` prints `0 of 4 rogue lines were accepted`
- [ ] `__init__` assigns `self.setpoint_c`, so construction runs the setter
- [ ] `prove_bypass.py` runs and shows both bypasses
- [ ] The README has `What public attributes allowed` and `What the underscore does not stop`, and it
      never calls an attribute private
- [ ] `is_valid_asset_tag` is static; `ovens_created` and `from_record` are class methods
- [ ] Committed and pushed at the end of Monday and Tuesday

---

## If it breaks

### 1. A setter that calls itself

```
RecursionError: maximum recursion depth exceeded
```

**Cause:** the setter says `self.setpoint_c = value`. That assignment runs the setter again, which
runs it again. Store into `self._setpoint_c`.

### 2. The setter reads a limit that does not exist yet

```
AttributeError: 'Oven' object has no attribute '_max_c'. Did you mean: 'max_c'?
```

**Cause:** `__init__` assigns `self.setpoint_c` before `self._max_c`. The setter compares against
`self._max_c`, so store it first. Order matters in a constructor.

### 3. A property with no setter, used as if it had one

```
AttributeError: property 'setpoint_c' of 'Oven' object has no setter
```

**Cause:** the getter exists but the `@setpoint_c.setter` method is missing or misspelled. The
decorator must use the property's own name.

### 4. The quiet one: construction skips the check

No error. `Oven("L3-OVN-01", "Cure Oven", 900.0, 240.0)` builds an oven with a 900 C setpoint, and
P1-4 fails with `a new oven with setpoint 300 and max 240 was accepted, expected ValueError`.

**Cause:** `__init__` writes `self._setpoint_c = setpoint_c`, which skips the setter. Nothing crashes,
which is why this is the bug that ships.

### 5. A count that never moves

P2-3 fails with `two good ovens and one refused oven changed the count by 0; expected 2`.

**Cause:** `self._ovens_created += 1` reads the class value and writes a new attribute on this one
oven. Write through the class: `Oven._ovens_created += 1`. Wednesday's lesson is about exactly this.

---

## Stretch goal

Add `@classmethod from_csv(cls, path)` that reads a CSV file with `csv.DictReader` and returns two
lists: the ovens built, and the rows refused, each with its line number and the error message. Make a
four-row test file with one bad tag and one setpoint above its maximum.

---

## Submission checklist

- [ ] Self-check 13 of 13 and rogue script 0 of 4
- [ ] `prove_bypass.py` committed
- [ ] Both README sections, honest
- [ ] AI usage log updated if you used a model
- [ ] Committed and pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Twenty minutes into Monday's Build 1, the student is still on step 3, or has hit the `RecursionError` twice | SCAFFOLDED |
| Steady progress; questions about which exception to raise | STANDARD |
| `9 of 9` on `part1` before Monday's Build 1 ends | EXTENDED |
| The student says an oven class has nothing to do with the apps they want to build | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the student receives the seven read-only properties already written, and the
  `setpoint_c` getter. They write the setter, the constructor checks, and the rest.
- **Steps:** step 6 checks only the range, not the type.
- **Checkpoints:** show the instructor `rogue_script.py` after step 4 and `part1` after step 8.
- **Keep steps 9 and 10.** The honest proof is the lesson.

**Acceptance criteria:** 12 of 13 (P1-5 may fail on its type checks); rogue script 0 of 4; both
README sections.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a concept the lab has not taught.

**Added requirement.** The shop's software keeps sets of ovens, and two `Oven` objects with the same
asset tag are the same physical oven. Make `Oven("L3-OVN-01", ...) == Oven("L3-OVN-01", ...)` true
even when the two objects were built separately, and make `len({oven_a, oven_b})` equal 1 for two ovens
with one tag. Two ovens with different tags are never equal. Comparing an oven with a string is not an
error.

**Hint, not the answer.** Two special methods control equality and set membership, and Python has a
rule about defining one without the other. Read the entries for `object.__eq__` and `object.__hash__`
in the data model reference, `https://docs.python.org/3/reference/datamodel.html`. Ask what the hash
should be built from, and why it must be something that never changes.

**Acceptance criteria:** all STANDARD criteria; the two equality facts above; the README explains why
the hash uses the tag and not the setpoint.

**Grading:** same scale.

---

## APPLIED

**For the student who wants to build apps, not ovens.** The same guarding, somewhere else.

**Changed scenario.** A phone app keeps a `WorkoutGoal`: a name, a weekly target in minutes (1 to
2400), minutes logged so far this week, and a streak count. A "sync" bug in another part of the app
keeps writing text into the minutes and resetting the streak. Build `WorkoutGoal` with read-only
properties for everything except the target, a validated `target_minutes` setter, a `log(minutes)`
method, a `@staticmethod is_valid_name(text)`, a class-level count of goals created, and
`from_record(record)` for goals saved as text. Invent every value; no personal information.

**What you build.** The class, a rogue script of your own with four lines that must all be refused, a
bypass proof, and a self-check of at least twelve checks.

**Acceptance criteria:** your rogue script shows 0 of 4 accepted; your self-check passes; the README
has both sections for your domain.

**Grading:** same scale. Requirements Fit is judged on whether every change to state runs a rule.

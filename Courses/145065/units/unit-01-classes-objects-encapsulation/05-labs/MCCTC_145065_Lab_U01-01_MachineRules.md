# Lab U01-01: Machine Rules
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Monday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1 and Build 2.
**Competencies:** 5.3.12 (write code to create classes, objects, and methods), 5.1.4 (procedural
and object-oriented programming, compared), 5.1.5 (data management through a programming language),
5.5.1 (data validation), 5.5.5 (naming conventions and comments), 5.4.2 (write and edit code in the
IDE).

Files: `lab-u01-01-files/press_tracker.py` (the program as it runs today),
`lab-u01-01-files/machine.py` (your starter), `lab-u01-01-files/shift_with_objects.py` (Part 2
starter), and `lab-u01-01-files/selfcheck_machine.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every tag, badge, and number in this lab is invented. No hardware is used.

---

## The scenario

Line 3 tracks its two presses with a program written last year: each press is a dictionary, and the
safety rules live in loose functions. The lockout rule is supposed to keep a press stopped while a
technician's hands are inside it, but nothing forces anyone to call the function that checks it.
Last week the end-of-shift report showed a locked-out press as running, and nobody could say which
line of code did it.

## What you will build

A `Machine` class that refuses to be built invalid and changes its own state only through methods
that enforce the shop's rules.

---

## Before you start

You wrote classes in 145060 Unit 7. This lab asks for more than a class that holds data. A `Machine`
that exists must be a valid `Machine`, and nothing outside the class should change its running state
or its lockout.

**The rule for this week.** A name that starts with an underscore, such as `self._running`, is
internal. Code outside the class never reads or writes it. Outside code asks through a method, such
as `is_running()`. Week 3, Monday explains exactly what Python does and does not enforce about this.

**Refuse by raising, never by printing.** The procedural functions printed their refusals. A class
that prints cannot be used by a test, a web page, or an operator panel. Your methods raise, and the
code that calls them decides what a person sees.

| When | Raise |
|---|---|
| an argument is the wrong type, such as `"15"` for a rating | `TypeError` |
| an argument is the right type with a bad value, such as `-5` | `ValueError` |
| the call is not allowed right now, such as starting a locked-out press | `RuntimeError` |

---

## Starter code

Copy the four files into `unit-01-labs/lab-u01-01/` in your `oop-semester` repository.

```
python press_tracker.py
python machine.py
python selfcheck_machine.py
```

`machine.py` runs and prints something like `<__main__.Machine object at 0x...>` and
`running: False`. Every method in it is a stub. The self-check prints 16 FAIL lines and ends:

```
Part 1: 0 of 7    Part 2: 0 of 9
0 of 16 self-checks passed
```

---

## Part 1: Build 1, steps 1 through 6

### Step 1. Read the report you cannot trust

Run `python press_tracker.py`. The end of the shift prints:

```
End of the shift
  L3-PRS-01 Press 1: RUNNING, -15 kW, 45 min run
  L3-PRS-02 Press 2: RUNNING, LOCKED OUT (tech-07), 22 kW, 0 min run
```

Read the last block of `main()`. In your lab README, under `## What the dictionaries allowed`, list
the three things wrong with this report and the line that caused each. One of the three does not
show up in the report at all. Find it anyway.

**Observable result:** three bullets, each naming a line.

### Step 2. Run the starter and commit

**Observable result:** `0 of 16 self-checks passed`. Commit the four files as they are.

### Step 3. Refuse a bad tag or name

In `__init__`, before storing anything, raise `ValueError` if `asset_tag` or `name` is not a string
or is blank after `.strip()`. Store both trimmed.

**Observable result:** checks 02 and 03 pass.

### Step 4. Refuse a bad rating, and store it as a float

Raise `TypeError` if `rated_kw` is not an `int` or `float`. **`True` is an `int` in Python**, so
refuse `bool` first, by name. Then raise `ValueError` unless the rating is finite and above 0 and at
most `MAX_RATED_KW`. `math.isfinite` refuses NaN and infinity. Store `float(rated_kw)`.

**Observable result:** checks 01, 04, and 05 pass.

### Step 5. Start and stop

`start()` sets `self._running` to `True`. `stop()` sets it to `False`. `is_running()` returns it. The
lockout check in `start()` comes in Part 2.

**Observable result:** check 06 passes.

### Step 6. A `__repr__` that looks like the call that built it

`repr(Machine("L3-PRS-01", "Press 1", 15))` must be exactly
`Machine(asset_tag='L3-PRS-01', name='Press 1', rated_kw=15.0)`. The `!r` format in an f-string adds
the quotes.

**Observable result:** `Part 1: 7 of 7    Part 2: 0 of 9`. Commit.

---

## Part 2: Build 2, steps 7 through 15

### Step 7. Lock out

`lock_out(badge)` raises `ValueError` for a blank or non-string badge. Otherwise it stops the machine
and records the trimmed badge in `self._locked_by`. `is_locked_out()` and `locked_out_by()` report it.

**Observable result:** check 08 passes.

### Step 8. A locked-out machine refuses to start

`start()` raises `RuntimeError` when `self._locked_by` is not `None`. The message names the tag and
the badge.

**Observable result:** check 09 passes.

### Step 9. Only the holder releases

`release_lockout(badge)` raises `RuntimeError` if nobody holds a lock, and `RuntimeError` if the badge
is not the holder's. Otherwise it clears the lock.

**Observable result:** check 10 passes.

### Step 10. Nobody takes over a lock

If a different badge calls `lock_out` while a lock is held, raise `RuntimeError` and change nothing.
The same badge locking again is harmless.

**Observable result:** checks 11 and 12 pass.

### Step 11. Run time

`record_run(minutes)` raises `RuntimeError` unless the machine is running, and `ValueError` unless
`minutes` is a positive whole number (not a `bool`, not a float, not text). Otherwise it adds to
`self._run_minutes`. `run_minutes()` returns the total.

**Observable result:** checks 13 and 14 pass.

### Step 12. The status line a person reads

`status_text()` returns exactly one of these shapes:

```
L3-PRS-01 Press 1: STOPPED, 0 min run
L3-PRS-01 Press 1: RUNNING, 45 min run
L3-PRS-01 Press 1: LOCKED OUT (tech-07), 45 min run
```

Check the lockout first. It is the state a person most needs to see.

**Observable result:** `16 of 16 self-checks passed`. Commit.

### Step 13. The same shift, with objects

Open `shift_with_objects.py`. Build the two presses as `Machine` objects and replay the first five
events from `press_tracker.py`. Each refusal is an exception now. Catch it and print
`  refused: ` followed by the message.

**Observable result:**

```
First half of the shift
  refused: L3-PRS-02 is locked out by tech-07 and cannot start
  refused: only tech-07 can release the lockout on L3-PRS-02
End of the shift
  L3-PRS-01 Press 1: RUNNING, 45 min run
  L3-PRS-02 Press 2: LOCKED OUT (tech-07), 0 min run
```

Your messages may be worded differently. The two refusals and the two status lines must mean the same
thing.

### Step 14. The three later lines, with objects

Add the three lines that three different people added to the old program, written the only ways your
class allows: the "quick fix" that makes Press 2 run, the setup script that sets Press 1 to -15 kW,
and the typo that sets `runing` to `False`. Run the file again, then print `press1.rated_kw`.

**Observable result:** one of the three is refused. Two are not: `press1.rated_kw` prints `-15`, and
the typo line raises nothing.

In your README, under `## What the class stopped and what it did not`, write one sentence for each
of the three lines. **Be honest.** The class stopped the rule bypass that went through its state. It
did not stop a bad value written straight into a plain attribute, and it did not stop a typo. Week 3,
Monday fixes the second one.

### Step 15. Commit and push

**Observable result:** `git status` shows nothing uncommitted. The README has both sections.

### Acceptance criteria, full lab

- [ ] `python selfcheck_machine.py` prints `16 of 16 self-checks passed`
- [ ] Every refusal raises the exception type in the table above
- [ ] No method prints anything. Only `shift_with_objects.py` prints.
- [ ] Code outside `Machine` never reads or writes an underscore name
- [ ] `shift_with_objects.py` prints the two refusals and the two status lines
- [ ] The README has `What the dictionaries allowed` and `What the class stopped and what it did not`
- [ ] Committed and pushed

---

## If it breaks

### 1. A method with no `self`

```
TypeError: Machine.start() takes 0 positional arguments but 1 was given
```

**Cause:** `def start():` has no parameter, but `press.start()` passes the object as the first
argument. Every instance method's first parameter is `self`.

### 2. A value that disappears

Check 06 fails with `after start(), is_running() should be True`, and there is no error message.

**Cause:** `_running = True` without `self.` makes a local variable inside `start()` that vanishes when
the method returns. The object never changed. This is the most common bug in the lab, because nothing
crashes.

### 3. A name spelled two ways

```
AttributeError: 'Machine' object has no attribute '_locked_by'. Did you mean: '_locked'?
```

**Cause:** `__init__` stores `self._locked` and a method reads `self._locked_by`. Pick one name and use
it everywhere. Python's suggestion at the end is often right.

### 4. `True` accepted as a rating

Check 04 fails with `rated_kw True was accepted, expected TypeError`.

**Cause:** `isinstance(True, int)` is `True` in Python. Refuse `bool` by name before the number check.
If you compared the range before checking the type, `Machine("L3-PRS-01", "Press 1", "15")` also
raises `TypeError: '<' not supported between instances of 'int' and 'str'`. That is the right
exception by accident. Check the type on purpose.

### 5. A method printed instead of used

`running: <bound method Machine.is_running of Machine(asset_tag='L3-PRS-01', name='Press 1', rated_kw=15.0)>`

**Cause:** `press.is_running` without parentheses is the method itself, not its answer. Write
`press.is_running()`.

---

## Stretch goal

Add `rename(new_name)`, which refuses a blank name and records the old name in a list of previous
names that `name_history()` returns. What should `name_history()` return so that a caller cannot
change the history? Write the answer and your reason in the README.

---

## Submission checklist

- [ ] Self-check 16 of 16
- [ ] Both README sections written, honestly
- [ ] `shift_with_objects.py` runs
- [ ] AI usage log updated if you used a model
- [ ] Committed and pushed by the end of Monday's block

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At the 20-minute mark of Build 1, the student is still on step 3, or is passing a dictionary into the class's methods | SCAFFOLDED |
| Steady progress, questions about which exception to raise | STANDARD |
| `Part 1: 7 of 7` before Build 1 ends | EXTENDED |
| The student says a factory press has nothing to do with anything they will build | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the student receives `__init__` with the tag and name checks already written, and
  a comment above each remaining check naming the exception to raise.
- **Steps:** step 10 (no takeover) and step 11's value checks move to the stretch goal.
- **Checkpoints:** show the self-check to the instructor after step 6 and after step 9.
- **Keep step 14.** Seeing what the class did not stop is the lesson.

**Acceptance criteria:** checks 01 through 10, 13, 15, and 16 pass; step 13 and step 14 are done.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a concept the lab has not taught.

**Added requirement.** Make the typo line from step 14 fail. After your change,
`press1.runing = False` must raise `AttributeError`, while every self-check still passes.

**Hint, not the answer.** Python classes can declare the exact set of attribute names an object is
allowed to have. Read the section on `__slots__` in the data model reference,
`https://docs.python.org/3/reference/datamodel.html`. Then ask what happens to `press1.rated_kw = -15`.

**Acceptance criteria:** all STANDARD criteria; the typo raises `AttributeError`; the README explains
in two sentences what `__slots__` stops and what it still does not stop.

**Grading:** same scale.

---

## APPLIED

**For the student who will never work in a factory.** The same rules, somewhere else.

**Changed scenario.** A gaming center rents consoles by the hour. A console can be reserved by one
member badge at a time (invent the badge IDs, no real names), only the member who reserved it can
release it, play time accumulates only while a session is running, and a console flagged for repair
refuses to start. Build `Console` with the same shape: validated construction, `start`, `stop`,
`flag_for_repair(badge)`, `clear_repair(badge)`, `record_play(minutes)`, `status_text()`, and
`__repr__`.

**What you build.** The class, a short script that replays one evening with at least two refusals,
and a self-check of your own with at least ten checks, including one for each exception type.

**Acceptance criteria:** your self-check passes; each refusal raises the right exception type; the
README has both sections from steps 1 and 14, for your domain.

**Grading:** same scale. Requirements Fit is judged on whether the rules are enforced by the class
and not by the script.

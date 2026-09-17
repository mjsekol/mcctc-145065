# Lab U3-01: Failures With Names
## 145065 Object-Oriented Programming · Unit 3 · Week 6

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1 (steps 1-4) and the
first 20 minutes of Monday Build 2 (steps 5-8).
**Competencies:** 5.3.10 (error handling techniques, including custom exception classes), 5.3.12
(create classes, objects, and methods).

Files: `lab-u03-01-files/errors.py`, `plant.py`, `shift_start.py`, and `selfcheck_errors.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every tag, name, and badge id in this lab is invented. No hardware is used.

---

## The scenario

Every morning a supervisor types a start-of-shift plan for Line 3, and `shift_start.py` runs it one
step at a time. The program never crashes. That sounds good until you read what it prints. A press
with its guard open, a press with a technician's lock on it, a tag that is not on this line, and a
typo in the oven setpoint all produce the same message: "something went wrong." Then the program
starts the oven anyway, after the plan was already known to be wrong.

The cause is one line: `except Exception:`. It treats every failure the same way, including the
failures nobody planned for.

## What you will build

A family of exception classes for the Line 3 model, a model that raises them, and a plan runner that
responds to each kind of failure in its own way and lets real bugs crash where you can see them.

---

## The family you are building

```
PlantError                                  catch this to catch all of them
|-- ConfigurationError (also ValueError)    a value the model refuses
`-- EquipmentError                          carries asset_tag
    |-- LockoutError                        locked out, or the wrong badge
    |-- EquipmentStateError                 wrong state: guard open, not running
    `-- UnknownEquipmentError               no such tag on this line
```

`ConfigurationError` has two parents on purpose. Step 3 explains why.

---

## Before you start

Copy the four files into `unit-03-lab/` in your `oop-semester` repository and run:

```
python shift_start.py
python selfcheck_errors.py
```

The starter prints:

```
step 1 failed: something went wrong
step 2 failed: something went wrong
step 3 done: L3-CNV-01 start
step 4 done: L3-OVN-01 setpoint 205
step 5 failed: something went wrong
step 6 failed: something went wrong
step 7 done: L3-OVN-01 start

Oven setpoint is 205 C and the oven is running
```

The self-check ends with `1 of 8 self-checks passed`. The one check that passes is the promise you
must keep: code that already catches `ValueError` keeps working. Commit.

Read `PLAN` in `shift_start.py`. For each failed step, write down in your README what actually went
wrong. You will need the list in step 8.

---

## Part 1 · Build 1 · Name the failures

### Step 1. Write the six classes

In `errors.py`, write the six classes in the diagram. Each needs only a class line and a docstring
that says when it is raised. `ConfigurationError` inherits from both `PlantError` and `ValueError`:

```python
class ConfigurationError(PlantError, ValueError):
```

`LockoutError` and `EquipmentStateError` are siblings. Neither inherits from the other.

**Observable result:** `2 of 8`. The `Step 1` line passes.

### Step 2. Make `EquipmentError` carry the tag

A handler that has to pull the tag out of the message text is fragile. Give `EquipmentError` an
`__init__(self, asset_tag, message)` that stores `asset_tag` as an attribute and then calls
`super().__init__(...)` with the text `"<tag>: <message>"`.

Check it in a Python prompt:

```python
>>> import errors
>>> error = errors.LockoutError("L3-PRS-02", "locked out by tech-07")
>>> error.asset_tag
'L3-PRS-02'
>>> str(error)
'L3-PRS-02: locked out by tech-07'
```

The three child classes need no `__init__` of their own. They inherit this one.

**Observable result:** `3 of 8`.

### Step 3. Make the model raise the family

`plant.py` raises built-in exceptions. Import the four classes you need from `errors`, and change
every `raise` below:

| Now raises | Where | Change it to |
|---|---|---|
| `ValueError` | `require_text`, `require_positive`, `require_count`, the tag check, `record_strokes`, the conveyor speed, the rack load | `ConfigurationError("same message")` |
| `RuntimeError` | `start`, `lock_out`, and `release_lockout` in `PoweredEquipment` | `LockoutError(tag, "message without the tag")` |
| `RuntimeError` | `Press.start` and `Press.record_strokes` | `EquipmentStateError(tag, "message without the tag")` |
| `KeyError` | `Line.get` | `UnknownEquipmentError(asset_tag, "not on this line")` |

That is 14 `raise` lines. **Leave every `TypeError` alone.** A wrong type, such as a rating of
`"fifteen"`, is a mistake in the code that called the model. A wrong value, such as a rating of `-5`,
is bad data. They deserve different responses.

Why two parents? Code written before today says `except ValueError`. Because a `ConfigurationError`
is also a `ValueError`, that code still catches it. That is how you change the errors a model raises
without breaking the code that calls it.

**Observable result:** `4 of 8`. Search `plant.py` for `RuntimeError` and `KeyError`. Neither
should appear.

### Step 4. Keep the cause when you translate an error

In `shift_start.py`, import `ConfigurationError` from `errors`. `parse_number()` calls `float(text)`.
With `"2O5"`, that raises a `ValueError` whose message says
nothing about the plan. Wrap it:

```python
try:
    return float(text)
except ValueError as error:
    raise ConfigurationError(f"{label} {text!r} is not a number") from error
```

`from error` stores the original error in the new one's `__cause__`. The traceback then shows both
errors, joined by "The above exception was the direct cause of the following exception."

Also change the two `ValueError` raises in `run_step()` to `ConfigurationError`.

**Observable result:** `5 of 8`. Every `Step 1` through `Step 4` line passes. Commit.

---

## Part 2 · Build 2, first 20 minutes · Respond to each failure

### Step 5. One handler per kind of failure

Import the other three classes you need. In `run_plan()`, delete `except Exception:`. Write four
handlers in its place, in this order. Each
one adds one report line:

| Handler | Report line |
|---|---|
| `except LockoutError as error:` | `step N SKIPPED, locked out: <error>` |
| `except EquipmentStateError as error:` | `step N SKIPPED, needs attention: <error>` |
| `except UnknownEquipmentError as error:` | `step N SKIPPED, not on this line: <error>` |
| `except ConfigurationError as error:` | `step N STOPPED, the plan is wrong: <error>` |

Keep the `else:` that reports `done`.

**Observable result:** `6 of 8`. The `Step 5` line still fails, because the report's last line says
`step 7 done: L3-OVN-01 start`. The oven started after the plan was found to be wrong. Step 6 fixes
that.

### Step 6. A wrong plan stops the plan

A locked-out press is a reason to skip one step. A typo in the plan is a reason to trust nothing
after it. In the `ConfigurationError` handler, add one more report line, `steps not run: N`, where N
is how many steps were left, and then `break`.

**Observable result:** `8 of 8 self-checks passed`, and `python shift_start.py` prints:

```
step 1 SKIPPED, needs attention: L3-PRS-01: guard is open; close it before starting
step 2 SKIPPED, locked out: L3-PRS-02: locked out by tech-07; cannot start
step 3 done: L3-CNV-01 start
step 4 done: L3-OVN-01 setpoint 205
step 5 SKIPPED, not on this line: L3-PRS-07: not on this line
step 6 STOPPED, the plan is wrong: setpoint '2O5' is not a number
steps not run: 1

Oven setpoint is 205 C and the oven is stopped
```

### Step 7. Prove what the catch-all was hiding

Put the old clause back for one minute, **after** your four handlers:

```python
        except Exception:
            report.append(f"step {number} failed: something went wrong")
```

Run the self-check. The self-check replaces the conveyor's `start()` with a function that divides by
zero, a bug nobody planned for:

```
FAIL  Step 7  a real bug is not swallowed
        run_plan() hid a ZeroDivisionError; never catch Exception

7 of 8 self-checks passed
```

Delete the clause again and confirm `8 of 8`. In your README, under `## What the catch-all hid`,
write two sentences: what the supervisor would have seen with the catch-all in place, and why a crash
is the better outcome for a bug.

### Step 8. The failure table

In your README, under `## Failures with names`, write one row per class you raise:

| Error | Raised when | What `run_plan` does | Why that response |
|---|---|---|---|

Use the list you wrote before step 1. Every "something went wrong" in the starter should now have a
row. Commit and push.

---

## Acceptance criteria, full lab

- [ ] `python selfcheck_errors.py` prints `8 of 8 self-checks passed`
- [ ] `python shift_start.py` prints the report in step 6, and the oven is stopped
- [ ] `plant.py` raises no `RuntimeError` and no `KeyError`; every `TypeError` is unchanged
- [ ] `shift_start.py` has no `except Exception`
- [ ] The README has the failure table and the step 7 section
- [ ] Committed at the end of Build 1 and at the end of the lab

---

## If it breaks

### 1. The message is a tuple

```
('L3-PRS-02', 'locked out by tech-07')
```

**Cause:** `EquipmentError.__init__` stored the tag but never called `super().__init__(...)`.
Python's `Exception` then keeps both arguments and prints them as a tuple. Call
`super().__init__(f"{asset_tag}: {message}")`.

### 2. A missing argument

```
TypeError: EquipmentError.__init__() missing 1 required positional argument: 'message'
```

**Cause:** a `raise LockoutError("locked out by tech-07")` with no tag. Every `EquipmentError` needs
the tag first and the message second.

### 3. Every equipment failure gets the same message

No error. Steps 1 and 2 both print `SKIPPED:` and the message, with no word saying which kind of
failure it was.

**Cause:** an `except EquipmentError` written above `except LockoutError`. Python uses the **first**
clause that matches, and a `LockoutError` is an `EquipmentError`, so the lockout clause never runs.
Put children above their parents.

### 4. The traceback says "During handling"

```
ValueError: could not convert string to float: '2O5'

During handling of the above exception, another exception occurred:
...
errors.ConfigurationError: setpoint '2O5' is not a number
```

**Cause:** `raise ConfigurationError(...)` without `from error`. Python still shows both errors, but
the wording says the second one happened by accident while handling the first. With `from error`, it
says "The above exception was the direct cause of the following exception," and `__cause__` is set.
The self-check's step 4 line tests `__cause__`.

### 5. Two classes in one clause

```
    except LockoutError, EquipmentStateError as error:
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: multiple exception types must be parenthesized
```

**Cause:** several classes in one `except` must be a tuple:
`except (LockoutError, EquipmentStateError) as error:`. This lab wants them separate anyway,
because each gets its own response.

### 6. A `ConfigurationError` nobody caught

```
errors.ConfigurationError: rated_kw must be above 0 and at most 500
```

**Cause:** this is correct behavior. Building a `Press` with `-5` kW outside `run_plan()` has no
handler. The traceback names your class, not `ValueError`, which is the point of the lab.

### Not an error, and the one that matters most: `except Exception`

A handler that catches everything never crashes and never tells the truth. Step 7 shows the bug it
hid.

**Error wording was captured on Python 3.13.7.** Confirm it on the lab's Python 3.14. Python 3.14
allows several exception types without parentheses when there is no `as`, so error 5 may read
differently there [VERIFY].

---

## Stretch goal

Write `test_errors.py` with `unittest`. Use `assertRaises` to prove each of the four plan failures
raises the class you expect, and one test that `except PlantError` catches all four. Then change
`LockoutError` to inherit from `EquipmentStateError`, run your tests and the self-check, and write
down which test or check caught the change.

---

## Submission checklist

- [ ] Self-check 8 of 8
- [ ] README sections: the failure table and "What the catch-all hid"
- [ ] The temporary `except Exception` from step 7 removed
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.3.10, 5.3.12) and grade on the same 100-point
five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 15 of Build 1, `errors.py` is still empty | SCAFFOLDED |
| Steady progress, questions about which `raise` lines to change | STANDARD |
| 5 of 8 before Build 1 is half over | EXTENDED |
| The student asks why a factory model matters to anything they will write | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out a different `errors.py`, with `PlantError`,
  `ConfigurationError`, and `EquipmentError` already written, and a different `shift_start.py`, whose
  `run_plan()` has the four handlers and their report text as comments. The self-check still starts
  at `1 of 8`.
- **Steps:** step 1 becomes "write the last three classes." Skip step 2; it is done.
- **Checkpoints:** show the self-check to the instructor after step 3 and after step 6.
- **Keep step 7.** The hidden bug is the lesson.

**Acceptance criteria:** 8 of 8, the failure table, the step 7 section.

**Grading:** same 100-point scale. Full completion earns the same grade as full completion of
STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one problem the lab has not taught.

**Added requirement.** The supervisor complains that the runner reports one problem per attempt:
fix the guard, run again, find the lockout, run again, find the typo. Write `preflight(line, plan)`.
It starts nothing. It checks every step and collects **every** problem it finds. If there are any,
it raises them together in one exception. Then write `report_preflight()`, which prints each problem
under a heading for its kind, and call it from `main()` on a fresh line.

**Hint, not the answer.** Python 3.11 added a way to raise several unrelated exceptions at once and
a new form of `except` to handle them by type. Read the section "Raising and Handling Multiple
Unrelated Exceptions" in the Python tutorial's errors chapter,
`https://docs.python.org/3/tutorial/errors.html`.

**Acceptance criteria:** all STANDARD criteria; on the sample line, the preflight reports the
lockout, the open guard, the unknown tag, and the setpoint typo in one run; a decision log entry
names the rejected alternative (for example, returning a list of strings).

**Grading:** same scale.

---

## APPLIED

**For the student who asks when they would use this.** The same skill in a game's mod loader.

**Changed scenario.** A game loads player-made mods at startup. The loader has one
`except Exception: print("mod failed")`, so a mod that needs a newer game version, a mod with a
broken file, and a real bug in the loader all look the same, and the game keeps loading mods that
depend on the broken one. Write `ModError`, `ModConfigError(ModError, ValueError)`, and
`ModLoadError(ModError)` carrying the mod's name, with children `IncompatibleVersionError` and
`MissingDependencyError`. Invent every mod name. No real game's content.

**What you build.** The family, a loader that skips an incompatible mod, stops on a broken
configuration file, and lets bugs crash, and a self-check of at least six checks modeled on
`selfcheck_errors.py`, including "a real bug is not swallowed."

**Acceptance criteria:** your self-check passes; your README has a failure table and a "What the
catch-all hid" section for your own loader.

**Grading:** same scale. Requirements Fit is judged on whether each handler's response fits its
failure.

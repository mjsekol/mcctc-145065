# Lecture Notes: Testing a Class
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W03_TestingAClass.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W03_TestingAClass.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and a terminal.

**Competencies:** 5.4.4 define test cases. 5.4.5 test the program using defined test cases.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop. The badge id `tech-07` is invented.

---

## Why this exists

All unit your classes have promised things. A locked-out press refuses to start. A negative rating is
refused. Two machines never share state. Right now, the only proof is that you ran the file once and
read the output.

That proof expires the moment anyone edits the class. Your refactor project changes working code on
purpose, and the whole point is that behavior stays the same. You need checks you can rerun in two
seconds, every time, that say PASS or FAIL without you reading anything.

That is a unit test. And the hardest part is not the code. It is deciding what to test before you
write it.

---

## The concept in plain language

### Define the cases first

A **test case** is one situation with one expected result. Write the cases in a table **before** any
test code. The table makes you think about what the class promises, including the refusals.

| # | Setup | Action | Expected | Why it matters |
|---|---|---|---|---|
| 1 | new press | none | not running | a new machine must never start by itself |
| 2 | new press | `start()` | running | the basic promise |
| 3 | running press | `lock_out("tech-07")`, then `start()` | stopped, then `RuntimeError` | lockout is a safety rule |
| 4 | none | build with rating 0, then -5 | `ValueError` each time | the object refuses to be invalid |
| 5 | two presses | start one | the other is still stopped | no shared state |

Rows 3 and 4 are **refusal tests**. They check that the class says no. A class tested only on the
happy path has half its promises unchecked. Your refactor project requires at least one refusal test
per class.

### Then write them with `unittest`

`unittest` is in the standard library. The pieces you need:

- A class that inherits from `unittest.TestCase`. Unit 2 explains inheritance. Today, copy the shape.
- Methods whose names start with `test_`. Each one is one case.
- `setUp`, which runs before **every** test, so each test gets a fresh object.
- Assertions: `assertEqual(a, b)`, `assertTrue(x)`, `assertFalse(x)`, and
  `with self.assertRaises(SomeError):` for refusals.
- `with self.subTest(bad=bad):` inside a loop, so one test can check several values and still report
  which one failed.

Run every test in the folder with `python -m unittest -v`. The `-v` prints one line per test.

---

## Worked example 1: the table, as tests

The class under test, `machine.py`:

```python
class Machine:
    def __init__(self, asset_tag, rated_kw):
        if rated_kw <= 0:
            raise ValueError("rated_kw must be above 0")
        self.asset_tag = asset_tag
        self.rated_kw = float(rated_kw)
        self._running = False
        self._locked_by = None

    @property
    def is_running(self):
        return self._running

    def start(self):
        if self._locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out")
        self._running = True

    def stop(self):
        self._running = False

    def lock_out(self, badge):
        self.stop()
        self._locked_by = badge
```

The tests, `test_machine.py`, in the same folder:

```python
# test_machine.py
import unittest

from machine import Machine


class MachineTests(unittest.TestCase):
    def setUp(self):
        # A fresh press for every test, so no test depends on another.
        self.press = Machine("L3-PRS-01", 15)

    def test_new_machine_is_stopped(self):
        self.assertFalse(self.press.is_running)

    def test_start_runs_the_machine(self):
        self.press.start()
        self.assertTrue(self.press.is_running)

    def test_lockout_stops_and_blocks_start(self):
        self.press.start()
        self.press.lock_out("tech-07")
        self.assertFalse(self.press.is_running)
        with self.assertRaises(RuntimeError):
            self.press.start()

    def test_zero_or_negative_rating_is_refused(self):
        for bad in [0, -5]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Machine("L3-PRS-02", bad)

    def test_two_machines_do_not_share_state(self):
        other = Machine("L3-PRS-02", 22)
        self.press.start()
        self.assertFalse(other.is_running)

    def test_that_cannot_fail(self):
        # The deliberate mistake: no parentheses, so this checks the method
        # object itself, which is always truthy. It passes on broken code.
        self.assertTrue(self.press.start)


if __name__ == "__main__":
    unittest.main()
```

Run from that folder:

```
python -m unittest -v
```

Output:

```
test_lockout_stops_and_blocks_start (test_machine.MachineTests.test_lockout_stops_and_blocks_start) ... ok
test_new_machine_is_stopped (test_machine.MachineTests.test_new_machine_is_stopped) ... ok
test_start_runs_the_machine (test_machine.MachineTests.test_start_runs_the_machine) ... ok
test_that_cannot_fail (test_machine.MachineTests.test_that_cannot_fail) ... ok
test_two_machines_do_not_share_state (test_machine.MachineTests.test_two_machines_do_not_share_state) ... ok
test_zero_or_negative_rating_is_refused (test_machine.MachineTests.test_zero_or_negative_rating_is_refused) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.008s

OK
```

Your time will differ. Tests run in alphabetical order by name, not in the order you wrote them, which
is one more reason each test must build its own object. Rows 1 to 5 of the table each became one test.
The sixth test is today's deliberate mistake, explained below.

---

## Worked example 2: reading a real FAIL report

Now break the class. Someone edits `start()` and leaves `self._running = False` where `True` belongs.
Run the same command:

```
test_lockout_stops_and_blocks_start (test_machine.MachineTests.test_lockout_stops_and_blocks_start) ... ok
test_new_machine_is_stopped (test_machine.MachineTests.test_new_machine_is_stopped) ... ok
test_start_runs_the_machine (test_machine.MachineTests.test_start_runs_the_machine) ... FAIL
test_that_cannot_fail (test_machine.MachineTests.test_that_cannot_fail) ... ok
test_two_machines_do_not_share_state (test_machine.MachineTests.test_two_machines_do_not_share_state) ... ok
test_zero_or_negative_rating_is_refused (test_machine.MachineTests.test_zero_or_negative_rating_is_refused) ... ok

======================================================================
FAIL: test_start_runs_the_machine (test_machine.MachineTests.test_start_runs_the_machine)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...\test_machine.py", line 17, in test_start_runs_the_machine
    self.assertTrue(self.press.is_running)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

----------------------------------------------------------------------
Ran 6 tests in 0.001s

FAILED (failures=1)
```

Read it in this order:

1. **The last line.** One failure. Not an error, which would mean the test itself crashed.
2. **The `FAIL:` heading.** Which test. A good test name already tells you which promise broke.
3. **The file and line.** Line 17 of the test file, the assertion.
4. **The `AssertionError` line.** What was checked and what was found: it expected true and got
   `False`.

The test points at the promise. It does not point at the broken line in `machine.py`. That part is
still your job, and now you know to look in `start()`.

---

## Worked example 3: `subTest` names the value that failed

Another edit changes the rating check to `if rated_kw < 0:`, so a zero rating slips through. Run only
that test:

```
python -m unittest test_machine.MachineTests.test_zero_or_negative_rating_is_refused
```

```
F
======================================================================
FAIL: test_zero_or_negative_rating_is_refused (test_machine.MachineTests.test_zero_or_negative_rating_is_refused) (bad=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...\test_machine.py", line 29, in test_zero_or_negative_rating_is_refused
    with self.assertRaises(ValueError):
         ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

`(bad=0)` on the heading says which value failed. `-5` is not listed, so it was still refused. Without
`subTest`, you would know only that something in the loop failed. `ValueError not raised` is how a
refusal test reports that the class said yes when it should have said no.

---

## The wrong version: a test that cannot fail

Look back at the last test in the file:

```python
    def test_that_cannot_fail(self):
        self.assertTrue(self.press.start)
```

In example 2, with `start()` broken, this test still printed `ok`. No parentheses means the code never
calls `start`. It checks the method object itself, and any method object counts as true. The test
passes on working code, on broken code, and on code where `start` does nothing at all.

There is no error message to show, and that is the problem. A test that cannot fail gives you a green
result and no information.

The check that catches it: **make the class wrong on purpose and watch each test fail.** If a test
still passes when the behavior it names is broken, the test is broken. Today's lab automates exactly
this with planted mutants.

---

## Why the wrong version is tempting

`self.press.start` and `self.press.is_running` look almost the same, and this week you learned that
properties have no parentheses. Methods still do. The two blur together fastest when you are writing
many tests quickly.

The deeper temptation is trusting a green `OK`. A passing run feels like proof. It is only proof if
each test could have failed. Seeing a test fail once, on purpose, is what earns your trust in it.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Test case** | one situation, one action, one expected result |
| **Unit test** | code that checks one small piece, like one class, automatically |
| **Refusal test** | a test that checks the code says no, usually with `assertRaises` |
| **`TestCase`** | the `unittest` class your test class inherits from |
| **`setUp`** | a method that runs before every test to build fresh objects |
| **Assertion** | a check that fails the test when it is false |
| **`subTest`** | a block that reports which value in a loop failed |
| **FAIL versus ERROR** | FAIL: an assertion was false. ERROR: the test crashed. |
| **Mutant** | a copy of the code with a deliberate bug, used to test the tests |

---

## Self-check

**Question 1.** Add a row to the test-case table for `release_lockout(badge)`, which must refuse a
badge that did not apply the lock. Fill in setup, action, expected, and why.

**Question 2.** Why does each test get its own press from `setUp`, instead of one press shared by
every test?

**Question 3.** A student's test is `self.assertTrue(self.cell.running)`, where `running` is a
**method** that returns a list. The cell has no running machines. Does the test pass or fail, and is
it a good test?

---

### Answers

**1.** Setup: a press locked out by `tech-07`. Action: `release_lockout("tech-12")`. Expected:
`RuntimeError`, and the press is still locked out. Why: only the person who applied a lock may remove
it, which is a safety rule.

**2.** Tests run in alphabetical order, not written order, and any test might change the object. A
shared press could arrive already running or locked out, so one test's result would depend on another.
A fresh object makes every test stand alone.

**3.** It passes, and it is a bad test. Without parentheses it checks the method object, which is
always true, so it would pass even with running machines, with none, or with broken code. The intended
check needs parentheses, and an empty list is false, so `self.assertEqual(self.cell.running(), [])`
states the real expectation.

Want more practice? Side quest SQ-17, Unit Tests for Something You Already Wrote, in the side quest
catalog, extends this lesson. You write a real test suite for an old program of yours, including
inputs designed to break it, and you are done when a test exposes a real defect and you fix it.

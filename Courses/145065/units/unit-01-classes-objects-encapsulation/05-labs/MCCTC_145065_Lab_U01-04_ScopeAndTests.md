# Lab U01-04: Scope and Tests
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Wednesday and Thursday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Part 1 on Wednesday, Build 1. Part 2
on Thursday, Build 1.
**Competencies:** 5.2.2 (identify the scope of data), 5.4.4 (define test cases), 5.4.5 (test the
program using defined test cases), 5.1.2 (how algorithms and data structures are used in information
processing), 5.3.12 (classes, objects, and methods), 5.4.7 (debug logic errors), 5.5.5 (naming
conventions and comments).

Files, Part 1: `lab-u01-04-files/shift_counters.py`, `lab-u01-04-files/scope_map_template.md`, and
`lab-u01-04-files/selfcheck_scope.py`.
Files, Part 2: `lab-u01-04-files/line3/` (the classes under test), `lab-u01-04-files/test_line3.py`
(your starter), `lab-u01-04-files/test_plan_template.md`, `lab-u01-04-files/mutant_check.py`, and
`lab-u01-04-files/collection_timer.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag, badge,
and count here is invented. The `line3/` folder is copied, unchanged, from the course's Line 3 plant
model. **Do not edit anything in `line3/`.** You are testing it, not fixing it.

---

## The scenario

Line 3's shift report says zero press starts on a morning when the presses started three times, and
it says "First shift" after the line changed over. The code runs and never crashes, and every one of
its mistakes is a name living at the wrong level. Meanwhile, the shop's `Machine` and `WorkCell`
classes have no tests at all, and the supervisor wants proof that the lockout and the cell's rules
hold before anyone builds on them.

## What you will build

A fixed shift counter with a map of where every name lives, and a planned test suite for `Machine`
and `WorkCell` that catches deliberately broken versions of both.

---

## Part 1: Wednesday Build 1, steps 1 through 7 · the scope hunt

### Step 1. Read the report, then read what it should say

Run `python shift_counters.py`. It prints:

```
First shift on Line 3: 0 starts
  L3-PRS-01: 360 strokes
  L3-PRS-02: 450 strokes
First shift on Line 3: 0 starts
  L3-PRS-01: 360 strokes
  L3-PRS-02: 450 strokes
```

The shift really went like this: three starts, then a changeover that zeroed everything.

```
First shift on Line 3: 3 starts
  L3-PRS-01: 360 strokes
  L3-PRS-02: 450 strokes
Second shift on Line 3: 0 starts
  L3-PRS-01: 0 strokes
  L3-PRS-02: 0 strokes
```

In your lab README, under `## What the report got wrong`, list the three differences.

**Observable result:** three bullets. Nothing has crashed, and nothing will.

### Step 2. Start the map

```
python selfcheck_scope.py
```

Copy `scope_map_template.md` to `scope_map.md` in the same folder.

**Observable result:** `0 of 5 self-checks passed`. Commit.

### Step 3. Map the levels before you change any code

Fill the **Level** column for all eleven rows: module (global), class, instance, or local. Read the
code, not the comments. A comment says what the author meant. The code says what happens.

**Observable result:** eleven levels filled. Three of them are not what the author meant. You may not
know which three yet.

### Step 4. The starts that vanished

Add `print(vars(presses[0]))` after the first `print(summary(presses))` in `main()`, and run the
program. Read what the press is holding. Explain in one sentence why `Press.starts_this_shift` is
still 0, then fix `start()` so every start is counted once, on the class. Remove the `print`.

**Observable result:** `selfcheck_scope.py` shows S2 passing. The report's first line says `3 starts`.

### Step 5. The strokes that would not reset

Fix `reset_for_new_shift()` so the press's own stroke count goes to zero.

**Observable result:** S3 passes.

### Step 6. The shift that would not change

Fix `change_shift()` so the module's `current_shift` becomes `"Second shift"`. The smallest fix is one
statement at the top of the function. Read "If it breaks" entry 1 before you try the first idea that
comes to mind.

**Observable result:** S1 and S4 pass. The program prints the report from step 1 exactly.

### Step 7. Finish the map

Fill **Lives until** and **Who should change it** for every row, the three bugs, and the design
question. Delete every `TODO`.

**Observable result:** `5 of 5 self-checks passed`. Commit and push.

---

## Part 2: Thursday Build 1, steps 8 through 16 · tests that can fail

### Step 8. The starting point

```
python -m unittest -v test_line3
python mutant_check.py
```

`mutant_check.py` copies `line3/` into a temporary folder, plants one bug at a time, and runs your
tests against each broken copy. If a test fails, your suite **caught** that mutant.

**Observable result:** one test passes. The mutant check ends `Caught 0 of 5 mutants`. One passing
test proves almost nothing.

### Step 9. Plan the Machine tests before you write them

Read `line3/machine.py`. Every rule a docstring or comment states is a test case waiting to happen.
Copy `test_plan_template.md` to `test_plan.md` and fill at least five more **Machine** rows: setup,
action, expected, and why it matters on the shop floor.

**Observable result:** at least six Machine rows, including a refusal at construction, a refused
property assignment, a lockout rule, and a reading the sensor could never produce. No test code yet.

### Step 10. Plan the WorkCell tests

Read `line3/cell.py`. Fill at least five **WorkCell** rows, including a duplicate, a machine that must
not be removed, and what a caller can and cannot do with `cell.machines`.

**Observable result:** at least five WorkCell rows. Commit the plan before any test code.

### Step 11. Write the Machine tests

In `test_line3.py`, one test method per Machine row. Name each method for the rule it checks. Build a
fresh press in every test. Use `assertRaises` for refusals and check that a refused call changed
nothing.

**Observable result:** `python -m unittest -v test_line3` lists every test as `ok`.

### Step 12. Write the WorkCell tests

`setUp` builds a fresh cell before every test. Add a method per WorkCell row.

**Observable result:** every test `ok`. At least eleven tests in total.

### Step 13. Do your tests catch anything

```
python mutant_check.py
```

**Observable result:** a line saying your tests pass on the real classes and how many ran, then one
`CAUGHT` or `MISSED` line per mutant, then `Caught N of 5 mutants`. Write N in your README.

### Step 14. The collection the cell keeps

```
python collection_timer.py
```

It times 3000 adds and 3000 lookups two ways: with `WorkCell`'s dictionary, and with a list scanned on
every call. Answer "The collection the cell keeps" in `test_plan.md`. Your times will differ from your
neighbor's. The ratio is the point.

**Observable result:** two times and a ratio, and three answers in your plan.

### Step 15. Catch the ones you missed

For each `MISSED` line, read the mutant's name, add a row to your plan, and write the test. Rerun
`mutant_check.py` after each one.

**Observable result:** at least `Caught 4 of 5 mutants`. `Caught 5 of 5 mutants` is the target, and one
of the five is genuinely hard to catch.

### Step 16. Say what you learned

Fill "After mutant_check.py" in your plan: which mutants your first run missed, and the test that now
catches each. Commit and push.

**Observable result:** `git status` is clean, and your plan has one row for every test method.

### Acceptance criteria, full lab

- [ ] `python selfcheck_scope.py` prints `5 of 5 self-checks passed`
- [ ] `scope_map.md` is complete, with the three bugs and the design question
- [ ] `test_plan.md` was committed before the first new test method
- [ ] Every test method matches a row in the plan
- [ ] `python -m unittest -v test_line3` passes, with at least eleven tests
- [ ] `python mutant_check.py` reports at least 4 of 5
- [ ] Nothing in `line3/` was changed
- [ ] Committed and pushed at the end of Wednesday and Thursday

---

## If it breaks

### 1. A global you tried to change without saying so

```
UnboundLocalError: cannot access local variable 'current_shift' where it is not associated with a value
```

**Cause:** inside `change_shift`, you wrote something like
`current_shift = current_shift + " (second)"`. Assigning to a name anywhere in a function makes it
local for the whole function, so the read on the right side has nothing to read. Tell Python the name
is the module's, or better, stop needing the global.

### 2. A Week 2 habit

```
ERROR: test_new_machine_is_stopped_with_no_reading (test_line3.MachineTests.test_new_machine_is_stopped_with_no_reading)
...
TypeError: 'bool' object is not callable
```

**Cause:** in `line3`, `is_running` is a property, so `press.is_running()` calls the `True` or
`False` it returns. Drop the parentheses. An `ERROR` means the test itself crashed. A `FAIL` means an
assertion was false.

### 3. The mutant check refuses to start

```
Your tests FAIL on the real classes (FAILED (failures=1)).
A test that fails on correct code is a wrong test. Fix it first:
    python -m unittest -v test_line3
```

**Cause:** one of your expected values is wrong, for example `AssertionError: 15 != 55` after run
times of 10 and 5. The classes in `line3/` are correct. Recheck your arithmetic and your plan.

### 4. Running from the wrong folder

```
ModuleNotFoundError: No module named 'test_line3'
```

It appears inside an `ImportError: Failed to import test module: test_line3` report.

**Cause:** `python -m unittest test_line3` looks for the file in the folder you are in. `cd` into the
lab folder that holds `test_line3.py` and `line3/`.

### 5. A test that cannot fail

Your suite passes, and `mutant_check.py` still misses a mutant your plan says you test.

**Cause:** a test that checks the value it set a line earlier, or that forgets the parentheses on a method, or
that has no assertion at all. Read that test aloud and ask: "Which broken version of the class would
make this line false?"

---

## Stretch goal

Rewrite `shift_counters.py` with no global at all: a `Shift` object holds the shift name and the
presses, and `change_shift` becomes its method. The report must not change. In the README, compare
the two versions in three sentences.

---

## Submission checklist

- [ ] Scope self-check 5 of 5, scope map complete
- [ ] Test plan committed before the tests
- [ ] Tests pass; mutant check at least 4 of 5, with N written in the README
- [ ] Collection answers in the plan
- [ ] AI usage log updated if you used a model
- [ ] Committed and pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| On Wednesday the scope map's Level column is still empty after 15 minutes, or on Thursday the student is writing tests with no plan | SCAFFOLDED |
| Steady progress; arguments about whether a loop variable is local | STANDARD |
| `Caught 5 of 5 mutants` before Thursday's Build 1 is half over | EXTENDED |
| The student asks why anyone would test code that already works | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Part 1:** the student receives `scope_map.md` with the Level column filled for eight of the eleven
  rows. The three rows left blank are the three bugs.
- **Part 2:** the student receives a test plan with the Setup and Action columns filled for six rows,
  and writes Expected, Why, and the tests.
- **Target:** at least 3 of 5 mutants.
- **Checkpoints:** show the instructor the scope map after step 3 and the plan after step 10.

**Acceptance criteria:** 5 of 5 on the scope self-check; at least nine tests that pass; at least 3 of 5
mutants caught.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a concept the lab has not taught.

**Added requirement.** Copy `mutant_check.py` to `my_mutant_check.py` and add a sixth mutant for a rule
none of the five breaks, such as the tag pattern, the run-time rule, or `remove()` on an unknown tag.
Confirm your current tests **miss** it, then write the test that catches it.

**Hint, not the answer.** Read how the script builds each mutant: it finds exact text in a file and
replaces it. Then read how it runs your tests in a separate process, in the `subprocess.run` section
of `https://docs.python.org/3/library/subprocess.html`. Your mutant is one more entry in a list. The
hard part is choosing a replacement that breaks a rule without breaking Python.

**Acceptance criteria:** all STANDARD criteria; `my_mutant_check.py` reports your mutant `MISSED` before
your new test and `CAUGHT` after it; the plan has a row for the new test.

**Grading:** same scale.

---

## APPLIED

**For the student who asks why anyone tests working code.** The same skill, somewhere else.

**Changed scenario.** A group chat app's `Poll` class lets members vote once each, lets only the poll's
creator close it, and refuses votes after it closes. Write the `Poll` class yourself in about 40 lines,
with invented member handles and no real names. Then write a test plan and a test suite for it. Then
break your own class three ways, one rule at a time, in copies, and show that your suite catches each.

**What you build.** `poll.py`, `test_plan.md`, `test_poll.py`, and three broken copies with a one-line
note on what each breaks.

**Acceptance criteria:** the suite passes on the real class and fails on each broken copy; every test
matches a plan row; the README says which broken copy was hardest to catch and why.

**Grading:** same scale. Requirements Fit is judged on whether each test would fail if its rule broke.

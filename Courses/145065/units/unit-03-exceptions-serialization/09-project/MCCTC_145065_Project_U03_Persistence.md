# Project · Make It Survive a Restart
## 145065 Object-Oriented Programming · Unit 3 · Week 6

**100 points. Projects category, 35 percent of your grade.**
**Due Week 6, Friday, at the end of the final project commit window (minutes 105-110).**

**Gate 3.** Full tooling, AI allowed, AI usage log required, decision log required.

---

## The brief

> From: the maintenance coordinator at Riverside Fabrication
>
> The hierarchy you built works. Then the PC restarted for an update, and everything it knew was
> gone, including which vehicles were tagged out. We went back to the clipboard for a morning.
>
> I need it to remember. I also need it not to lie. If the file gets damaged, I want to be told
> where, not handed a half-empty fleet. If someone edits the file, I want to know what the program
> can catch and what it cannot. And I want a written plan, before the day it happens, for what we
> do when the file is gone.
>
> When something goes wrong, tell my people what went wrong. "Error" is not a message.

Riverside Fabrication is a **composite**, the invented shop you have worked with all semester.
**You extend your own Unit 2 hierarchy**, the fleet or the domain you chose. Invent every name and
number. No real person's information.

**That is the whole brief.** It does not say which failures deserve their own exception class, what
a restart must remember, or which checks only a person can do. Deciding those, and writing them
down, is part of the grade.

---

## What you are building

| # | Piece | Form |
|---|---|---|
| 1 | Your Unit 2 package, extended | copied into `unit-03-persistence/`, standard library only |
| 2 | An error family | `errors.py` in your package |
| 3 | Saving and loading | `storage.py` in your package |
| 4 | Tests | `unittest`, run with `python -m unittest` |
| 5 | A recovery plan | `RECOVERY_PLAN.md`, from the template below |
| 6 | A decision log, an AI usage log, and a README | the usual course formats |

---

## Technical requirements

1. **An exception family.** One root class for your domain. At least one class that also inherits a
   built-in exception, so old `except` code keeps working. At least one class that carries data as
   an attribute, such as a tag or a field path. A test proves one `except` clause catches the whole
   family.
2. **Name every planned failure.** Your model raises your family, not `ValueError`, `RuntimeError`,
   or `KeyError`, for every failure it plans for. A wrong **type** may stay `TypeError`. **No
   `except Exception` anywhere** in your package.
3. **Every class describes and rebuilds itself.** `to_dict()` returns only JSON types.
   `from_dict()` is a class method that goes through the constructor and the setters, so loaded data
   obeys the same rules as typed data.
4. **A round trip.** A test proves `dumps(loads(dumps(x))) == dumps(x)` for a sample with every kind
   in it.
5. **Decide what a restart remembers.** At least one value is saved because a restart must not
   forget it, and at least one is deliberately **not** saved. A test proves each. The README says
   why for each.
6. **UTF-8.** Files are written and read with `encoding="utf-8"`, and non-ASCII names are readable
   in the file. A test saves a name with a non-ASCII letter and checks its bytes.
7. **A guarded load.** An allowlist of kinds; exact fields; JSON types checked; `NaN` and `Infinity`
   refused; the file size checked before reading; a non-UTF-8 file refused. Every refusal is one of
   your exceptions and says **where** in the file the problem is. At least three bad files of your
   own, each with a test.
8. **Never pickle.** A test proves your storage module imports no pickle.
9. **A save that cannot destroy the last good copy.** Build the text first; back up the current
   file; write a temporary file and flush it to disk; swap it in with `os.replace()`. A restore that
   loads the backup before trusting it. A test for each, including a simulated failure during the
   replace.
10. **`RECOVERY_PLAN.md`**, every section of the template below.
11. **The decision log** has at least three Unit 3 entries, each naming the option you rejected.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| Standard library only | `json`, `os`, `shutil`, and `pathlib` are what this unit teaches, and nothing is installed on lab machines. |
| No pickle, no class chosen by name from the file | Loading is the moment of trust. A file must never choose which code runs. |
| Tests write only to a temporary folder | A test that leaves `fleet.json` behind is a test that can overwrite real data. |
| No save files committed | Your repository holds code and fixtures, not the program's working data. |
| Invented data only | Program rule. No personal information anywhere, and nothing in any AI tool. |
| AI models are local or not used | Program rule. Commercial AI accounts require users to be 18 or older. |

---

## Required repository structure

```
oop-semester/
  README.md
  decision-log.md
  unit-02-hierarchy/              unchanged from Week 5
  unit-03-persistence/
    README.md
    RECOVERY_PLAN.md
    DEMO_CHECKLIST.md             filled in by your partner on Thursday
    ai-usage-log.md
    <your package>/
      errors.py
      storage.py
      ...
    demo.py
    tests/
      test_*.py
      bad_files/                  your hand-made bad files
```

---

## The recovery plan template

Copy this into `unit-03-persistence/RECOVERY_PLAN.md` and fill in every section. Your answers are
about **your** program and **your** data.

```markdown
# Recovery Plan · <your program's name>

## 1. What is lost
What the data file holds, what it deliberately does not hold, and what stops working without it.

## 2. How it can be lost
A table: each cause (a failed save, a hand edit that breaks the file, a hand edit that does not,
a deleted file, a dead drive) and what your program does about it.

## 3. Who notices, and who decides
Who sees the problem first, who decides it is safe to go on, and what people do until then.

## 4. The steps, in order
Numbered. Start with what NOT to do. Say which copy to restore and how it is checked first.

## 5. What only a person can check
A table: each check, and why the program cannot do it.

## 6. Testing this plan
Which automated tests cover it, and how people rehearse the rest, and how often.

## 7. What this plan does not cover
At least one honest gap.
```

---

## DMAIC checkpoints

### Define · Monday, Build 2 (P1)

Read the brief. List the failures your program plans for and what the code that catches each one
should do differently. **Checkpoint:** `errors.py` and its family test, and a decision log entry
naming a class you chose not to create.

### Measure · Tuesday, Build 2 (P2)

List every field each class holds and mark it "saved" or "not saved," with a reason.
**Checkpoint:** the round-trip test and the what-survives tests pass.

### Analyze · Wednesday, Build 2 (P3)

Write three bad files of your own. For each, predict what your loader should say and where.
**Checkpoint:** the guarded load and three bad-file tests pass. `storage.py` imports no pickle.

### Improve · Thursday, Build 2 (P4)

The safe save, the checked restore, their tests, and `RECOVERY_PLAN.md`. Last 10 minutes: rehearse
the demo with a partner.

### Control · Friday

**Checkpoint:** every test passes, the README says how to run the tests and the demo, and everything
is pushed inside the final commit window.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| P1 | Error family | Week 6 Mon, end of block | `errors.py` and its test are committed |
| P2 | Round trip | Week 6 Tue, end of block | the round-trip and what-survives tests pass |
| P3 | Guarded load | Week 6 Wed, end of block | three bad-file tests pass |
| P4 | Backup, restore, recovery plan, demo rehearsal | Week 6 Thu, end of block | both tests pass; `RECOVERY_PLAN.md` and `DEMO_CHECKLIST.md` are committed |
| **Due** | **Everything** | **Week 6 Fri, minutes 105-110** | the submission checklist is complete |

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality.

### Small, and completely finished

**Family:** a root, one two-parent class, one class with data, and a missing-file class. **Load:**
every requirement 7 check, three bad files. **Save:** the four steps and the restore.

**What makes it full marks:** every requirement met, and a recovery plan with a real section 5.

**The risk:** a thin recovery plan. Small scope does not shrink the plan.

### Medium, and the one most students should aim for

Everything in small, plus **a family whose classes each change what a handler does**, with a
docstring saying how, and **a demo that damages a file and restores it** in a temporary folder.

**What it adds:** evidence that each class earns its place, and a demo that shows recovery instead
of describing it.

**The risk:** time on Wednesday. The field checks take longer than students expect.

### Large, only if the medium version passes by Thursday, Build 1

**Adds one of:** a version 2 of your format and a migration from version 1, with a test that the
old document is unchanged; or a checksum beside every save, with a test that a hand edit is refused.

**What it adds:** an idea from Lab U03-02, applied to your own format, with a decision log entry
about it.

**The risk:** the extra idea eats the time for the recovery plan, which is worth more.

### Scope calibration

| If you | Aim for |
|---|---|
| used the SCAFFOLDED Lab U03-02 starter, or missed a day this week | Small |
| had 13 of 17 on Lab U03-02 by Wednesday | Medium |
| finished Lab U03-02 on Thursday with time left, or did its EXTENDED option | Large |

---

## Grading · the 100-point project rubric

| Dimension | Points |
|---|---|
| Functionality | 25 |
| Code Quality | 20 |
| Documentation | 20 |
| Process | 15 |
| Demonstration | 10 |
| Polish | 10 |

### What each dimension means here

**Functionality, 25.** Requirements 1 through 9 work: the family catches together, the round trip is
identical, the right things survive, bad files are refused with a place, and a failed save leaves
the last good file whole.

**Code Quality, 20.** Scored on the five-dimension standard. Correctness: loaded objects obey the
same rules as typed ones. Security: no pickle, no class chosen by name, no private state written from
the file. Readability: every refusal says where and what. Performance: the size is checked before
reading, and the text is built once per save. Requirements Fit: the coordinator's "tell my people
what went wrong" is met.

**Documentation, 20.** `RECOVERY_PLAN.md` is specific to your program, and section 5 names real
checks. The README says what is saved, what is not, and why, and lets someone else run everything.

**Process, 15.** P1 through P4 on time, three decision log entries with rejected options, and a
commit at the end of every period.

**Demonstration, 10.** The five-minute demo below, rehearsed Thursday. Your partner fills in the
checklist and commits it with you. Your instructor watches part of at least one rehearsal during the
last 10 minutes of Thursday's Build 2, or asks you for items 3 and 4 at your desk on Friday.

**Polish, 10.** Clear names, no leftover `TODO`s, no save files or `.bak` files committed, tidy
output from `demo.py`.

---

## The five-minute demo

| Time | What |
|---|---|
| 0:00 to 0:45 | Show your error family. Say what one handler does differently because of one class. |
| 0:45 to 1:45 | Run `demo.py`: save, reload, and show what survived and what did not. |
| 1:45 to 2:45 | Load one of your bad files. Read the message aloud. Point at where it says the problem is. |
| 2:45 to 3:45 | Show the test that fails a save in the middle, and explain what is on disk afterward. |
| 3:45 to 5:00 | Read section 5 of your recovery plan. Name one check only a person can do, and why. |

### The demonstration checklist

Your partner copies this into `DEMO_CHECKLIST.md` and marks it during your rehearsal.

| # | | Points |
|---|---|---|
| 1 | A class in the family, and the different response it causes | 2 |
| 2 | Something saved and something not saved, each with a reason | 2 |
| 3 | A bad file refused with a message that says where | 2 |
| 4 | The failed-save test explained: what is on disk afterward | 2 |
| 5 | A check only a person can do, and why the program cannot | 2 |
| | **Total** | **10** |

---

## Submission checklist

- [ ] `python -m unittest` in `unit-03-persistence/` passes
- [ ] No `except Exception` in your package; no pickle import
- [ ] At least three bad files of your own, each with a test
- [ ] Tests and `demo.py` write only to temporary folders
- [ ] `RECOVERY_PLAN.md` has all seven sections
- [ ] `DEMO_CHECKLIST.md` is filled in by your partner
- [ ] Three or more Unit 3 decision log entries, each with a rejected option
- [ ] README: how to run, what is saved and why, what is not and why
- [ ] AI usage log complete
- [ ] No save files, `.bak`, or `.tmp` files committed; no personal information anywhere
- [ ] Committed and pushed inside the Friday window

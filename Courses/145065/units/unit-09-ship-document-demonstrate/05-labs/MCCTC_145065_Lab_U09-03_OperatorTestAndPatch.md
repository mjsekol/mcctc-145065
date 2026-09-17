# Lab U09-03 · The Operator Test and the Patch
## 145065 Object-Oriented Programming · Unit 9 · Week 18, Monday and Tuesday

**Files:** `lab-u09-03-files/`
**Time:** Part 1 in Monday Build 1 and Build 2. Part 2 in Tuesday Build 1.
**Due:** Part 1 at the end of Monday. Part 2 at the end of Tuesday Build 1.
**Competencies:** 5.6.17 (collect feedback and maintain), 5.6.14 (user acceptance testing),
5.7.2 (baseline), 5.7.3 (impact of changes), 5.4.5 (test with defined test cases), 1.2.5 (communicate
for an audience).

---

## Safety brief, read aloud before Part 1

- **Today uses the simulator on a lab PC. Nobody touches a Pi, a sensor, or a wire.**
- If your instructor sets up a station with the lab Pi, only your instructor runs it: ESD strap on, the
  Pi powered off before any wire moves, no mains voltage, and your signed Lab Acceptable Use and Safety
  Agreement on file.
- **The panel monitors. It never switches equipment on or off.** Nothing in an operator test controls a
  machine.
- **No personal data.** You never write a visitor's name, anywhere. You record a role: "a welding
  program student", "an office staff member".

---

## The scenario

A panel that makes sense to the person who built it can still send an operator the wrong way on the
first day. Your Unit 8 panel passed every test you wrote, because you wrote the tests. Today someone who
has never seen it uses it with nothing but your guide, and you watch without helping.

**You will run an operator test on your own panel, turn what you saw into decisions, and practice a
change request from finding to release on a small library where every result is known.**

Riverside Fabrication and its Line 3 are a composite, an invented shop.

---

## What is in the folder

| Path | What it is |
|---|---|
| `operator-test-kit/participant-script.md` | the one page you hold during a session, with the consent line |
| `operator-test-kit/task-cards.md` | five task cards, T1 to T5 |
| `operator-test-kit/control-script.md` | for your partner: which simulator mode, when |
| `operator-test-kit/session-record-sheet.md` | print one per person |
| `operator-test-kit/severity-sheet.md` | turns numbered lines into decisions |
| `sensor-service/` | the Line 3 simulator, copied from the course's HMI reference. Python standard library only. |
| `TileWords/` | a small practice library: the screen words, a guide, and 13 tests. Version 1.0.0. |

---

# Part 1 · The operator test · Monday

**You work in pairs, and you swap.** In one session you are the **facilitator**, at the desk beside the
visitor. In the next you are the **control partner** for your partner's panel, behind the divider.

**Step 1. Set up the station (before the first visitor).** Put your printed user guide on the desk. Start
the simulator and your panel as `control-script.md` says.
*You should see* your panel in full screen, CONNECTED, and a `200` from
`python sim_control.py --port 8700 read` in your partner's terminal.

**Step 2. Dry run with your partner (5 minutes).** Your partner plays the visitor and reads the consent
line back to you. You read T1 aloud. Your partner switches modes for T2 and T5. Do not skip this: a
control command that fails in front of a visitor wastes their time.
*You should see* the oven turn red about ten seconds after `mode drift`, and every tile go dark about
three seconds after `mode silent`. Then switch back to `mode normal`.

**Step 3. Run the session.** Follow `participant-script.md` exactly: consent line word for word, a yes
out loud, then T1 to T5. Write what they did on the left and what they said on the right, with the task
and a time.
*You should see* a record sheet with no name on it and at least eight lines.

**Step 4. Close.** Ask the closing question, write the answer word for word, thank them, and walk them
out.
*You should see* the "Did you break a rule?" box ticked honestly.

**Step 5. Reset.** Your partner runs `mode normal`. Put a fresh guide on the desk. Number the lines on
your sheet: `O1 L1`, `O1 L2`, and so on.
*You should see* CONNECTED again before the next visitor sits down.

**Step 6. Swap roles** and run your partner's session.

**Step 7. After the last session,** stop the simulator with Ctrl+C and check the port is free.
*You should see* `Stopped.` and no output from `netstat -ano | findstr :8700`.

**Step 8.** Type your record sheet into your project as `docs/OPERATOR_TEST.md`, using the exemplar
layout your instructor shows. Commit.

### Part 1 acceptance criteria

- [ ] At least one person who is **not in this class and not a programmer** used your panel with only
      your guide
- [ ] The consent line was read as written, and the sheet says so
- [ ] Every line is numbered, and no name appears anywhere
- [ ] The closing question's answer is recorded word for word
- [ ] Any rule you broke is recorded, with the task
- [ ] `docs/OPERATOR_TEST.md` committed

---

# Part 2 · From finding to release · Tuesday Build 1

**Why practice on a small library first.** A change request touches code, tests, documents, and
people. On a library of 60 lines you can see every one of those at once, and every result below is
known. Then you do the same on your own panel in Build 2.

## Practice: CR-18-01 on TileWords (20 minutes)

The practice finding, from a composite operator test on the practice panel:

| # | Finding | Evidence | Sessions | Severity |
|---|---|---|---|---|
| P1 | The operator read the tile word STALE and asked whether the number was still good. One said "stale like bread?" | three sessions | 3 of 4 | Medium |

**CR-18-01:** change the tile word STALE to NOT UPDATING. The meaning of the state does not change.

**Step 9.** Copy `TileWords/` into your repository as `oop-semester/unit-09-tilewords/`. Run the tests.

```
dotnet test Line3.Words.Tests
```

*You should see* `Passed: 13, Total: 13`. This is the baseline, version 1.0.0.

**Step 10.** Before you edit anything, write a prediction table in `unit-09-tilewords/CR-18-01.md`:
which files change, which tests fail, which documents change, and what version this becomes. Commit it.
*You should see* the commit in your history before any code change.

**Step 11.** Change **only** the code: in `ScreenWords.ForTile`, make `TileState.Stale` return
`"NOT UPDATING"`. Run the tests.
*You should see* `Failed: 2, Passed: 11`. Write down which two.

**Step 12.** Change `docs/screen-words.txt` to match. Run the tests.
*You should see* `Failed: 1, Passed: 12`.

**Step 13.** The last failing test expects the old word. A test is part of the specification, so
changing it is a decision: write one sentence in `CR-18-01.md` saying why this test's expectation
should change. Then change it. Run the tests.
*You should see* `Passed: 13, Total: 13`.

**Step 14.** Open `docs/USER_GUIDE.md`. Search it for STALE.
*You should see* the old word, still teaching operators the screen that no longer exists, with every
test passing. Write two sentences in `CR-18-01.md`: why `TheGuideUsesEveryScreenWord` passed, and what
that tells you about green tests.

**Step 15.** Fix the guide. Change the version in `Line3.Words.csproj`. Add an entry at the top of
`CHANGELOG.md` with the version, "Week 18 Tue", what changed for the operator, why, and why this version
number. Run the tests once more and commit.

**Step 16.** Fill in the **Actual** column of your prediction table. Mark every row you got wrong.

## Your own panel (15 minutes)

**Step 17.** Fill in `operator-test-kit/severity-sheet.md` from your own and your partner's record
sheets. At least two findings, each with line numbers, a session count, a severity, and a decision.

**Step 18.** For every finding you decided to fix in code, write a change request in your project's
`docs/CHANGE_IMPACT.md`, with a prediction table, **before** Build 2 starts. You make the change in
Build 2.

### Part 2 acceptance criteria

- [ ] `CR-18-01.md`: prediction committed before step 11, the sentence from step 13, the two sentences
      from step 14, and the Actual column
- [ ] TileWords: 13 of 13 tests pass, the guide no longer uses the old word, the version and change log
      agree
- [ ] Your severity sheet: two or more findings, every one citing lines
- [ ] A change request with a prediction table for every code fix, committed before Build 2

---

## If it breaks

**1. `sensor_service.py: error: the following arguments are required: --port`**
The simulator has no default port, on purpose. Add `--port 8700`.

**2. `Cannot start: port 8700 is already in use on 127.0.0.1; choose another or stop that program`**
Someone's simulator from the last session is still running. Stop it with Ctrl+C in its terminal. If you
cannot find it, use `--port 8701` for the simulator, as Unit 8's run-book does, and start your panel with
`--url http://127.0.0.1:8701`.

**3. `No answer from http://127.0.0.1:8700: timed out`** after `sim_control.py ... read`
The simulator is in `silent` mode, which is what T5 asks for. Run
`python sim_control.py --port 8700 mode normal`. Mode commands still work while it is silent.

**4. The tests fail with this, after step 11:**

```
Failed Line3.Words.Tests.ScreenWordsTests.TheWordsFileListsExactlyWhatTheCodeCanShow
Assert.Equal() Failure: Collections differ
                                           ↓ (pos 3)
Expected: [···, "ALARM HIGH", "ALARM LOW", "NOT UPDATING", "NO DATA", "WAITING", ···]
Actual:   [···, "ALARM HIGH", "ALARM LOW", "STALE", "NO DATA", "WAITING", ···]
```

That is the lab working. The code and the words file disagree at position 3. Step 12 fixes it. Read
the arrow: it points at the exact word.

**5. A visitor asks you what a word on the screen means.**
Do not answer. Say "What would you do if I were not here?" If they are still stuck after three minutes,
say "Let's move on," and record the task as not done. The question itself is a finding. Write it down.

---

## Stretch goal

Make `TheGuideUsesEveryScreenWord` impossible to fool. Write a new test that counts a screen word only
where it is **not** part of a longer screen word, so "NOT UPDATING" inside "DATA NOT UPDATING" does not
count. Run it against the guide from step 14 and confirm it fails there.

---

## Submission checklist

- [ ] `docs/OPERATOR_TEST.md` in your project, numbered lines, no names
- [ ] `unit-09-tilewords/` with `CR-18-01.md`, the changed code, words file, test, guide, csproj, and
      change log
- [ ] Severity sheet copied into `docs/OPERATOR_TEST.md`
- [ ] A change request in `docs/CHANGE_IMPACT.md` for each code fix
- [ ] Simulator stopped, port 8700 free
- [ ] No `bin` or `obj` folders committed

---

# Extended options

All four assess 5.6.17 and 5.7.3 on the same scale: evidence collected without helping, decisions tied
to that evidence, and a change whose impact was predicted before it was made.

## SCAFFOLDED

**Part 1: three tasks instead of five.** Run T1, T2, and T5 only. Your instructor sits in on your first
session and gives you one note afterward.

**Part 2: a filled prediction table.** Your instructor gives you the CR-18-01 prediction table with the
Files and Tests rows filled in. You fill in Documents and Version, and the whole Actual column. Steps
9 to 16 are otherwise the same.

## STANDARD

The lab as written.

## EXTENDED

**Close the gap step 14 found, for good.** Do the stretch goal. Then add a list of **retired** words to
`ScreenWords`, put STALE on it, and write a test that fails if the guide still uses any retired word.

The C# you need: a `static IReadOnlyList<string>` property, and LINQ's `Where` over it. For the
"longer word" test, look up `string.Replace(string, string, StringComparison)` on learn.microsoft.com
[VERIFY the page before you start]: remove every longer screen word from a copy of the guide before you
search it.

**How you know it works.** With the guide from step 14, both new tests fail and name the problem. With
the fixed guide, 15 of 15 pass.

## APPLIED

**Same skill, a different screen.** Run the same kind of test on something physical in this building
that a stranger must operate: the lab's 3D printer touchscreen, a copier, or the sign-in tablet at the
front desk. Write three task cards that follow the three rules in `task-cards.md`. Run them with one
person, record numbered lines, and fill in the severity sheet. You will not change the device. Your
decisions are "tell the owner," "change the sign next to it," or "no change," each with a reason.

**Why this version.** The method is about watching people, not about C#.

---

## Which version, three observable signals

| If you see | Hand them |
|---|---|
| At step 2, the student cannot get through the dry run without looking up which mode is which, or freezes reading the consent line | **SCAFFOLDED** for Part 1 |
| The student's prediction table in step 10 already names the guide and the version, and they reach step 16 with ten minutes left | **EXTENDED** for Part 2 |
| The student's panel is not finished enough to test, or they say "nothing will go wrong, it's obvious how it works" | **APPLIED**. A copier will change their mind in five minutes, and the record still counts while their panel is fixed. |

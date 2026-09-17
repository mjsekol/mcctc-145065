# Lab U8-05: The Alarm That Stays
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Wednesday

**Gate:** 3 (open tooling, AI allowed and logged), except step 2, which is done on paper.
**Duration:** Wednesday Build 1. Step 10 opens Build 2.
**Competencies:** 5.6.6 (design fail-safe outputs and processes), 5.3.5 and 5.3.7 (conditional and
selection structures in a state machine), 5.6.1 (a requirement: confirmation before an action), 5.6.14
(testing).

Files: `lab-u08-05-files/AlarmThatStays/`. `ObservableObject.cs` is copied unchanged from the course's
HMI anchor; `StateRules.cs` is Lab U08-03's file without `SideOf`. You write two latch rules and three
acknowledge methods.

**Riverside Fabrication is a composite.** No hardware, no service: `ShiftReplay` plays a scripted
stretch of an invented shift. **Acknowledging an alarm changes what the panel shows and records. It never
changes anything on a machine.**

---

## The scenario

An oven on Line 3 runs hot at the start of second shift. A minute later a cart clips the Pi's cable. If
the panel forgets the alarm because it lost the data, the next person to look sees a dark tile and no
warning, and nobody checks the oven. If a gloved hand brushing the screen can acknowledge an alarm, an
alarm can be "seen" by nobody.

## What you will build

The alarm memory: a small state machine that remembers an alarm until a person has acknowledged it and a
live value is back inside limits. Then the two-step acknowledge: a button that only opens a question, a
YES that acts, and a CANCEL that changes nothing.

---

## The latch

Four states:

| State | Means | Banner |
|---|---|---|
| `Clear` | nothing to report | none |
| `ActiveUnacked` | out of limits, nobody has acknowledged | UNACKNOWLEDGED ALARM |
| `ActiveAcked` | out of limits, a person acknowledged | ACKNOWLEDGED, NOT CLEARED |
| `ReturnedUnacked` | back inside limits, nobody acknowledged the alarm that happened | ALARM ENDED, NOT ACKNOWLEDGED |

Six rules, from the comment at the top of `AlarmLatch.cs`:

1. A live value out of limits makes the alarm active. If a person already acknowledged it, it stays
   acknowledged.
2. A live value back inside limits ends an active alarm. An acknowledged alarm then clears. An
   unacknowledged one becomes `ReturnedUnacked`.
3. **Stale or missing data changes nothing.**
4. Acknowledging an active alarm marks it acknowledged. It does not clear it.
5. Acknowledging a returned alarm clears it.
6. Acknowledging when there is nothing to acknowledge changes nothing.

---

## Starter code

```
AlarmThatStays/
  AlarmThatStays.sln
  Alarms/
    StateRules.cs              the state names (given)
    AlarmLatch.cs              YOU WRITE Next and Acknowledge
    ViewModels/
      ObservableObject.cs      (given)
      AlarmBoard.cs            AlarmTile and AlarmBoard; YOU WRITE three methods
  ShiftReplay/                 plays one stretch of a shift through your code (given)
  Alarms.SelfCheck/            23 checks (given)
```

The starter's `Next` never moves the latch, so no alarm is ever remembered. The starter's three
acknowledge methods do nothing.

Use an artifacts folder outside your repository on every `dotnet` command, for example
`--artifacts-path C:\build\lab05` [VERIFY a folder students may write to].

---

## Part 1: the memory

### Step 1. Build, run, check

```
dotnet build AlarmThatStays.sln --artifacts-path C:\build\lab05
dotnet run --project ShiftReplay --artifacts-path C:\build\lab05
dotnet test Alarms.SelfCheck --artifacts-path C:\build\lab05
```

**Observable result:** 0 warnings. `ShiftReplay` prints thirteen steps; at step 2 the oven reads 236.0 and
is in `Alarm`, the latch says `Clear`, and the banner column says `(none)`. The self-check reports
**8 passed, 15 failed**.

### Step 2. The latch table, on paper

Draw a table with the four latch states as rows and four columns: **live in limits**, **live out of
limits**, **stale or missing**, **acknowledge**. Fill all sixteen cells from the six rules.

**Observable result:** sixteen cells filled, before any code. Circle the cells that are "no change".

### Step 3. Read the board

Read `AlarmTile` and `Observe` in `AlarmBoard.cs`. Answer in your README: **what does the banner
follow, and what would a panel that bound the banner to the tile's `State` show when the cable is
pulled?**

**Observable result:** two sentences.

### Step 4. Write `Next`

A `switch` expression on `evaluated` is the natural shape: an arm for `SensorState.Alarm`, an arm for
`SensorState.Normal` (with its own `switch` on `current`), and a discard arm for everything else.
**Think about what the discard arm must return.**

**Observable result:** checks A01 through A04 pass.

### Step 5. Write `Acknowledge`

Rules 4 to 6.

**Observable result:** A05 passes. The self-check reports **18 passed, 5 failed**: only the acknowledge
checks that need your three methods still fail. `ShiftReplay` step 2 now shows `ActiveUnacked` and the
banner, and steps 3 and 4 keep them.

### Step 6. Break it on purpose, then restore

Change your discard arm to return `AlarmLatchState.Clear`. Run `ShiftReplay`.

**Observable result:** at step 3, `the Pi freezes`, the latch is `Clear` and the banner is gone. The
self-check fails four checks. Copy steps 2 to 4 into your README under `## An alarm is a memory`, and write
one sentence about what the next shift would know. Restore the discard arm.

---

## Part 2: acknowledging, in two steps

### Step 7. `RequestAcknowledge`

Only when `tile.CanAcknowledge` is true: call `ComposeConfirmation(tile)`, then open the question by
setting `PendingAcknowledge = tile`. **Change no latch.**

**Observable result:** K01 passes: the button opens the question and the latch is still
`ActiveUnacked`.

### Step 8. `ConfirmAcknowledge`

Close the question first: keep the pending tile in a local variable and set `PendingAcknowledge` to
`null`. If there was nothing pending, stop. Otherwise move that sensor's latch with your
`AlarmLatch.Acknowledge`. If it changed, store it in `latches`, call `tile.Show(tile.State, after)`, and
add a line to `Log`: `"<label>: alarm acknowledged and cleared"` or
`"<label>: alarm acknowledged, still active"`.

**Observable result:** the self-check reports **22 passed, 1 failed**. K02 still fails: CANCEL does not
close the question yet.

### Step 9. `CancelAcknowledge`

Close the question. Nothing else.

**Observable result:** **23 passed**. `ShiftReplay` prints this table:

| Step | What happens | State | Latch | Banner | Question |
|---|---|---|---|---|---|
| 1 | oven reads 212.0, live | Normal | Clear | (none) | closed |
| 2 | oven reads 236.0, live | Alarm | ActiveUnacked | UNACKNOWLEDGED ALARM | closed |
| 3 | the Pi freezes | Stale | ActiveUnacked | UNACKNOWLEDGED ALARM | closed |
| 4 | the cable is pulled | Missing | ActiveUnacked | UNACKNOWLEDGED ALARM | closed |
| 5 | operator presses ACKNOWLEDGE ALARM | Missing | ActiveUnacked | UNACKNOWLEDGED ALARM | OPEN |
| 6 | operator presses CANCEL | Missing | ActiveUnacked | UNACKNOWLEDGED ALARM | closed |
| 7 | ACKNOWLEDGE ALARM, then YES | Missing | ActiveAcked | ACKNOWLEDGED, NOT CLEARED | closed |
| 8 | cable back, oven reads 234.0, live | Alarm | ActiveAcked | ACKNOWLEDGED, NOT CLEARED | closed |
| 9 | oven reads 212.0, live | Normal | Clear | (none) | closed |
| 10 | oven reads 237.0, live | Alarm | ActiveUnacked | UNACKNOWLEDGED ALARM | closed |
| 11 | oven reads 212.0, nobody acknowledged | Normal | ReturnedUnacked | ALARM ENDED, NOT ACKNOWLEDGED | closed |
| 12 | ACKNOWLEDGE ALARM, then YES | Normal | Clear | (none) | closed |
| 13 | operator presses ACKNOWLEDGE ALARM | Normal | Clear | (none) | closed |

Step 13 opens nothing: there is nothing to acknowledge.

### Step 10. Move your work into the project

Copy `Next` and `Acknowledge` into the project's `Line3.Hmi.Core/AlarmLatch.cs`. Then write the same
three methods in the project's `PanelViewModel`. The shape is yours from steps 7 to 9; the project's
names differ:

- `RequestAcknowledge(SensorTileViewModel tile)`: the same as step 7.
- `ConfirmAcknowledge()`: close the question; if a tile was pending, call
  `monitor.Acknowledge(tile.Id, clock.UtcNow, out PanelEvent? acknowledged)`; when that returns `true`,
  `Log(acknowledged!)`; then `Refresh()`.
- `CancelAcknowledge()`: the same as step 9.

**Observable result:** every project test passes, including the three REQ07 tests. Commit.

---

## Acceptance criteria

- [ ] The paper latch table was filled before `Next` was written
- [ ] `dotnet test Alarms.SelfCheck` reports 23 passed
- [ ] `ShiftReplay` prints the table above
- [ ] Your README has the banner answer and `## An alarm is a memory`
- [ ] The project's tests all pass
- [ ] No `bin` or `obj` committed

---

## If it breaks

### 1. Missing data clears the alarm

```
Assert.Equal() Failure: Values differ
Expected: ActiveUnacked
Actual:   Clear
```

**Cause:** the discard arm returns `Clear` (or an arm for `Missing` does). Rule 3: stale or missing
changes nothing. A03, A04, K03, and K09 fail with it.

### 2. A switch expression with no discard arm

```
AlarmLatch.cs(53,101): warning CS8509: The switch expression does not handle all possible values of its input type (it is not exhaustive). For example, the pattern 'Line3.Hmi.Core.SensorState.Stale' is not covered.
```

Then, when a stale or missing state arrives:

```
System.Runtime.CompilerServices.SwitchExpressionException : Non-exhaustive switch expression failed to match its input.
```

**Cause:** no arm for stale or missing. Read the warning: the compiler told you before it ran. Your line
numbers will differ.

### 3. Acknowledging clears an active alarm

```
Assert.Equal() Failure: Values differ
Expected: ActiveAcked
Actual:   Clear
```

**Cause:** rule 4. Acknowledging says "I saw it". Only a live value back inside limits ends an alarm.

### 4. The button acknowledges straight away

```
Assert.Equal() Failure: Values differ
Expected: ActiveUnacked
Actual:   ActiveAcked
```

**Cause:** `RequestAcknowledge` moved the latch (or called `ConfirmAcknowledge`). K01 and K02 fail. The
button only opens the question.

### 5. CANCEL leaves the question open

K02 fails. **Cause:** `CancelAcknowledge` is still empty. In a window, the question would stay on screen
over everything.

---

## Stretch goal

Make the board announce every latch change with a C# event, so another part of the program (a shift
report, a stack light display, a test) can react the moment an alarm starts, is acknowledged, or clears,
without asking the board every second.

---

## Submission checklist

- [ ] Paper latch table in your README
- [ ] Self-check 23 of 23
- [ ] README sections complete
- [ ] Project tests all passing
- [ ] AI usage log updated if you used a model
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| The paper table has "Clear" in the stale or missing column after ten minutes | SCAFFOLDED |
| Steady progress, arguing about rule 2 | STANDARD |
| 23 of 23 early in Build 1 | EXTENDED |
| "Alarms are a factory thing" | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the paper table arrives with the stale or missing column filled. `Next` arrives with
  its three arms and the discard arm written; the student fills the `Alarm` and `Normal` arms.
- **Steps:** step 8 arrives with the "close the question first" lines written.
- **Checkpoints:** show the self-check after step 5 and after step 9.
- **Keep step 6.** Watching the banner vanish is the lesson.

**Acceptance criteria:** 23 of 23, `## An alarm is a memory`, the project tests.

**Grading:** same scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus the stretch goal as a requirement.

**Added requirement.** Add `public event EventHandler<LatchChangedEventArgs>? LatchChanged;` to
`AlarmBoard`, with an event-args class carrying the sensor id and the states before and after. Raise it
once for every latch move, from `Observe` and from `ConfirmAcknowledge`, and never when the latch stays
the same. Add a check that subscribes, plays alarm, missing, alarm, acknowledge, normal, and expects
exactly three announcements.

**Hint, not the answer.** Read "Handle and raise events" in the .NET documentation on
learn.microsoft.com [VERIFY the exact page]. The null-conditional `?.Invoke` raises an event safely when
nobody has subscribed.

**Acceptance criteria:** all STANDARD criteria; the new check passes.

**Grading:** same scale.

---

## APPLIED

**For the student who thinks alarms are a factory thing.** The same skill, somewhere else.

**Changed scenario.** A home water-leak sensor under a sink sends "wet" or "dry" to a phone app. If the
sensor's battery dies while it reads wet, the app must keep the leak warning up. Dismissing the warning
must ask first, and must not remove it while the sensor still reads wet.

**What you build.** The same four latch states and six rules, named for the leak app, with a sixteen-cell
table test, and a two-step dismiss with a CANCEL that changes nothing.

**Acceptance criteria:** the battery-dies-while-wet case keeps the warning; dismissing asks first; tests
for every cell of the table.

**Grading:** same scale. Requirements Fit is judged on rule 3.

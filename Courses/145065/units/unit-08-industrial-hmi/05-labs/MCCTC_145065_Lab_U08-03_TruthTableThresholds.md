# Lab U8-03: Truth Table and Thresholds
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Wednesday

**Gate:** 3 (open tooling, AI allowed and logged), except step 2, which is done on paper with no tools.
**Duration:** Wednesday Build 1 (Part 1) and Build 2 (Part 2).
**Competencies:** 5.3.1 (Boolean logic), 5.3.2 (truth tables), 5.3.3 and 5.3.4 (logical and relational
operators), 5.6.14 (testing), 1.2.7 (problem-solving and consensus building).

Files: `lab-u08-03-files/TruthTable/`, a solution with three projects. `PanelConfig.cs` is copied from
the course's HMI anchor with one method body removed. The thresholds file is the Line 3 file with the
oven's reason removed for your team to write.

**Riverside Fabrication is a composite.** Its limits are decisions the invented shop made, not figures
from a real process sheet. No hardware is used in this lab.

---

## The scenario

Every tile on the Line 3 panel will say one of four things: NORMAL, ALARM, STALE, or NO DATA. If the
rule that picks the word is wrong in even one of its sixteen cases, an operator will someday see an alarm
on a number that is not live, or a calm tile over a dead sensor. And every alarm limit on the screen must
be one the people who run the line agreed to and can explain.

## What you will build

The one function that picks a tile's state from four facts, a test that covers all sixteen cases, the
limit check, and your team's oven limit with a reason you can defend.

---

## The four facts and the four states

| Letter | Fact | True when |
|---|---|---|
| A | have an answer | the request worked and the reply parsed |
| K | sensor ok | this sensor reported `ok: true` with a value |
| F | fresh | the sample is not older than the stale limit |
| W | within limits | the value is inside its documented limits |

| State | The course's definition |
|---|---|
| MISSING | there is no current value: no answer, or the sensor reported `ok: false` |
| STALE | the panel has a value, but it is not fresh, so it is not live |
| ALARM | a **live** value outside its documented limits |
| NORMAL | a **live** value inside its documented limits |

A value exactly on a limit is inside.

---

## Starter code

```
TruthTable/
  TruthTable.sln
  Rules/
    StateRules.cs           the state names (given)
    StateRules.Truth.cs     YOU WRITE Decide
    PanelConfig.cs          the thresholds loader; YOU WRITE SensorThreshold.Check
  RulesDemo/
    Program.cs              prints your truth table and your limits (given)
    thresholds.json         YOUR TEAM WRITES the oven's reason
  Rules.SelfCheck/
    TruthTableChecks.cs     checks Decide against the definitions (given)
    LimitChecks.cs          checks Check and your thresholds file (given)
    MyTruthTableTests.cs    YOU FINISH: all sixteen rows
```

The starter's `Decide` answers Missing for everything, and its `Check` answers Within for everything.
Both are the answers that are never dangerous and never useful.

Use an artifacts folder outside your repository on every `dotnet` command, for example
`--artifacts-path C:\build\lab03` [VERIFY a folder students may write to].

---

## Part 1: Build 1

### Step 1. Build, run, check

From `TruthTable/`:

```
dotnet build TruthTable.sln --artifacts-path C:\build\lab03
dotnet run --project RulesDemo --artifacts-path C:\build\lab03
dotnet test Rules.SelfCheck --artifacts-path C:\build\lab03
```

**Observable result:** the demo prints sixteen rows that all say `Missing`, then
`16 rows: Normal 0, Alarm 0, Stale 0, Missing 16`, then the limits, with every boundary value reading
`Within` and the oven's reason flagged as the placeholder. The self-check reports **11 passed,
11 failed**. Eleven pass by accident: "always Missing" and "always Within" happen to be right for them.

### Step 2. The truth table, on paper, no tools

Draw a table with columns A, K, F, W, and State, and sixteen rows: A, K, F, W counting from all false to
all true, the way a binary number counts. Fill the State column from the definitions above, one row at a
time.

**Observable result:** sixteen rows filled in, before any code. Count each state and write the four
counts at the bottom.

### Step 3. Four expressions

In the comment block at the top of `StateRules.Truth.cs`, write each state as a Boolean expression over
A, K, F, W, using `!`, `&&`, and `||`. Check each one against three rows of your paper table.

**Observable result:** four expressions in the comment. Exactly one of them is true for any row.

### Step 4. Write `Decide`

Turn the expressions into `if` statements. **The order of the checks is the design.** Ask yourself:
can a value you do not have be stale? Can a value that is not live be judged against a limit?

**Observable result:** `RulesDemo` prints your sixteen rows and a count line that matches your paper
counts. Self-checks T01 through T04 pass.

### Step 5. Your sixteen-row test

In `MyTruthTableTests.cs`, add fourteen `[InlineData]` rows **from your paper table**, not from your
code. A test copied from the code it tests proves nothing.

**Observable result:** self-check T05 passes, and your own `EveryRow` theory shows sixteen passing cases.

### Step 6. Break it on purpose, then restore

Move your limit check above your freshness check, so a stale value outside its limits comes out as an
alarm. Run the self-check.

**Observable result:** two failures. One reads:

```
Assert.Equal() Failure: Values differ
Expected: Stale
Actual:   Alarm
```

Under a README heading `## Order is the design`, write one sentence: what would an operator see, and why
is it wrong? Then restore the order and confirm the failures are gone.

### Step 7. Write `SensorThreshold.Check`

In `PanelConfig.cs`, write `Check(double value)`. `Low` and `High` are `double?`: either may be missing,
and a missing limit is never checked. Below the low limit is `BelowLow`, above the high limit is
`AboveHigh`, and everything else, including a value exactly on a limit, is `Within`.

**Observable result:** self-checks L01 through L04 pass, and the self-check reports **35 passed,
1 failed**: L05 waits for your team's reason. `RulesDemo` prints, for the oven,
`189.9 -> BelowLow   190.0 -> Within   230.0 -> Within   230.1 -> AboveHigh`. Commit.

---

## Part 2: Build 2, agreeing on a limit

A limit is an agreement between the people who run the line, the people who maintain it, and the people
who pay for scrap. Today your team makes one.

### Step 8. Read the file and its rules

Open `RulesDemo/thresholds.json`. Read the press and coolant reasons: they are the model. Read the loader's
rules in `PanelConfig.Parse`: every sensor needs at least one limit, low must be below high, and every
reason must be a real sentence of at least 20 characters.

**Observable result:** you can say what the panel does with a thresholds file that breaks one rule.
(It refuses to start and says why.)

### Step 9. Gather evidence

Start the simulator on port 8700 in normal mode and run your Lab U08-02 reader for 30 polls. Record the
lowest and highest oven value you see. Then switch to drift for ten polls and record how fast the oven
climbs.

**Observable result:** a normal range and a climb rate in your notes, with the command you ran.

### Step 10. The threshold meeting

Pair up with another pair. Take turns. For **the other pair's** oven limit, one of you is the operator
and one is the maintenance lead. The pair proposing the limit follows these five steps out loud:

1. **State the problem the limit prevents.** "Parts discolor above 230 C" is a problem. "230 seems high"
   is not.
2. **Bring the evidence.** The normal range and the climb rate from step 9. Any process range you were
   given.
3. **Propose a number and its reason**, in one sentence an operator could read.
4. **Argue both sides.** A tighter limit catches problems sooner and raises more false alarms. A looser
   limit is quieter and catches problems later. Say which cost is worse on this line.
5. **Agree, or record the disagreement.** Write who agreed. If you did not agree, write the two
   positions and what evidence would settle it.

The operator and the maintenance lead each ask at least one question. Listen to the whole answer before
replying.

**Observable result:** a decision, or a recorded disagreement, for both pairs' oven limits.

### Step 11. Write it into the file

Replace the oven's placeholder reason in `thresholds.json` with your team's sentence. Change the limits
only if your meeting agreed to.

**Observable result:** `dotnet test Rules.SelfCheck` reports **36 passed**. If L06 fails, your limits
alarm during normal running: go back to step 10.

### Step 12. Defend it in writing

Create `docs/THRESHOLDS.md` in your project repository from the project template. For the oven: the
problem, the evidence, the number and its reason, the strongest case for a tighter limit, the strongest
case for a looser one, the decision, who agreed, and what new evidence would make you change it.

**Observable result:** every heading in the template is filled.

### Step 13. Move your work into the project

Copy your `Decide` into the project's `Line3.Hmi.Core/StateRules.Truth.cs`, your `Check` into the
project's `PanelConfig.cs`, and your `thresholds.json` over the project's
`Line3.Hmi.Panel/thresholds.json`. Keep the project's `service_url`. Run the project's tests.

**Observable result:** in the project, `REQ13_EveryLimitHasAReasonYourTeamWrote`,
`REQ13_TheSimulatorsNormalRunningIsInsideYourLimits`, and `REQ13_AValueOnALimitIsInsideAndOneStepPastIsOutside`
pass. Commit both repositories' work.

---

## Acceptance criteria

- [ ] The paper truth table was finished before `Decide` was written
- [ ] `dotnet test Rules.SelfCheck` reports 36 passed
- [ ] `RulesDemo` prints `16 rows: Normal 1, Alarm 1, Stale 2, Missing 12`
- [ ] Your README has `## Order is the design`
- [ ] `thresholds.json` has your team's oven reason; `docs/THRESHOLDS.md` defends it
- [ ] Your work is pasted into the project and its three REQ13 tests pass
- [ ] No `bin` or `obj` committed

---

## If it breaks

### 1. An enum value without its type name

```
MyTruthTableTests.cs(30,41): error CS0103: The name 'Normal' does not exist in the current context
```

**Cause:** `InlineData` needs `SensorState.Normal`, not `Normal`.

### 2. A row with four values instead of five

```
MyTruthTableTests.cs(30,6): error xUnit1009: InlineData values must match the number of method parameters. Remove unused parameters, or add more data for the missing parameters. (https://xunit.net/xunit.analyzers/rules/xUnit1009)
```

**Cause:** a row is missing one of A, K, F, W, or the expected state. xunit's analyzer reports it as a
build error. A second message, `xUnit1010`, names the value that no longer fits its parameter.

### 3. Using `.Value` on a limit that is not there

```
System.InvalidOperationException : Nullable object must have a value.
```

**Cause:** `Low.Value` on the press sensor, which has no low limit. The build also warned you:
`warning CS8629: Nullable value type may be null.` Use `Low is double low && value < low`.

### 4. A value on the limit is an alarm

```
Assert.Equal() Failure: Values differ
Expected: Within
Actual:   AboveHigh
```

**Cause:** `>=` where the course's rule needs `>`. "Above 230" and "230 or above" are different alarms.

### 5. The thresholds file is refused

```
thresholds.json was refused: Sensor "oven-temp" has no reason for its limits. Write why these numbers, in a sentence an operator can read.
```

**Cause:** the reason is under 20 characters. The loader cannot check that a reason is true; it can check
that one was written.

---

## Stretch goal

Write the four expressions a second way, using De Morgan's laws, so that MISSING has no `||` in it.
Prove on paper that both versions agree in all sixteen rows.

---

## Submission checklist

- [ ] Paper truth table photographed or typed into your README
- [ ] Self-check 36 of 36
- [ ] `## Order is the design` in the README
- [ ] `thresholds.json` and `docs/THRESHOLDS.md` committed
- [ ] The project's three REQ13 tests pass
- [ ] AI usage log updated if you used a model
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| The paper table has rows missing or repeated after ten minutes | SCAFFOLDED |
| The paper table is done and the student is arguing about row order | STANDARD |
| 22 of 22 before Build 1 ends | EXTENDED |
| "When would anyone outside a factory need a truth table?" | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the paper table arrives with the A, K, F, W columns filled and the first four State
  cells filled. `MyTruthTableTests.cs` arrives with eight rows.
- **Steps:** step 3 gives MISSING's expression; the student writes the other three.
- **Checkpoints:** show the paper table to the instructor before step 4.
- **Keep step 6 and all of Part 2.** The order and the meeting are the competencies.

**Acceptance criteria:** 36 of 36, the README sentence, the thresholds file and document.

**Grading:** same scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus sixteen rows that are generated instead of typed, and still checked against
an independent source.

**Added requirement.** Write a second theory that gets its sixteen rows from a method instead of sixteen
`InlineData` attributes, and gets each expected state from your **paper table's state column** written as
a sixteen-character string, not from any expression. Explain in a comment why generating the expected
answers from the same logic as `Decide` would prove nothing.

**Hint, not the answer.** Read xunit's documentation on `MemberData` and `TheoryData`
(`https://xunit.net/docs/getting-started/netcore/cmdline` is the getting-started page; find the data
attributes from there) [VERIFY the page], and notice that a row number from 0 to 15, written in binary,
is exactly A, K, F, W.

**Acceptance criteria:** all STANDARD criteria; the new theory runs sixteen cases and passes.

**Grading:** same scale.

---

## APPLIED

**For the student who asks where else this matters.** The same skill, somewhere else.

**Changed scenario.** The school greenhouse club has a soil-moisture sensor for each bed and a screen in
the hallway. The screen must say WATER NOW, OK, CHECK SENSOR (the reading is old), or NO READING, from
four facts: the sensor answered, it reported a value, the value is recent, and the value is above the dry
limit. The club must agree on the dry limit.

**What you build.** A `Decide` for the greenhouse states with a sixteen-row test, a `Check` for a
one-sided dry limit, and a `limits.md` that records the club's meeting: the problem (plants wilting over
long weekends), the evidence (invented readings, no names), both sides, and the decision.

**Acceptance criteria:** sixteen passing rows; a one-sided limit that treats a value on the limit as OK;
the meeting record with both sides argued.

**Grading:** same scale. Requirements Fit is judged on whether "the reading is old" is checked before the
dry limit.

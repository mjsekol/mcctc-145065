# Lab U06-03: Two Sources, One Contract
## 145065 Object-Oriented Programming · Unit 6 · Week 12

**Gate:** 3 (open tooling). **Duration:** four 35-minute Build 1 blocks, Week 12 Monday through
Thursday. **Competencies:** 5.3.12 (classes, objects, and methods), 5.5.5 (naming and comments),
5.1.4 and 5.1.6 (object-oriented design, strengths and weaknesses of approaches), 5.3.7 (switch),
5.6.13 (static analysis), 5.7.1 and 5.7.3 (interface control, impact of changes), 5.5.1 (data
validation), 5.4.4 and 5.4.5 (test cases).

Riverside Fabrication is a composite: an invented small metal fabrication shop. All readings are
invented.

---

## The scenario

The Line 3 panel will read oven temperatures from a Raspberry Pi in Unit 8. Until then, the team
tests the panel's logic with readings replayed from a script and readings pasted from old log files.
The panel code must not care where a reading came from, must never show a missing reading as a
number, and must survive a teammate adding a feature nobody thought through.

## What you will build

A small C# library, `Line3.Monitor`, grown one concept a day: a locked-down `Reading`, an interface
kept by two very different sources, a classifier built on `switch`, and a build that treats warnings
as errors.

---

## Starter code

The files are in `05-labs/lab-u06-03-files/`. Copy the whole folder.

| Path | What it is |
|---|---|
| `Line3.Monitor.sln` | The library and its tests. `Intruder` is not in it, on purpose |
| `Line3.Monitor/Reading.cs` | Part 1. Works, and leaks |
| `Line3.Monitor/ShiftReport.cs` | Given. Builds with two warnings. **Leave it alone until Part 4** |
| `Line3.Monitor.Tests/ReadingTests.cs` | Part 1 tests, switched on |
| `Line3.Monitor.Tests/SourceTests.cs.txt` | Part 2 tests, switched off |
| `Line3.Monitor.Tests/ClassifierTests.cs.txt` | Part 3 tests, switched off |
| `Line3.Monitor.Tests/ReportTests.cs.txt` | Part 4 tests, switched off |
| `Intruder/` | A separate project that uses the library the wrong way |

To switch a test file on, rename it from `.cs.txt` to `.cs`. Never edit a test file.

The starter's `Reading.cs`:

```csharp
public class Reading
{
    public string SensorId;
    public double? Value;
    public int Sequence;

    public Reading(string sensorId, double? value, int sequence)
    {
        SensorId = sensorId;
        Value = value;
        Sequence = sequence;
    }

    public bool IsMissing => Value == null;
}
```

Create `LAB_LOG.md` in the folder. Every error and every result this lab asks you to record goes in
it, pasted from your own terminal.

---

## Part 1: Monday · Lock it down

### Step 1. Build and test the starter

```
dotnet build Line3.Monitor.sln
dotnet test Line3.Monitor.sln
```

**Observable result:** the build succeeds with two warnings, CS8618 and CS8602, both in
`ShiftReport.cs`. Leave them. The tests report 6 failed and 3 passed.

### Step 2. Run the intruder

```
dotnet run --project Intruder
```

**Observable result:**

```
id '', value NaN, sequence -1, missing False
```

A reading with no sensor, a value that is not a number, a negative sequence, and a claim that it is
not missing. Paste the line into `LAB_LOG.md` and write one sentence about what a panel would show.

### Step 3. Validate in the constructor

Refuse a blank sensor id, a value that is NaN or infinite, and a negative sequence. A `null` value is
allowed: it is how a missing reading is spelled. Throw `ArgumentException` or
`ArgumentOutOfRangeException`.

**Observable result:** 8 of 9 tests pass. `P1_06_no_public_fields` still fails.

### Step 4. Replace the fields

Turn the three public fields into get-only properties. Nothing outside the constructor may set them.
Choose whether `Reading` should be `sealed`, and write why in one sentence.

**Observable result:** all 9 `ReadingTests` cases pass.

### Step 5. Run the intruder again

```
dotnet build Intruder
```

**Observable result:** the build fails with three CS0200 errors, one per assignment. Paste all three.
In one sentence, say why the message says "read only" even though you could have written
`private set`. The lesson notes, worked example 3, explain it.

### Acceptance criteria, Part 1

1. All 9 `ReadingTests` cases pass
2. `Intruder` no longer builds, and its three errors are in `LAB_LOG.md`
3. The step 2 output and your sentence about it are in `LAB_LOG.md`

---

## Part 2: Tuesday · One contract, two sources

### Step 6. Switch on the tests

Rename `SourceTests.cs.txt` to `SourceTests.cs` and build.

**Observable result:** the build fails. The first error is:

```
SourceTests.cs(13,30): error CS0246: The type or namespace name 'IReadingSource' could not be found (are you missing a using directive or an assembly reference?)
```

That list is your to-do list for today.

### Step 7. The interface

Create `Line3.Monitor/IReadingSource.cs`:

- `string Name { get; }`, a human name for the source
- `Reading? Next()`, the next reading, or `null` when the source has nothing more

Write a comment that says the difference between `Next()` returning `null` and a reading whose
`Value` is `null`.

### Step 8. `ScriptedSource`

`ScriptedSource(string name, string sensorId, IEnumerable<double?> values)` replays the values in
order. The first reading has sequence 1. After the last value, `Next()` returns `null` every time it
is called. Copy the values when the object is built, so a caller who changes their list later cannot
change the script.

Before you write `Next()`, build once with only `Name` written.

**Observable result:** `error CS0535: 'ScriptedSource' does not implement interface member
'IReadingSource.Next()'`. Paste it. Then write `Next()`.

### Step 9. `LogLineSource`

`LogLineSource(string name, IEnumerable<string> lines)` reads lines shaped like `oven-temp,212.4`.

- A line that does not split into exactly two parts becomes a reading with the sensor id
  `unreadable` and a `null` value.
- A value that does not parse, or parses to NaN or infinity, becomes a `null` value.
- The sequence is the line number, from 1.
- Parse with `double.TryParse(text, NumberStyles.Float, CultureInfo.InvariantCulture, out double v)`,
  so `212.4` means the same thing on every lab machine. Add `using System.Globalization;`.

**Observable result:** the P2_01 to P2_04 cases pass. If `oven-temp,1e999` fails, read "If it breaks"
number 3.

### Step 10. The monitor

Create `Line3.Monitor/ShiftMonitor.cs` with a record and a static class:

```csharp
public sealed record MonitorSummary(int Count, int Missing, double? Highest);
```

`ShiftMonitor.Summarize(IReadingSource source, int maxReadings)` pulls readings until the source is
finished or `maxReadings` have been read, and counts them, counts the missing ones, and keeps the
highest real value. `ShiftMonitor` may not mention `ScriptedSource` or `LogLineSource` anywhere.

**Observable result:** every `SourceTests` case passes. Commit.

### Acceptance criteria, Part 2

1. Every `SourceTests` case passes, including the contract test that runs against both sources
2. `ShiftMonitor.cs` never names either source class
3. The CS0535 line is in `LAB_LOG.md`

---

## Part 3: Wednesday · The classifier

### Step 11. Switch on the tests

Rename `ClassifierTests.cs.txt` to `ClassifierTests.cs`.

### Step 12. `Level` and `Classify`

Create `Line3.Monitor/Classifier.cs` with:

```csharp
public enum Level
{
    Missing,
    Normal,
    Warning,
    Alarm,
}
```

and a static class `Classifier` with
`public static Level Classify(Reading reading, double warnAt, double alarmAt)`. Refuse limits where
`warnAt` is not below `alarmAt`. Then return a **switch expression** on `reading.Value`.

Write the arms with the warning test first and the alarm test second, and run the tests.

**Observable result:** it builds with no warning, and three test cases fail, including:

```
Failed Line3.Monitor.Tests.ClassifierTests.P3_01_classify_uses_the_limits_in_the_right_order(value: 240, expected: Alarm)
Assert.Equal() Failure: Values differ
Expected: Alarm
Actual:   Warning
```

Paste it, write one sentence on why the compiler did not catch the order, and fix the order.

### Step 13. `Label`

`public static string Label(Level level)` is a **switch statement** returning `"MISSING"`, `"ok"`,
`"WARNING"`, or `"ALARM"`. Its `default` throws `ArgumentOutOfRangeException`, because an enum
variable can hold a number that is not one of its names.

### Step 14. `Levels`

Add `ShiftMonitor.Levels(IReadingSource source, double warnAt, double alarmAt)`, which returns the
level of every reading until the source is finished.

**Observable result:** every `ClassifierTests` case passes. Commit.

### Acceptance criteria, Part 3

1. Every `ClassifierTests` case passes, including 240.0 and 9999.0 as `Alarm` and `(Level)42` refused
2. `Classify` is a switch expression and `Label` is a switch statement
3. The step 12 failure and your sentence are in `LAB_LOG.md`

---

## Part 4: Thursday · The build reviews you

### Step 15. Switch on the report tests, warnings still off

Rename `ReportTests.cs.txt` to `ReportTests.cs` and run the tests.

**Observable result:** both `ReportTests` cases fail with `System.NullReferenceException`. The build
has been warning you about this all week.

### Step 16. Warnings become errors

In `Line3.Monitor/Line3.Monitor.csproj`, inside `<PropertyGroup>`, add:

```xml
<TreatWarningsAsErrors>true</TreatWarningsAsErrors>
```

Build.

**Observable result:** the build fails:

```
ShiftReport.cs(15,12): error CS8618: Non-nullable property 'Title' must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring the property as nullable.
ShiftReport.cs(34,36): error CS8602: Dereference of a possibly null reference.
```

### Step 17. Fix both, for real

Fix the constructor so `Title` holds the title. Fix `Render` so a report with no note says
`Note: none`. **Do not use `!` and do not use `#pragma`.** Either one makes the build pass and leaves
one of the crashes in place.

**Observable result:** 0 warnings, 0 errors, and all 37 tests pass.

### Step 18. Change the contract, and read the impact

Add one member to `IReadingSource`:

```csharp
int Remaining { get; }
```

Build.

**Observable result:** two CS0535 errors, one for each source. The order may differ from your
neighbor's. Paste both.

### Step 19. Decide, and write `IMPACT.md`

In `IMPACT.md`, write:

1. the proposed change, as code
2. the error list, pasted
3. which classes broke, which did not, and why `ShiftMonitor` is not on the list
4. your decision: keep the member and implement it in both sources, or remove it, with your reason.
   Think about the live Raspberry Pi source that arrives in Unit 8.

Then make the build match your decision.

**Observable result:** the build is back to 0 warnings and 0 errors, and all 37 tests pass. Commit
and push.

### Step 20. Now do steps 16 and 18 on your port

Turn on `TreatWarningsAsErrors` in your port's library and fix what appears. Add one member to your
port's interface, paste the list into your port's `IMPACT.md`, and decide.

### Acceptance criteria, Part 4

1. The library builds with warnings as errors: 0 warnings, 0 errors
2. No `!` operator and no `#pragma` anywhere in `Line3.Monitor`
3. All 37 tests pass
4. `IMPACT.md` has all four parts, and the build matches the decision

---

## Acceptance criteria, full lab

- [ ] `dotnet test Line3.Monitor.sln` reports 37 passed, 0 failed
- [ ] `dotnet build Intruder` fails with three CS0200 errors
- [ ] `TreatWarningsAsErrors` is on, and the build is clean
- [ ] No public fields, no `!`, no `#pragma` in `Line3.Monitor`
- [ ] `ShiftMonitor` works through `IReadingSource` only
- [ ] A missing reading is never shown or counted as a number anywhere
- [ ] `LAB_LOG.md` has every pasted result the steps ask for, and `IMPACT.md` is complete
- [ ] No test file edited; `bin/` and `obj/` not committed

---

## If it breaks

These were recorded by making each mistake in the starter or in a finished library.

### 1. A type the tests need does not exist yet

```
SourceTests.cs(13,30): error CS0246: The type or namespace name 'IReadingSource' could not be found (are you missing a using directive or an assembly reference?)
```

**Cause:** a test file was switched on before the code it tests exists, or the new file's
`namespace` line is not `namespace Line3.Monitor;`. Write the type, in that namespace.

### 2. A class promises the interface and skips a member

```
ScriptedSource.cs(6,38): error CS0535: 'ScriptedSource' does not implement interface member 'IReadingSource.Next()'
```

**Cause:** exactly what it says. The line and column point at the class declaration, not at the
missing member, because the member does not exist to point at.

### 3. `oven-temp,1e999` or `oven-temp,NaN` fails

```
Failed Line3.Monitor.Tests.SourceTests.P2_04_a_value_that_is_not_a_finite_number_is_missing(line: "oven-temp,1e999")
System.ArgumentOutOfRangeException : a reading must be a finite number or null (Parameter 'value')
Actual value was ∞.
```

**Cause:** `double.TryParse` succeeds on `"NaN"` and turns `"1e999"` into infinity. Your
`LogLineSource` passed that value to `Reading`, and your Part 1 validation refused it, which is the
validation doing its job. Check `double.IsFinite` in the source and make the value `null` instead.

### 4. The monitor stops at the limit, and a reading vanishes

```
Failed Line3.Monitor.Tests.SourceTests.P2_06_the_monitor_stops_at_the_limit
Assert.NotNull() Failure: Value is null
```

**Cause:** the loop asks the source for a reading **before** checking the limit, so it takes one
reading too many and throws it away. Check `count < maxReadings` first. `&&` stops at the first false.

### Also likely in Part 4: the build still fails after you "fixed" it

If you added a `!`, the build passes and a Part 4 test still throws `NullReferenceException`. That is
step 17's warning, happening.

Your line and column numbers will match your own files.

---

## Stretch goal

**Part A.** Write a third source, `RandomWalkSource`, that gives a fixed number of readings, starting
at 200 and moving up or down by up to 2 degrees each time, using `new Random(seed)` so a test can
repeat it. The provided contract test expects three specific values, so it cannot run against a
random source. Write your own in `MySourceTests.cs`, with a class named `MySourceTests`: a theory that
runs against all three sources and checks only the two promises, a non-blank name and `null` forever
after the last reading.

**Part B.** In `LAB_LOG.md`, answer in four sentences: your third source needed no change to
`ShiftMonitor`. Which feature of C# made that true, and what would the Python version of the same
design have had to trust instead?

---

## Submission checklist

- [ ] 37 tests pass, and `Intruder` fails to build on purpose
- [ ] `LAB_LOG.md` and `IMPACT.md` complete
- [ ] Port: warnings as errors on, and its `IMPACT.md` exists
- [ ] `git status` clean, pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension
scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Part 1 not finished by the end of Monday's Build 1, or unsure what `get` means | SCAFFOLDED |
| Each day's tests going green inside the block | STANDARD |
| Part 2 finished with ten minutes left on Tuesday, or asked about `internal` | EXTENDED |
| Asked why a panel would ever read from a pasted log | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Part 1:** `Reading`'s properties are given. The student writes the three constructor checks.
- **Part 2:** `ScriptedSource` is given complete. The student writes the interface, `LogLineSource`,
  and `Summarize`.
- **Part 3:** `Label` is given. The student writes `Classify` and `Levels`.
- **Part 4 is unchanged.** Warnings as errors and the impact list are the point of Thursday.
- **Checkpoints:** show you the test count at the end of each Build 1.

**Acceptance criteria:** 37 tests pass; `Intruder` fails with three CS0200 errors; `IMPACT.md` is
complete.

**Grading:** same 100-point scale, judged against this version's list. A complete SCAFFOLDED
submission earns the same grade as a complete STANDARD one.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one addition that needs something you have not been taught in depth.

**Added requirement.** Move the finite-number check that `Reading` and `LogLineSource` both need into
one helper class, `Checks`, that every file in `Line3.Monitor` can use and no other project can. Then
prove it: add one line to `Intruder` that calls it, and paste the error.

**Hint, not the answer.** One of Monday's four access modifiers means "this project only." Read the
C# language reference page on access modifiers on learn.microsoft.com **[VERIFY]** the page address,
and look at what it says about assemblies.

**Acceptance criteria:** all STANDARD criteria, plus `Checks` used by both classes, and the
`Intruder` error pasted. On the build machine, with the call on line 7 of
`Intruder/Program.cs`, that error read
`Program.cs(7,19): error CS0122: 'Checks' is inaccessible due to its protection level`.

**Grading:** same scale.

---

## APPLIED

**For the student who asks why a panel would read from a pasted log.**

**Changed scenario.** Pick a feed you understand: a game's score events, a bus tracker's arrival
times, or a heart-rate strap during practice. Invent all data. **Use no real personal data about
anyone, including yourself.**

**What you build.** The same shape with your own names: a locked-down value class, an interface kept
by a scripted source and a text-line source, a classifier with at least three levels plus a missing
level, and the Part 4 steps. Write your own tests: at least one contract test that runs against both
sources, and one test above your highest limit.

**Acceptance criteria:** all STANDARD criteria in your domain, and `IMPACT.md` about your own
interface.

**Grading:** same scale. Requirements Fit is judged on whether "missing" is handled as carefully as
the Line 3 version requires.

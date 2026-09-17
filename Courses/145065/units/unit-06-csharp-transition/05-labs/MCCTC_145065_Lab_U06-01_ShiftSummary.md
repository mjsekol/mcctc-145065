# Lab U06-01: Shift Summary
## 145065 Object-Oriented Programming · Unit 6 · Week 11

**Gate:** 3 (open tooling). **Duration:** three 35-minute Build 1 blocks, Week 11 Monday, Tuesday,
and Wednesday. **Competencies:** 5.1.7 (compilers and interpreters), 5.4.3 (compile a working
program), 5.4.6 (correct syntax errors), 5.2.1 (primitive types), 5.2.3 (arithmetic operations),
2.3.2 (convert between number bases), 5.3.6 (repetition control structures).

Riverside Fabrication is a composite: an invented small metal fabrication shop. The readings in this
lab are invented.

---

## The scenario

At the end of every shift, the Line 3 lead writes a summary by hand from the press counter and the
oven chart. It takes twenty minutes and the arithmetic is wrong about once a week. The lead wants a
program that prints the summary from the shift's numbers.

## What you will build

A C# console program that prints Press 1's uptime and box count, the press status word in three
number bases, and a summary of the oven's first thirty minutes.

**Monday you build and break it. Tuesday you do the arithmetic. Wednesday you write the loops.** One
new idea per day, because a program with a type bug and a loop bug at the same time is very hard to
debug.

---

## Starter code

The files are in `05-labs/lab-u06-01-files/ShiftSummary/`. Copy the whole folder into your own
repository.

| File | What it is |
|---|---|
| `ShiftSummary.csproj` | The project file. It targets `net8.0` |
| `ShiftData.cs` | The shift's numbers. **Do not edit it** |
| `Program.cs` | Your code goes here |

`Program.cs` builds and runs right now. It does nothing useful yet:

```csharp
// Program.cs
// Lab U06-01: Shift Summary. Prints an end-of-shift summary for Line 3.
//
// This file builds and runs right now. It does not calculate anything yet.
// Replace each TODO with real lines, one part per day.

using ShiftSummary;

Console.WriteLine("SHIFT SUMMARY - LINE 3");
Console.WriteLine("----------------------");

// ----- Part 2, Tuesday: types and arithmetic -------------------------------
// TODO 1: Press 1 uptime as a percent, stored in a double.
// TODO 2: How many full boxes the parts fill, and how many parts are left over.
// TODO 3: The status word printed three ways: decimal, hexadecimal, binary.

// ----- Part 3, Wednesday: loops ---------------------------------------------
// TODO 4: Average and highest oven temperature, with a foreach loop.
// TODO 5: The first minute out of tolerance, with a for loop.
// TODO 6: Minutes in tolerance before the first drift, with a while loop.
// TODO 7: Minutes out of tolerance, and the percent of minutes in tolerance.

Console.WriteLine("Nothing is calculated yet.");
Console.WriteLine($"Oven readings on file: {ShiftData.OvenTempsC.Length}");
```

`ShiftData.cs` gives you these names, all under `ShiftData.`:

| Name | Type | Meaning |
|---|---|---|
| `SetpointC` | `double` | The oven's target, 200.0 |
| `ToleranceC` | `double` | How far a reading may drift either way, 10.0 |
| `OvenTempsC` | `double[]` | One reading per minute, 30 of them. Index 0 is minute 1 |
| `ScheduledMinutes` | `int` | Press 1's scheduled minutes, 480 |
| `RunMinutes` | `int` | Minutes Press 1 actually ran, 437 |
| `PartsMade` | `int` | Parts made, 1250 |
| `PartsPerBox` | `int` | Parts in a full box, 48 |
| `StatusWord` | `int` | The press controller's status word, `0x2C` |

---

## Part 1: Monday, steps 1 through 5

### Step 1. Build and run the starter

In a terminal, in the `ShiftSummary` folder:

```
dotnet build
dotnet run
```

In Visual Studio 2026: open `ShiftSummary.csproj`, then Build, Build Solution, then Debug, Start
Without Debugging. **[VERIFY]** the menu names on your lab machine.

**Observable result:** the build reports 0 errors, and the program prints four lines ending with
`Oven readings on file: 30`. Commit.

### Step 2. Create `BUILD_LOG.md`

In the project folder, create `BUILD_LOG.md` with a heading for each part of this lab. Every error you
cause this week goes in here, pasted from your own terminal, never retyped from memory.

**Observable result:** the file exists and is committed.

### Step 3. Break it: a missing semicolon

Delete the semicolon at the end of the first `Console.WriteLine` line. Build.

**Observable result:** the build fails with error CS1002. Paste the whole error line into
`BUILD_LOG.md`, then write one sentence: which file, which line, which column, and what the compiler
wanted. Put the semicolon back and build again.

### Step 4. Break it: a misspelled name

Add these two lines above `Console.WriteLine("Nothing is calculated yet.");`:

```csharp
int runMinutes = 437;
Console.WriteLine(runMinuts);
```

Build.

**Observable result:** error CS0103, and a warning about `runMinutes`. Paste both. In one sentence,
say why the warning appeared too. Delete both lines and build again.

### Step 5. Break it: text where a number belongs

Add `int partsMade = "1250";` and build.

**Observable result:** error CS0029. Paste it. In one sentence, say what the Python version of that
line would have done. Delete the line, build, run, and commit with a message that says what you
learned.

### Acceptance criteria, Part 1

1. The program builds with 0 errors and runs
2. `BUILD_LOG.md` has three pasted error lines, CS1002, CS0103, and CS0029, each with a sentence
3. At least two commits today

---

## Part 2: Tuesday, steps 6 through 9

### Step 6. Uptime, the wrong way first

Replace TODO 1 with exactly this:

```csharp
double uptimePercent = ShiftData.RunMinutes / ShiftData.ScheduledMinutes * 100;
Console.WriteLine($"  Uptime: {uptimePercent:F1}%");
```

Build and run.

**Observable result:** it builds with no warning and prints `Uptime: 0.0%`. Press 1 ran 437 of 480
minutes. Write in `BUILD_LOG.md`, in one sentence, why the answer is 0 and why nothing warned you.

### Step 7. Uptime, the right way

Change the arithmetic so the division happens in `double`, not in `int`. Do not add a cast to the
result. Print the minutes too.

**Observable result:** `Uptime: 91.0% (437 of 480 minutes)`.

### Step 8. Boxes and leftovers

Replace TODO 2. Full boxes use division. Leftover parts use the remainder operator.

**Observable result:** `Parts: 1250, full boxes: 26, left over: 2`. Here integer division is exactly
what you want. A box is full or it is not. Say that in your build log.

### Step 9. The status word, three ways

Replace TODO 3. Print the status word in decimal, in hexadecimal with two digits, and in binary with
eight digits. You need `ToString("X2")`, `Convert.ToString(value, 2)`, and `PadLeft(8, '0')`.

**Observable result:** `Status word: 44 = 0x2C = 00101100`. Check it by hand: 2 sixteens plus 12,
and 32 plus 8 plus 4.

Put a `Press 1` heading line above the three results. Commit.

### Acceptance criteria, Part 2

1. Uptime prints `91.0%`, and the arithmetic is done in `double` before the division
2. Boxes and leftovers are `int`, and correct
3. The status word prints as `44 = 0x2C = 00101100`
4. `BUILD_LOG.md` explains the silent 0 in one sentence

---

## Part 3: Wednesday, steps 10 through 14

### Step 10. Break a loop on purpose

Above your Part 3 code, add this, build, and run:

```csharp
for (int i = 0; i <= ShiftData.OvenTempsC.Length; i++)
{
    Console.WriteLine($"Minute {i + 1}: {ShiftData.OvenTempsC[i]}");
}
```

**Observable result:** it builds with 0 warnings, prints 30 minutes, then fails with
`System.IndexOutOfRangeException`. Paste the exception line into `BUILD_LOG.md`, name the one
character that caused it, and say why the compiler could not warn you. Then delete the loop.

### Step 11. Average and highest, with `foreach`

Replace TODO 4. One `foreach` loop, a running total, and a highest-so-far.

**Observable result:** `Average: 206.2 C, highest: 221.5 C`, with one decimal on both.

### Step 12. The minute of the highest reading, and the first drift, with `for`

Replace TODO 5. A reading is out of tolerance when it is more than `ToleranceC` away from
`SetpointC` in either direction. `Math.Abs` gives the distance. Minutes count from 1, and indexes
count from 0.

**Observable result:** the highest reading is at minute 19, and the first minute out of tolerance
is 15.

### Step 13. Steady minutes, with `while`

Replace TODO 6. Count minutes from the start of the shift while the reading is in tolerance. The loop
must stop at the end of the array even if the oven never drifted, so check the index **before** you
read the array.

**Observable result:** `Minutes in tolerance before the first drift: 14`.

### Step 14. Out of tolerance, and the percent

Replace TODO 7. Count the minutes out of tolerance, then print the percent of minutes in tolerance
with one decimal. Remember step 6.

**Observable result:** 9 minutes out, `In tolerance: 70.0% of minutes`. Delete the
`Nothing is calculated yet.` and `Oven readings on file` lines. Commit and push.

### The full expected output

```
SHIFT SUMMARY - LINE 3
----------------------
Press 1
  Uptime: 91.0% (437 of 480 minutes)
  Parts: 1250, full boxes: 26, left over: 2
  Status word: 44 = 0x2C = 00101100
Cure oven, first 30 minutes
  Average: 206.2 C, highest: 221.5 C at minute 19
  First minute out of tolerance: 15
  Minutes in tolerance before the first drift: 14
  Minutes out of tolerance: 9
  In tolerance: 70.0% of minutes
```

Your output must match this line for line. Number formats like `206.2` assume a lab machine set to
United States number formatting, where the decimal mark is a period.

---

## Acceptance criteria, full lab

- [ ] `dotnet build` reports 0 errors and 0 warnings
- [ ] The output matches the expected output line for line
- [ ] Every percent is computed in `double` before any division
- [ ] Full boxes and leftovers use `int` division and `%` on purpose
- [ ] All three loop kinds are used: `foreach`, `for`, and `while`
- [ ] The `while` condition checks the index before it reads the array
- [ ] No `<=` against an array's `Length` anywhere
- [ ] `BUILD_LOG.md` has the three Part 1 errors, the silent 0, and the step 10 exception, each with
      a sentence
- [ ] Every period ended with a commit

---

## If it breaks

### 1. A missing semicolon

```
Program.cs(9,44): error CS1002: ; expected
```

**Cause:** a statement with no `;` at the end. The line number is the line that is missing it. The
column points at the spot right after the last character. Python ended statements at the line break,
so your fingers are not used to this yet.

### 2. `ShiftData` does not exist

```
Program.cs(23,45): error CS0103: The name 'ShiftData' does not exist in the current context
```

**Cause:** `ShiftData` lives in the `ShiftSummary` namespace, and the `using ShiftSummary;` line at
the top of `Program.cs` was deleted or misspelled. Put it back. If the line is there, check that
`ShiftData.cs` is in the same folder as the project file.

### 3. A `double` put into an `int`

```
Program.cs(46,15): error CS0266: Cannot implicitly convert type 'double' to 'int'. An explicit conversion exists (are you missing a cast?)
```

**Cause:** the right side is a `double`, such as an average, and the variable is an `int`. The
compiler suggests a cast. **Do not take the suggestion** here. A cast chops the fraction off, and
the lab needs the fraction. Make the variable a `double`.

### 4. A running total with no starting value

```
Program.cs(40,5): error CS0165: Use of unassigned local variable 'total'
```

**Cause:** `double total;` with no value, then `total += reading;` inside the loop. C# will not read a
variable that was never given a value. Write `double total = 0;`.

These positions were recorded by breaking the starter (errors 1 and 2) and a finished
`Program.cs` (errors 3 and 4). Your line and column numbers will match your own file.

### Not a compiler error: the program crashes after printing

`Unhandled exception. System.IndexOutOfRangeException: Index was outside the bounds of the array.`
This is step 10. Look for `<=` against `Length`.

### Not an error at all: `Uptime: 0.0%`

This is step 6. The division happened in `int`.

---

## Stretch goal

**Part A.** Print the oven's readings as a small text chart, one row per minute, with a `#` for every
2 degrees above 195. Minute 19 should have the longest bar.

**Part B.** In `BUILD_LOG.md`, answer in three or four sentences: the compiler caught three of this
week's mistakes and missed two. For each of the two it missed, what would have caught it? Name a
real tool or habit, not "being careful."

---

## Submission checklist

- [ ] `dotnet build` and `dotnet run` both work from a fresh clone
- [ ] Output matches the expected output line for line
- [ ] `BUILD_LOG.md` is complete, with pasted error lines, not retyped ones
- [ ] `bin/` and `obj/` are not committed
- [ ] `git status` shows nothing uncommitted
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension
scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Still fixing the Part 1 errors at minute 20 on Monday, or retyping errors instead of pasting them | SCAFFOLDED |
| Working steadily, asking about formatting and wording rather than about types | STANDARD |
| Finished Part 2 by minute 20 on Tuesday, or asked what the status word's bits mean | EXTENDED |
| Said the shop floor has nothing to do with them, or asked when they would ever need this | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Part 2:** step 7's fixed line is given with one blank, `double uptimePercent = ShiftData.RunMinutes * ____ / ShiftData.ScheduledMinutes;`, and the student fills in the blank and explains it.
- **Part 3:** the `foreach` loop for the average is given complete. The student writes the `for` and
  `while` loops only, and skips step 14's percent.
- **Step 10 stays.** The deliberate crash is the most important minute of Wednesday.
- **Checkpoints:** show you the build output after step 5, after step 7, and after step 13.

**Acceptance criteria:** the output matches the expected output except the last two lines; the
build log has the three Part 1 errors, the silent 0, and the step 10 exception.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. A student
who completes this version fully earns the same grade as one who completes STANDARD fully.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one addition that needs something you have not been taught.

**Added requirement.** The press controller's manual, for this composite shop, says the status word's
bits mean:

| Bit | Value | Meaning |
|---|---|---|
| 2 | 4 | guard closed |
| 3 | 8 | running |
| 4 | 16 | fault |
| 5 | 32 | service due |

Print four more lines under the status word, each `True` or `False`: guard closed, running, fault,
service due. Declare each bit as a named constant written in binary. Then test your code with a
second status word, `0x14`, and say in your build log what that word means.

**Hint, not the answer.** You need an operator that keeps only the bits two numbers share. Read the
C# language reference page on bitwise and shift operators on learn.microsoft.com **[VERIFY]** the
page address, and look for the logical AND operator for integer types.

**Acceptance criteria:** all STANDARD criteria, plus four correct flag lines for `0x2C`, named
binary constants, and the `0x14` explanation.

**Grading:** same scale. A student who attempts this, gets it partly wrong, and documents the attempt
honestly loses very little. A student who pastes code they cannot explain fails the program's one
outright rule.

---

## APPLIED

**For the student who says this does not apply to them.** Same skills, different domain.

**Changed scenario.** Pick something you track that has a number per day or per minute: a phone
battery through a day, minutes of practice across a season, steps per day for a month, or laps in a
swim set. Invent the data, 20 values or more. **Use no real personal data about anyone, including
yourself.**

**What you build.** A `Data.cs` file shaped like `ShiftData.cs`, and a summary that uses:

- one percent that must be computed in `double`, with the silent-zero version shown first in your
  build log
- one division where integer division is the right answer, with a sentence saying why
- one value printed in hexadecimal and binary, such as a day number or a lap count
- a `foreach`, a `for`, and a `while` loop, where the `while` stops on a condition

**Acceptance criteria:** all STANDARD criteria, applied to your data, plus the two division
explanations.

**Grading:** same scale. Requirements Fit is judged on whether each type choice fits the value it
holds, which is a harder question than the standard version asks.

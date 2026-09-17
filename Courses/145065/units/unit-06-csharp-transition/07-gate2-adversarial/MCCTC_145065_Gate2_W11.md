# Gate 2: Adversarial Review · Week 11
## 145065 Object-Oriented Programming · Unit 6 · Week 11, Friday

**40 minutes.** Individual. You may and should build and run the code. You may not ask a model
whether it is correct, because a model is what is being reviewed.

The code is in `gate2-w11-files/`. Copy the whole folder.

Riverside Fabrication is a composite: an invented small metal fabrication shop. The readings are
invented.

---

## What you are looking at

The Line 3 team asked an AI assistant to port a small Python class to C# for the future panel. It
produced `Line3.Readings/ReadingLog.cs`. It is tidy, commented, and it builds with **warnings treated
as errors**, so the compiler found nothing at all.

Your job is to find what the compiler cannot.

**Five defects, one in each category:** Correctness, Security, Readability, Performance,
Requirements Fit. None of them is a syntax error. All five are design or logic problems in code that
builds and runs.

**One of them hides inside a line that looks like floating-point math.** Read every division twice.

---

## PART A: The requirements

> Port our Python `ReadingLog` to a C# class library for the Line 3 panel. It must:
>
> 1. Hold readings from one sensor, identified by its sensor id.
> 2. Keep only the newest readings, up to a limit set when the log is created: 3,600 by default,
>    86,400 at most. When the log is full, drop the oldest reading.
> 3. Refuse a reading that is not a finite number. **Nothing but `Record` may put a value into the
>    log.**
> 4. `Latest`: the newest reading, or **null** when there is none. A missing reading must never look
>    like a number.
> 5. `PercentInRange(low, high)`: the percent of stored readings from low to high, inclusive, to one
>    decimal place.
> 6. `CountAboveAverage()`: how many stored readings are above the average of the stored readings.
>    It runs on every screen refresh, so it must stay fast on a full log.
> 7. The panel must be able to tell a log that has never received a reading apart from one that has.

---

## PART B: What the AI produced

```
gate2-w11-files/
  Line3.Readings.sln
  Line3.Readings/ReadingLog.cs      the code under review
  ReadingsDemo/Program.cs           a short demo run
```

Build and run the demo from the `gate2-w11-files` folder:

```
dotnet build Line3.Readings.sln
dotnet run --project ReadingsDemo
```

A real run:

```
oven-temp: 4 readings, keeps the last 5
Latest: 230
In range 200 to 215: 0%
Above average: 1
Stale: False
After two more: 205, 210, 230, 199, 198
coolant-level: latest NaN, stale True
Refused: a reading must be a finite number
```

**Read those lines against Part A before you read the code.** The demo recorded 201, 205, 210, and
230. At least two lines of that output are already wrong.

---

## What to submit

For each defect: **file and line**, **dimension**, **what goes wrong for a real user or a real
panel**, and **the fix**. Then one final entry: **what I was unsure about**, naming something
specific. That entry is scored, and a blank costs more than a wrong guess.

You may write a few lines of your own C# in the demo to prove a defect. Say what you ran and what it
printed. Proof beats opinion.

### How to spend 40 minutes

- **First 5:** build and run. Compare every output line with Part A.
- **Next 10:** read Part A one requirement at a time and point at the line that meets it.
- **Next 15:** read every comment and every name, and ask whether the code under it does what it
  says. Look at the class declaration line as hard as at the methods.
- **Rest:** try to break requirement 3 from the demo's `Program.cs`. Try to make the panel show a
  wrong number.

---

## Scoring

Five defects, one point each, plus one for the "what I was unsure about" entry. Your instructor states
the security weighting before you start.

**Four of five is a strong score.** One of these is designed to be missed.

# Gate 2: Adversarial Review · Week 12
## 145065 Object-Oriented Programming · Unit 6 · Week 12, Friday

**40 minutes.** Individual. You may and should build and run the code. You may not ask a model
whether it is correct, because a model is what is being reviewed.

The code is in `gate2-w12-files/`. Copy the whole folder.

Riverside Fabrication is a composite: an invented small metal fabrication shop. The readings are
invented.

---

## What you are looking at

The Line 3 team asked an AI assistant for the first piece of the operator panel: a status board that
shows every sensor and switch, one line each. It produced the `Line3.Status` library. It uses an
interface, access modifiers, and switch expressions, everything from this week. It builds with
**warnings treated as errors** and reports 0 warnings.

**Five defects, one in each category:** Correctness, Security, Readability, Performance,
Requirements Fit. These are design defects. Every one of them builds and runs.

**One of them costs nothing on a small board and a great deal on a big one.** Look at what each
property returns, not only at what the loops do.

---

## PART A: The requirements

> Write a C# class library for the Line 3 status board. It must:
>
> 1. Define one interface that everything on the board implements, with at least a tag and a status
>    level: Normal, Warning, Missing, or Alarm.
> 2. Provide two implementations: a temperature probe with a warning limit and a higher alarm limit,
>    and a guard switch that is closed, open, or not yet heard from.
> 3. A probe at or above its alarm limit shows **Alarm**. A probe at or above its warning limit and
>    below its alarm limit shows **Warning**.
> 4. A reporter that has not reported yet shows **Missing**, never Normal.
> 5. **Only a new report from the device may change what a reporter shows.** The board monitors. It
>    never changes the state of anything.
> 6. The board prints one line per reporter, with its tag, its level, and a short description of its
>    current state, and it reports the most urgent level on the board.
> 7. The board is redrawn ten times a second and may hold up to 5,000 reporters on the plant-wide
>    screen. Both of the board's methods must stay fast at that size.

---

## PART B: What the AI produced

```
gate2-w12-files/
  Line3.Status.sln
  Line3.Status/StatusLevel.cs
  Line3.Status/IStatusReporter.cs
  Line3.Status/TemperatureProbe.cs
  Line3.Status/GuardSwitch.cs
  Line3.Status/StatusBoard.cs
  StatusDemo/Program.cs          a short demo run
```

Build and run the demo from the `gate2-w12-files` folder:

```
dotnet build Line3.Status.sln
dotnet run --project StatusDemo
```

A real run:

```
Start of shift
  L3-OVN-01    Normal   212.0 C
  L3-PRS-01-G  Normal   guard closed
  L3-PRS-02-G  Missing  no signal
  Worst: Missing
Twenty minutes later
  L3-OVN-01    Warning  250.0 C
  L3-PRS-01-G  Alarm    guard OPEN
  L3-PRS-02-G  Missing  no signal
  Worst: Alarm
```

The oven's warning limit is 215 and its alarm limit is 240. **Check every line against Part A before
you open a single `.cs` file.** One line is already wrong.

---

## What to submit

For each defect: **file and line**, **dimension**, **what goes wrong for an operator or for the
panel**, and **the fix**. Then one final entry: **what I was unsure about**, naming something
specific. That entry is scored, and a blank costs more than a wrong guess.

You may add lines to the demo to prove a defect. Say what you ran and what it printed.

### How to spend 40 minutes

- **First 5:** build, run, and check the output against requirement 3.
- **Next 10:** read the interface. For each member, ask whether **both** implementations can keep
  the promise, and whether requirement 5 allows it.
- **Next 10:** read `StatusBoard`. For each property it uses, ask what it returns and how often it is
  read.
- **Rest:** write a third reporter in the demo, a pressure gauge, and put it on the board. Read what
  the board prints for it, and compare with the comment above `Lines()`.

---

## Scoring

Five defects, one point each, plus one for the "what I was unsure about" entry. Your instructor states
the security weighting before you start.

**Four of five is a strong score.** At least one is genuinely arguable, and one is designed to be
missed.

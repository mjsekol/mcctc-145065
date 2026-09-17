# Gate 2: Adversarial Review · Week 5
## 145065 Object-Oriented Programming · Unit 2 · Week 5, Friday

**35 minutes.** Individual and silent. You may and should run the code and write your own small
tests. You may not ask an AI tool whether the code is correct.

The program is `gate2-w05-files/line_inspect.py`. Copy it into a folder of your own and run it.

**Riverside Fabrication is a composite**, an invented shop. Every tag, reading, and badge id is
invented.

---

## What you are looking at

A developer asked an AI assistant to refactor Line 3's inspection to use polymorphism and
composition, from the requirements in Part A. The result runs cleanly, uses `abc`, a frozen
dataclass, and composed sensors, and reads like this week's lecture notes.

**Gate 2 in this course plants design defects.** The code runs. Each defect is a decision.

**Five defects, one in each dimension:**

| Dimension | What to look for this week |
|---|---|
| **Correctness** | A subclass that quietly drops what its parent provides |
| **Security** | A part of an object that outside code can take away |
| **Readability** | A comment or docstring that the code does not do |
| **Performance** | The same work done twice for one answer |
| **Requirements Fit** | A relationship that lets in something the requirements forbid |

**One of the five is genuinely arguable.** Argue both sides of it for a point.

**The sample run hides the subtle one.** The machine it affects has nothing wrong with it in the
sample.

---

## Part A: The requirements

> Refactor Line 3's inspection.
>
> 1. `Line.inspect_all()` asks every machine the same question, `inspect()`, and never checks what
>    kind it is. It returns the findings with the most severe first: `stop`, then `warning`, then
>    `info`.
> 2. Every machine's `inspect()` returns the shared findings first (its lockout, then each of its
>    sensors' findings), then the findings only its kind makes.
> 3. Powered equipment **has** sensors. `attach_sensor()` is the only way to add one. **Nothing
>    outside the machine may remove or replace a sensor.**
> 4. A sensor id is unique on its machine. Two machines may each have a sensor with the same id.
> 5. **A line holds cells only.** A cell holds machines and smaller cells.
> 6. Adding a new kind of machine must need no change to `Line`.
> 7. Lines will hold hundreds of machines, each with several sensors, and are inspected every few
>    seconds.

---

## Part B: What the AI produced

The code is in `gate2-w05-files/line_inspect.py`. Run it:

```
python line_inspect.py
```

A real run:

```
4 machines inspected
  [WARNING] L3-PRS-01: coolant-level reads 14 %, below 20
  [WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C
  [STOP] L3-PRS-02: guard is open; press cannot run
  [INFO] L3-PRS-02: locked out by tech-07
```

**Compare that output with requirement 1 before you read the code.**

---

## What to submit

For each defect: **the line or method**, **the dimension**, **what goes wrong on Line 3**, **how you
proved it** (the command or test and what it printed), and **the fix**.

Then:

- **The arguable one:** the strongest case that it is a defect, and the strongest case that it is an
  acceptable design.
- **What I was unsure about:** something specific.

### How to spend 35 minutes

- **First 5:** run it. Check the output against requirement 1.
- **Next 10:** give each machine a sensor reading outside its limits, and a lockout. Does every
  machine report both? Try it on a machine the sample leaves quiet.
- **Next 10:** take a machine from the sample and try to change its sensors from outside the class.
  Then try to put a machine straight onto a `Line`.
- **Last 10:** count how many times one call to `inspect()` asks the sensors. Write up.

---

## Scoring

Five defects, one point each, plus one point for the arguable entry argued both ways, plus one point
for the unsure-about entry. A finding scores only with a location, a consequence, and a fix. Your
instructor states the Security weighting before you start.

**Four of five is a strong score.**

# Gate 2: Adversarial Review · Week 6
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Friday

**35 minutes.** Individual and silent. You may and should run the code and write your own small
tests. You may not ask an AI tool whether the code is correct.

The program is `gate2-w06-files/line_store.py`. Copy it into a folder of your own and run it.

**Riverside Fabrication is a composite**, an invented shop. Every tag, name, and badge id is
invented.

---

## What you are looking at

A developer asked an AI assistant to save and load Line 3's equipment register, from the
requirements in Part A. The result is short and runs cleanly. It keeps a backup, raises its own
exception class, and has a loader that "needs no changes for new equipment types."

**Gate 2 in this course plants design defects.** The code runs. Each defect is a decision.

**Five defects, one in each dimension:**

| Dimension | What to look for this week |
|---|---|
| **Correctness** | A save that can leave the line with no usable file at all |
| **Security** | A file that decides more than the values it holds |
| **Readability** | A comment that the code does not do |
| **Performance** | Work repeated once per item that only needed doing once |
| **Requirements Fit** | Something a restart must remember and does not |

**One of the five is genuinely arguable.** Argue both sides of it for a point.

**The sample run hides the subtle one.** Nothing goes wrong until a save fails, and then it takes
two failures in a row to see the whole problem.

---

## Part A: The requirements

> Save and load Line 3's equipment register.
>
> 1. `save()` writes the whole register to one JSON file and keeps the previous save as a backup.
>    **A failed save must never leave the line without a usable file.**
> 2. `load()` rebuilds the register. Any file it cannot use raises `PlantFileError`, and nothing
>    else.
> 3. **The file is untrusted.** It is stored on a shared drive and can be edited by anyone. A file
>    may set a machine's saved values, and only through the same rules the program uses. It may not
>    choose what code runs or change anything the program did not save.
> 4. **After a restart, every machine comes back at least as safe as it was:** stopped, guard
>    treated as open, and every lockout still in place.
> 5. A register holds a few hundred machines and is loaded each time an operator panel starts.
> 6. New equipment types will be added later.

---

## Part B: What the AI produced

The code is in `gate2-w06-files/line_store.py`. Run it:

```
python line_store.py
```

A real run:

```
Saved 459 bytes
Loaded:
  L3-PRS-01 Press 1 15 kW, stopped, not locked out
  L3-PRS-02 Press 2 22 kW, stopped, not locked out
  L3-RCK-01 Rack, Área de Soldadura 640 of 1200 kg
```

**Read `build_sample()` and compare it with that output before you read anything else.**

---

## What to submit

For each defect: **the line or function**, **the dimension**, **what goes wrong on Line 3**, **how
you proved it** (the command or test and what it printed), and **the fix**.

Then:

- **The arguable one:** the strongest case that it is a defect, and the strongest case that it is
  acceptable.
- **What I was unsure about:** something specific.

### How to spend 35 minutes

- **First 5:** run it. Compare the output with `build_sample()` and requirement 4.
- **Next 10:** open the saved file. Write a file by hand that changes something the program never
  saved, and load it. Try a `kind` the program never wrote.
- **Next 10:** make a save fail. A value JSON cannot hold, such as a Python `set`, will do. What is
  on disk afterward? Now make it fail again.
- **Last 10:** read `_check_duplicates()` and count the work for 300 machines. Write up.

**Work only inside a temporary folder or a copy.** Never point this program at a real file.

---

## Scoring

Five defects, one point each, plus one point for the arguable entry argued both ways, plus one point
for the unsure-about entry. A finding scores only with a location, a consequence, and a fix. Your
instructor states the Security weighting before you start.

**Four of five is a strong score.**

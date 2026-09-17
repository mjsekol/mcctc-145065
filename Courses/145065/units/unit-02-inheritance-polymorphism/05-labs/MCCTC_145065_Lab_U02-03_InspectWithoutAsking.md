# Lab U2-03: Inspect Without Asking
## 145065 Object-Oriented Programming · Unit 2 · Week 5

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1.
**Competencies:** 5.3.5 (conditional control structures, and replacing them with polymorphism),
5.3.12 (classes, objects, and methods), 5.5.2 (the `abc` reuse library).

Files: `lab-u02-03-files/inspection.py` (starter) and `lab-u02-03-files/selfcheck_inspection.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag, name,
and reading is invented.

---

## The scenario

Every morning Line 3's inspection report runs through one long function that asks each machine what
kind it is and then applies that kind's rules. The shop is about to add a welder, and the last time a
new machine was added, nobody updated the function, and the report crashed in front of the
supervisor. The rules for each machine also live far from the machine's own class, where nobody
reading the class can see them.

## What you will build

An inspection that asks every machine the same question and lets each class answer, proven to give
exactly the same findings as the old function, and a welder added without touching the loop.

---

## Starter code

Copy both files into one folder and run:

```
python inspection.py
python selfcheck_inspection.py
```

The starter prints:

```
Findings, from the if/elif chain:
  [WARNING] L3-PRS-01: service due: 20150 strokes since service (interval 20000)
  [STOP] L3-PRS-02: guard is open; press cannot run
  [WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C
  [WARNING] L3-CNV-01: running with belt speed 0 m/s; check for a stall or a missing setpoint
  [WARNING] L3-RCK-01: at 96% of capacity

Findings, asked polymorphically: 0
```

and the self-check ends `0 of 8 self-checks passed`.

**Do not change `inspect_by_kind()` or `inspect_line_by_kind()`.** They are the "before" picture, and
your proof that the refactor changed nothing.

---

## Steps

### Step 1. Read the chain, and map it

In your README, under `## Where each rule belongs`, write a table with one row per branch of
`inspect_by_kind()`: the `kind` it checks, the class that should own it, and how many lines it has.
Then answer: to add a welder to this design, which function must change?

**Observable result:** four rows, and the answer names `inspect_by_kind()`.

### Step 2. Move the press branch into `Press`

In `Press`, write `_kind_findings(self)`. Copy the press branch's body into it. Change every `item.`
to `self.`, start with `findings = []`, and return `findings`.

**Observable result:** `python inspection.py` still prints the same chain findings. The self-check
has not changed yet.

### Step 3. Do the same for `Conveyor` and `Oven`

Watch the oven's `else:`. In the chain it pairs with `if sensor is None`. In your method, the
no-reading case can `return` early, and the rest need no `else` at all.

**Observable result:** the program still runs.

### Step 4. Do the same for `StorageRack`

**Observable result:** the self-check shows `2 of 8`: both Step 2-4 checks PASS, including the check
that compares your method with the chain at boundary values such as exactly 90 percent full.

### Step 5. Make `Equipment` an abstract base with `inspect()`

Add `from abc import ABC, abstractmethod`. Make `Equipment` inherit from `ABC`. Give it
`inspect(self)`, which returns `self._kind_findings()`, and an abstract `_kind_findings()`.

**Observable result:** `4 of 8`.

### Step 6. Write the polymorphic loop

Fill in `inspect_all(items)`: start an empty list, extend it with `item.inspect()` for every item,
return it. **No `if` about kinds, no `isinstance()`.**

**Observable result:** `6 of 8`. One of the new passing checks adds a `Grinder` class your loop has
never seen, and your loop still asks it.

### Step 7. Prove the refactor changed nothing

Change `main()` so it prints the polymorphic findings under `Findings, asked polymorphically:`, and
then the line `Same as the if/elif chain:` followed by the result of comparing `inspect_all(items)`
with `inspect_line_by_kind(items)`.

**Observable result:**

```
Findings, asked polymorphically:
  [WARNING] L3-PRS-01: service due: 20150 strokes since service (interval 20000)
  [STOP] L3-PRS-02: guard is open; press cannot run
  [WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C
  [WARNING] L3-CNV-01: running with belt speed 0 m/s; check for a stall or a missing setpoint
  [WARNING] L3-RCK-01: at 96% of capacity
Same as the if/elif chain: True
```

The two lists compare equal because `Finding` is a dataclass, and dataclasses compare field by field.

### Step 8. Add a welder, and touch nothing else

Below `StorageRack`, write `Welder(PoweredEquipment)` with `kind = "welder"`, a `LOW_WIRE_KG = 2.0`
class attribute, a `wire_kg` argument, and a `_kind_findings()` that returns a `warning` finding
`wire low: <kg> kg left` when the welder is running with less than 2 kg of wire. Do **not** add it to
`inspect_by_kind()`.

At the end of `main()`, add a running welder with 1.5 kg of wire to the list, print what
`inspect_all()` says about it, and then call `inspect_line_by_kind()` inside a `try` that prints the
`ValueError`.

**Observable result:** `8 of 8 self-checks passed`, and the program ends:

```
After adding a welder, the polymorphic loop says:
  [WARNING] L3-WLD-01: wire low: 1.5 kg left
The if/elif chain says: ValueError: no inspection rule for kind 'welder'
```

### Step 9. Count the cost

Under `## The cost of a new kind` in your README, list every file and function you edited to add the
welder in step 8, then every one you would have had to edit in the chain design. Two sentences: which
design fails earlier when someone forgets, and who sees that failure.

**Observable result:** two lists and two sentences. Commit.

---

## Acceptance criteria

- [ ] `python selfcheck_inspection.py` prints `8 of 8 self-checks passed`
- [ ] `python inspection.py` prints `Same as the if/elif chain: True` and ends with the chain's `ValueError`
- [ ] `inspect_all()` contains no `if` about kinds and no `isinstance()`
- [ ] `inspect_by_kind()` is unchanged
- [ ] The README has the step 1 table and the step 9 section
- [ ] Committed and pushed

---

## If it breaks

### 1. `abc` turned on before every kind has its answer

```
TypeError: Can't instantiate abstract class Oven without an implementation for abstract method '_kind_findings'
```

**Cause:** step 5 was done while a class still had no `_kind_findings()`. The message names the first
class `build_sample()` tried to create. Finish steps 2 through 4.

### 2. A copied branch that still says `item`

```
NameError: name 'item' is not defined. Did you mean: 'iter'?
```

**Cause:** inside a method, the object is `self`. Every `item.` in the copied branch must become
`self.`.

### 3. The method, not its result

```
TypeError: 'method' object is not iterable
```

**Cause:** `findings.extend(item.inspect)` passes the method itself. Call it: `item.inspect()`.

### 4. `append` where `extend` belongs

No error. The program prints each machine's findings as a list in brackets, like
`[Finding(asset_tag='L3-PRS-01', ...)]`, and says `Same as the if/elif chain: False`. The self-check
drops to `6 of 8`.

**Cause:** `findings.append(item.inspect())` adds each machine's whole list as one item. `extend()`
adds the findings one at a time.

### Not an error: a welder added to the chain

The self-check's last line fails with a message that says to leave the chain alone. The chain is the
"before" picture. Adding kinds to it is exactly the cost this lab measures.

**Error wording was captured on Python 3.13.7.** Confirm it on the lab's Python 3.14.

---

## Stretch goal

A `Press` should also warn when its strokes are within 500 of the service interval. Add that rule to
`Press._kind_findings()` only. Then explain in your README why the self-check's comparison with the
chain now fails, and what that tells you about keeping a "before" function around after a refactor.

---

## Submission checklist

- [ ] Self-check 8 of 8
- [ ] README: where each rule belongs, and the cost of a new kind
- [ ] `inspect_by_kind()` unchanged
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.3.5, 5.3.12, 5.5.2) and grade on the same
100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 12 of Build 1, the press method is not written, or the student is editing `inspect_by_kind()` | SCAFFOLDED |
| Steady progress through steps 2 to 4 | STANDARD |
| 8 of 8 with 10 minutes of Build 1 left | EXTENDED |
| The student asks why anyone would not write the if/elif chain | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out an `inspection.py` in which `Equipment` is already the
  abstract base with `inspect()`, and `Press._kind_findings()` is already written as the worked
  example. `Conveyor`, `Oven`, and `StorageRack` have stub methods marked `TODO` that return an empty
  list.
- **Steps:** skip steps 2 and 5. Step 3 and step 4 copy the pattern from `Press`.
- **Checkpoints:** show the instructor the self-check after step 4 and after step 8.

**Acceptance criteria:** 8 of 8 and the step 9 section.

**Grading:** same scale. Full completion earns the same grade as STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one idea the lab has not taught.

**Added requirement.** Write `inspect_by_match(item)`: the same inspection as the chain, as a
`match` statement with **class patterns**. It must return the same findings as `item.inspect()` for
the five sample machines and raise `ValueError` for the welder. Then write two sentences: what the
`match` version improves over the if/elif chain, and what it still has in common with it.

**Hint, not the answer.** Read the `match` section of the Python tutorial,
`https://docs.python.org/3/tutorial/controlflow.html#match-statements`, especially the part about
patterns that look like `Point(x=0, y=0)`. A `case` can have an `if` guard after the pattern. This is
a preview of the `switch` statement you meet in C# in Unit 6.

**Acceptance criteria:** all STANDARD criteria; a printed line comparing `inspect_by_match()` with
`inspect()` for the five sample machines says `True`; the two sentences.

**Grading:** same scale.

---

## APPLIED

**For the student who asks why anyone would not write the chain.** The same move in a grade book.

**Changed scenario.** A grade tool computes late penalties with one if/elif chain over assignment
kinds: quizzes, essays, and labs, each with its own late rule. Write the chain first, then refactor
to an abstract `Assignment` with a `penalty(days_late)` method each kind answers. Add a fourth kind,
`Project`, with a grace day. Invent every title and rule.

**What you build.** Both designs in one file, a check that they agree on the first three kinds at
0, 1, 2, and 5 days late, and a run showing the chain fails on `Project` while the polymorphic version
does not.

**Acceptance criteria:** the agreement check prints `True`; the README has the step 9 section for your
domain.

**Grading:** same scale.

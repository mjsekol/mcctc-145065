# Lab U2-02: Layout Walk
## 145065 Object-Oriented Programming · Unit 2 · Week 4

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Thursday Build 1 and the first 30
minutes of Build 2.
**Competencies:** 5.3.8 (nested structures and recursion), 5.3.12 (classes, objects, and methods).

Files: `lab-u02-02-files/layout.py` (starter), `lab-u02-02-files/line3_parts.py` (given, do not
change), and `lab-u02-02-files/selfcheck_layout.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag and name
is invented.

---

## The scenario

Line 3 is organized in cells, and one cell already holds a smaller cell. The supervisor wants an
outline of the whole line, a machine count, and the total rated power, and next year's layout may
nest cells deeper than anyone has planned for. Code with a fixed number of loops will silently miss
whatever sits one level lower.

## What you will build

Recursive functions that walk a line of cells to any depth, and a guard that keeps the layout from
ever containing itself.

---

## The layout

```
Line 3
|-- Forming              (cell)
|   |-- L3-PRS-01        Press 1, 15 kW
|   `-- L3-PRS-02        Press 2, 22 kW
|-- Finishing            (cell)
|   |-- L3-OVN-01        Cure Oven, 45 kW
|   `-- Transfer         (a cell inside a cell)
|       `-- L3-CNV-01    Transfer Conveyor, 3 kW
`-- Staging              (cell)
    `-- L3-RCK-01        Finished Goods Rack, no power
```

`line3_parts.py` gives you a small `Machine` class. A machine has `asset_tag`, `name`, `kind`,
`rated_kw`, and `describe()`, and it holds nothing. A `Cell` and a `Line` both have `items`. That is
the whole trick: anything with `items` can be walked, and a machine is where every walk stops.

---

## Starter code

Copy the three files into one folder and run:

```
python layout.py
python selfcheck_layout.py
```

The starter prints:

```
Line 3

Machines on the line: 0
Rated power on the line: 0 kW
Found two levels down: nothing
```

and the self-check ends `0 of 9 self-checks passed`. Five functions are stubs marked `TODO` that
return harmless values so the program runs. The self-check labels each check with the step that
fixes it.

---

## Build 1 · steps 1 through 4

### Step 1. `count_equipment(node)`

Write the base case first: if `node` is a `Machine`, return 1. Then the recursive case: return the
sum of `count_equipment(child)` for every child in `node.items`.

**Observable result:** `python layout.py` prints `Machines on the line: 5`. The self-check shows
`2 of 9`, both Step 1 lines PASS.

### Step 2. `walk(node, depth=0)`

Return a list of `(depth, item)` pairs for everything below `node`, depth first. For each item:
append `(depth, item)`, and if the item is a `Cell`, extend the list with `walk(item, depth + 1)`.

**Observable result:** `5 of 9`. `find()` and the no-fixed-depth check pass too, because both use
`walk()`. `Found two levels down: L3-CNV-01 Transfer Conveyor (conveyor)`.

### Step 3. `Line.outline()`

Start a list with the line's name. For each `(depth, item)` from `walk(self)`, add the cell's name or
the machine's `describe()`, indented two spaces for each level, plus two more.

**Observable result:** `6 of 9`, and the program prints the full outline:

```
Line 3
  Forming
    L3-PRS-01 Press 1 (press)
    L3-PRS-02 Press 2 (press)
  Finishing
    L3-OVN-01 Cure Oven (oven)
    Transfer
      L3-CNV-01 Transfer Conveyor (conveyor)
  Staging
    L3-RCK-01 Finished Goods Rack (rack)
```

### Step 4. `total_rated_kw(node)`

The same shape as `count_equipment()`, adding `rated_kw` instead of 1.

**Observable result:** `7 of 9`, and `Rated power on the line: 85 kW`. Commit.

---

## Build 2 · steps 5 through 8

### Step 5. `Cell.contains_cell(target)`

Return `True` if `target` is anywhere below this cell. Loop over the cell's items. For each item that
is a `Cell`, return `True` if the item **is** `target` (use `is`, not `==`), or if
`item.contains_cell(target)` is `True`. After the loop, return `False`.

**Observable result:** `8 of 9`.

### Step 6. Refuse a loop in `Cell.add()`

Where the `TODO Step 6` comment is, refuse a cell that would create a loop: if the item is a `Cell`,
and it is this cell or it already contains this cell, raise `ValueError` with a message that names
both cells.

**Observable result:** `9 of 9 self-checks passed`. Commit.

### Step 7. Break it twice, on purpose

**First break.** Delete the base case from `count_equipment()` and run `python layout.py`.

**Observable result:** the outline prints, because `walk()` has its own stopping rule. Then the count
fails with a traceback ending:

```
AttributeError: 'Machine' object has no attribute 'items'
```

Restore the base case.

**Second break.** Comment out the two lines of your step 6 guard. Run:

```
python -c "import layout; line = layout.build_sample_line(); finishing = line.items[1]; transfer = finishing.items[1]; transfer.add(finishing); print('added'); print(layout.count_equipment(line))"
```

**Observable result:** it prints `added`, then a very long traceback that ends:

```
RecursionError: maximum recursion depth exceeded
```

Restore the guard and confirm 9 of 9. In your README, under `## Two ways recursion never ends`, write
one sentence for each break: what was missing, and why the function could not stop.

### Step 8. Trace one call by hand

In your README, under `## Trace of count_equipment(Finishing)`, write a table with one row per call:
the node, whether it is a machine, and what the call returns. Start from `count_equipment` on the
Finishing cell and end with the value Finishing returns.

**Observable result:** a table with four rows, one per call. The Finishing row returns 2.

---

## Acceptance criteria, full lab

- [ ] `python selfcheck_layout.py` prints `9 of 9 self-checks passed`
- [ ] `python layout.py` prints the full outline, `Machines on the line: 5`, and `Rated power on the line: 85 kW`
- [ ] Every recursive function has its base case written before its recursive case
- [ ] `Cell.add()` refuses a loop; `line3_parts.py` is unchanged
- [ ] The README has the step 7 and step 8 sections
- [ ] Committed and pushed

---

## If it breaks

### 1. No base case, or a walk into a machine

```
AttributeError: 'Machine' object has no attribute 'items'
```

**Cause:** the function asked a machine for `.items`. Either the base case is missing, or `walk()`
recursed into every item instead of only into cells. Check the base case, and check the
`isinstance(item, Cell)` test in `walk()`.

### 2. A loop in the data

```
RecursionError: maximum recursion depth exceeded
```

**Cause:** a cell was added inside itself, directly or further down, so no path ever ends at a
machine. Finish step 6, and rebuild the line: a line that already contains a loop stays broken.

### 3. `append` where `extend` belongs

```
AttributeError: 'tuple' object has no attribute 'describe'
```

**Cause:** `walk()` used `rows.append(walk(item, depth + 1))`, which puts a whole list inside the
list as one element. `outline()` then unpacks the wrong things. Use `rows.extend(...)`.

### 4. The recursive result thrown away

No error. The outline shows only the three top cells, and `Found two levels down: nothing`.

**Cause:** `walk(item, depth + 1)` was called and its result never added to `rows`. A recursive call
that returns a value does nothing unless you use the value.

### Not an error: every item at the same depth

The outline prints, flat, with no extra indentation for Transfer's conveyor. **Cause:** the recursive
call passed `depth` instead of `depth + 1`.

**Error wording was captured on Python 3.13.7.** Confirm it on the lab's Python 3.14.

---

## Stretch goal

Write `deepest(node)`, which returns how many cells deep the deepest machine sits: 1 for Forming's
presses, 2 for the conveyor. Base case first. Then add a cell inside Transfer with a machine in it and
check the answer changes to 3 without any other edit.

---

## Submission checklist

- [ ] Self-check 9 of 9
- [ ] README: two ways recursion never ends, and the trace table
- [ ] Both breaks restored
- [ ] `line3_parts.py` unchanged
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.3.8, 5.3.12) and grade on the same 100-point
five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 15 of Build 1, `count_equipment()` still has no base case, or the student has written nested `for` loops | SCAFFOLDED |
| Steady progress, and questions about what `depth` is for | STANDARD |
| 9 of 9 before Build 1 ends | EXTENDED |
| The student asks where recursion shows up outside a factory | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out a `layout.py` in which `count_equipment()`, `walk()`,
  and the step 6 guard are already written. The student reads `count_equipment()` first and names
  its base case and recursive case aloud, then writes `outline()`, `total_rated_kw()`, and
  `contains_cell()`, which have comments saying what to copy.
- **Checkpoints:** show the instructor the trace table after step 4, before writing more code.
- **Keep step 7.** The breaks are the lesson.

**Acceptance criteria:** 9 of 9, the two README sections.

**Grading:** same scale. Full completion earns the same grade as STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one idea the lab has not taught.

**Added requirement.** A line with 100,000 items should never be copied into one giant list, and
`find()` should stop walking as soon as it finds its tag. Rewrite `walk()` and `iter_equipment()` as
**generators**. The self-check must still pass.

**Hint, not the answer.** Read about the `yield` statement and `yield from` in the Python reference,
`https://docs.python.org/3/reference/simple_stmts.html#the-yield-statement`, and the tutorial section
on generators, `https://docs.python.org/3/tutorial/classes.html#generators`.

**Acceptance criteria:** 9 of 9; `type(layout.walk(line)).__name__` prints `generator`; a decision log
entry says what the generator version gives up (you cannot index it or take its length).

**Grading:** same scale.

---

## APPLIED

**For the student who asks where else this shows up.** The same skill with files and folders.

**Changed scenario.** A music library is folders inside folders. Build a `Folder` with songs (title,
minutes) and subfolders, nested at least three deep. Invent every title. No real artist or song
names.

**What you build.** Recursive `count_songs()`, `total_minutes()`, `outline()`, and `find(title)`, a
guard that refuses a folder being added inside itself, and a self-check with at least six checks,
including one at five levels deep.

**Acceptance criteria:** your self-check passes; your README has both "never ends" sentences and a
trace table for one call.

**Grading:** same scale. Requirements Fit is judged on whether every function has a base case and the
loop guard works.

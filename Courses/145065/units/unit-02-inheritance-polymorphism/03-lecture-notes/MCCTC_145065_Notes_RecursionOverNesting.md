# Lecture Notes: Recursion Over a Nested Structure
## 145065 Object-Oriented Programming · Unit 2 · Week 4, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W04_RecursionOverNesting.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W04_RecursionOverNesting.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.3.8 write code that uses nested structures and recursion. This is the only place
in the course that teaches recursion, and 5.3 is about a quarter of the WebXam.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop.

---

## Why this exists

Line 3 is laid out in cells. The Finishing cell holds the oven and a smaller cell called Transfer,
which holds the conveyor. Next year Transfer may hold a smaller cell of its own. Nobody can promise
how deep it goes.

A loop can walk a list. Two nested loops can walk a list of lists. But every loop you write has a
fixed depth: someone had to decide how many levels to handle. When the data can nest to any depth,
the code has to be able to follow it to any depth. That is what recursion does.

---

## The concept in plain language

A **recursive function** calls itself on a smaller piece of the problem.

It fits any structure that contains more of itself. Folders hold files and folders. Comment threads
hold replies that hold replies. A cell holds machines and cells.

Every recursive function has two parts:

- **The base case** returns an answer without calling itself. For a count of machines, a machine
  counts as 1. It has nothing inside.
- **The recursive case** calls the function on each smaller piece and combines the answers. A cell
  counts whatever its items count.

Each call has to move toward the base case. Here, each call goes one level deeper, and every path
down the tree ends at a machine.

Python keeps a **stack** of calls that have started and not finished. Each recursive call adds one.
If a function never reaches its base case, the stack grows until Python stops it with a
`RecursionError`. The limit is usually 1000 calls deep.

---

## Worked example 1: counting machines at any depth

```python
# count_machines.py
class Machine:
    def __init__(self, tag):
        self.tag = tag


class Cell:
    def __init__(self, name, items):
        self.name = name
        self.items = items


line = Cell("Line 3", [
    Cell("Forming", [Machine("L3-PRS-01"), Machine("L3-PRS-02")]),
    Cell("Finishing", [Machine("L3-OVN-01"), Cell("Transfer", [Machine("L3-CNV-01")])]),
    Cell("Staging", [Machine("L3-RCK-01")]),
])


def count_machines(node):
    if isinstance(node, Machine):
        return 1                                                   # base case
    return sum(count_machines(child) for child in node.items)      # recursive case


print(count_machines(line))
print(count_machines(line.items[1]))
print(count_machines(Machine("L3-PRS-09")))
```

Output:

```
5
2
1
```

Trace `count_machines(line.items[1])`, the Finishing cell, by hand:

| Call | Is it a machine? | Returns |
|---|---|---|
| `count_machines(Finishing)` | no | count(`L3-OVN-01`) + count(`Transfer`) |
| `count_machines(L3-OVN-01)` | yes, base case | 1 |
| `count_machines(Transfer)` | no | count(`L3-CNV-01`) |
| `count_machines(L3-CNV-01)` | yes, base case | 1 |
| back in `Transfer` | | 1 |
| back in `Finishing` | | 1 + 1 = 2 |

The last line of output shows the base case alone: one machine counts 1.

---

## Worked example 2: knowing how deep you are

```python
# show_tree.py
class Machine:
    def __init__(self, tag):
        self.tag = tag


class Cell:
    def __init__(self, name, items):
        self.name = name
        self.items = items


line = Cell("Line 3", [
    Cell("Forming", [Machine("L3-PRS-01"), Machine("L3-PRS-02")]),
    Cell("Finishing", [Machine("L3-OVN-01"), Cell("Transfer", [Machine("L3-CNV-01")])]),
    Cell("Staging", [Machine("L3-RCK-01")]),
])


def show(node, depth=0):
    label = node.tag if isinstance(node, Machine) else node.name
    print("  " * depth + label)
    if isinstance(node, Cell):             # a machine has nothing inside: stop
        for child in node.items:
            show(child, depth + 1)         # one level deeper


show(line)
```

Output:

```
Line 3
  Forming
    L3-PRS-01
    L3-PRS-02
  Finishing
    L3-OVN-01
    Transfer
      L3-CNV-01
  Staging
    L3-RCK-01
```

`depth` is passed down and grows by one on each call, so each level indents two more spaces. Nobody
wrote "handle three levels." The data decided.

---

## Worked example 3: the same shape outside the shop

```python
# playlist_minutes.py
music = {"name": "Music", "songs": [3.5, 4.0], "folders": [
    {"name": "Gym", "songs": [2.75, 3.25, 4.5], "folders": []},
    {"name": "Road Trip", "songs": [5.0], "folders": [
        {"name": "Chill", "songs": [3.0, 3.5], "folders": []},
    ]},
]}


def total_minutes(folder):
    # A folder with no subfolders adds nothing from below: sum() of nothing is 0.
    return sum(folder["songs"]) + sum(total_minutes(sub) for sub in folder["folders"])


print(total_minutes(music))
print(total_minutes(music["folders"][1]))
```

Output:

```
29.5
11.5
```

A music folder holds songs and more folders. `total_minutes()` adds its own songs, then asks each
subfolder for its total. The base case is hidden inside `sum()`: a folder with no subfolders sums an
empty list, which is 0, and the recursion stops there. The second line is the Road Trip folder alone:
5.0 of its own plus 6.5 from Chill.

---

## The wrong version, twice

### No base case

```python
# count_no_base.py
class Machine:
    def __init__(self, tag):
        self.tag = tag


class Cell:
    def __init__(self, name, items):
        self.name = name
        self.items = items


line = Cell("Line 3", [
    Cell("Forming", [Machine("L3-PRS-01"), Machine("L3-PRS-02")]),
    Cell("Finishing", [Machine("L3-OVN-01"), Cell("Transfer", [Machine("L3-CNV-01")])]),
    Cell("Staging", [Machine("L3-RCK-01")]),
])


def count_machines(node):
    return sum(count_machines(child) for child in node.items)      # no base case


print(count_machines(line))
```

Output:

```
Traceback (most recent call last):
  File "...\count_no_base.py", line 24, in <module>
    print(count_machines(line))
          ~~~~~~~~~~~~~~^^^^^^
  File "...\count_no_base.py", line 21, in count_machines
    return sum(count_machines(child) for child in node.items)      # no base case
  File "...\count_no_base.py", line 21, in <genexpr>
    return sum(count_machines(child) for child in node.items)      # no base case
               ~~~~~~~~~~~~~~^^^^^^^
  File "...\count_no_base.py", line 21, in count_machines
    return sum(count_machines(child) for child in node.items)      # no base case
  File "...\count_no_base.py", line 21, in <genexpr>
    return sum(count_machines(child) for child in node.items)      # no base case
               ~~~~~~~~~~~~~~^^^^^^^
  File "...\count_no_base.py", line 21, in count_machines
    return sum(count_machines(child) for child in node.items)      # no base case
                                                  ^^^^^^^^^^
AttributeError: 'Machine' object has no attribute 'items'
```

The function asks every node for `.items`. The cells have items. The first machine does not, and the
recursion walks straight into it. **The fix** is the base case: `if isinstance(node, Machine): return
1`, before the line that reads `.items`.

### A base case the data never reaches

This version has the base case, and the data contains a loop: the line is placed inside one of its
own cells.

```python
# count_loop.py
class Machine:
    def __init__(self, tag):
        self.tag = tag


class Cell:
    def __init__(self, name, items):
        self.name = name
        self.items = items


line = Cell("Line 3", [
    Cell("Forming", [Machine("L3-PRS-01"), Machine("L3-PRS-02")]),
    Cell("Finishing", [Machine("L3-OVN-01"), Cell("Transfer", [Machine("L3-CNV-01")])]),
    Cell("Staging", [Machine("L3-RCK-01")]),
])


def count_machines(node):
    if isinstance(node, Machine):
        return 1
    return sum(count_machines(child) for child in node.items)


transfer = line.items[1].items[1]
transfer.items.append(line)              # the line is now inside one of its own cells
print(count_machines(line))
```

The output is about 2,500 lines of the same two calls repeating. Its first lines and its last lines:

```
Traceback (most recent call last):
  File "...\count_loop.py", line 28, in <module>
    print(count_machines(line))
          ~~~~~~~~~~~~~~^^^^^^
  File "...\count_loop.py", line 23, in count_machines
```

```
  File "...\count_loop.py", line 23, in count_machines
    return sum(count_machines(child) for child in node.items)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RecursionError: maximum recursion depth exceeded
```

The function is correct. The data is not a tree any more, so every path goes around forever and never
ends at a machine. **The fix belongs in the data:** `Cell.add()` refuses a cell that already contains
the cell it is being added to. Lab U02-02 step 6 writes that check. It is recursive too.

---

## Why the wrong version is tempting

The recursive line looks like it does all the work, so the base case feels optional. On the sample
data a missing base case sometimes still returns something, and the bug waits for different data.

Loops in data are tempting for a different reason: `append()` never asks where an object already
is. The habit that prevents both: **write the base case first, and guard the structure where things
are added**, not where they are read.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Recursion** | a function that calls itself on a smaller piece of the problem |
| **Base case** | the input a recursive function answers without calling itself |
| **Recursive case** | the part that calls the function again and combines the answers |
| **Nested structure** | data that contains more of the same kind of data |
| **Call stack** | the calls that have started and not yet returned |
| **`RecursionError`** | Python's error when the call stack grows past its limit |
| **Tree** | a nested structure with no loops: every path ends |

---

## Self-check

**Question 1.** In worked example 1, how many times is `count_machines` called in total for the whole
line? Count every call, including the first.

**Question 2.** Write the base case and the recursive case of `total_minutes()` in one plain-English
sentence each.

**Question 3.** Why can't the loop in the second wrong version be fixed by changing
`count_machines()` alone?

---

### Answers

**1.** Ten. One for Line 3, one for each of its three cells, one for Transfer, and one for each of the
five machines: 1 + 3 + 1 + 5 = 10.

**2.** Base case: a folder with no subfolders is worth the total of its own songs. Recursive case: any
other folder is worth its own songs plus the total of each subfolder.

**3.** The function already has a correct base case. The problem is that no path through the data
reaches it. You could add a "seen" set inside the function, but every other recursive function would
need one too. Refusing the loop in `Cell.add()` fixes the data once for every function that walks it.

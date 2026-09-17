# Lecture Notes: Where a Name Lives
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W03_WhereANameLives.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W03_WhereANameLives.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competency:** 5.2.2 identify the scope of data (e.g., global versus local, variables, constants,
arrays).

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop.

---

## Why this exists

In 145060 Unit 4 you met scope with two levels: a variable inside a function is local, and one at the
top of the file is global. Classes add two more levels, and the new ones produce the quietest bug in
this unit.

Here is the bug. You want one count shared by every machine. You write `self.starts_today += 1`. It
runs. It gives numbers. The numbers are wrong, and no error ever appears. Understanding why takes
knowing exactly where Python looks for a name and where it puts a new one.

This is also on the state exam. Competency 5.2.2 asks you to identify the scope of data.

---

## The concept in plain language

A name can live at four levels in a Python program with classes:

| Level | Where it is assigned | Who shares it | How long it lasts |
|---|---|---|---|
| **Module (global)** | at the top level of the file | every function and class in the file | while the program runs |
| **Class** | in the class body, outside any method | every object of the class | while the program runs |
| **Instance** | through `self.name = ...` | only that one object | as long as the object |
| **Local** | inside a function or method | only that one call | until the call returns |

### Reading follows a path

When you **read** `self.line_name`, Python checks the object first. If the object has no attribute by
that name, it checks the class. That is how every machine can read one shared `line_name`.

### Assigning does not follow the path

When you **assign** `self.line_name = ...`, Python does not look anywhere. It creates or replaces an
attribute **on that object**. From then on, that object's own attribute **shadows** the class
attribute. The class value did not change. That one object stopped seeing it.

The same rule applies to functions. Assigning to a name anywhere inside a function makes that name
local for the **whole** function, unless you declare otherwise.

### Constants

A module-level name in capitals, like `SITE_NAME`, is a **constant by convention**. It says "do not
change me". Like the underscore, Python does not enforce it.

### The `global` keyword

`global name` inside a function tells Python "assign to the module's name, not a new local". It works.
You should avoid it, because any function in the file can now change that value, and finding which
one did is slow. Pass the value in and return the new value instead. Inside a class, the object's own
attributes usually hold that state.

---

## Worked example 1: all four levels in one file

```python
# four_levels.py
SITE_NAME = "Riverside Fabrication"          # module (global) scope


class Machine:
    line_name = "Line 3"                     # class scope

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag           # instance scope

    def label(self):
        text = f"{SITE_NAME}, {self.line_name}, {self.asset_tag}"   # local scope
        return text


press = Machine("L3-PRS-01")
print(press.label())
try:
    print(text)
except NameError as error:
    print("Outside the method:", error)

SITE_NAME = "Somewhere Else"                 # capitals are a promise, not a lock
print(press.label())
```

Output:

```
Riverside Fabrication, Line 3, L3-PRS-01
Outside the method: name 'text' is not defined
Somewhere Else, Line 3, L3-PRS-01
```

`label` reads a global, a class attribute, and an instance attribute, and makes a local. The local
`text` is gone once `label` returns. The last line shows a "constant" being changed with no complaint.

---

## Worked example 2: shadowing a class attribute

```python
# scope_map.py
SITE_NAME = "Riverside Fabrication"          # module (global) scope


class Machine:
    line_name = "Line 3"                     # class scope: shared by every machine
    starts_today = 0                         # class scope: meant to be one shared count

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag           # instance scope: each machine has its own

    def start(self):
        self.starts_today += 1               # the deliberate mistake
        label = f"{SITE_NAME}, {self.line_name}"   # local scope: gone after return
        return f"{label}: {self.asset_tag} started"


press1, press2 = Machine("L3-PRS-01"), Machine("L3-PRS-02")
print(press1.start())
press1.start()
press2.start()
print("press1:", press1.starts_today, "press2:", press2.starts_today, "class:", Machine.starts_today)
press2.line_name = "Line 9"
print(press1.line_name, press2.line_name, Machine.line_name)
print(vars(press1), vars(press2))
```

Output:

```
Riverside Fabrication, Line 3: L3-PRS-01 started
press1: 2 press2: 1 class: 0
Line 3 Line 9 Line 3
{'asset_tag': 'L3-PRS-01', 'starts_today': 2} {'asset_tag': 'L3-PRS-02', 'starts_today': 1, 'line_name': 'Line 9'}
```

Three starts happened. The class count says 0. Here is what `self.starts_today += 1` really does:

1. **Read** `self.starts_today`. The object has none, so Python finds the class value, 0.
2. Add 1.
3. **Assign** `self.starts_today = 1`. That creates an instance attribute on this one machine.

Every later start on that machine reads its own copy. The class count is never touched. The last line,
`vars()`, shows each object's own attributes, and there are the two stray `starts_today` copies.

`press2.line_name = "Line 9"` is the same mistake from outside. One machine moved to Line 9. The
others did not.

The fix names the class when it changes class data:

```python
# scope_map_fixed.py
class Machine:
    starts_today = 0                         # class scope: one shared count

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def start(self):
        Machine.starts_today += 1            # name the class, not self


press1, press2 = Machine("L3-PRS-01"), Machine("L3-PRS-02")
press1.start()
press1.start()
press2.start()
print("press1:", press1.starts_today, "press2:", press2.starts_today, "class:", Machine.starts_today)
print(vars(press1), vars(press2))
```

Output:

```
press1: 3 press2: 3 class: 3
{'asset_tag': 'L3-PRS-01'} {'asset_tag': 'L3-PRS-02'}
```

Every machine reads the one shared count, and no object has a stray copy. A class method from
yesterday, changing `cls.starts_today`, is the other correct way.

---

## Worked example 3: `global` versus passing the value

```python
# alarms.py
alarms_today = 0


def record_alarm_global(asset_tag):
    global alarms_today                # works, and any function can now change it
    alarms_today += 1
    return f"{asset_tag}: alarm {alarms_today}"


def record_alarm(count, asset_tag):
    """Takes the count in and hands the new count back. No hidden state."""
    count += 1
    return count, f"{asset_tag}: alarm {count}"


print(record_alarm_global("L3-OVN-01"))
print(record_alarm_global("L3-OVN-01"))

count = 0
count, message = record_alarm(count, "L3-OVN-01")
print(message)
count, message = record_alarm(count, "L3-PRS-02")
print(message, "| count:", count)
```

Output:

```
L3-OVN-01: alarm 1
L3-OVN-01: alarm 2
L3-OVN-01: alarm 1
L3-PRS-02: alarm 2 | count: 2
```

Both versions count correctly. The difference is who can see the change. With `global`, you have to
read every function in the file to know who changes the count. With the second version, the change is
visible at the call: `count, message = ...`. In your refactor project, the rule is stronger still: no
state threaded through every function. State that belongs to something lives in that object.

---

## The wrong version, and the error it produces

```python
alarms_today = 0


def record_alarm(asset_tag):
    alarms_today += 1                # the deliberate mistake
    return f"{asset_tag}: alarm {alarms_today}"


print(record_alarm("L3-OVN-01"))
```

Output:

```
Traceback (most recent call last):
  File "...\alarm_count.py", line 9, in <module>
    print(record_alarm("L3-OVN-01"))
          ~~~~~~~~~~~~^^^^^^^^^^^^^
  File "...\alarm_count.py", line 5, in record_alarm
    alarms_today += 1                # the deliberate mistake
    ^^^^^^^^^^^^
UnboundLocalError: cannot access local variable 'alarms_today' where it is not associated with a value
```

`+=` assigns, so Python decides before the function runs that `alarms_today` is local for the whole
function. The line then tries to read the local before it has a value. The message says exactly that:
a local variable with no value yet.

Notice the contrast with example 2. For a function, the same shape crashes. For `self.name`, it runs
and gives a wrong number. The crash is the kinder of the two.

---

## Why the wrong version is tempting

Reading `alarms_today` inside the function works. Reading `self.starts_today` works. Both lines look
like "use the shared value and add one". The trap is that adding one is an **assignment**, and
assignment decides where the name lives.

`self.` is also a habit you spent all last week building, for good reason. For class-level data, it is
the wrong habit.

The tool that prevents both is a **scope map**: a short table, at the top of the file or in your
README, listing every important name and its level. Your refactor project requires one.

| Name | Level | Why it lives there |
|---|---|---|
| `SITE_NAME` | module | one value for the whole program, a constant |
| `Machine.starts_today` | class | one count shared by every machine |
| `self.asset_tag` | instance | each machine has its own |
| `label` in `start` | local | only needed during one call |

If a name's row is hard to fill in, the design is not settled yet.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Scope** | the part of a program where a name can be used |
| **Module (global) scope** | names assigned at the top level of a file |
| **Class scope** | names assigned in a class body, shared by every object |
| **Instance scope** | names assigned through `self`, one copy per object |
| **Local scope** | names assigned inside a function, gone when it returns |
| **Shadowing** | a name at a nearer level hiding the same name at a farther level |
| **Constant** | a name in capitals that the team agrees not to change |
| **`global`** | a keyword that makes a function assign to a module-level name |
| **`UnboundLocalError`** | reading a local variable before it has been given a value |
| **Scope map** | a table listing each important name and the level it lives at |

---

## Self-check

**Question 1.** `class Team: wins = 0`, and a method does `self.wins += 1`. Two teams each win once.
What do `team_a.wins`, `team_b.wins`, and `Team.wins` print?

**Question 2.** A function reads `MAX_TEMP_C` from the module and never assigns it. Does it need
`global`? Why?

**Question 3.** Fill in the scope level for each: (a) `total` inside `def average(scores)`;
(b) `self._songs` in `Playlist`; (c) `MAX_SONGS = 100` in the `Playlist` class body;
(d) `APP_NAME` at the top of `main.py`.

---

### Answers

**1.** `1`, `1`, and `0`. Each `self.wins += 1` read the class value 0 and created an instance
attribute of 1 on that team. The class attribute never changed. If the goal was one shared total,
the method should change `Team.wins`. If each team should have its own wins, then `self.wins` is
right, and it should be set in `__init__`, not in the class body.

**2.** No. `global` is only needed to **assign**. Reading a module-level name from inside a function
works, because Python looks outward when a name is not local.

**3.** (a) local. (b) instance. (c) class. (d) module, and a constant by convention.

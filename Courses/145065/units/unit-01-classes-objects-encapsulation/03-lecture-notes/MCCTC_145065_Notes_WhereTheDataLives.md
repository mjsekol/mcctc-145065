# Lecture Notes: Where the Data Lives
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W02_WhereTheDataLives.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W02_WhereTheDataLives.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.1.4 describe, compare, and contrast the basics of procedural, structured,
object-oriented (OO), and event-driven programming. 5.1.5 describe the concepts of data management
through programming languages. 5.3.12 write code to create classes, objects, and methods.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop. The badge ids like `tech-07` are invented too.

---

## Why this exists

You have already written a class. In 145060 Unit 7, Storm Relay v4 had `Room`, `Player`, and `Game`,
each with `__init__`, `self`, and methods. So this unit does not start from zero. It starts from a
harder question: **what does a class protect?**

Think back to the Data Pipeline in 145060 Unit 5. You built it with no classes allowed. The data sat
in dictionaries and lists, and loose functions received it and changed it. That worked. It also meant
any line in the program could change any value, with no check at all.

On a shop floor that matters. A press under lockout must not run. If the "running" flag is a dictionary
value, one careless line can set it, and the program never notices. This is the thread for the whole
course: **the dangerous design is the one that works today.**

---

## The concept in plain language

A program's data has to live somewhere. Where you put it decides who can change it.

- **Loose variables and dictionaries.** The data is in one place. The rules are in functions
  somewhere else. Nothing forces a caller to use the functions.
- **An object.** The data and the only operations allowed to change it live together. The object
  checks its inputs when it is built, so it can never exist in an invalid state. After that, its
  state changes only through its methods.

That second idea has a name you will use all semester: the object **guards its own rules**.

### A leading underscore means "internal"

In this course, an attribute name that starts with one underscore, like `self._running`, means:
**internal, change me only through my methods.** Treat it as a rule of the team.

Be clear about one thing now. Python does not enforce that rule. Week 3, Monday explains exactly what
the underscore does and does not do. Until then, you follow it because you agreed to.

### Why the examples use `is_running()` this week

This week you read an object's state through methods like `press.is_running()`. In Week 3 you learn
properties, and the same check becomes `press.is_running` with no parentheses. That change is planned.
Methods first, properties second.

### Four ways to organize a program

The exam asks you to compare four styles, called paradigms. They are not rivals. Most real programs
mix them.

| Paradigm | The main idea | A one-line example |
|---|---|---|
| **Procedural** | The program is a list of procedures (functions) that receive data and act on it | `start(press)`, where `press` is a dictionary |
| **Structured** | Control flows only through sequence, selection (`if`), and repetition (loops), in blocks with one way in and one way out | A shift report: a `for` loop over the log with an `if` inside |
| **Object-oriented** | Data and the behavior allowed to change it are bundled into objects | `press.start()`, where the press refuses if it is locked out |
| **Event-driven** | The program waits, then runs a handler when something happens | Your phone runs the snooze code when you tap Snooze |

Every Python program you have written is structured, because Python has no `goto`. Your methods this
week are structured code inside objects. In Unit 7 you write event-driven code in C#, where a button
click calls a method.

---

## Worked example 1: the data in a dictionary

This is 145060 style. The data is a dictionary. The rules are loose functions.

```python
# press_as_dict.py
# 145060 style: the data is a dictionary, the rules are loose functions.
press = {"tag": "L3-PRS-01", "running": False, "locked_by": None}


def lock_out(machine, badge):
    machine["running"] = False
    machine["locked_by"] = badge


def start(machine):
    if machine["locked_by"] is not None:
        print(machine["tag"], "is locked out and cannot start")
        return
    machine["running"] = True


lock_out(press, "tech-07")
start(press)                 # refused, correctly
press["running"] = True      # any line in the program can do this
print(press)
```

Output:

```
L3-PRS-01 is locked out and cannot start
{'tag': 'L3-PRS-01', 'running': True, 'locked_by': 'tech-07'}
```

The rule in `start` worked. Then the next line skipped it. The last line shows a locked-out press that
is running. No error. A dictionary also accepts typos without complaint:

```python
press = {"tag": "L3-PRS-01", "running": False, "locked_by": None}
press["runing"] = True       # a typo, and no error
print(press)
```

Output:

```
{'tag': 'L3-PRS-01', 'running': False, 'locked_by': None, 'runing': True}
```

---

## Worked example 2: the data in an object

```python
# press_as_object.py
# The data and the only operations allowed to change it, in one place.
class Machine:
    def __init__(self, asset_tag, rated_kw):
        if not isinstance(asset_tag, str) or not asset_tag.strip():
            raise ValueError("asset_tag must be a non-blank string")
        if isinstance(rated_kw, bool) or not isinstance(rated_kw, (int, float)):
            raise TypeError(f"rated_kw must be a number, not {type(rated_kw).__name__}")
        if rated_kw <= 0:
            raise ValueError(f"rated_kw must be above 0, not {rated_kw}")
        self.asset_tag = asset_tag.strip()
        self.rated_kw = float(rated_kw)
        # A leading underscore means "internal: change me only through my methods".
        self._running = False
        self._locked_by = None

    def lock_out(self, badge):
        self._running = False
        self._locked_by = badge

    def start(self):
        if self._locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self._locked_by}")
        self._running = True

    def is_running(self):
        return self._running

    def __repr__(self):
        return f"Machine(asset_tag={self.asset_tag!r}, rated_kw={self.rated_kw!r})"


press = Machine("L3-PRS-01", 15)
press.lock_out("tech-07")
try:
    press.start()
except RuntimeError as error:
    print("Refused:", error)
print(press, "running:", press.is_running())
```

Output:

```
Refused: L3-PRS-01 is locked out by tech-07
Machine(asset_tag='L3-PRS-01', rated_kw=15.0) running: False
```

The refusal is now an exception, not a printed line a caller can ignore. The state is underscored, so
your team knows not to touch it. `__repr__` makes the object print as something useful.

---

## Worked example 3: refusing to be built invalid

A rule checked in `__init__` runs for every object, every time. Using the `Machine` class above:

```python
attempts = [("L3-PRS-02", -5), ("   ", 10), ("L3-PRS-03", True), ("L3-PRS-04", "fast")]
for tag, kw in attempts:
    try:
        Machine(tag, kw)
    except (TypeError, ValueError) as error:
        print(f"Refused {tag!r}, {kw!r}: {error}")
```

Output:

```
Refused 'L3-PRS-02', -5: rated_kw must be above 0, not -5
Refused '   ', 10: asset_tag must be a non-blank string
Refused 'L3-PRS-03', True: rated_kw must be a number, not bool
Refused 'L3-PRS-04', 'fast': rated_kw must be a number, not str
```

Look at the third line. In Python, `True` counts as a number, so the class checks for `bool` first.
Without that check, a press rated at `True` would quietly become 1.0 kW. A rule in `__init__` also
means no other code has to remember to check. Every `Machine` that exists passed these tests.

---

## The wrong version, and what it produces

This is the mistake made live in class. It does not crash.

```python
class Machine:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self._running = False

    def start(self):
        _running = True          # the deliberate mistake: no "self."

    def is_running(self):
        return self._running


press = Machine("L3-PRS-01")
press.start()
print("running:", press.is_running())
```

Output:

```
running: False
```

Without `self.`, `_running` is a local variable inside `start`. It is created, set to `True`, and
thrown away when the method returns. The object never changed.

Two close cousins do crash. Forgetting `self` in the parameter list:

```python
    def start():
        self._running = True
```

```
Traceback (most recent call last):
  File "...\no_self.py", line 11, in <module>
    press.start()
    ~~~~~~~~~~~^^
TypeError: Machine.start() takes 0 positional arguments but 1 was given
```

Python hands the object to every method call. "1 was given" is the object you did not make room for.
And building an object without every required argument, against a `Machine` whose `__init__` takes
`asset_tag` and `rated_kw`:

```python
press = Machine("L3-PRS-01")
```

```
Traceback (most recent call last):
  File "...\build_press.py", line 7, in <module>
    press = Machine("L3-PRS-01")
TypeError: Machine.__init__() missing 1 required positional argument: 'rated_kw'
```

---

## Why the wrong version is tempting

In every function you wrote in 145060, `total = 0` made a variable you could use. Inside a method, the
same line still makes a local variable. Only `self.` puts the value on the object. The missing `self.`
is tempting because the line looks complete and nothing turns red.

The dictionary version is tempting for a different reason. It is shorter, and on the day you write
it, it works. The danger arrives later, when someone else adds a line.

The habit that prevents both: after you write a method that changes state, print the state through a
method and check it changed.

---

## Vocabulary

| Term | What it means |
|---|---|
| **State** | the data an object holds right now, like whether a press is running |
| **Class** | the blueprint that says what data an object holds and what it can do |
| **Object (instance)** | one thing built from a class, with its own state |
| **`__init__`** | the method that runs when an object is built. It sets and checks the starting state. |
| **`self`** | the object a method was called on |
| **Leading underscore** | the team rule "internal: change me only through my methods" |
| **`__repr__`** | the method that says how an object prints |
| **Procedural** | a style where functions receive data and act on it |
| **Structured** | a style that uses only sequence, selection, and repetition blocks |
| **Object-oriented** | a style that bundles data with the behavior allowed to change it |
| **Event-driven** | a style where handlers run when something happens |

---

## Self-check

**Question 1.** A procedural program keeps a press as a dictionary and has a `start` function that
checks for a lockout. Name one way a locked-out press can still end up running.

**Question 2.** A method contains `_count = _count + 1` instead of `self._count = self._count + 1`.
Does it crash, or does it give a wrong answer? Explain.

**Question 3.** A smart doorbell app shows a notification when someone presses the button. Which
paradigm describes that behavior, and why?

---

### Answers

**1.** Any line can write `press["running"] = True` directly and skip the function. Nothing forces a
caller to use `start`. A typo like `press["runing"]` can also add a new key without any error.

**2.** It crashes. `_count` on the right side is a local variable that has no value yet, so Python
raises `UnboundLocalError`. The version in the notes, `_running = True`, does not crash, because it
only assigns. Both are the same mistake: without `self.`, the object never changes.

**3.** Event-driven. The app does not run top to bottom and finish. It waits, and a handler runs when
the event (the button press) happens.

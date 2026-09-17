# Lecture Notes: Encapsulation, Honestly
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W03_EncapsulationHonestly.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W03_EncapsulationHonestly.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competency:** 5.3.12 write code to create classes, objects, and methods.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop. The badge id `tech-07` is invented.

---

## Why this exists

Last week you put a leading underscore on internal state and agreed to change it only through
methods. You were promised an honest answer about what that underscore does. Here it is: **nothing.**
Python does not stop anyone.

Many tutorials call `_name` "private" and `__name` "really private". Both claims are wrong in a way
that matters. If you believe Python protects your data, you stop protecting it yourself.

So today has two parts. First, the truth about underscores. Second, the tool Python does give you:
**properties**, which let an attribute run your rules every time it is set, including when the
object is built.

---

## The concept in plain language

### What the underscores really do

- **One underscore, `_running`.** A convention. It tells people "internal". Python allows any code to
  read it and write it.
- **Two underscores, `__locked_by`.** Inside a class, Python **renames** the attribute to
  `_Machine__locked_by`. This is called **name mangling**. Its real purpose is to stop a subclass from
  clobbering the name by accident. The attribute is renamed, not hidden. Anyone who knows the new
  name can change it.

Nothing enforces either one until Unit 6. In C#, `private` is checked by the compiler, and code that
touches a private field from outside does not build. That strictness is one of the things C# buys
you. Python trusts you instead.

### What a property does

A **property** looks like an attribute from outside and runs a method inside.

- The **getter**, marked `@property`, runs when code reads `press.rated_kw`.
- The **setter**, marked `@rated_kw.setter`, runs when code writes `press.rated_kw = 18.5`. It can
  check the value and refuse it.
- A property with a getter and **no setter** is **read-only**. Assigning to it raises an error.
- The value itself lives in an underscore attribute, `self._rated_kw`. The property is the guard in
  front of it.

Two rules make properties work:

1. Inside the setter, store the value in the **underscore** name.
2. Inside `__init__`, assign through the **property** name, so construction runs the same rules.

Last week you read state with `press.is_running()`. From today it is `press.is_running`, a
read-only property. That was planned. The data did not change. The way you ask for it did.

---

## Worked example 1: a guarded machine

```python
# guarded_machine.py
import math


class Machine:
    MAX_RATED_KW = 500.0

    def __init__(self, asset_tag, rated_kw):
        self._asset_tag = asset_tag
        self.rated_kw = rated_kw          # no underscore: this runs the setter
        self._running = False
        self.__locked_by = None           # two underscores: Python renames it

    @property
    def asset_tag(self):
        return self._asset_tag            # a getter and no setter: read-only

    @property
    def rated_kw(self):
        return self._rated_kw

    @rated_kw.setter
    def rated_kw(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"rated_kw must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or not 0 < value <= Machine.MAX_RATED_KW:
            raise ValueError(f"rated_kw must be above 0 and at most {Machine.MAX_RATED_KW:g}")
        self._rated_kw = float(value)

    @property
    def is_running(self):
        return self._running

    def lock_out(self, badge):
        self._running = False
        self.__locked_by = badge

    @property
    def locked_out_by(self):
        return self.__locked_by
```

```python
from guarded_machine import Machine

press = Machine("L3-PRS-01", 15)
press.rated_kw = 18.5                     # looks like an attribute, runs the rules
print(press.asset_tag, press.rated_kw, press.is_running)
for bad in [-5, float("nan"), "fast"]:
    try:
        press.rated_kw = bad
    except (TypeError, ValueError) as error:
        print("Refused:", error)
try:
    press.asset_tag = "L3-PRS-99"
except AttributeError as error:
    print("Refused:", error)
try:
    Machine("L3-PRS-02", 0)
except ValueError as error:
    print("Refused at construction:", error)
```

Output:

```
L3-PRS-01 18.5 False
Refused: rated_kw must be above 0 and at most 500
Refused: rated_kw must be above 0 and at most 500
Refused: rated_kw must be a number, not str
Refused: property 'asset_tag' of 'Machine' object has no setter
Refused at construction: rated_kw must be above 0 and at most 500
```

The calling code reads like plain attributes. Every write still goes through the rules. The last line
proves `__init__` uses the setter: a zero rating cannot even be built.

---

## Worked example 2: what the underscores do not stop

```python
from guarded_machine import Machine

press = Machine("L3-PRS-01", 15)

# What the underscores do NOT stop
press._running = True
print("running after press._running = True:", press.is_running)
press.lock_out("tech-07")
try:
    print(press.__locked_by)
except AttributeError as error:
    print("Hidden?", error)
press._Machine__locked_by = "anyone"
print("lock holder now:", press.locked_out_by)
print(list(vars(press)))
```

Output:

```
running after press._running = True: True
Hidden? 'Machine' object has no attribute '__locked_by'
lock holder now: anyone
['_asset_tag', '_rated_kw', '_running', '_Machine__locked_by']
```

Line one of the output: a single underscore stopped nothing. Line two looks like protection, but it
is only a missing name. Line three: the lock holder was replaced from outside the class. Line four
shows the renamed attribute sitting in plain view. Name mangling renames. It does not hide.

So what protects the machine? Your team. The underscore is a promise that code reviews enforce, and
Gate 2 this week asks you to catch broken promises.

---

## Worked example 3: two traps in a setter that looks fine

```python
# naive_setter.py
import math


class NaiveOven:
    def __init__(self, setpoint_c):
        self.setpoint_c = setpoint_c

    @property
    def setpoint_c(self):
        return self._setpoint_c

    @setpoint_c.setter
    def setpoint_c(self, value):
        if value <= 0:                     # looks like validation
            raise ValueError("setpoint must be above 0")
        self._setpoint_c = value


for sneaky in [True, float("nan")]:
    oven = NaiveOven(sneaky)
    print("accepted:", oven.setpoint_c)

nan = float("nan")
print(isinstance(True, int), True + True)
print(nan <= 0, nan > 0, nan == nan, math.isfinite(nan))
```

Output:

```
accepted: True
accepted: nan
True 2
False False False False
```

**The `True` trap.** In Python, `bool` is a kind of `int`, so `True` passes `value <= 0` as 1. Check
for `bool` first, as `Machine` does.

**The NaN trap.** NaN means "not a number". Every comparison with NaN is `False`, even `nan == nan`.
So `nan <= 0` is `False`, and the check waves it through. A NaN setpoint then poisons every
calculation it touches. `math.isfinite(value)` is `False` for NaN and for infinity, so
`not math.isfinite(value)` catches both.

---

## The wrong versions, and what they produce

### Mistake 1: the setter stores through the property

```python
class Machine:
    def __init__(self, rated_kw):
        self.rated_kw = rated_kw

    @property
    def rated_kw(self):
        return self._rated_kw

    @rated_kw.setter
    def rated_kw(self, value):
        if value <= 0:
            raise ValueError("rated_kw must be above 0")
        self.rated_kw = value         # the deliberate mistake: no underscore


press = Machine(15)
```

```
Traceback (most recent call last):
  File "...\recursive_setter.py", line 16, in <module>
    press = Machine(15)
  File "...\recursive_setter.py", line 3, in __init__
    self.rated_kw = rated_kw
    ^^^^^^^^^^^^^
  File "...\recursive_setter.py", line 13, in rated_kw
    self.rated_kw = value         # the deliberate mistake: no underscore
    ^^^^^^^^^^^^^
  File "...\recursive_setter.py", line 13, in rated_kw
    self.rated_kw = value         # the deliberate mistake: no underscore
    ^^^^^^^^^^^^^
  File "...\recursive_setter.py", line 13, in rated_kw
    self.rated_kw = value         # the deliberate mistake: no underscore
    ^^^^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Assigning to `self.rated_kw` runs the setter. The setter assigns to `self.rated_kw`, which runs the
setter. Python gives up after about a thousand calls. The fix is `self._rated_kw = value`.

### Mistake 2: `__init__` skips the setter

```python
class Machine:
    def __init__(self, rated_kw):
        self._rated_kw = rated_kw     # the deliberate mistake: skips the setter

    @property
    def rated_kw(self):
        return self._rated_kw

    @rated_kw.setter
    def rated_kw(self, value):
        if value <= 0:
            raise ValueError("rated_kw must be above 0")
        self._rated_kw = value


press = Machine(-5)
print("Built a press rated at", press.rated_kw, "kW")
```

```
Built a press rated at -5 kW
```

No error. This is the more dangerous mistake, because it is silent. The setter is correct and never
runs during construction, so every object can be born invalid. The fix is `self.rated_kw = rated_kw`
in `__init__`, with no underscore.

---

## Why the wrong versions are tempting

Mistake 1 is tempting because this lesson taught you "use the property name". Inside the setter is
the one place where that is wrong.

Mistake 2 is tempting because you also learned "internal state has an underscore", and
`__init__` sets internal state. Both rules are right. The skill is knowing which one applies where:
**the setter stores in the underscore name. Everyone else, including `__init__`, goes through the
property.**

The honesty part is tempting to skip for a different reason. "Private" is a comforting word. It is
safer to know exactly what Python does and to guard your data on purpose.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Encapsulation** | keeping an object's data behind the methods that guard it |
| **Convention** | a rule a team follows that the language does not enforce |
| **Name mangling** | Python renaming `__name` inside a class to `_ClassName__name` |
| **Property** | an attribute that runs a getter on read and a setter on write |
| **Getter** | the `@property` method that returns the value |
| **Setter** | the `@name.setter` method that checks and stores a new value |
| **Read-only property** | a property with a getter and no setter |
| **NaN** | "not a number", a float value that is unequal to everything, itself included |
| **`math.isfinite`** | `True` only for a real, finite number. `False` for NaN and infinity. |

---

## Self-check

**Question 1.** A classmate says "I used two underscores, so nobody outside the class can change it."
Write one line of code that proves them wrong for an attribute `__code` in a class `Locker`.

**Question 2.** A `Thermostat` setter checks `if not 10 <= value <= 30: raise ValueError(...)`. Does
it refuse `float("nan")`? Does it refuse `True`?

**Question 3.** `__init__` contains `self._setpoint_c = setpoint_c`, and the setter is correct. What
goes wrong, and when would anyone notice?

---

### Answers

**1.** `locker._Locker__code = "0000"`. Name mangling renamed the attribute to `_Locker__code`, and
that name can be read and written from anywhere.

**2.** It refuses NaN. `10 <= nan` is `False`, so the whole range check is `False`, `not` makes it
`True`, and the error is raised. It also refuses `True`, but only by luck, because `True` is 1 and 1
is outside 10 to 30. A range that includes 1 would accept it. Check for `bool` on purpose, and use
`math.isfinite` so the NaN check does not depend on how the comparison is written.

**3.** Construction skips validation, so a thermostat can be built with any setpoint, including a
negative one or NaN. Nobody notices at construction, because there is no error. It shows up later,
when some other code uses the bad value.

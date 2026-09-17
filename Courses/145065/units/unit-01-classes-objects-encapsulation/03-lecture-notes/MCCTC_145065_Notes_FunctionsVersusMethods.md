# Lecture Notes: Functions Versus Methods
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W02_FunctionsVersusMethods.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-01-classes-objects-encapsulation/04-slides/MCCTC_145065_Slides_W02_FunctionsVersusMethods.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competency:** 5.3.9 write code that creates and calls functions.

The examples use Riverside Fabrication, Line 3. It is a composite: an invented small metal
fabrication shop.

---

## Why this exists

Your 145060 Data Pipeline was all functions. Now you are turning programs like it into classes, and
every function asks the same question: **does this belong inside a class, or does it stay out?**

Get it wrong one way and you have a class stuffed with code that has nothing to do with it. Get it
wrong the other way and you have loose functions reaching into an object's internal data, which is
exactly the leak Monday's class was built to stop.

There is a rule for this. It fits in one sentence, and today you learn it.

---

## The concept in plain language

A **method** is a function that lives in a class and receives the object as its first parameter,
`self`. That is the whole difference.

When you write `press.status_text()`, Python runs `Machine.status_text(press)`. The object before the
dot becomes `self`. Nothing magic happens. It is a function call with the object passed in for you.

### The decision rule

> If the behavior needs **this object's data**, it is a method. If it needs **no object**, it stays a
> function.

Two signs that you have it wrong:

- **A function that reaches into an object's underscore data** is a method in the wrong place. Move
  it into the class, next to the data it reads.
- **A method that never uses `self`** probably did not need to be a method. A pure conversion, like
  Celsius to Fahrenheit, needs a number, not a machine. Leave it as a function.

Week 3, Tuesday adds a third home for behavior: static and class methods, for code that belongs with a
class but does not need one object. Today there are two homes.

---

## Worked example 1: a function and two methods

```python
# functions_and_methods.py
def celsius_to_fahrenheit(celsius):
    """A function: it needs a number, not a machine."""
    return celsius * 9 / 5 + 32


class Machine:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name
        self._temperature_c = None

    def record_temperature(self, celsius):
        """A method: it changes THIS machine's data."""
        self._temperature_c = celsius

    def status_text(self):
        """A method: it reads THIS machine's data."""
        if self._temperature_c is None:
            return f"{self.asset_tag} {self.name}: no reading"
        fahrenheit = celsius_to_fahrenheit(self._temperature_c)
        return f"{self.asset_tag} {self.name}: {self._temperature_c:.1f} C ({fahrenheit:.1f} F)"


press = Machine("L3-PRS-01", "Press 1")
print(press.status_text())
press.record_temperature(41.5)
print(press.status_text())
print(Machine.status_text(press))        # the same call, written out longhand
print(type(celsius_to_fahrenheit).__name__, type(press.status_text).__name__)
```

Output:

```
L3-PRS-01 Press 1: no reading
L3-PRS-01 Press 1: 41.5 C (106.7 F)
L3-PRS-01 Press 1: 41.5 C (106.7 F)
function method
```

Lines two and three are the same call. The last line shows Python's own names for the two kinds.
A method can call a function, as `status_text` calls `celsius_to_fahrenheit`. That is normal.

Notice `None` for "never read". A new press has no temperature, and zero would be a lie. Unit 8 builds
an operator panel on exactly that difference.

---

## Worked example 2: a function in the wrong place

```python
# hot_check.py
class Machine:
    HOT_C = 60.0

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self._temperature_c = None

    def record_temperature(self, celsius):
        self._temperature_c = celsius

    def is_hot(self):
        """The method version: the rule lives with the data it reads."""
        return self._temperature_c is not None and self._temperature_c > Machine.HOT_C


def is_hot(machine):
    """A method in the wrong place: it reads one machine's internal data."""
    return machine._temperature_c > 60


oven = Machine("L3-OVN-01")
oven.record_temperature(72.0)
print("function:", is_hot(oven), "method:", oven.is_hot())

new_press = Machine("L3-PRS-02")          # never read
print("method:", new_press.is_hot())
print("function:", is_hot(new_press))
```

Output:

```
function: True method: True
method: False
Traceback (most recent call last):
  File "...\hot_check.py", line 28, in <module>
    print("function:", is_hot(new_press))
                       ~~~~~~^^^^^^^^^^^
  File "...\hot_check.py", line 19, in is_hot
    return machine._temperature_c > 60
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'NoneType' and 'int'
```

The outside function works on the first machine and crashes on the second. It had to know two
internal facts: the attribute's name and that it can be `None`. The method already knows both,
because it sits beside the data. When the class changes, the method changes with it. The outside
function breaks somewhere else, later.

---

## Worked example 3: a function that should stay a function

```python
# time_text.py
def minutes_to_text(minutes, short=False):
    """A function: it needs a number of minutes, not a machine or a person."""
    hours, rest = divmod(minutes, 60)
    if short:
        return f"{hours}:{rest:02d}"
    return f"{hours} h {rest} min"


print(minutes_to_text(95))
print(minutes_to_text(95, short=True))
print(minutes_to_text(minutes=480))
# The same function works for a game night as well as a press run.
gaming_tonight = 45 + 70
print("Gaming tonight:", minutes_to_text(gaming_tonight))
```

Output:

```
1 h 35 min
1:35
8 h 0 min
Gaming tonight: 1 h 55 min
```

This is still the 145060 skill: a parameter with a default, a call by position, a call by keyword, and
a return value. It needs no object, so it stays a function. Putting it inside `Machine` would make it
unusable for your game night, and it would drag in a `self` it never reads.

---

## The wrong version, and the error it produces

Calling a method on the class with no object. This is a shorter `Machine`, so the error stands
out:

```python
# status_call.py
class Machine:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    def status_text(self):
        return f"{self.asset_tag} {self.name}"


press = Machine("L3-PRS-01", "Press 1")
print(Machine.status_text(press))
print(Machine.status_text())             # no object handed in
```

Output:

```
L3-PRS-01 Press 1
Traceback (most recent call last):
  File "...\status_call.py", line 12, in <module>
    print(Machine.status_text())             # no object handed in
          ~~~~~~~~~~~~~~~~~~~^^
TypeError: Machine.status_text() missing 1 required positional argument: 'self'
```

This error is the lesson in one line. `self` is a real parameter. Called through an object, Python
fills it. Called through the class, you must hand it the object, or it is missing. The question the
error asks is "status of which machine?"

---

## Why the wrong version is tempting

`Machine.status_text()` looks like asking the class for a status. In your head, "the machine" is one
thing. In code, `Machine` is the blueprint, and a blueprint has no temperature.

The misplaced function is tempting because it is how 145060 taught you to work. You had the data, you
wrote a function, you passed the data in. That habit is fine for a number. For an object with its own
rules, it spreads those rules across files.

The habit that prevents both: before you place a function, ask "which object's data does this read or
change?" One object means a method. No object means a function.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Function** | a named block of code defined with `def`, called by name |
| **Method** | a function defined in a class that receives the object as `self` |
| **Parameter** | a name in the `def` line that receives a value |
| **Argument** | the value passed in a call |
| **Default parameter** | a parameter with a value used when the call leaves it out |
| **Keyword argument** | an argument passed by name, like `minutes=480` |
| **Return value** | the value a call hands back with `return` |
| **Bound method** | `press.status_text`, a method already tied to one object |

---

## Self-check

**Question 1.** A procedural tool crib program has `def overdue_minutes(now, checked_out_at)`, which
subtracts two numbers. Method or function, and why?

**Question 2.** It also has `def check_in(tool): tool["holder"] = None`, where `tool` is a dictionary. After you write a `Tool`
class, where does `check_in` go, and why?

**Question 3.** Rewrite `press.record_temperature(41.5)` as a call through the class. What does Python
do with `press`?

---

### Answers

**1.** A function. It needs two numbers and no tool object. It could be used for anything timed.

**2.** It becomes a method, `Tool.check_in(self)`, because it changes one tool's internal data. Left
outside, it reaches into data the class is supposed to guard.

**3.** `Machine.record_temperature(press, 41.5)`. Python passes `press` as the first argument, which
the method calls `self`. `41.5` becomes `celsius`.

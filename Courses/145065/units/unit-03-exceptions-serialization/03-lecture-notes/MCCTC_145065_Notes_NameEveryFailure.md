# Lecture Notes: Name Every Failure You Plan For
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W06_NameEveryFailure.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-03-exceptions-serialization/04-slides/MCCTC_145065_Slides_W06_NameEveryFailure.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.3.10 code error handling techniques, including custom exception classes.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop. Badge ids,
ticket codes, and readings are invented.

---

## Why this exists

In 145060 you caught `ValueError` and `KeyError`. Those names describe what went wrong inside
Python: a bad conversion, a missing key. They do not describe what went wrong on Line 3.

Three different things can stop a press from starting. A technician has it locked out, so someone
may be inside it. The guard is open, so a person needs to look. Or the shift plan has a typo, so the
whole plan is suspect. Each needs a different response. If all three raise `RuntimeError`, the code
that catches them cannot tell them apart. If the handler says `except Exception`, it cannot even tell
them from a bug.

---

## The concept in plain language

**An exception is an object, and its class is its name.** You can write your own exception classes,
and arrange them in a family with inheritance, exactly like the equipment hierarchy.

- A **root** class for the family (`PlantError`) lets one `except` clause catch every failure the
  family plans for.
- **Child classes** name specific failures (`LockoutError`, `EquipmentStateError`), so a handler can
  catch exactly the one it knows how to handle.
- A class can **carry data**. `EquipmentError` stores `asset_tag`, so a handler can act on the tag
  without picking it out of the message text.
- A class can **also inherit a built-in exception**. `ConfigurationError(PlantError, ValueError)`
  means code written last month that says `except ValueError` still catches it. That is how you
  change an error type without breaking the people who catch it.

Three rules for handlers:

1. **Catch the narrowest class that tells you what to do next.** Python takes the **first** `except`
   clause that matches, so specific classes go above their parents.
2. **Never catch `Exception` to be safe.** An error nobody planned for is a bug. Let it stop the
   program where you can see it.
3. **When you convert one error into another, keep the cause:** `raise NewError(...) from error`.
   The traceback then shows both, and says which caused which.

---

## Worked example 1: a family, and handlers that choose

```python
# plant_errors.py
class PlantError(Exception):
    """Root of the family. except PlantError catches every member."""


class ConfigurationError(PlantError, ValueError):
    """A value the model refuses. Still a ValueError for older callers."""


class EquipmentError(PlantError):
    def __init__(self, asset_tag, message):
        self.asset_tag = asset_tag                    # data a handler can use
        super().__init__(f"{asset_tag}: {message}")


class LockoutError(EquipmentError):
    """Locked out, or the wrong badge."""


class EquipmentStateError(EquipmentError):
    """Wrong state: guard open, not running."""


def start(tag, locked_by=None, guard_closed=True):
    if locked_by is not None:
        raise LockoutError(tag, f"locked out by {locked_by}")
    if not guard_closed:
        raise EquipmentStateError(tag, "guard is open")
    return f"{tag} started"


for args in [("L3-PRS-01",), ("L3-PRS-02", "tech-07"), ("L3-PRS-03", None, False)]:
    try:
        print(start(*args))
    except LockoutError as error:
        print(f"SKIP, someone is inside: {error} (tag {error.asset_tag})")
    except EquipmentStateError as error:
        print(f"NEEDS A PERSON: {error}")
print([cls.__name__ for cls in LockoutError.__mro__])
```

Output:

```
L3-PRS-01 started
SKIP, someone is inside: L3-PRS-02: locked out by tech-07 (tag L3-PRS-02)
NEEDS A PERSON: L3-PRS-03: guard is open
['LockoutError', 'EquipmentError', 'PlantError', 'Exception', 'BaseException', 'object']
```

The locked-out press and the open guard are both `EquipmentError`s, and each got its own handler and
its own response. The last line is the family tree Python searches when it matches an `except`
clause: a `LockoutError` is also an `EquipmentError`, a `PlantError`, and an `Exception`.

---

## Worked example 2: converting an error and keeping its cause

```python
# setpoint_from.py
class PlantError(Exception):
    """Root of the family. except PlantError catches every member."""


class ConfigurationError(PlantError, ValueError):
    """A value the model refuses. Still a ValueError for older callers."""


class EquipmentError(PlantError):
    def __init__(self, asset_tag, message):
        self.asset_tag = asset_tag                    # data a handler can use
        super().__init__(f"{asset_tag}: {message}")


class LockoutError(EquipmentError):
    """Locked out, or the wrong badge."""


class EquipmentStateError(EquipmentError):
    """Wrong state: guard open, not running."""


def parse_setpoint(text):
    try:
        return float(text)
    except ValueError as error:
        raise ConfigurationError(f"setpoint {text!r} is not a number") from error


print(parse_setpoint("205"))
try:
    parse_setpoint("2O5")
except ConfigurationError as error:
    print("caught:", error)
    print("cause: ", repr(error.__cause__))
    print("still a ValueError:", isinstance(error, ValueError))
parse_setpoint("2O5")
```

Output:

```
205.0
caught: setpoint '2O5' is not a number
cause:  ValueError("could not convert string to float: '2O5'")
still a ValueError: True
Traceback (most recent call last):
  File "...\setpoint_from.py", line 26, in parse_setpoint
    return float(text)
ValueError: could not convert string to float: '2O5'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "...\setpoint_from.py", line 38, in <module>
    parse_setpoint("2O5")
    ~~~~~~~~~~~~~~^^^^^^^
  File "...\setpoint_from.py", line 28, in parse_setpoint
    raise ConfigurationError(f"setpoint {text!r} is not a number") from error
ConfigurationError: setpoint '2O5' is not a number
```

Inside the `try`, the handler caught a `ConfigurationError` whose `__cause__` is the original
`ValueError`. It is still a `ValueError` too, so older code keeps working. The last call is not
caught, so Python prints both errors, joined by **"The above exception was the direct cause of the
following exception."** That sentence comes from `from error`.

Without `from`, Python prints a different sentence: **"During handling of the above exception,
another exception occurred."** That wording suggests a second, accidental failure inside the handler.
`from` says the conversion was on purpose.

---

## Worked example 3: the same idea at a school dance

```python
# dance_tickets.py
class TicketError(Exception):
    """Anything that stops a ticket sale."""


class SoldOutError(TicketError):
    pass


class NotOnListError(TicketError):
    def __init__(self, ticket_code):
        self.ticket_code = ticket_code
        super().__init__(f"{ticket_code} is not on the guest list")


GUEST_LIST = {"T-1001", "T-1002"}
capacity = {"left": 1}


def check_in(code):
    if code not in GUEST_LIST:
        raise NotOnListError(code)
    if capacity["left"] == 0:
        raise SoldOutError("the gym is at capacity")
    capacity["left"] -= 1
    return f"{code} checked in"


for code in ["T-1001", "T-9999", "T-1002"]:
    try:
        print(check_in(code))
    except NotOnListError as error:
        print(f"send to the front table: {error.ticket_code}")
    except SoldOutError as error:
        print(f"wait outside: {error}")
```

Output:

```
T-1001 checked in
send to the front table: T-9999
wait outside: the gym is at capacity
```

`T-9999` is not on the list, so that person goes to the front table. `T-1002` is on the list, but the
gym is full, so that person waits. Both are `TicketError`s. The door staff respond differently
because the classes are different, and `NotOnListError` carries the code they need.

---

## The wrong version, twice

### Catching everything

```python
# swallowed_bug.py
readings = {"L3-OVN-01": 212.4, "L3-PRS-01": 3.1}


def percent_of_limit(tag, limit):
    return round(readings[tag] / limit * 100)


for tag, limit in [("L3-OVN-01", 240), ("L3-PRS-01", 0), ("L3-CNV-01", 1.5)]:
    try:
        print(tag, percent_of_limit(tag, limit), "%")
    except Exception:
        print(tag, "no reading")
```

Output:

```
L3-OVN-01 88 %
L3-PRS-01 no reading
L3-CNV-01 no reading
```

Two lines say "no reading," and neither is true in the same way. `L3-CNV-01` really has no reading:
that was a `KeyError`. `L3-PRS-01` has a reading of 3.1, and the program hit a **bug**: a limit of 0
caused `ZeroDivisionError`. `except Exception` gave both the same excuse. **The fix** catches
`KeyError` for the missing reading and lets the `ZeroDivisionError` crash, where someone will fix the
bad limit.

### The parent above the child

```python
# parent_first.py
class PlantError(Exception):
    """Root of the family. except PlantError catches every member."""


class ConfigurationError(PlantError, ValueError):
    """A value the model refuses. Still a ValueError for older callers."""


class EquipmentError(PlantError):
    def __init__(self, asset_tag, message):
        self.asset_tag = asset_tag                    # data a handler can use
        super().__init__(f"{asset_tag}: {message}")


class LockoutError(EquipmentError):
    """Locked out, or the wrong badge."""


class EquipmentStateError(EquipmentError):
    """Wrong state: guard open, not running."""


def start(tag, locked_by):
    raise LockoutError(tag, f"locked out by {locked_by}")


try:
    start("L3-PRS-02", "tech-07")
except EquipmentError as error:
    print("generic handler:", error)
except LockoutError as error:
    print("lockout handler:", error)
```

Output:

```
generic handler: L3-PRS-02: locked out by tech-07
```

No error, and the lockout handler never ran. Python checks `except` clauses from the top and takes
the first that matches. A `LockoutError` **is an** `EquipmentError`, so the first clause took it.
**The fix:** put `except LockoutError` above `except EquipmentError`.

---

## Why the wrong version is tempting

`except Exception` feels responsible. The program never crashes, the demo always finishes, and the
output always looks tidy. The cost is invisible until a real bug is reported as a routine event.

Putting the parent first is tempting because it reads naturally, general case first. Python reads it
the same way and stops at the general case.

The habits that prevent both: **name the failure before you catch it**, and **order `except` clauses
from most specific to most general.**

---

## Vocabulary

| Term | What it means |
|---|---|
| **Exception** | an object that signals something went wrong; its class says what |
| **Custom exception** | an exception class you write, usually inheriting from `Exception` |
| **Exception hierarchy (family)** | exception classes arranged with inheritance under one root |
| **Handler** | an `except` clause and the code under it |
| **Exception chaining** | `raise NewError(...) from error`, which stores the original as `__cause__` |
| **Swallowing an error** | catching an exception and continuing as if nothing happened |

---

## Self-check

**Question 1.** Which of these catches a `LockoutError`: `except PlantError`, `except ValueError`,
`except EquipmentStateError`, `except Exception`?

**Question 2.** Why does `ConfigurationError` inherit from `ValueError` as well as `PlantError`?

**Question 3.** Rewrite the handler in the first wrong version so the missing reading and the bug are
treated differently. What does the program print?

---

### Answers

**1.** `except PlantError` and `except Exception`. A `LockoutError` is not a `ValueError`, and it is a
sibling of `EquipmentStateError`, not a child.

**2.** So code that already catches `ValueError` keeps catching bad values after the model switched to
`ConfigurationError`. It changes the error's name without breaking its callers.

**3.** Catch only the failure you planned for:

```python
# swallowed_fixed.py
readings = {"L3-OVN-01": 212.4, "L3-PRS-01": 3.1}


def percent_of_limit(tag, limit):
    return round(readings[tag] / limit * 100)


for tag, limit in [("L3-OVN-01", 240), ("L3-PRS-01", 0), ("L3-CNV-01", 1.5)]:
    try:
        print(tag, percent_of_limit(tag, limit), "%")
    except KeyError:
        print(tag, "no reading")
```

Output:

```
L3-OVN-01 88 %
Traceback (most recent call last):
  File "...\swallowed_fixed.py", line 11, in <module>
    print(tag, percent_of_limit(tag, limit), "%")
               ~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "...\swallowed_fixed.py", line 6, in percent_of_limit
    return round(readings[tag] / limit * 100)
                 ~~~~~~~~~~~~~~^~~~~~~
ZeroDivisionError: float division by zero
```

The oven prints, then the program stops at `L3-PRS-01`. That crash is correct: a limit of 0 is a
mistake in the data, and now someone sees it. `L3-CNV-01` never runs in this version; once the bad
limit is fixed, it prints `no reading`.

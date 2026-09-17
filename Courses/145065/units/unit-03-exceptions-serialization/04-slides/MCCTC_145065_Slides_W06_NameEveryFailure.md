# Name Every Failure You Plan For
---
## Slide 1: Four failures, one message
- Step 1 failed: something went wrong
- Step 2 failed: something went wrong
- Step 5 failed: something went wrong
- Step 7 done: the oven started anyway
Speaker notes: This is the real output of your lab starter. A locked-out press, an open guard, a typo in the plan, and an unknown tag all print the same sentence. Then the program starts the oven after the plan was already known to be wrong. One except clause caught everything, so nothing could respond correctly.
Image: A report printout with four identical lines highlighted in launch red.
---
## Slide 2: Different failures, different responses
- Locked out: skip it, never retry
- Guard open: a person must look
- Typo in the plan: stop the whole plan
- A bug: crash where you can see it
Speaker notes: Each of these needs a different response. A lockout means someone may be inside the machine. An open guard needs a person. A typo means nothing after it can be trusted. And an error nobody planned for is a bug, and bugs should stop the program.
Image: Four road signs: skip, look, stop, and crash barrier.
---
## Slide 3: An exception is a class
```python
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
```
Speaker notes: A root for the family. A configuration error that is also a value error, so older code that catches value error keeps working. An equipment error that stores the asset tag as data. Two children for the two equipment failures.
Image: None. This slide is code.
---
## Slide 4: Handlers that choose
```python
for args in [("L3-PRS-01",), ("L3-PRS-02", "tech-07"), ("L3-PRS-03", None, False)]:
    try:
        print(start(*args))
    except LockoutError as error:
        print(f"SKIP, someone is inside: {error} (tag {error.asset_tag})")
    except EquipmentStateError as error:
        print(f"NEEDS A PERSON: {error}")
print([cls.__name__ for cls in LockoutError.__mro__])
```
```
L3-PRS-01 started
SKIP, someone is inside: L3-PRS-02: locked out by tech-07 (tag L3-PRS-02)
NEEDS A PERSON: L3-PRS-03: guard is open
['LockoutError', 'EquipmentError', 'PlantError', 'Exception', 'BaseException', 'object']
```
Speaker notes: Two handlers, two responses, and the lockout handler reads the tag straight from the error. The last line is the family tree Python walks when it matches an except clause.
Image: None. This slide is code.
---
## Slide 5: Keep the cause
```python
def parse_setpoint(text):
    try:
        return float(text)
    except ValueError as error:
        raise ConfigurationError(f"setpoint {text!r} is not a number") from error
```
```
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
Speaker notes: When you turn a value error into your own error, write from error. The traceback then shows both, joined by the sentence: the above exception was the direct cause. Without from, Python says during handling, another exception occurred, which sounds like an accident.
Image: None. This slide is code.
---
## Slide 6: The wrong way: parent first
```python
try:
    start("L3-PRS-02", "tech-07")
except EquipmentError as error:
    print("generic handler:", error)
except LockoutError as error:
    print("lockout handler:", error)
```
```
generic handler: L3-PRS-02: locked out by tech-07
```
Speaker notes: No error. But the lockout handler never ran. Python takes the first except clause that matches, and a lockout error is an equipment error, so the first clause took it. Specific classes go above their parents.
Image: None. This slide is code.
---
## Slide 7: The wrong way: catching everything
- except Exception: print("no reading")
- A missing reading gets that message
- A divide-by-zero bug gets it too
- The bug is hidden forever
Speaker notes: The other wrong way looks responsible. Catch everything, print something tidy, keep going. In the notes, a limit of zero causes a division error, and the program calls it no reading, the same as a sensor that really has none. The bug never gets fixed because nobody ever sees it.
Image: A rug with a bulge under it labeled bug.
---
## Slide 8: Three rules for handlers
- Catch the narrowest class that tells you what to do
- Order clauses from specific to general
- Convert with raise ... from error
Speaker notes: Three rules. Catch only what you know how to handle. Put children above parents. And when you convert an error, keep its cause.
Image: A numbered list on a clipboard, launch blue.
---
## Slide 9: Changing an error type safely
- Last week: raise ValueError
- This week: raise ConfigurationError
- ConfigurationError is also a ValueError
- Old callers keep working
Speaker notes: Here is a design move worth remembering. The model used to raise value error. Now it raises configuration error. Because configuration error also inherits value error, every caller that already says except value error still works. You changed the name without breaking anyone.
Image: An adapter plug connecting an old socket to a new plug.
---
## Slide 10: What you are about to build
- Lab U03-01, Failures With Names
- Six exception classes
- Replace every built-in raise in the model
- Four handlers, and stop on a bad plan
- Then your own project's error family
Speaker notes: The lab gives you the starter that prints something went wrong. You write the six classes, change every raise in the model, chain the setpoint error, give each failure its own handler, and stop the plan on a configuration error. Self-check eight of eight. Build 2 is your own hierarchy's error family.
Image: A family tree of six error classes under PlantError.

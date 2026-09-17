# Lecture Notes: Override to Extend, and Keep the Parent's Promise
## 145065 Object-Oriented Programming · Unit 2 · Week 4, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W04_OverrideToExtend.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W04_OverrideToExtend.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.3.12 write code to create classes, objects, and methods.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop. Badge ids such as
`tech-07` are invented and stand for no one.

---

## Why this exists

A press follows every rule powered equipment follows, plus one more: it must not start with its
guard open. So `Press` needs its own `start()`. The danger is in how you write it.

If `Press.start()` checks the guard and nothing else, it has quietly thrown away the lockout rule
its parent enforced. A technician locks the press out, someone closes the guard, and the press
starts. That is the most dangerous kind of bug in this course: **it works today**, and it removes a
safety rule without an error.

---

## The concept in plain language

When a child class defines a method with the same name as a parent's method, the child's version
**overrides** the parent's. Python finds the child's version first (the method resolution order from
Monday) and never looks further.

There are two ways to override:

- **Replace.** The child's method does its own thing and never runs the parent's. Everything the
  parent's method did is gone.
- **Extend.** The child's method adds its rule and calls `super().method(...)`, so the parent's rule
  still runs. This is almost always what you want.

A parent's method makes a **promise** to everyone who calls it. `stop()` promises "after this, the
machine is stopped." `lock_out()` relies on that promise: it calls `self.stop()` before it records
the lock. Any child that overrides `stop()` must keep the promise, or `lock_out()` breaks in a class
nobody touched.

---

## Worked example 1: replacing, and what it throws away

```python
# replacing_press.py
class PoweredEquipment:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self.running = False
        self.locked_by = None

    def start(self):
        if self.locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self.locked_by}")
        self.running = True

    def stop(self):
        self.running = False

    def lock_out(self, badge):
        self.stop()
        self.locked_by = badge


class Press(PoweredEquipment):
    def __init__(self, asset_tag):
        super().__init__(asset_tag)
        self.guard_closed = False

    def start(self):                      # REPLACES the parent's start()
        if not self.guard_closed:
            raise RuntimeError(f"{self.asset_tag} guard is open")
        self.running = True


press = Press("L3-PRS-01")
press.lock_out("tech-07")
press.guard_closed = True
press.start()
print("running:", press.running, "| locked by:", press.locked_by)
```

Output:

```
running: True | locked by: tech-07
```

The press is running while it is locked out. `Press.start()` replaced the parent's `start()`, and the
lockout check lived only in the parent.

---

## Worked example 2: extending, so both rules run

```python
# extending_press.py
class PoweredEquipment:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self.running = False
        self.locked_by = None

    def start(self):
        if self.locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self.locked_by}")
        self.running = True

    def stop(self):
        self.running = False

    def lock_out(self, badge):
        self.stop()
        self.locked_by = badge


class Press(PoweredEquipment):
    def __init__(self, asset_tag):
        super().__init__(asset_tag)
        self.guard_closed = False

    def start(self):                      # EXTENDS the parent's start()
        if not self.guard_closed:
            raise RuntimeError(f"{self.asset_tag} guard is open")
        super().start()                   # the lockout rule still runs

    def open_guard(self):
        self.guard_closed = False
        self.stop()                       # whatever stop() means for this object


press = Press("L3-PRS-01")
press.guard_closed = True
press.start()
press.open_guard()
print("after open_guard, running:", press.running)
press.lock_out("tech-07")
press.guard_closed = True
press.start()
```

Output:

```
after open_guard, running: False
Traceback (most recent call last):
  File "...\extending_press.py", line 43, in <module>
    press.start()
    ~~~~~~~~~~~^^
  File "...\extending_press.py", line 29, in start
    super().start()                   # the lockout rule still runs
    ~~~~~~~~~~~~~^^
  File "...\extending_press.py", line 10, in start
    raise RuntimeError(f"{self.asset_tag} is locked out by {self.locked_by}")
RuntimeError: L3-PRS-01 is locked out by tech-07
```

Two things to notice.

1. `open_guard()` calls `self.stop()` instead of setting `self.running = False` itself. Whatever
   `stop()` means for this object, it happens. If a subclass ever needs a longer stop sequence, it
   overrides `stop()` and `open_guard()` gets it for free.
2. The last `start()` raises the parent's error. The guard was closed, so `Press.start()` passed its
   own check and called `super().start()`, and the lockout rule did its job.

That traceback is the program working correctly.

---

## Worked example 3: extending text as well as rules

```python
# group_preview.py
class Notification:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text

    def preview(self):
        return f"{self.sender}: {self.text[:20]}"


class GroupNotification(Notification):
    def __init__(self, sender, text, group):
        super().__init__(sender, text)
        self.group = group

    def preview(self):
        return f"[{self.group}] {super().preview()}"


for note in (Notification("Maya", "are you coming to practice tonight"),
             GroupNotification("Jordan", "bus leaves at 3:15 sharp", "Robotics")):
    print(note.preview())
```

Output:

```
Maya: are you coming to pr
[Robotics] Jordan: bus leaves at 3:15 s
```

`GroupNotification.preview()` does not rebuild the sender and the shortened text. It asks the parent
for that part with `super().preview()` and adds the group name in front. If the parent changes how
it shortens messages, the group version changes with it.

---

## The wrong version: an override that breaks a promise

```python
# lazy_press.py
class PoweredEquipment:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self.running = False
        self.locked_by = None

    def start(self):
        if self.locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self.locked_by}")
        self.running = True

    def stop(self):
        self.running = False

    def lock_out(self, badge):
        self.stop()
        self.locked_by = badge


class Press(PoweredEquipment):
    def __init__(self, asset_tag):
        super().__init__(asset_tag)
        self.guard_closed = False

    def start(self):                      # EXTENDS the parent's start()
        if not self.guard_closed:
            raise RuntimeError(f"{self.asset_tag} guard is open")
        super().start()                   # the lockout rule still runs

    def open_guard(self):
        self.guard_closed = False
        self.stop()                       # whatever stop() means for this object


class LazyPress(Press):
    def stop(self):
        pass                              # "the ram returns by itself"


press = LazyPress("L3-PRS-01")
press.guard_closed = True
press.start()
press.open_guard()
print("guard closed:", press.guard_closed, "| running:", press.running)
press.lock_out("tech-07")
print("locked by:", press.locked_by, "| running:", press.running)
```

Output:

```
guard closed: False | running: True
locked by: tech-07 | running: True
```

**There is no error message.** That is the problem. `LazyPress.stop()` does nothing, so:

- `open_guard()` called `self.stop()` and the press kept running with its guard open.
- `lock_out()` called `self.stop()` and recorded a lockout on a running press.

Neither `open_guard()` nor `lock_out()` was changed. Both are now wrong, because a method they rely
on broke its promise.

**The fix:** an override of `stop()` does its extra work and then calls `super().stop()`.

```python
    def stop(self):
        self.arc_on = False       # this kind's own step first (a welder's arc)
        super().stop()            # then the promise: stopped
```

---

## Why the wrong version is tempting

Overriding feels like writing a new method, so people write it from scratch and forget the parent
had a body at all. Tests often check the new class's new behavior and never call the inherited
methods that depend on the overridden one.

The habit that prevents it: **every override asks two questions.** Does my version still call
`super()`? What does the parent's version promise, and does mine still promise it?

---

## Vocabulary

| Term | What it means |
|---|---|
| **Override** | a child method with the same name as a parent method; the child's runs instead |
| **Replace** | an override that never calls the parent's version |
| **Extend** | an override that adds behavior and calls `super().method()` |
| **Contract (promise)** | what a method guarantees to its callers, such as "after `stop()`, not running" |
| **Template method** | a parent method that calls other methods a child can override, such as `lock_out()` calling `stop()` |

---

## Self-check

**Question 1.** In worked example 2, why did `open_guard()` set `running` to `False` even though it
contains no line that mentions `running`?

**Question 2.** A `Welder` overrides `stop()` to turn off its arc and calls nothing else. What does
`welder.lock_out("tech-07")` leave behind?

**Question 3.** Rewrite worked example 3's `GroupNotification.preview()` as a replacement instead of
an extension. What would you have to copy, and what would break later?

---

### Answers

**1.** It calls `self.stop()`, and `stop()` sets `running` to `False`. The rule lives in one place.

**2.** A welder with its arc off and `running` still `True`, and a lockout recorded on it. The
override did the welder's extra step and dropped the promise that the machine is stopped.

**3.** You would copy `f"{self.sender}: {self.text[:20]}"` into the child. If the parent later
changed the preview (say, 30 characters instead of 20), group notifications would keep the old
length, and nothing would say so.

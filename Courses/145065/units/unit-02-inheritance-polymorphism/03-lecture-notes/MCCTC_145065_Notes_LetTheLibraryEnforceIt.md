# Lecture Notes: Let the Standard Library Enforce the Design
## 145065 Object-Oriented Programming · Unit 2 · Week 4, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W04_LetTheLibraryEnforceIt.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W04_LetTheLibraryEnforceIt.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.5.2 develop programs that use reuse libraries. 5.3.12 write code to create
classes, objects, and methods.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop.

---

## Why this exists

Your hierarchy has a rule nobody can see: every concrete kind of equipment must say what it checks
during an inspection. On Tuesday that rule lived in a comment. A comment is a request. The next
person to add a `Grinder` can skip it, and the grinder will pass every inspection because it never
reports anything.

You also keep writing the same kind of class over and over: a small record with three fields, an
`__init__` that copies them, an `__eq__` so two equal records compare equal, and a `__repr__` so it
prints usefully. That is twelve lines of code with a place to make a mistake in every one.

The Python standard library already solved both problems. A **reuse library** is code someone else
wrote, tested, documented, and keeps maintaining, that your program builds on instead of rewriting.
The standard library comes with Python, so nothing is installed.

---

## The concept in plain language

**`abc`, abstract base classes.** Import `ABC` and `abstractmethod`. A class that inherits from `ABC`
and marks a method with `@abstractmethod` is **abstract**: Python refuses to create an object from
it, and refuses to create an object from any subclass that has not written that method. The rule is
no longer a comment. It is enforced the moment someone tries to build the object.

**The template method.** An abstract base often has one ordinary method that calls the abstract one.
`inspect()` runs the shared checks, then calls `_kind_findings()`. Every kind answers the same
question in the same order, and a kind cannot forget the shared part, because it never writes
`inspect()` at all.

**`dataclasses`, records written for you.** Put `@dataclass` above a class with annotated fields and
Python writes `__init__`, `__eq__`, and `__repr__`. Add `frozen=True` and the record cannot be
changed after it is made, which is what a record of something that already happened should be. Add
`__post_init__` when a field needs checking.

---

## Worked example 1: an abstract base with a template method

```python
# abstract_rack.py
from abc import ABC, abstractmethod


class Equipment(ABC):
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def inspect(self):
        """The template: shared checks first, then this kind's own."""
        return self.common_findings() + self._kind_findings()

    def common_findings(self):
        return []

    @abstractmethod
    def _kind_findings(self):
        """Every concrete kind must answer this."""


class StorageRack(Equipment):
    def __init__(self, asset_tag, load_kg, capacity_kg):
        super().__init__(asset_tag)
        self.load_kg = load_kg
        self.capacity_kg = capacity_kg

    def _kind_findings(self):
        if self.load_kg > self.capacity_kg:
            return [f"{self.asset_tag}: overloaded"]
        return []


print(StorageRack("L3-RCK-01", 1500, 1200).inspect())
try:
    Equipment("L3-ABC-01")
except TypeError as error:
    print("TypeError:", error)
```

Output:

```
['L3-RCK-01: overloaded']
TypeError: Can't instantiate abstract class Equipment without an implementation for abstract method '_kind_findings'
```

The rack answers `_kind_findings()`, so it can be built and inspected. `Equipment` has an abstract
method with no answer, so Python refuses to build one. The leading underscore on `_kind_findings`
says "callers use `inspect()`, not this."

---

## Worked example 2: twelve lines by hand, or three with a dataclass

```python
# finding_record.py
from dataclasses import FrozenInstanceError, dataclass


class FindingByHand:
    def __init__(self, asset_tag, severity, message):
        self.asset_tag = asset_tag
        self.severity = severity
        self.message = message

    def __eq__(self, other):
        return ((self.asset_tag, self.severity, self.message)
                == (other.asset_tag, other.severity, other.message))

    def __repr__(self):
        return (f"FindingByHand(asset_tag={self.asset_tag!r}, "
                f"severity={self.severity!r}, message={self.message!r})")


@dataclass(frozen=True)
class Finding:
    asset_tag: str
    severity: str
    message: str


a = Finding("L3-PRS-02", "stop", "guard is open")
b = Finding("L3-PRS-02", "stop", "guard is open")
print(a)
print(a == b, FindingByHand("x", "info", "y") == FindingByHand("x", "info", "y"))
try:
    a.severity = "info"
except FrozenInstanceError as error:
    print("FrozenInstanceError:", error)
```

Output:

```
Finding(asset_tag='L3-PRS-02', severity='stop', message='guard is open')
True True
FrozenInstanceError: cannot assign to field 'severity'
```

Both classes print usefully and compare by value. The hand-written one took twelve lines and has
three places to misspell a field. The dataclass took three lines, and `frozen=True` added protection
the hand-written one does not have: `FindingByHand` would let anyone change `severity` after the
fact.

---

## Worked example 3: a record that checks itself

```python
# hoodie_order.py
from dataclasses import dataclass

SIZES = ("S", "M", "L", "XL")


@dataclass(frozen=True)
class HoodieOrder:
    order_id: str
    size: str
    quantity: int = 1

    def __post_init__(self):
        # The dataclass writes __init__. This runs right after it.
        if self.size not in SIZES:
            raise ValueError(f"size must be one of {SIZES}, not {self.size!r}")


orders = [HoodieOrder("R-0413", "M"), HoodieOrder("R-0413", "M"), HoodieOrder("R-0977", "XL", 2)]
print(orders[2])
print(len(orders), "orders,", len(set(orders)), "different")
try:
    HoodieOrder("R-1200", "medium")
except ValueError as error:
    print("ValueError:", error)
```

Output:

```
HoodieOrder(order_id='R-0977', size='XL', quantity=2)
3 orders, 2 different
ValueError: size must be one of ('S', 'M', 'L', 'XL'), not 'medium'
```

The club's order records get `quantity` with a default of 1. `__post_init__` refuses a size that is
not on the list. Because the dataclass is frozen, Python can also put orders in a `set`, and the two
identical orders count once. The order ids are invented.

---

## The wrong version, and the error it produces

The oven was written before `_kind_findings` was the rule. It still has the old method name:

```python
# oven_forgot.py
from abc import ABC, abstractmethod


class Equipment(ABC):
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def inspect(self):
        """The template: shared checks first, then this kind's own."""
        return self.common_findings() + self._kind_findings()

    def common_findings(self):
        return []

    @abstractmethod
    def _kind_findings(self):
        """Every concrete kind must answer this."""


class StorageRack(Equipment):
    def __init__(self, asset_tag, load_kg, capacity_kg):
        super().__init__(asset_tag)
        self.load_kg = load_kg
        self.capacity_kg = capacity_kg

    def _kind_findings(self):
        if self.load_kg > self.capacity_kg:
            return [f"{self.asset_tag}: overloaded"]
        return []


class Oven(Equipment):
    def __init__(self, asset_tag, setpoint_c):
        super().__init__(asset_tag)
        self.setpoint_c = setpoint_c

    def problems(self):                   # the old name, never renamed
        return []


oven = Oven("L3-OVN-01", 200)
```

Output:

```
Traceback (most recent call last):
  File "...\oven_forgot.py", line 42, in <module>
    oven = Oven("L3-OVN-01", 200)
TypeError: Can't instantiate abstract class Oven without an implementation for abstract method '_kind_findings'
```

This error is a **good** outcome. Without `abc`, the oven would have been built, its inspection would
have returned only the shared checks, and an oven above its maximum temperature would have passed.
With `abc`, the program refuses to start until the oven says what it checks.

**The fix:** rename `problems()` to `_kind_findings()` and make it return the oven's findings.

---

## Why the wrong version is tempting

Renaming a method across a hierarchy often gets done halfway. The old name still works when you call
it directly, and your quick test calls it directly. Without an abstract method, nothing checks that
every class answers the new name.

The second temptation is to skip the library and write it yourself, "so I understand it." Writing a
record class by hand once is a fine exercise. Writing it by hand in every project is how typos in
`__eq__` reach production.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Reuse library** | tested, maintained code your program builds on instead of rewriting |
| **Standard library** | the modules that come with Python, such as `abc`, `dataclasses`, and `json` |
| **Abstract class** | a class Python refuses to create objects from directly |
| **Abstract method** | a method every concrete subclass must write, marked `@abstractmethod` |
| **Concrete class** | a class with every abstract method written, so it can be created |
| **Template method** | a base-class method that calls methods its subclasses supply |
| **Dataclass** | a class whose `__init__`, `__eq__`, and `__repr__` Python writes from its fields |
| **Frozen** | a dataclass whose fields cannot change after the object is made |

---

## Self-check

**Question 1.** `PoweredEquipment` inherits from the abstract `Equipment` and does not write
`_kind_findings()`. Can you create a `PoweredEquipment` object? Can you create a `Press` that does
write it?

**Question 2.** Why is a frozen dataclass a good fit for `Finding` and a poor fit for a `Press`?

**Question 3.** In worked example 3, why does `len(set(orders))` print 2 and not 3?

---

### Answers

**1.** No. `PoweredEquipment` still has an abstract method with no answer, so it is abstract too.
Yes, a `Press` that writes `_kind_findings()` is concrete and can be created.

**2.** A finding records something that was observed at one moment. Changing it later would falsify
the record. A press changes all the time: it starts, stops, and gets locked out, so its state must
be changeable, through its methods.

**3.** The dataclass wrote `__eq__`, so the two `R-0413` orders with size `M` and quantity 1 are
equal. A frozen dataclass can also be hashed, so the set keeps only one of them.

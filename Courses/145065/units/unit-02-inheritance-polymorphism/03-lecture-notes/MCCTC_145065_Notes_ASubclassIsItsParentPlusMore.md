# Lecture Notes: A Subclass Is Its Parent, Plus More
## 145065 Object-Oriented Programming · Unit 2 · Week 4, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W04_ASubclassIsItsParentPlusMore.md). There is no
exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W04_ASubclassIsItsParentPlusMore.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.3.12 write code to create classes, objects, and methods. 5.1.4 describe,
compare, and contrast procedural and object-oriented programming.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described.

---

## Why this exists

Line 3 has two presses, an oven, a conveyor, and a rack. In Unit 1 you wrote one `Machine` class.
Now the machines differ: a press has a guard, an oven has a setpoint, a rack has no power at all.

The first version of the new code was written the fast way. Someone copied `Press`, renamed it
`Oven`, and changed a few lines. It works. Then the lockout rule changed, and somebody updated it in
`Press` and forgot `Oven`. Now a locked-out oven keeps running. **Nothing crashed.**

Copied code drifts. Every copy is a place a fix can be forgotten. Inheritance puts each shared rule
in exactly one place.

---

## The concept in plain language

**Inheritance** says one class **is a** more specific kind of another. A press is a piece of powered
equipment. Powered equipment is a piece of equipment.

The more general class is the **parent** (also called the base class or superclass). The more
specific class is the **child** (subclass). You write the child like this:

```python
class PoweredEquipment(Equipment):
```

The name in the parentheses is the parent. The child gets every attribute and method the parent
has. Then it adds its own.

One rule matters more than any other: **the child's `__init__` calls `super().__init__(...)`**. That
line runs the parent's `__init__`, so the parent sets up its part of the object. Skip it, and the
parent's attributes are never created.

**The sentence test.** Before you write `class B(A)`, say "a B is an A" out loud. "A press is a piece
of equipment" is true. "A rack is a piece of powered equipment" is false, so a rack inherits from
`Equipment`, not from `PoweredEquipment`.

**How this differs from procedural code (5.1.4).** In procedural code, data and the functions that
use it are separate, and a rule shared by two kinds of machine is usually a function with an `if`
inside. In object-oriented code, the rule lives on the class that owns the data, and the hierarchy
decides which classes share it.

---

## Worked example 1: two levels

```python
# two_levels.py
class Equipment:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    def describe(self):
        return f"{self.asset_tag} {self.name}"


class PoweredEquipment(Equipment):
    def __init__(self, asset_tag, name, rated_kw):
        super().__init__(asset_tag, name)  # the parent sets up its part
        self.rated_kw = rated_kw           # the child adds its own
        self.running = False

    def start(self):
        self.running = True


oven = PoweredEquipment("L3-OVN-01", "Cure Oven", 45)
oven.start()
print(oven.describe())                     # written once, in Equipment
print(oven.rated_kw, oven.running)
print(isinstance(oven, Equipment), isinstance(oven, PoweredEquipment))
```

Output:

```
L3-OVN-01 Cure Oven
45 True
True True
```

`describe()` was written once, in `Equipment`. The oven can use it because a `PoweredEquipment` is
an `Equipment`. `isinstance()` agrees: the oven is both.

---

## Worked example 2: the same idea in a game

```python
# healer.py
class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_hit(self, damage):
        self.health = max(0, self.health - damage)


class Healer(Character):
    def __init__(self, name, health, potions):
        super().__init__(name, health)
        self.potions = potions

    def heal(self, other):
        if self.potions > 0:
            other.health += 20
            self.potions -= 1


tank = Character("Rook", 100)
medic = Healer("Sage", 60, potions=2)
tank.take_hit(35)
medic.heal(tank)
print(tank.name, tank.health)
print(medic.name, medic.health, medic.potions)
print(hasattr(tank, "heal"), hasattr(medic, "take_hit"))
```

Output:

```
Rook 85
Sage 60 1
False True
```

A `Healer` is a `Character`, so it can take hits. A plain `Character` is not a `Healer`, so it cannot
heal. Inheritance only flows downward.

---

## Worked example 3: three levels, and who is whose parent

```python
# three_levels.py
class Equipment:
    kind = "equipment"


class PoweredEquipment(Equipment):
    kind = "powered"


class Press(PoweredEquipment):
    kind = "press"


class StorageRack(Equipment):
    kind = "rack"


print([cls.__name__ for cls in Press.__mro__])
print(issubclass(Press, Equipment), issubclass(StorageRack, PoweredEquipment))
print(Press.kind, StorageRack.kind, PoweredEquipment.kind)
```

Output:

```
['Press', 'PoweredEquipment', 'Equipment', 'object']
True False
press rack powered
```

`__mro__` is the **method resolution order**: the list of classes Python searches, in order, when you
ask a `Press` for an attribute. It starts at `Press`, climbs to `PoweredEquipment`, then
`Equipment`, then `object`, the parent of every Python class. The first class that has the name
wins, which is why each class answers `kind` with its own value.

`StorageRack` is not a `PoweredEquipment`. It sits at level 2, beside `PoweredEquipment`, not under
it. That is the sentence test turned into code.

---

## The wrong version, and the error it produces

This `Press` forgot `super().__init__(...)`:

```python
# press_no_super.py
class Equipment:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    def describe(self):
        return f"{self.asset_tag} {self.name}"


class PoweredEquipment(Equipment):
    def __init__(self, asset_tag, name, rated_kw):
        super().__init__(asset_tag, name)  # the parent sets up its part
        self.rated_kw = rated_kw           # the child adds its own
        self.running = False

    def start(self):
        self.running = True


class Press(PoweredEquipment):
    def __init__(self, asset_tag, name, rated_kw, tonnage):
        self.tonnage = tonnage             # forgot super().__init__(...)


press = Press("L3-PRS-01", "Press 1", 15, 60)
print("built, tonnage", press.tonnage)
press.start()
print("started")
print(press.describe())
```

Output:

```
built, tonnage 60
started
Traceback (most recent call last):
  File "...\press_no_super.py", line 30, in <module>
    print(press.describe())
          ~~~~~~~~~~~~~~^^
  File "...\press_no_super.py", line 8, in describe
    return f"{self.asset_tag} {self.name}"
              ^^^^^^^^^^^^^^
AttributeError: 'Press' object has no attribute 'asset_tag'
```

Read the output in order. The press was **built** with no error. It even **started**, because
`start()` only sets an attribute. The crash comes later, in `describe()`, and the message names
`asset_tag`, an attribute the parent was supposed to create. The mistake is in `Press.__init__`.
The error is somewhere else.

**The fix** is one line, first in `Press.__init__`:

```python
super().__init__(asset_tag, name, rated_kw)
```

---

## Why the wrong version is tempting

The child's `__init__` looks complete. It sets its own attribute, and the program runs for a while.
Nothing warns you when the parent's setup is skipped. The first method that needs a parent's
attribute fails, possibly far from the class, possibly in code someone else wrote.

The habit that prevents it: **the first line of every child `__init__` is `super().__init__(...)`**,
with exactly the arguments the parent asks for.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Inheritance** | a class built as a more specific kind of an existing class |
| **Parent (base class, superclass)** | the more general class |
| **Child (subclass)** | the more specific class that inherits |
| **`super()`** | a way to call the parent's version of a method from the child |
| **"is a" relationship** | the relationship inheritance models: a press is powered equipment |
| **Method resolution order (MRO)** | the order Python searches classes for an attribute |
| **Hierarchy** | the family tree of classes, from most general to most specific |

---

## Self-check

**Question 1.** A classmate writes `class Forklift(Battery)`. Use the sentence test to say whether
that inheritance is right.

**Question 2.** What does `print(PoweredEquipment.kind)` print in worked example 3, and why is it not
`"equipment"`?

**Question 3.** In the wrong version, why did `press.start()` succeed before `describe()` failed?

---

### Answers

**1.** "A forklift is a battery" is false. A forklift **has** a battery. The sentence test fails, so
`Forklift` should not inherit from `Battery`. Week 5 shows what to do instead.

**2.** It prints `powered`. Python looks for `kind` on `PoweredEquipment` first and finds it there,
so it never climbs to `Equipment`.

**3.** `start()` only sets `self.running = True`. Setting an attribute creates it, so nothing was
missing. `describe()` reads `self.asset_tag`, which only the parent's `__init__` creates, and that
never ran.

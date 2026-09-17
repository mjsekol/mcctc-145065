# Lecture Notes: Ask Every Object the Same Question
## 145065 Object-Oriented Programming · Unit 2 · Week 5, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W05_AskEveryObjectTheSameQuestion.md). There is no
exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W05_AskEveryObjectTheSameQuestion.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.3.5 write code that uses conditional control structures, and recognize when
polymorphism should replace them. 5.3.12 write code to create classes, objects, and methods.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop. The assignment
titles in worked example 1 are invented.

---

## Why this exists

Somewhere in most programs there is a function shaped like this (a sketch, not a whole program):

```
if item.kind == "press":
    ...
elif item.kind == "conveyor":
    ...
elif item.kind == "oven":
    ...
else:
    raise ValueError("no rule for this kind")
```

It is a **conditional control structure**, the if/elif/else you have written since 145060. It works.
It also has three costs that grow with the program:

1. Every new kind means editing this function, and every other function shaped like it.
2. A kind someone forgot falls through to `else` and fails **at run time**, in front of a user.
3. The rules for a press live far from the `Press` class, so a person reading `Press` cannot see them.

---

## The concept in plain language

**Polymorphism** means "many shapes": one call works on many kinds of object, and each kind answers
in its own way.

Instead of asking an object what it is and then deciding what to do, you ask every object the same
question and let each class answer. The branch does not disappear. It moves into the class
hierarchy: Python picks the right method by looking at the object's class, which is the method
resolution order from Week 4.

The pattern has three parts you already know:

1. An abstract method on the base class: the question.
2. One answer in each concrete class.
3. A loop that asks every object, and never checks what kind it is.

A new kind is a new class with its own answer. The loop does not change. And `abc` catches a new
kind with no answer the moment someone tries to create one, long before a user sees it.

---

## Worked example 1: late work, three kinds, one question

```python
# late_work.py
from abc import ABC, abstractmethod


class Assignment(ABC):
    def __init__(self, title, score):
        self.title = title
        self.score = score

    def final_score(self, days_late):
        return max(0, self.score - self.penalty(days_late))

    @abstractmethod
    def penalty(self, days_late):
        """Points taken off. Each kind answers for itself."""


class Quiz(Assignment):
    kind = "quiz"

    def penalty(self, days_late):
        return self.score if days_late > 0 else 0     # a late quiz earns nothing


class Essay(Assignment):
    kind = "essay"

    def penalty(self, days_late):
        return 10 * days_late                         # 10 points a day


class Lab(Assignment):
    kind = "lab"

    def penalty(self, days_late):
        return min(15, 5 * days_late)                 # 5 a day, at most 15


work = [Quiz("Unit 2 quiz", 36), Essay("Design analysis", 88), Lab("Layout walk", 95)]
for item in work:
    print(f"{item.title}: {item.final_score(days_late=2)}")
```

Output:

```
Unit 2 quiz: 0
Design analysis: 68
Layout walk: 85
```

The loop calls `final_score()` on every assignment. `final_score()` is written once, in the base
class, and it calls `penalty()`, which each kind answers differently. There is no `if` about kinds
anywhere.

---

## Worked example 2: the chain and the polymorphic call, side by side

The same file, with the old if/elif chain added, and a fourth kind added later:

```python
# late_work_chain.py
from abc import ABC, abstractmethod


class Assignment(ABC):
    def __init__(self, title, score):
        self.title = title
        self.score = score

    def final_score(self, days_late):
        return max(0, self.score - self.penalty(days_late))

    @abstractmethod
    def penalty(self, days_late):
        """Points taken off. Each kind answers for itself."""


class Quiz(Assignment):
    kind = "quiz"

    def penalty(self, days_late):
        return self.score if days_late > 0 else 0     # a late quiz earns nothing


class Essay(Assignment):
    kind = "essay"

    def penalty(self, days_late):
        return 10 * days_late                         # 10 points a day


class Lab(Assignment):
    kind = "lab"

    def penalty(self, days_late):
        return min(15, 5 * days_late)                 # 5 a day, at most 15


def final_score_by_kind(item, days_late):
    if item.kind == "quiz":
        penalty = item.score if days_late > 0 else 0
    elif item.kind == "essay":
        penalty = 10 * days_late
    elif item.kind == "lab":
        penalty = min(15, 5 * days_late)
    else:
        raise ValueError(f"no late rule for kind {item.kind!r}")
    return max(0, item.score - penalty)


class Project(Assignment):
    kind = "project"

    def penalty(self, days_late):
        return 0 if days_late <= 1 else 20            # one grace day, then 20 points


work = [Quiz("Unit 2 quiz", 36), Essay("Design analysis", 88), Lab("Layout walk", 95),
        Project("Class hierarchy", 91)]
print("polymorphic:", [item.final_score(2) for item in work])
print("chain:      ", [final_score_by_kind(item, 2) for item in work])
```

Output:

```
polymorphic: [0, 68, 85, 71]
Traceback (most recent call last):
  File "...\late_work_chain.py", line 61, in <module>
    print("chain:      ", [final_score_by_kind(item, 2) for item in work])
                           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "...\late_work_chain.py", line 47, in final_score_by_kind
    raise ValueError(f"no late rule for kind {item.kind!r}")
ValueError: no late rule for kind 'project'
```

The first line is the polymorphic version. `Project` answered for itself, and the loop never
changed. The chain never heard of projects and failed.

Notice what the chain duplicated: every penalty rule is written twice, once in its class and once in
the chain. When the essay rule changes, somebody has to find both.

---

## Worked example 3: inspecting the line

```python
# inspect_loop.py
from abc import ABC, abstractmethod


class Equipment(ABC):
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def inspect(self):
        return self._kind_findings()

    @abstractmethod
    def _kind_findings(self):
        """Each kind answers in its own class."""


class Press(Equipment):
    def __init__(self, asset_tag, guard_closed):
        super().__init__(asset_tag)
        self.guard_closed = guard_closed

    def _kind_findings(self):
        return [] if self.guard_closed else [f"{self.asset_tag}: guard is open"]


class Rack(Equipment):
    def __init__(self, asset_tag, load_kg, capacity_kg):
        super().__init__(asset_tag)
        self.load_kg, self.capacity_kg = load_kg, capacity_kg

    def _kind_findings(self):
        if self.load_kg > self.capacity_kg:
            return [f"{self.asset_tag}: overloaded"]
        return []


def inspect_all(items):
    findings = []
    for item in items:              # never asks what kind item is
        findings.extend(item.inspect())
    return findings


class Welder(Equipment):            # added later; inspect_all() did not change
    def __init__(self, asset_tag, wire_kg):
        super().__init__(asset_tag)
        self.wire_kg = wire_kg

    def _kind_findings(self):
        return [f"{self.asset_tag}: wire low"] if self.wire_kg < 2 else []


line = [Press("L3-PRS-01", True), Press("L3-PRS-02", False), Rack("L3-RCK-01", 1300, 1200),
        Welder("L3-WLD-01", 1.5)]
print(inspect_all(line))
```

Output:

```
['L3-PRS-02: guard is open', 'L3-RCK-01: overloaded', 'L3-WLD-01: wire low']
```

`Welder` was added after `inspect_all()` was written. Nothing in `inspect_all()` changed, and the
welder's finding is in the list. This is the pattern Lab U02-03 builds on the real Line 3 model.

---

## The wrong version, and the error it produces

A new kind that forgot to answer the question:

```python
# welder_forgot.py
from abc import ABC, abstractmethod


class Equipment(ABC):
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def inspect(self):
        return self._kind_findings()

    @abstractmethod
    def _kind_findings(self):
        """Each kind answers in its own class."""


class Press(Equipment):
    def __init__(self, asset_tag, guard_closed):
        super().__init__(asset_tag)
        self.guard_closed = guard_closed

    def _kind_findings(self):
        return [] if self.guard_closed else [f"{self.asset_tag}: guard is open"]


class Rack(Equipment):
    def __init__(self, asset_tag, load_kg, capacity_kg):
        super().__init__(asset_tag)
        self.load_kg, self.capacity_kg = load_kg, capacity_kg

    def _kind_findings(self):
        if self.load_kg > self.capacity_kg:
            return [f"{self.asset_tag}: overloaded"]
        return []


def inspect_all(items):
    findings = []
    for item in items:              # never asks what kind item is
        findings.extend(item.inspect())
    return findings


class Welder(Equipment):
    def __init__(self, asset_tag, wire_kg):
        super().__init__(asset_tag)
        self.wire_kg = wire_kg


line = [Press("L3-PRS-01", True), Welder("L3-WLD-01", 1.5)]
print(inspect_all(line))
```

Output:

```
Traceback (most recent call last):
  File "...\welder_forgot.py", line 50, in <module>
    line = [Press("L3-PRS-01", True), Welder("L3-WLD-01", 1.5)]
                                      ~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: Can't instantiate abstract class Welder without an implementation for abstract method '_kind_findings'
```

This error happens where the welder is **created**, not where it is inspected. With the chain, the
same mistake surfaces later: `ValueError: no late rule for kind 'project'`, raised from inside a
report, possibly while a supervisor is waiting for it. Both are errors. One is found by the person who
wrote the class. The other is found by the person using the program.

---

## Why the wrong version is tempting

The chain is the first thing anyone writes, and for two kinds it is fine. It is readable, it is all in
one place, and it passes every test written for the kinds that exist today.

A second temptation catches students who already know polymorphism: keeping the loop, but "fixing"
it with `isinstance()` checks for the one kind that behaves differently. That is the chain again,
hidden inside the loop.

The habit that prevents it: **when you write `if item.kind ==` or `if isinstance(item, ...)` about
your own classes, stop and ask which class that branch belongs to.**

---

## Vocabulary

| Term | What it means |
|---|---|
| **Polymorphism** | one call that works on many kinds of object, each answering its own way |
| **Conditional control structure** | `if`, `elif`, `else`: code that chooses a path by testing a condition |
| **Dispatch** | choosing which code runs for a call; Python dispatches on the object's class |
| **Polymorphic method** | the method every kind answers, such as `penalty()` or `inspect()` |
| **Duck typing** | Python's habit of calling a method on anything that has it, whatever its class |

---

## Self-check

**Question 1.** A fifth kind, `Presentation`, has no late penalty. In worked example 2, list every
place you must edit in the polymorphic design, then in the chain design.

**Question 2.** What does `Quiz("x", 50).final_score(0)` return, and which class's code computed the
penalty?

**Question 3.** A classmate says "polymorphism removed the if statements." Is that right? Where did the
decision go?

---

### Answers

**1.** Polymorphic: write one new class, `Presentation`, with `penalty()` returning 0. Chain: write the
class and also add an `elif item.kind == "presentation"` branch to `final_score_by_kind()`, plus every
other function shaped like it.

**2.** `50`. `final_score()` in `Assignment` ran, and it called `Quiz.penalty(0)`, which returned 0
because the quiz was not late.

**3.** Partly. The `if` about **kinds** is gone from the loop. The decision about which penalty applies
is now made by Python's method lookup, based on the object's class. Individual classes can still
contain their own `if` statements, such as the quiz's `days_late > 0`.

# Lecture Notes: The Design Walkthrough
## 145065 Object-Oriented Programming · Unit 2 · Week 5, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W05_TheDesignWalkthrough.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W05_TheDesignWalkthrough.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and the
walkthrough guide, `09-project/project-files/WALKTHROUGH_GUIDE.md`.

**Competencies:** 5.6.9 review the design (peer walkthrough). 1.2.3 use verbal, nonverbal, and
active listening skills to communicate effectively. 1.2.4 use negotiation and conflict-resolution
skills to reach solutions.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop.

---

## Why this exists

A design mistake costs a few minutes to fix while it is a line on a diagram. It costs an afternoon
once twenty tests and three other classes depend on it. It costs far more once it has shipped. The
cheapest time to find a design problem is before the design is finished, and the person least able
to find it is the person who designed it, because they already know what they meant.

A **design walkthrough** puts a second person in front of the design at the cheap moment. In
industry it goes by several names: design review, peer walkthrough, design critique. The idea is the
same.

---

## The concept in plain language

In a walkthrough, the **author** walks a **reviewer** through a design, and the reviewer looks for
problems. It has three rules, and each one is harder than it sounds.

**1. The reviewer asks real questions.** "Looks good" finds nothing. Good review questions test the
design against something: "What happens when a second kind of X arrives?" "Which class owns this
rule?" "Say the sentence test for this `class B(A)` out loud."

**2. The author listens more than they explain.** This is **active listening** (1.2.3): you let the
reviewer finish, you repeat the point back in your own words ("so you're saying a line could take a
loose machine through `add()`"), and your first reply to a finding is a question, not a defense.
**Nonverbal** listening counts too: face the person, keep your hands off the keyboard, and write the
finding down while they talk. Explaining your code for a full minute teaches the reviewer your
opinion and teaches you nothing.

**3. Disagreements end in a recorded decision, not a winner.** This is **negotiation and conflict
resolution** (1.2.4). When you disagree, each person states the strongest version of their side. Then
you look for what would settle it: a test you could write, a requirement that decides it, or a choice
you can reverse later. The record says what you decided, what you rejected, and why. "We agreed to
disagree" is allowed only when it comes with a next step.

A walkthrough reviews the **design**. Every finding is about a class or a relationship, never about
the person.

---

## Worked example 1: a question that finds a real problem

The author's design has a base class with a `label()` method. The reviewer asks: **"What happens
when someone adds a kind you did not plan for?"** The author tries it:

```python
# base_knows_subclasses.py
class Equipment:
    def __init__(self, tag):
        self.tag = tag

    def label(self):
        """Each kind shows its own detail."""
        if isinstance(self, Press):
            return f"{self.tag} press, {self.tonnage:g} t"
        if isinstance(self, Oven):
            return f"{self.tag} oven, {self.setpoint_c:g} C"
        return f"{self.tag} equipment"


class Press(Equipment):
    def __init__(self, tag, tonnage):
        super().__init__(tag)
        self.tonnage = tonnage


class Oven(Equipment):
    def __init__(self, tag, setpoint_c):
        super().__init__(tag)
        self.setpoint_c = setpoint_c


class Grinder(Equipment):                  # added by someone else, a month later
    def __init__(self, tag, wheel_mm):
        super().__init__(tag)
        self.wheel_mm = wheel_mm


for item in (Press("L3-PRS-01", 60), Oven("L3-OVN-01", 200), Grinder("L3-GRD-01", 150)):
    print(item.label())
```

Output:

```
L3-PRS-01 press, 60 t
L3-OVN-01 oven, 200 C
L3-GRD-01 equipment
```

The grinder lost its detail. The base class **knows its subclasses by name**, so every new kind means
editing `Equipment`. The docstring says each kind shows its own detail, and the code says otherwise.
The finding goes in the record: "`label()` should call a method each subclass writes." The question
found it. The author's explanation would not have.

---

## Worked example 2: a genuine disagreement, side one

The design has `class Line(Cell)`. The reviewer says a line should hold only cells. The author says a
line **is** a named group, like a cell. Both are partly right. They agree to settle it with a test:
can a loose machine get onto the line?

```python
# line_is_a_cell.py
class Cell:
    def __init__(self, name):
        self.name = name
        self._items = []

    def add(self, item):
        self._items.append(item)
        return item

    @property
    def items(self):
        return tuple(self._items)


class Line(Cell):
    """For: a line is a named group, like a cell. Against: it may hold only cells."""

    def add_cell(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError("a line holds cells")
        return self.add(cell)


class Press:
    def __init__(self, tag):
        self.tag = tag


line = Line("Line 3")
line.add_cell(Cell("Forming"))
line.add(Press("L3-PRS-09"))             # inherited add() skips the rule
print([type(item).__name__ for item in line.items])
try:
    line.add_cell(Press("L3-PRS-10"))
except TypeError as error:
    print("TypeError:", error)
```

Output:

```
['Cell', 'Press']
TypeError: a line holds cells
```

`add_cell()` refuses a press. The inherited `add()` accepts one. The author's sentence test passed,
and the design still allows something the requirements forbid.

---

## Worked example 3: the same disagreement, side two

```python
# line_has_cells.py
class Cell:
    def __init__(self, name):
        self.name = name
        self._items = []

    def add(self, item):
        self._items.append(item)
        return item

    @property
    def items(self):
        return tuple(self._items)


class Line:
    """A line HAS cells. It has no add(), so a loose machine has no way in."""

    def __init__(self, name):
        self.name = name
        self._cells = []

    def add_cell(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError("a line holds cells")
        self._cells.append(cell)
        return cell

    @property
    def items(self):
        return tuple(self._cells)


class Press:
    def __init__(self, tag):
        self.tag = tag


line = Line("Line 3")
line.add_cell(Cell("Forming"))
print([type(item).__name__ for item in line.items])
try:
    line.add(Press("L3-PRS-09"))
except AttributeError as error:
    print("AttributeError:", error)
```

Output:

```
['Cell']
AttributeError: 'Line' object has no attribute 'add'
```

The composed version has no `add()` to misuse. It gives up something real, though: every place that
treated lines and cells the same way (a recursive walk, an outline printer) now depends on both
having `items`, not on inheritance. The record for this disagreement looks like this:

| | |
|---|---|
| **Finding** | `Line(Cell)` inherits `add()`, which accepts loose machines |
| **Author's position** | a line is a named group; inheritance avoids duplicating `items` |
| **Reviewer's position** | the requirement says a line holds only cells |
| **What settled it** | a test showed `line.add(press)` succeeds |
| **Decision** | `Line` holds a list of cells and does not inherit from `Cell` |
| **Rejected** | keeping `Line(Cell)` and overriding `add()` to refuse, because every other inherited list-changing path would need the same guard |
| **Next step** | the author commits the change and the test that proves it |

---

## The wrong version of a walkthrough

Here is the start of a walkthrough that goes wrong. The exchange is invented, and the pattern is
common:

> **Reviewer:** Why is `Line` a subclass of `Cell`?
>
> **Author:** Because a line is basically a cell. See, it has a name, and it has items, and `walk()`
> treats them the same, and I already wrote `Cell` so I didn't want to write it twice, and it works,
> all my tests pass.
>
> **Reviewer:** OK.

The error it produces is silence. The reviewer's question was good, the author answered a question
nobody asked ("does it work?"), and the reviewer gave up. The finding from worked example 2 was one
test away and never got written down.

The same exchange, with the listening moves:

> **Reviewer:** Why is `Line` a subclass of `Cell`?
>
> **Author:** Good question. What are you worried it allows?
>
> **Reviewer:** A cell can take a machine. Can a line?
>
> **Author:** So you're asking whether a machine can get onto the line without a cell. I don't know.
> Let's try it.

---

## Why the wrong version is tempting

Defending your design feels like doing your job. You worked on it, you know why each choice was
made, and a question sounds like an accusation. Reviewers make it worse by being polite: "looks
good" is kinder than a hard question, and it is useless.

The habits that prevent it: **the author's first answer is a question back**, the reviewer brings
three prepared questions, and **every disagreement gets a test or a recorded decision** before the
pair moves on.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Design walkthrough (peer walkthrough)** | a structured review of a design by someone who did not write it |
| **Author** | the person whose design is reviewed |
| **Reviewer** | the person looking for problems |
| **Finding** | one specific problem, about the design, written down |
| **Active listening** | letting the speaker finish, repeating their point back, and asking before answering |
| **Nonverbal communication** | what your face, posture, and hands say while someone talks |
| **Negotiation** | reaching an agreement both sides can accept |
| **Conflict resolution** | turning a disagreement into a decision and a next step |

---

## Self-check

**Question 1.** Write two review questions that test a design against something, for a hierarchy you
have not seen.

**Question 2.** A reviewer says "your `Forklift(Battery)` is wrong." What is the author's best first
reply?

**Question 3.** In worked example 3's record, why is the rejected option written down at all?

---

### Answers

**1.** Any two that could reveal a problem, for example: "What changes when a new kind arrives?"
"Say the sentence test for each `class B(A)`." "Which class owns this rule?" "What happens if this
collection is changed from outside?"

**2.** A question that shows you heard it and asks for the reason, such as "What makes it wrong: can a
forklift have more than one, or swap them?" Not an explanation of why you wrote it.

**3.** So the next person who thinks of overriding `add()` sees that it was considered, and why it
lost. Without it, the same argument happens again next month.

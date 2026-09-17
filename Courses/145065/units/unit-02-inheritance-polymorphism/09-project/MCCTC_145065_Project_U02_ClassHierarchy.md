# Project · The Class Hierarchy
## 145065 Object-Oriented Programming · Unit 2 · Weeks 4-5

**100 points. Projects category, 35 percent of your grade.**
**Due Week 5, Friday, at the end of the commit window.**

**Gate 3.** Full tooling, AI allowed, AI usage log required, decision log required.

---

## The brief

> From: the maintenance coordinator at Riverside Fabrication
>
> Our forklifts, pallet jacks, and parts carts get a check at the start of every shift. Right now
> that is a clipboard, and a spreadsheet somebody fills in when they remember. Half the checks are the
> same for everything, and the other half depend on what the thing is. Nobody can tell me which
> vehicles are cleared to use this morning without walking the floor.
>
> I want a model of the fleet I can ask one question: is this one ready? Every vehicle answers it,
> in its own way. Some vehicles have parts that get swapped, like batteries. The vehicles are parked
> in zones, and some zones are inside other zones.
>
> We will add new kinds of equipment. When we do, I do not want someone rewriting the whole thing.
>
> Show me the design before you build it. I have been burned by software that looked finished and
> fell apart the first time we added something.

Riverside Fabrication is a **composite**, the invented small metal fabrication shop you have worked
with all semester. **You may model a different domain instead**, one you know well: a school
makerspace's tools, a robotics team's parts, a game's items and characters, a bike shop's rentals. If
you do, record the choice and the rejected option in your decision log, and make sure your domain can
meet every technical requirement below. **Invent every name and number. No real person's
information, and no real company described as having done anything.**

**That is the whole brief.** It does not say how many kinds of vehicle, what "ready" means, what gets
swapped, or how deep the zones go. Deciding those, and writing them down before you code, is part of
the grade.

---

## What you are building

| # | Piece | Form |
|---|---|---|
| 1 | The hierarchy and its parts | a package or module in `unit-02-hierarchy/`, standard library only |
| 2 | Tests | `unittest`, run with `python -m unittest` |
| 3 | A design | `DESIGN.md`: the relationship list and a UML class diagram, **committed before any code** |
| 4 | A written analysis | `INHERITANCE_OR_COMPOSITION.md`, from `project-files/INHERITANCE_OR_COMPOSITION_TEMPLATE.md` |
| 5 | A walkthrough record | `WALKTHROUGH.md`, from `project-files/WALKTHROUGH_RECORD.md` |
| 6 | A decision log | `decision-log.md` entries for this project |
| 7 | An AI usage log and a README | the usual course formats |

---

## Technical requirements

1. **A hierarchy at least three levels deep.** Every `class B(A)` passes the sentence test: "a B is
   an A." At least one branch stops at level 2, the way a rack or a cart does.
2. **An abstract base class using `abc`,** with at least one `@abstractmethod` that every concrete
   class must write. A test proves the base class cannot be created.
3. **At least one frozen dataclass** for a record your model produces, such as a check result.
4. **One polymorphic method**, the question every object answers, called in a loop that never checks
   what kind an object is. Keep the if/elif version it replaced (or write one) in a separate module,
   and a test that proves both give identical answers for every existing kind.
5. **A new kind needs no change to the loop.** A test adds a kind the loop has never seen and shows
   it is asked.
6. **One deliberate composition,** a "has a" part in its own class. The owner has one method that adds
   or replaces the part, checks it, and never hands out its internal collection.
7. **A nested grouping walked by recursion.** At least one recursive function with a base case, and a
   test at three or more levels deep. Adding a group to itself is refused.
8. **Every child `__init__` calls `super().__init__(...)`.** Every override that must keep the parent's
   behavior calls `super()`.
9. **At least eight tests,** all passing, covering requirements 2, 4, 5, 6, and 7.
10. **`DESIGN.md`** has a relationship list (at least five "is a" and two "has a" sentences), the
    polymorphic question, and a UML class diagram. The first version is committed before any project
    code. The final version matches the code, or the decision log says why it changed.
11. **`INHERITANCE_OR_COMPOSITION.md`**, 250 to 500 words: one place you used inheritance and why; one place you
    deliberately did not and what you used instead; the strongest argument against each choice.
12. **`WALKTHROUGH.md`** from the Week 5, Wednesday walkthrough. Every finding you accepted is either a
    commit or a decision log entry saying why you did not act on it.
13. **The decision log** has at least three entries, each naming the option you rejected.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| Diagram before code | The coordinator asked to see the design first. A design reviewed on paper is the cheapest one to change. |
| Standard library only | `abc` and `dataclasses` are the reuse libraries this unit teaches, and nothing is installed on lab machines. |
| No `isinstance()` or kind checks in the polymorphic loop | That is the if/elif chain in disguise, and requirement 5 exists to catch it. |
| No public internal collections | A part anyone can remove is a part nobody can rely on. |
| Invented data only | Program rule. No personal information anywhere, and nothing in any AI tool. |
| AI models are local or not used | Program rule. Commercial AI accounts require users to be 18 or older. |

---

## Required repository structure

```
oop-semester/
  README.md
  decision-log.md
  unit-02-hierarchy/
    README.md
    DESIGN.md
    INHERITANCE_OR_COMPOSITION.md
    WALKTHROUGH.md
    ai-usage-log.md
    <your package or module>
    legacy_<name>.py            the if/elif version, kept for the proof
    demo.py
    tests/
      test_*.py
```

---

## DMAIC checkpoints

### Define · Week 4, Wednesday, Build 2 (M1)

Choose the domain. Write the relationship list and the polymorphic question in `DESIGN.md`.
**Checkpoint:** a decision log entry naming the domain chosen and one rejected, and `DESIGN.md` with at
least five "is a" and two "has a" sentences. No code.

### Measure · Week 4, Thursday, last 10 minutes of Build 2

List every kind you will model, what each one has, and the rules each one checks. Name the nested
grouping. **Checkpoint:** `DESIGN.md` names the structure the recursion will walk.

### Analyze · Week 4, Friday, Build 2 (M2)

Draw the UML class diagram. Mark abstract classes and methods. Decide where inheritance ends and
composition begins. **Checkpoint:** the diagram and a second decision log entry, committed, with no
project code yet.

### Improve · Week 5, Monday through Thursday

Three short sprints, each starting with a two-minute plan of three tasks on your task board.

- **Sprint 1, Monday Build 2 (M3):** the levels, the abstract base, the polymorphic method and loop,
  at least four tests.
- **Sprint 2, Tuesday Build 2 (M4):** the composed part, the recursive walk, their tests.
- **Wednesday:** the walkthrough (M5). Build 1 prepares the packet; Build 2 is two rounds.
- **Sprint 3, Thursday Build 2:** the walkthrough changes, the legacy chain and its proof test, and
  `INHERITANCE_OR_COMPOSITION.md`.

### Control · Week 5, Friday

**Checkpoint:** every test passes, `DESIGN.md` matches the code, the README says how to run the tests
and the demo, and everything is pushed inside the commit window.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Domain and relationships | Week 4 Wed, end of Build 2 | the decision log entry and `DESIGN.md` are committed |
| M2 | Class diagram | Week 4 Fri, end of block | the diagram is committed, before any code |
| M3 | Hierarchy and polymorphism | Week 5 Mon, end of block | four or more tests pass |
| M4 | Composition and recursion | Week 5 Tue, end of block | their tests pass |
| M5 | Walkthrough record | Week 5 Wed, end of block | `WALKTHROUGH.md` is committed |
| **Due** | **Everything** | **Week 5 Fri, commit window** | the submission checklist is complete |
| Demo | Five minutes at your desk | Week 5 Fri Build 2, or Week 6 Mon or Tue Build 2 | the demo script below |

**BPA State competitors:** M1 and M2 are due Week 5, Monday. The final due date does not move.

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality.

### Small, and completely finished

**Domain:** Riverside's fleet with three concrete kinds: forklift, pallet jack, cart. **Composition:**
a battery on powered vehicles. **Recursion:** zones one level deep inside the fleet, tested at three
levels with a test-only zone.

**What makes it full marks:** every requirement met, clear tests, an honest analysis.

**The risk:** a thin analysis. Small scope does not shrink `INHERITANCE_OR_COMPOSITION.md`.

### Medium, and the one most students should aim for

**Domain:** any. Four concrete kinds, one of them at level 2. **Composition:** a part that can be
swapped, with a test that swaps it. **Polymorphism:** the legacy chain kept with a proof test for
every kind, and a test that adds a kind the chain has never heard of.

**What it adds:** evidence that the refactor changed nothing, and a design a new kind can join
without edits.

**The risk:** time. The legacy chain and its proof test take a full sprint for some students.

### Large, only if the medium version is finished by Week 5, Tuesday

**Domain:** any, with five or more concrete kinds. **Adds:** one of the EXTENDED ideas from this
unit's labs: a hierarchy that refuses a subclass with no `kind`, a generator-based walk, or a `match`
statement version compared with the polymorphic one.

**What it adds:** an idea you taught yourself from documentation, with a decision log entry about it.

**The risk:** the extra idea eats the time for the analysis and the walkthrough changes. Those are
worth more.

### Scope calibration

| If you | Aim for |
|---|---|
| finished Lab U02-01 on the SCAFFOLDED starter, or missed days for BPA State | Small |
| had 14 of 14 on Lab U02-01 by Wednesday | Medium |
| finished Labs U02-03 and U02-04 early, including an EXTENDED option | Large |

---

## Grading · the 100-point project rubric

| Dimension | Points |
|---|---|
| Functionality | 25 |
| Code Quality | 20 |
| Documentation | 20 |
| Process | 15 |
| Demonstration | 10 |
| Polish | 10 |

### What each dimension means here

**Functionality, 25.** Requirements 1 through 9 work: three levels, an enforced abstract base, a
record type, a polymorphic loop that a new kind can join, a guarded composition, a recursive walk,
and a passing test suite.

**Code Quality, 20.** Scored on the five-dimension standard. Correctness: overrides keep their
parents' promises. Security: composed parts cannot be changed from outside; groups cannot contain
themselves. Readability: every class passes the sentence test and says why in a comment where it is
not obvious. Performance: each walk and each question happens once. Requirements Fit: the brief's
"ready" question is answered.

**Documentation, 20.** `DESIGN.md` is true to the code. `INHERITANCE_OR_COMPOSITION.md` argues both sides of each
choice. The README lets someone else run everything.

**Process, 15.** M1 through M5 on time, the diagram committed before the code, a walkthrough record
with real findings and a recorded disagreement, accepted findings acted on, three decision log
entries with rejected options, and a commit at the end of every period.

**Demonstration, 10.** The five-minute desk demo below.

**Polish, 10.** Names that say what things are, no leftover `TODO`s, no dead copies of methods, tidy
output from `demo.py`.

---

## The five-minute desk demo

Your instructor comes to your desk. Five minutes, timed.

| Time | What |
|---|---|
| 0:00 to 0:45 | Show the class diagram. Read two "is a" sentences and one "has a" sentence out loud. |
| 0:45 to 1:45 | Run `demo.py`. Point at the loop that asks every object the same question. |
| 1:45 to 2:45 | Run the tests. Show the test that adds a new kind, and the one that proves the old chain agrees. |
| 2:45 to 3:45 | Your instructor names one class. Say whether it should have inherited, or been composed, and why. |
| 3:45 to 5:00 | One walkthrough finding you acted on, and one you rejected, with the reason. |

### The demonstration checklist

| # | | Points |
|---|---|---|
| 1 | Relationship sentences read correctly from the diagram | 2 |
| 2 | Polymorphic loop shown and explained | 2 |
| 3 | New-kind test and chain-proof test shown passing | 2 |
| 4 | The named class defended, inheritance or composition | 3 |
| 5 | A finding acted on and a finding rejected, with reasons | 1 |
| | **Total** | **10** |

Item 4 matters most. Defending a design choice you made is the difference between building a
hierarchy and copying one.

---

## Submission checklist

- [ ] `python -m unittest` in `unit-02-hierarchy/` runs at least eight tests, all passing
- [ ] The first `DESIGN.md` diagram is committed before any project code
- [ ] `DESIGN.md` matches the final code, or the decision log says why not
- [ ] The polymorphic loop has no kind checks; a test adds a new kind
- [ ] The legacy chain and its proof test are present
- [ ] `INHERITANCE_OR_COMPOSITION.md` is 250 to 500 words and argues both sides
- [ ] `WALKTHROUGH.md` is complete; accepted findings are commits or decision log entries
- [ ] Three or more decision log entries, each with a rejected option
- [ ] README says how to run the tests and `demo.py`
- [ ] AI usage log complete
- [ ] No personal information anywhere
- [ ] Committed and pushed inside the Friday commit window

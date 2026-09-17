# Project · The Refactor
## 145065 Object-Oriented Programming · Unit 1 · Weeks 2-3

**100 points. Projects category, 35 percent of your grade.**
**Due Week 3, Friday, at the end of the commit window.** The class diagram and class boundaries (M2)
are due Week 2, Friday, **before you write any class code.**

**Gate 3.** Full tooling, AI allowed, AI usage log required, decision log required.

**Competencies:** 5.3.12 (classes, objects, and methods), 5.1.4 (procedural and object-oriented
programming compared), 5.1.3 and 5.6.7 (model and document a design with UML), 5.3.9 (functions and
methods), 5.2.2 (scope of data), 5.1.2 (data structures in information processing), 5.4.4 and 5.4.5
(define and run test cases), 5.1.5 (data management through a language), 5.5.5 (naming and comments),
5.4.2 (write and edit code in the IDE).

---

## The brief

> From: the incoming treasurer of the Oak Hollow High School Game Club
>
> I take over the club's books next year, and I inherit the pipeline you wrote last semester. It
> works. I have run it. I have also opened it, and I cannot tell where anything lives. There is a
> list of problems that gets passed into five different functions, and I had to read all five to
> find out which one added the line I was looking at.
>
> Next year I will need to change things. The discount rule, probably. Maybe a new platform. I need to
> be able to change one thing and know what else it touches. I also need to know it still gives the
> same numbers it gives now, because the advisor has this year's report and will compare.
>
> Before you change any code, show me the plan: what the pieces will be, and why each piece is a
> piece. I would rather argue about a drawing than about a finished program.

The Oak Hollow High School Game Club and its treasurers are invented, as they were in 145060.

**That is the whole brief.** It does not say what the pieces are, how many there should be, or what
"the same numbers" means for a file. Deciding those, and writing down why, is most of the grade.

---

## Choosing your program

**The default: your own 145060 Unit 5 Data Pipeline.** You wrote it under a rule that said no
classes, so it is genuinely procedural: data in lists and dictionaries, rules in functions, and state
passed from function to function.

| You may refactor | Why |
|---|---|
| Your own 145060 Data Pipeline | The default. It is yours, it is procedural, and it has real rules to protect. |
| Another procedural 145060 program of your own, of at least 150 lines, with at least four functions that share data | Only with your instructor's written approval in your decision log, by the end of Week 2, Tuesday's Build 2. |

**You may not refactor Storm Relay v3.** Storm Relay v4 already is that refactor, and you wrote it in
145060 Unit 7.

**If you cannot find your pipeline, or never finished it,** tell your instructor on Week 2, Tuesday.
You will be given a procedural program to refactor instead, and you record that in your decision log.

Record the program you chose and one you rejected in `decision-log.md`.

---

## What you are building

| # | Piece | Form |
|---|---|---|
| 1 | The old program, unchanged | `before/`, copied from your 145060 repository |
| 2 | The behavior baseline | `golden/`, written by `golden_check.py record` |
| 3 | The class diagram | `class_diagram.md`, Mermaid text, committed before any class code |
| 4 | The class boundaries | `CLASS_BOUNDARIES.md`, from `project-files/CLASS_BOUNDARIES_TEMPLATE.md` |
| 5 | The refactored program | `after/`, same command line, same output |
| 6 | The test plan and tests | `TEST_PLAN.md`, and `after/test_*.py` |
| 7 | The README | how to run both, how to check them, the scope map, and before-and-after |
| 8 | The decision log and AI usage log | as always |

---

## Behavior preserved: the golden check

A refactor changes how code is organized and never what it does. `golden_check.py` proves it.

**Record once, from the old program, on Week 2, Tuesday:**

```
python golden_check.py record --dir before --outputs output --clean -- python pipeline.py
```

**Compare after every class you build, from the new program:**

```
python golden_check.py compare --dir after --outputs output --clean -- python pipeline.py
```

Change `pipeline.py`, `output`, and anything after it to match your own program: its file name, the
folder it writes, and any arguments it needs, such as your fixture site's address. If your program
reads from the Swap Shelf fixture site, start the site first, in another terminal, on the port your
instructor gives you.

A passing compare ends `GOLDEN CHECK PASSED: 6 of 6 match`, or whatever your count is. Any
`DIFFERENT` line tells you the first line that changed.

**The four ways the check goes wrong, before you blame the tool:**

1. **The old program changed.** Record from `before/` and never edit `before/` again.
2. **An old output file is still there.** `--clean` deletes the output folder before each run.
3. **Your output contains a time or a random value.** Use `--ignore` with a pattern for that line, and
   explain it in `CLASS_BOUNDARIES.md`, section 5.
4. **The fixture site is not running.** Both programs then fail the same way, and the check passes.
   That proves nothing. Read the baseline's first line after you record it.

---

## Technical requirements

1. **The diagram comes first.** `class_diagram.md` and `CLASS_BOUNDARIES.md` sections 1 to 4 are
   committed in a commit that comes **before** the first commit containing a `class` statement in
   `after/`. Your instructor checks the history.
2. **At least three classes**, each with its own data and at least one rule it enforces.
3. **Every class boundary is justified** in `CLASS_BOUNDARIES.md`: what it owns, what it enforces, why
   it is its own class, what you rejected, and the collection it keeps and why.
4. **Internal state is internal.** Every attribute that outside code must not set directly starts
   with an underscore, and outside code never touches one.
5. **At least one validated property**, whose setter refuses bad values, and whose object's
   `__init__` assigns through that property.
6. **At least one static method or class method**, with the reason in `CLASS_BOUNDARIES.md`. A
   `from_row` or `from_record` class method is the usual one.
7. **No state travels.** No value is created in one place and passed through three or more functions
   or methods only so each can change it. Objects own their own state.
8. **Every old function is placed.** Each became a method or stayed a function, and the table in
   `CLASS_BOUNDARIES.md` says why.
9. **Behavior is preserved.** `golden_check.py compare` passes, or every difference is listed and
   justified in section 5.
10. **Tests.** A `TEST_PLAN.md` written before the tests, and a `unittest` test case for every class,
    with at least one refusal test for every validated property. `python -m unittest -v`, run in
    `after/`, passes.
11. **The README** has four sections: `How to run`, `How to check it` (the golden check and the
    tests), `Scope map` (every module-level name, every class attribute, and three instance
    attributes, each with its level), and `Before and after` (one paragraph comparing the procedural
    and object-oriented versions).
12. **Standard library only**, as in 145060.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| The diagram before the code | A design is cheapest to change on paper. The client asked for the plan first. |
| `before/` is never edited | The baseline is only honest if the program it came from never moves. |
| The same command line and output | The advisor compares this year's report. A refactor that changes a number is a rewrite. |
| No new features | A refactor with new behavior cannot be checked against the old behavior. Write the idea in your README as next steps. |
| No personal information in any file, test, or AI tool | Program rule. Every name in the data is invented. |
| AI is local or not used | Program rule. Commercial AI accounts require users to be 18 or older. |
| Standard library only | Nothing new is installed on lab machines for this project. |

---

## Required repository structure

```
oop-semester/
  decision-log.md
  unit-01-refactor/
    README.md
    CLASS_BOUNDARIES.md
    class_diagram.md
    TEST_PLAN.md
    golden_check.py           copied from project-files/, unchanged
    golden/                   written by golden_check.py record
    before/                   your 145060 program, unchanged
    after/
      <your modules>.py
      test_<name>.py          one or more
    ai-usage-log.md
```

Add `before/output/` and `after/output/`, or whatever your program writes, to `.gitignore`.
**Commit `golden/`.** It is the evidence.

---

## DMAIC checkpoints

### Define · Week 2, Tuesday, Build 2 (M1)

Choose the program. Copy it into `before/`. Run it and record the baseline. **Checkpoint:** the
decision log entry, `before/`, and `golden/` are committed, and `golden/stdout.txt` shows a real
report, not an error.

### Measure · Week 2, Tuesday and Wednesday, Build 2

Fill `CLASS_BOUNDARIES.md` sections 1 and 2: every function, every piece of data, and the state that
travels. **Checkpoint:** every function in `before/` has a row.

### Analyze · Week 2, Wednesday to Friday, Build 2 (M2)

Place every function (section 3), draw the diagram, and justify every class (section 4).
**Checkpoint, due Week 2, Friday:** the M2 checklist below.

### Improve · Week 3, Monday to Wednesday, Build 2

Build one class at a time, in `after/`, starting from a copy of `before/`. Run the golden compare after
each class. Commit each time it passes. This is the sprint: at the start of each Build 2, write the one
class you will finish today at the top of your task board card.

### Control · Week 3, Thursday (M3) and Friday

The test plan, the tests, and the README. **Checkpoint, Thursday:** tests pass and the golden check
passes. **Due Friday:** everything, pushed inside the commit window.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Program chosen, baseline recorded | Week 2 Tue, end of Build 2 | `before/` and `golden/` are committed |
| M2 | Diagram and boundaries | **Week 2 Fri, end of Build 2** | the M2 checklist is complete, **before any class code** |
| | Improve | Week 3 Mon-Wed, Build 2 | one class a day, golden check passing after each |
| M3 | Tests and README | Week 3 Thu, end of Build 2 | `python -m unittest -v` and the golden compare both pass |
| **Due** | **Everything** | **Week 3 Fri, commit window** | the submission checklist is complete and pushed |
| Demo | Five minutes at your desk | Week 3 Fri Build 2, or the start of Week 4 | the demo script below |

### The M2 checklist

- [ ] `class_diagram.md` shows every class with attributes, types, `+` and `-` marks, methods with
      parameters and returns, and every line between classes with a multiplicity
- [ ] `CLASS_BOUNDARIES.md` sections 1 to 4 are complete: inventory, placement, and one section per
      class
- [ ] Every function in `before/` has a placement row with a reason
- [ ] The state that travels is named, and the class that will own it is named
- [ ] **No file in `after/` contains a `class` statement yet**
- [ ] Committed and pushed

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality. These use the Swap Shelf data
pipeline, since most of you are refactoring one.

### Small, and completely finished

**Three classes:** `ProblemLog`, `Sale` with a validated `sold_for`, and `SalesLog` with the read
logic. Everything else stays functions, each placement explained. **Tests:** one test case per class,
eight tests.

**What makes it full marks:** the golden check passes; the problem list no longer travels; the
boundaries document says honestly why the scraping and report code stayed functions this time.

**The risk:** a thin section 4. Three classes still need three real justifications.

### Medium, and the one most students should aim for

**Five or six classes:** the three above, plus `Listing` with a `from_row` class method, a `Shelf` that
holds listings in a dictionary and matches sales, and a report class. **Tests:** a test case per
class, about twenty tests, with hand-checked report numbers.

**What it adds:** every stage of the pipeline has an owner. The client's example, changing the discount
rule, now touches one class.

**The risk:** a report class that does everything. Keep the arithmetic in one place and the layout in
another, and say which is which.

### Large, and only if the medium version passes the golden check by Wednesday

**Everything in medium, plus the scraper as a class** that keeps the pages it fetched and its own
problems, and **each class reporting its own problems**, combined in order at the end, so no log is
passed anywhere. **Tests:** the scraper tested against the fixture site on a port your instructor
gives you, with a fast `robots.txt` copy.

**What it adds:** nothing travels at all.

**The risk:** the order of the problems in the report. Combine them in the order the old program found
them, or the golden check fails on the last five lines.

### Scope calibration

| If you | Aim for |
|---|---|
| finished Lab U01-02 late, or your pipeline is small | Small |
| had 16 of 16 on Lab U01-01 and 18 of 18 on Lab U01-02 on time | Medium |
| passed the golden check with the medium design by Week 3, Wednesday | Large |

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

**Functionality, 25.** The golden check passes. The tests pass. Every technical requirement is met.

**Code Quality, 20.** Scored on the five-dimension standard. Correctness: behavior preserved.
Security: internal state is internal, construction runs the same checks as later changes, refusals
change nothing. Readability: names say what things are, and code lives where a reader would look for
it. Performance: the right collection for each class, and no repeated work. Requirements Fit: every
class earns its place, and no new features appeared.

**Documentation, 20.** `CLASS_BOUNDARIES.md` justifies every boundary and every function that stayed a
function. The diagram matches the code. The README's four sections are complete and true.

**Process, 15.** M1, M2, and M3 on time. The diagram's commit comes before the first class. A golden
compare after each class, visible in the history. A decision log with real decisions, each naming the
option rejected. A commit at the end of every period.

**Demonstration, 10.** The five-minute demo below.

**Polish, 10.** Template instructions deleted, no commented-out old code, no leftover output folders
committed, and a README a stranger could follow.

---

## The five-minute desk demo

Your instructor comes to your desk during Week 3, Friday's Build 2, or at the start of Week 4 if you
were not reached. Five minutes, timed.

| Time | What |
|---|---|
| 0:00 to 0:45 | Run the golden compare. Read the last line aloud. |
| 0:45 to 1:45 | Open the diagram. Point at the class that owns the state that used to travel. |
| 1:45 to 2:45 | Your instructor names one class. Defend its boundary: what it owns, what it enforces, and what you considered instead. |
| 2:45 to 3:45 | Run one refusal test, then show the rule in the class that the test protects. |
| 3:45 to 4:30 | Your instructor names one function that stayed a function. Say why. |
| 4:30 to 5:00 | The client's example: where would a change to the discount rule go, and what else would it touch? |

### The demonstration checklist

| # | | Points |
|---|---|---|
| 1 | Golden compare run and read | 2 |
| 2 | The owner of the travelling state named on the diagram | 2 |
| 3 | A boundary defended, including the rejected alternative | 3 |
| 4 | A refusal test run and its rule shown | 1 |
| 5 | A function that stayed a function, explained | 1 |
| 6 | The discount change located | 1 |
| | **Total** | **10** |

Item 3 matters most. If you cannot explain why a class you wrote exists, that is the one way to fail
this program outright: submitting work you cannot explain.

---

## Submission checklist

- [ ] `python golden_check.py compare ...` passes, or every difference is in section 5
- [ ] `python -m unittest -v` in `after/` passes
- [ ] The diagram's commit comes before the first class
- [ ] `CLASS_BOUNDARIES.md` complete, and the diagram matches the code
- [ ] `TEST_PLAN.md` complete, with a refusal row for every validated property
- [ ] README: How to run, How to check it, Scope map, Before and after
- [ ] Decision log: the program chosen and rejected, plus at least two design decisions
- [ ] AI usage log complete
- [ ] No personal information anywhere
- [ ] `before/` unchanged, `golden/` committed, output folders ignored
- [ ] Committed and pushed inside Week 3, Friday's commit window

# Unit 6 Project · The Python-to-C# Port
## 145065 Object-Oriented Programming · Unit 6 · Weeks 11-12

**100 points. Projects category, 35 percent of your grade.**
**Due Week 12, Friday, at the end of the commit window. The last commit pushed then is your
submission.**

Riverside Fabrication is a composite: an invented small metal fabrication shop.

---

## The brief

> From: the controls lead, Line 3
>
> We are moving the operator panel to C#. Half the team thinks that is a waste of time, because the
> Python model of the line works. The other half thinks C# will fix everything. I do not believe
> either of them.
>
> You built a class model in Python this spring. Port it. Same classes, same behavior, same output.
> If the C# version prints something different from the Python version, I want to know why before
> anyone else does.
>
> Then tell me, with evidence, what the switch actually bought us. Not what the internet says about
> compiled languages. What **your** compiler refused, in **your** code, that Python let run. And tell
> me what it did not catch, because I will be the one on the floor when that part fails.
>
> One more thing. The panel is going to read from a simulator this year and a real device next year.
> Whatever piece of the model the panel talks to, I want it behind something that more than one kind
> of thing can plug into.
>
> I have been burned by a demo that worked and a design nobody could explain. Show me it works, and
> then show me you know why.

**That is the whole brief.** It does not name the interface. It does not say how many compiler catches
are enough. It does not say what "same output" means for a number printed as `212` in one language and
`212.0` in the other. **Pulling requirements out of that is part of the grade.**

---

## What you are building

A C# port of **your own Unit 2 class hierarchy**, with:

1. every class ported, with real access modifiers and validated properties
2. an **interface with at least two implementing classes**, and code that works through the interface
   only
3. a C# test project that proves the port behaves like the Python
4. a demo that prints what the Python demo printed
5. `COMPARISON.md`: a written comparison of what the compiler caught, what it did not, and what cost
   more code
6. the evidence behind every claim: pasted compiler output from your own builds

**If your Unit 2 hierarchy does not run,** tell your instructor by Week 11, Tuesday. With approval, you
port the fallback hierarchy in `project-files/fallback-hierarchy/` instead, and you say so in your
decision log. The fallback is the same amount of work. It is not a shortcut, and your comparison must
still be about **your** builds.

---

## Technical requirements

Every requirement exists for a reason, and the reason is next to it.

| # | Requirement | Why |
|---|---|---|
| R1 | The Python hierarchy is in `python/`, unchanged from Unit 2 except for bug fixes you name in the decision log, and its tests still run. | The comparison is only honest if the original is there to compare. |
| R2 | C# targets `net8.0`. The solution is classic `.sln`: `dotnet new sln -n Name --format sln`. | Lab machines may have an older SDK than the one you build on, and an older SDK cannot open `.slnx`. |
| R3 | The library project has `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`. | A warning in a panel library is a bug that has not happened yet. Week 12, Thursday. |
| R4 | No public fields. Every settable property validates before it assigns. | Week 12, Monday. A public field lets any caller skip your rules. |
| R5 | At least one interface, kept by at least two classes, and at least one method or loop that uses only the interface. | The brief: more than one kind of thing must plug in. |
| R6 | A switch statement or expression wherever one value maps to several cases. | Week 12, Wednesday. 5.3.7. |
| R7 | No `!` null-forgiving operator and no `#pragma warning disable` in the library, unless `DECISION_LOG.md` gives the proof for each one. | Week 12, Thursday. Silencing is not fixing. |
| R8 | A test project created with `dotnet new xunit -n Name.Tests -f net8.0`, with at least one test per class, one per interface implementation, and one that compares the demo output with the Python's. | The brief: prove the output is the same. `-f net8.0` pins the test packages the lab machines have. |
| R9 | `COMPARISON.md` quotes at least **five different** compiler messages from **your** builds, each beside the Python that ran. | The brief: evidence, not opinion. |
| R10 | `COMPARISON.md` has a section on what the compiler did **not** catch and a section on what took more code in C#. | The brief, and the unit's rule: stricter, not better. |
| R11 | `IMPACT.md` records one interface change, the error list it produced, and your decision. | Week 12, Thursday. 5.7.1 and 5.7.3. |
| R12 | `WALKTHROUGH.md` records the Week 12 Thursday walkthrough, with a decision for every finding. | 5.6.13. |
| R13 | No real personal data anywhere. Invented names and badge ids only. | Program rule. |
| R14 | `bin/`, `obj/`, and `.vs/` are never committed. Every period ends with a commit. | Build output is not source. Version control is daily. |

**Check your structure with the tool.**

```
python project-files/port_check.py path/to/your-port
```

It checks that the pieces exist and have the right shape: 25 checks on a complete port. It cannot
tell whether your comparison is true. A person does that, in the walkthrough and in grading.

---

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| No NuGet package beyond the four test packages `dotnet new xunit -f net8.0` adds | The lab machines have those in their local cache. Anything else may not restore. |
| No AI tool writes your comparison | The comparison is evidence of what **your** compiler did. A model has not built your code. You may use a model for other parts under the usual AI usage log rules. |
| Every compiler message in `COMPARISON.md` is pasted, never retyped | A retyped message is a claim. A pasted one is evidence. |
| Python and C# live side by side in one repository | The controls lead wants to compare them without switching repositories. |

---

## Required repository structure

```
your-port/
  README.md             what it is, how to run both halves, what is not finished
  DECISION_LOG.md       every choice, with what you rejected
  PORT_PLAN.md          Define, Measure, and Analyze, from Week 11
  COMPARISON.md         what the compiler caught, what it did not, what took more code
  IMPACT.md             the interface change experiment
  WALKTHROUGH.md        the Week 12 Thursday record
  .gitignore            includes bin/, obj/, .vs/
  python/               your Unit 2 hierarchy, its demo, its tests, EXPECTED_OUTPUT.txt
  csharp/
    YourName.sln        classic format
    YourName/           the class library, net8.0, warnings as errors
    YourName.Tests/     xunit, net8.0
    YourDemo/           optional console project that prints the demo output
```

Templates for `PORT_PLAN.md`, `COMPARISON.md`, and `WALKTHROUGH.md` are in `project-files/`.

---

## DMAIC checkpoints

The same framework you have used since 145060. Agile ceremonies live inside Improve: a stand-up line
in your decision log at the start of each Improve day.

### Define · Week 11, Tuesday, Build 2

What exactly are you porting? Every class, its level, its parent, its polymorphic method, and every
hand-written type or value check in the Python, with file and line.

**Checkpoint, end of Build 2:** `PORT_PLAN.md` has the class table and the checks list, and the
Python tests run.

### Measure · Week 11, Wednesday, Build 2

What does "same behavior" mean in numbers? Capture the Python demo's output into
`python/EXPECTED_OUTPUT.txt`. Record the Python test count. For each hand-written check, predict:
"the compiler will do this" or "still my job."

**Checkpoint, end of Build 2:** the expected output committed from a real run, and a prediction for
every check.

### Analyze · Week 11, Friday, Build 2

Map every Python member to its C# type, access modifier, and kind: field, property, or method. Decide
which behavior becomes the interface, what its members are, and which two or more classes keep it.

**Checkpoint, end of Build 2:** the mapping table and the interface decision in `PORT_PLAN.md`.

### Improve · Week 12, Monday to Wednesday, Build 2

- **Monday:** the solution, the library, and every class with its modifiers. It builds.
- **Tuesday:** the interface and its implementations, and the first tests.
- **Wednesday:** switches, the demo, the output test, and the first five `COMPARISON.md` entries.

**Checkpoint, end of each Build 2:** the day's item builds and is committed.

### Control · Week 12, Thursday and Friday

Prove it stays working, and have someone else look.

- **Thursday, Build 1:** warnings as errors on; the interface experiment and `IMPACT.md`.
- **Thursday, Build 2:** the peer walkthrough and your five-minute demo.
- **Friday:** fixes from the walkthrough, `COMPARISON.md` finished, `port_check.py` clean, final push.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Defined | Week 11 Tue, end of Build 2 | `PORT_PLAN.md` has classes and checks |
| M2 | Measured | Week 11 Wed, end of Build 2 | `EXPECTED_OUTPUT.txt` from a real run; every check has a prediction |
| M3 | Analyzed | Week 11 Fri, end of Build 2 | mapping table and interface decision |
| M4 | It builds | Week 12 Mon, end of Build 2 | every class ported; `dotnet build` succeeds |
| M5 | It plugs in | Week 12 Tue, end of Build 2 | interface with two implementations; one test each |
| M6 | It matches | Week 12 Wed, end of Build 2 | output test passes; five `COMPARISON.md` entries |
| M7 | It is reviewed | Week 12 Thu, end of block | warnings as errors; `IMPACT.md`; `WALKTHROUGH.md` |
| **Due** | **Everything** | **Week 12 Fri, commit window** | `port_check.py` passes every check; last push |

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not in quality.

### Small, and completely finished

**What it is:** the Unit 2 hierarchy as it was, three levels and one polymorphic method. The
interface is that polymorphic method, kept by two classes. Five compiler catches, each from a real
mistake made during the port.

**What makes it full marks:** every requirement met, every catch real, an honest "did not catch"
section, and a demo that matches line for line.

**Why someone would choose it:** a Unit 2 hierarchy that is already small, or a week with lost days.

**The risk:** a comparison that lists five catches and nothing else. The brief asked what the
compiler did **not** catch, and so does the rubric.

### Medium, and the one most students should aim for

**What it adds:** a composed class, like a sensor inside a machine, ported with a nullable value for
"no reading"; a recursive method, if Unit 2 had one; three classes keeping the interface, one of them
outside the main hierarchy; seven or more catches; and a Python test ported to C# for each class.

**Why someone would choose it:** this is where the interface does real work, because a class outside
the hierarchy can only plug in through it.

**The risk:** the nullable value. The compiler will suggest a cast. A cast compiles and throws on the
day the value is missing. The comparison should say so.

### Large, and only with Wednesday's checkpoint met early

**What it adds:** the whole Python test suite ported, a second interface experiment where the new
member goes into a separate, narrower interface instead, and a "did not catch" section where every row
has a C# test that proves the hand-written check works.

**Why someone would choose it:** BPA 330 C# Programming competitors, and anyone who wants the port to
be the base of the Unit 7 and 8 panel.

**The risk:** the test suite eats Thursday, and the walkthrough happens with nothing to show. Cut the
suite before you cut the walkthrough.

### Scope calibration

| If you | Aim for |
|---|---|
| lost more than one day in Week 11, or your hierarchy is under 150 lines | Small |
| met M3 on time and your hierarchy has a composed class | Medium |
| met M4 by Monday's Build 1 and your Python has a test suite | Large |

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

**Functionality, 25.** The library builds with warnings as errors. Every class is ported. The
interface has at least two implementations, and some code uses only the interface. The tests pass.
The demo prints what the Python printed, and a test proves it.

**Code Quality, 20.** Scored on the five-dimension standard: Correctness, Security, Readability,
Performance, Requirements Fit. No public fields. Validation before assignment. No `!` or `#pragma`
without proof. C# names. Comments that say why.

**Documentation, 20.** `COMPARISON.md` is the heart of it: at least five real catches with the Python
beside each, an honest "did not catch" section, and a "more code in C#" section with a measured
example. `IMPACT.md` has the error list and a decision with a reason. `README.md` says how to run both
halves and what is not finished. `port_check.py` passing is the floor, not the grade.

**Process, 15.** M1 to M7 met on their days. A commit at the end of every period. A decision log with
what you chose and what you rejected, including the pattern you chose and the one you rejected. A
walkthrough record with a decision on every finding.

**Demonstration, 10.** The five-minute script below, in your walkthrough group, including the
question.

**Polish, 10.** The repository reads well to a stranger. Output formats match the Python. No leftover
lab files, no build output, no TODOs.

---

## The five-minute demo script

Five minutes. Timed by your recorder. The walkthrough starts when you stop.

| Minutes | What |
|---|---|
| 0:00 to 0:30 | **The brief, in the controls lead's words.** What did they ask for? |
| 0:30 to 1:30 | **Run both.** The Python demo, then the C# demo. Point at one line and say it matches. |
| 1:30 to 2:30 | **One catch, live.** Make one mistake from your `COMPARISON.md` in the C# code, build, and read the error aloud. Then show that the same mistake runs in Python. |
| 2:30 to 3:30 | **The interface.** Show the two classes that keep it and the code that only knows the interface. |
| 3:30 to 4:15 | **One thing the compiler did not catch,** and the check or test that does. |
| 4:15 to 5:00 | **The question.** |

### The question

Your instructor asks it, in person, during Thursday's walkthrough or in Friday's last ten minutes,
without notes:

> Name one mistake your compiler refused that Python ran. Then name one check you still had to write
> by hand, and say why the compiler could not do it.

**The only way to fail this program outright is submitting work you cannot explain.** This question
is where that is checked.

### The ten-point demonstration checklist

| # | | Points |
|---|---|---|
| 1 | The brief stated in the controls lead's terms | 1 |
| 2 | Both demos run, and a matching line is pointed at | 2 |
| 3 | A real compiler catch made live, read aloud, and contrasted with Python | 2 |
| 4 | The interface shown with its two implementations | 2 |
| 5 | One thing the compiler did not catch, with its check | 1 |
| 6 | The question, answered without notes | 2 |
| | **Total** | **10** |

---

## Peer walkthrough questions

Your reviewer asks these on Thursday. You do not defend. Your recorder writes.

1. Which member did you make more visible than it needs to be, and why?
2. What does your interface promise that one of its classes cannot keep?
3. Which hand-written check did you keep, and what would happen without it?
4. Where is the proof behind each `!`, if there is one?
5. What does your code do with a missing value?

---

## Submission checklist

- [ ] `python project-files/port_check.py .` passes every check
- [ ] `dotnet build` succeeds with warnings as errors, targeting `net8.0`
- [ ] `dotnet test` passes, and you can say how many tests
- [ ] `python -m unittest` in `python/` still passes
- [ ] The C# demo prints what `python/EXPECTED_OUTPUT.txt` holds, and a test checks it
- [ ] `COMPARISON.md`: five or more pasted catches, the "did not catch" section, the "more code"
      section
- [ ] `IMPACT.md` and `WALKTHROUGH.md` complete
- [ ] `DECISION_LOG.md` names what you rejected
- [ ] No personal data. No `bin/`, `obj/`, or `.vs/` committed
- [ ] Pushed inside the Week 12 Friday commit window

# Additional Resources · Week 5
## 145065 Object-Oriented Programming · Unit 2 · Week 5
### Topic: polymorphism in place of conditionals, composition over inheritance, and the design walkthrough

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**Your project ships Friday.** Every resource here is optional reading for a busy week. If you have
time for one, pick the one that matches the part of your project you are least sure of.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Refactoring Guru, "Replace Conditional with Polymorphism" | On-level | 15 min |
| 2 | Refactoring Guru, "Replace Inheritance with Delegation" | On-level | 15 min |
| 3 | Video: Fun Fun Function, "Composition over Inheritance" | On-level | about 8.5 min |
| 4 | Python Tutorial, chapter 9, "Classes" | Remediation | 30 min |
| 5 | Python Tutorial, section 4.7, `match` statements | Extension | 20 min |
| 6 | Python Tutor, one call and many answers | On-level | 20 min |
| 7 | Google Engineering Practices, the code review guides | On-level | 25 min |
| 8 | Think Python 3e, chapter 17, the "favor composition" prompt | Extension | 10 min |
| 9 | Side quest: SQ-16, or SQ-17 | Extension | one block |

---

## 1. Primary reading for Monday

**Refactoring Guru, "Replace Conditional with Polymorphism"** ·
`https://refactoring.guru/replace-conditional-with-polymorphism` · **Opened.**

**What it is.** A free reference page on one refactoring. It has four parts: the problem, the
solution, why to refactor, and how to do it step by step. The examples are in several languages,
including Python and C#.

**Why this one.** It is Monday's concept, named the way working developers name it. Compare its "How to
Refactor" steps with what you do in Lab U02-03. The C# example is a preview of Unit 6.

**Watch for this.** The site also sells a paid course. You do not need it. The refactoring pages are
free to read.

**Time.** 15 minutes. **Level.** On-level.

---

## 2. Primary reading for Tuesday

**Refactoring Guru, "Replace Inheritance with Delegation"** ·
`https://refactoring.guru/replace-inheritance-with-delegation` · **Opened.**

**What it is.** The refactoring for a subclass that uses only part of its parent. You give the class
a field that holds the other object, and hand work to it, instead of inheriting from it.

**Why this one.** It is Tuesday's "has a, not is a" from the direction you will meet it at work: a
hierarchy someone else built that should have been composition. Your written analysis asks for the
strongest argument against each choice. Read this page with that in mind.

**Time.** 15 minutes. **Level.** On-level.

---

## 3. Video, under 20 minutes

**Fun Fun Function, "Composition over Inheritance"** ·
`https://www.youtube.com/watch?v=wfMtDGfHWpA` · **Opened.** Running time about 8 and a half
minutes, read from the page when this file was written.

**What it is.** A short, informal video that argues for composition over inheritance with a worked
code example.

**Why this one.** It gives Tuesday's "has a, not is a" idea a second voice. The code is JavaScript,
not Python. The design argument is the same in any language, and reading it in another language is
a small rehearsal for Unit 6.

**Level.** On-level. YouTube may be blocked on the school network.

---

## 4. Official documentation, and remediation

**The Python Tutorial, chapter 9, "Classes"** · `https://docs.python.org/3/tutorial/classes.html` ·
**Opened.**

**What it is.** The official tutorial on classes. Section 9.5, "Inheritance," shows how Python
looks up a method: it checks the object's class first, then the parent.

**Why this one.** That lookup is what makes polymorphism work. When the loop calls
`item._kind_findings()`, Python finds the version on the object's own class. If Monday's concept
felt like magic, section 9.5 is the mechanism.

**Give yourself one question to answer from the page:** "When a subclass and its parent both define
a method, which one does Python run, and why?"

**Time.** 30 minutes. **Level.** Remediation for anyone below 8 of 8 on Lab U02-03.

---

## 5. Extension documentation

**The Python Tutorial, section 4.7, "`match` Statements"** ·
`https://docs.python.org/3/tutorial/controlflow.html` · **Opened.** Scroll to section 4.7.

**What it is.** The official introduction to `match`, including class patterns such as
`case Point(x=0, y=0):`.

**Why this one.** Monday's EXTENDED option rewrites the if/elif chain as a `match` statement. Do it,
then ask yourself the honest question: is the `match` version any better at handling a new kind of
equipment? A `match` is still a conditional. It is cleaner to read. It still needs an edit for every
new kind. Unit 6 returns to this idea in C#.

**Time.** 20 minutes. **Level.** Extension.

---

## 6. Interactive practice

**Python Tutor** · `https://pythontutor.com/` · **Opened.**

**What it is.** A free tool that draws your objects and frames as the code runs.

**Why this one.** Polymorphism is invisible in the source. Python Tutor shows it: each object points
to its own class, and each call lands in a different method.

**Try this.** Make a parent class `Snack` with a method `label()` that raises
`NotImplementedError`. Make `Chips` and `Pretzels` answer `label()` in their own way. Put one of each
in a list and call `label()` in a loop. Step through and watch which method each call enters. Then
add `Popcorn` with no `label()` and see which line fails, and when.

**One rule.** The site also offers an AI tutor chat. Do not use it. This course runs AI on lab
hardware only. Use the visualizer only, with made-up data.

**Time.** 20 minutes. **Level.** On-level.

---

## 7. Real industry work: how a large engineering team reviews design

**Google Engineering Practices, code review guides** · all **Opened.**

| Page | Address | Read it for |
|---|---|---|
| Introduction | `https://google.github.io/eng-practices/review/` | what a review looks for, starting with design |
| How to write code review comments | `https://google.github.io/eng-practices/review/reviewer/comments.html` | reviewer role: comment on the code, not the developer |
| How to handle reviewer comments | `https://google.github.io/eng-practices/review/developer/handling-comments.html` | author role: never answer in anger, work toward consensus |

**What it is.** The public version of the review guidelines one large software company gives its
engineers.

**Why this one.** Wednesday's walkthrough asks you to do three things professionals are paid for:
review a design, listen to criticism, and settle a disagreement with a recorded decision. These
pages show that the same rules apply at scale. Read the reviewer page before you review. Read the
author page before you are reviewed.

**Watch for this.** These guides are written for reviewing code changes, not a design packet.
The listening and disagreement advice carries over. The process details do not.

**About the listening competency.** No free source was opened that teaches active listening on its
own in a way that fits this course. The walkthrough guide in your project folder is the primary
source for Wednesday's listening moves. These pages support it.

**Time.** 25 minutes. **Level.** On-level. Read before Wednesday Build 2.

---

## 8. Extension: a question worth arguing

**Think Python, 3rd edition, chapter 17, "Inheritance"** ·
`https://allendowney.github.io/ThinkPython/chap17.html` · **Opened.**

**What it is.** The chapter you may have read last week. Near its end is a discussion prompt about
the advice "favor composition over inheritance."

**Why this one.** The chapter's own `Hand` class inherits from `Deck`. Is a hand a deck? Write the
strongest case for inheritance and the strongest case for composition, in your `INHERITANCE_OR_COMPOSITION.md` style.
That is exactly the skill Friday's arguable Gate 2 defect rewards.

**One rule.** The prompt suggests asking a virtual assistant. Do not. Argue it yourself, or with a
classmate.

**Time.** 10 minutes. **Level.** Extension.

---

## 9. Side quest

**SQ-16 · The Class That Should Not Be a Class** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**Why this one.** It is the Friday option for anyone who shipped early. It asks the question this
week keeps asking, one level up: not "inheritance or composition," but "a class at all?"

**If you already did SQ-16 last week:** do **SQ-17 · Unit Tests for Something You Already Wrote**,
pointed at `inspection.py` from Lab U02-03. Write a test with a kind of equipment nobody planned for.

**Time.** One block. **Level.** Extension. Only after the project is committed.

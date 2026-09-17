# Additional Resources · Week 2
## 145065 Object-Oriented Programming · Unit 1 · Week 2
### Topic: classes that guard their own rules, class diagrams before code, methods versus functions, and objects that hold objects

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before you rely on it.

Web pages change. Click any link once before you use it in a later year. Everything here is free,
needs no account, and involves no AI tool.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Think Python 3e, chapter 15, "Classes and Methods" | On-level | 30 min |
| 2 | Python for Everybody, chapter 14, "Object-oriented programming" | Remediation | 25 min |
| 3 | The Python Tutorial, section 9.3, "A First Look at Classes" | On-level | 20 min |
| 4 | Mermaid, "Class diagrams" syntax page | On-level | 15 min |
| 5 | GitHub Docs, "Creating diagrams" | On-level | 5 min |
| 6 | Video: Python for Everybody, Objects, Parts 1 and 2 | Remediation | under 20 min each, [VERIFY] |
| 7 | Practice: the Think Python chapter 15 exercises, in your own editor | On-level | 30 min |
| 8 | Industry essay: "Tell Don't Ask" | Extension | 10 min |
| 9 | Side quest: SQ-06 | Extension | one block |

---

## 1. Primary reading

**Think Python, 3rd edition, chapter 15, "Classes and Methods"** ·
`https://allendowney.github.io/ThinkPython/chap15.html` · **Opened.**

**What it is.** A free textbook chapter by Allen Downey. It turns functions that take a `Time` object
into methods of the `Time` class. Its sections include "Defining methods," "Another method," "The
`__str__` method," "The init method," and "Debugging."

**Why this one.** Wednesday's concept is the move this chapter makes on every page: a function that
needs an object's data becomes a method of that object. Read "Defining methods" and "Another method"
first. They show why `start.print_time()` and `Time.print_time(start)` are the same call, which is
Wednesday's longhand call. The chapter also has a section called "Static methods." Skip it for now.
That is Week 3, Tuesday.

**Time.** 30 minutes. **Level.** On-level.

**If you want the step before it.** Chapter 14, "Classes and Functions"
(`https://allendowney.github.io/ThinkPython/chap14.html`, **Opened**), keeps the functions outside the
class. It is the procedural version of chapter 15, the same shape as Monday's dictionary press.

---

## 2. Remediation reading

**Python for Everybody, chapter 14, "Object-oriented programming"** ·
`https://www.py4e.com/html3/14-objects` · **Opened.**

**What it is.** A free textbook chapter by Charles Severance. Its sections include "Our first Python
object," "Classes as types," "Object lifecycle," and "Multiple instances."

**Why this one.** It moves slowly. If Monday's class felt like a jump from 145060, read "Our first
Python object" and "Multiple instances." They show that two objects from one class keep separate
data, which is why `self` exists. Stop before "Inheritance." That is Unit 2.

**Time.** 25 minutes. **Level.** Remediation.

---

## 3. Official documentation: the language

**The Python Tutorial, chapter 9, "Classes"** · `https://docs.python.org/3/tutorial/classes.html` ·
**Opened.**

**What it is.** The official tutorial chapter on classes, written by the people who maintain Python.

**Why this one.** Read section 9.3, "A First Look at Classes," this week. Subsection 9.3.4, "Method
Objects," explains exactly what happens when you call `press.status_text()`: the object is passed as
the first argument. That is Wednesday's concept in the language's own words. Sections 9.2 and 9.6
are Week 3 reading.

**Time.** 20 minutes. **Level.** On-level. It is dense. Read it after the Think Python chapter, not
before.

---

## 4. Official documentation: the diagram

**Mermaid, "Class diagrams"** · `https://mermaid.js.org/syntax/classDiagram.html` · **Opened.**

**What it is.** The reference page for the Mermaid text format you use to draw class diagrams on
Tuesday.

**Why this one.** It is the source for every symbol your diagram uses. The "Visibility" section lists
`+` for public and `-` for private, and says a `$` at the end of a method marks it static. The
"Defining Relationship" section lists `o--` for aggregation. The "Cardinality / Multiplicity on
relations" section shows how to write `1`, `0..1`, `1..*`, and `*` on a line.

**Watch for this.** Mermaid calls `-` "Private." In Python, `-` means a name with a leading
underscore, which is a convention and not a lock. Week 3, Monday shows exactly what that means.

**Time.** 15 minutes. **Level.** On-level.

---

## 5. Official documentation: where the diagram shows up

**GitHub Docs, "Creating diagrams"** ·
`https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams`
· **Opened.**

**What it is.** GitHub's page on drawing diagrams in Markdown. It says to put Mermaid text inside a
fenced code block marked `mermaid`, and that this works in Markdown files.

**Why this one.** Your refactor's class diagram lives in your repository. This page tells you how to
make GitHub draw it as boxes. If your diagram does not render in your own repository, commit it
anyway and tell your instructor. A photo of a paper diagram with the Mermaid text beside it also
counts.

**Time.** 5 minutes. **Level.** On-level.

---

## 6. Video, under 20 minutes

**Python for Everybody, lesson "Object-Oriented Programming"** ·
`https://www.py4e.com/lessons/Objects` · **Opened.**

**What it is.** Charles Severance's lesson page. It lists four short videos. Watch two: "Objects -
Introduction - Part 1" and "Objects - A Sample Class - Part 2." The lesson page lists them at 10:40
and 8:22. **[VERIFY]** the running time on the video player before you rely on it, since this file
read the lengths from the page, not from the videos.

**Why this one.** Part 2 builds one small class line by line and says out loud what `self` is doing.
If Monday's instruction moved too fast, this is the slower version. Skip Part 4. It covers
inheritance, which is Unit 2.

**Level.** Remediation. The lesson page also has a quiz and a discussion forum that need a login. You
do not need them. The videos may be hosted on YouTube, which the school network may block.
**[VERIFY]** they play on a lab machine.

---

## 7. Interactive practice

**Think Python chapter 15 exercises, run in your own editor** ·
`https://allendowney.github.io/ThinkPython/chap15.html`, section "Exercises" · **Opened.**

**What it is.** The exercises at the end of the chapter from resource 1. You copy the starting code
into a `.py` file in VS Code, write the method each exercise asks for, and run it.

**Why this one, and not a practice website.** The practice sites checked for this week either needed
an account, showed ads, or included an AI chat panel. None of those fit this course. The book's own
exercises need nothing but the editor you already use, and each one asks you to turn behavior into a
method, which is Wednesday's decision. The book's chapters are also Jupyter notebooks with a link to
run them in Google Colab. That needs a Google account, so it is optional. **[VERIFY]** whether your
school account opens it before you try.

**How to use it.** Before you write each method, write one sentence: "This needs the object's ___."
If you cannot fill the blank, it should stay a function.

**Time.** 30 minutes. **Level.** On-level.

---

## 8. Industry connection

**Martin Fowler, "Tell Don't Ask"** · `https://martinfowler.com/bliki/TellDontAsk.html` · **Opened.**

**What it is.** A short essay, dated 2013, by a well-known author on software design. It uses a
monitoring example, a value with a limit that raises an alarm, and compares two styles. In one,
outside code asks the object for its data and decides. In the other, you tell the object what to do,
and it applies its own rule.

**Why this one.** It is Monday's concept, argued by someone who designs software for a living, and
its example is close to a shop-floor alarm. It is also honest about the other side. Here is the
strongest case each way:

- **For keeping behavior with the data.** The rule lives in one place. No caller can forget to check
  the limit, because the object checks it every time. That is why your `Machine` refuses to start
  when it is locked out.
- **Against following it everywhere.** Fowler writes that he does not use the principle himself. He
  argues that trying to remove every method that reports data can make code worse, because some
  code needs to read data, such as a report. That is why your `Machine` still has `is_running()`.

**How to use it.** After you read it, write two sentences: one method in your refactor that should
"tell," and one that should "ask," and why.

**Time.** 10 minutes. **Level.** Extension.

### The current article slot

**Deliberately unfilled.** The essay above is established, not current. No current news article
about object design in industrial software could be opened and honestly described while this file
was written, and this file does not invent one. If your instructor adds one, it goes here, marked
**[VERIFY]**.

---

## 9. Side quest

**SQ-06 · Flowchart the Thing You Already Built** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**What it is.** Take a program you already wrote and produce a flowchart and an IPO chart for it,
after the fact. Then hand both to somebody who has not seen your code and ask them to describe what
the program does. It is done when their description matches what the program really does. If it does
not, the diagram is wrong, and fixing it is the assignment.

**Why this one.** Tuesday says the diagram comes first. Most people do not believe that until they
draw one after the fact and see what it would have caught. If you did SQ-06 in 145060, skip it and
try it on your 145060 Data Pipeline instead, which is the program your refactor rebuilds.

**Time.** One block. **Level.** Extension. It is graded under BPA / Credential / Capstone.

---

## For the refactor project

This week your refactor is all design. No class code gets committed until your class diagram and
`CLASS_BOUNDARIES.md` are pushed on Friday. These resources help most:

- **Tuesday's inventory and Wednesday's placement table.** Resource 1's "Defining methods" section is
  the placement decision, done once for a `Time` class. Do the same for every function in your
  pipeline: what data does it need?
- **Thursday's boundaries.** For each class, write the collection it keeps and why. Your 145060 Unit 5
  notes on choosing a dictionary, a list, or a set are the reference. The reason is part of the grade.
- **The diagram itself.** Resource 4 for the symbols, resource 5 so it renders in your repository.
- **A common failure mode.** A class that only holds functions and no data is a folder wearing a class
  name. If a box in your diagram has methods and no attributes, ask whether it should be a class at
  all, and write your answer in `CLASS_BOUNDARIES.md`.

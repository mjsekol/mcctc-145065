# Additional Resources · Week 3
## 145065 Object-Oriented Programming · Unit 1 · Week 3
### Topic: encapsulation told honestly, instance, static, and class methods, scope at four levels, and testing a class

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
| 1 | The Python Tutorial, sections 9.2, 9.3.5, and 9.6 | On-level | 30 min |
| 2 | Think Python 3e, chapter 15, section "Static methods" | On-level | 10 min |
| 3 | Python docs, Built-in Functions: `property`, `staticmethod`, `classmethod` | On-level | 20 min |
| 4 | Python docs, `unittest` | On-level | 25 min |
| 5 | PEP 8, "Designing for Inheritance" | Extension | 10 min |
| 6 | Video: "Python OOP Tutorial 6: Property Decorators" | On-level | [VERIFY] length |
| 7 | Practice: predict, then run, two official examples | On-level | 30 min |
| 8 | Industry essay: "Unit Test" | Extension | 15 min |
| 9 | Side quest: SQ-17 | Extension | one to two blocks |

---

## 1. Primary reading

**The Python Tutorial, chapter 9, "Classes"** · `https://docs.python.org/3/tutorial/classes.html` ·
**Opened.**

**What it is.** The official tutorial chapter on classes. Last week you read section 9.3. This week
you read three more parts:

- **9.6, "Private Variables."** Read this before Monday's lab. It says in plain words that
  "private" instance variables, reachable only from inside an object, do not exist in Python. It
  says a leading underscore marks a name as non-public by convention, and that a name starting with
  two underscores is rewritten to include the class name. That rewrite is called name mangling.
- **9.2, "Python Scopes and Namespaces,"** with its example in 9.2.1. Read this before Wednesday. It
  is where a name lives, from the people who wrote the rules.
- **9.3.5, "Class and Instance Variables."** Also for Wednesday. It shows a class variable shared by
  every object, and the bug you get when a shared value is something you can change.

**Why this one.** This week's honest line is "Python has no real private." You should not take that
from your instructor or a slide. Section 9.6 says it in the official documentation.

**Time.** 30 minutes across the week. **Level.** On-level. Section 9.2 is the hardest reading in the
unit. Read it twice, and run its example (resource 7) before you decide you understand it.

---

## 2. A second reading for Tuesday

**Think Python, 3rd edition, chapter 15, section "Static methods"** ·
`https://allendowney.github.io/ThinkPython/chap15.html` · **Opened.**

**What it is.** The section you skipped last week. It shows a static method that is called on the
class itself, with no object.

**Why this one.** It is a short, concrete case of Tuesday's question: what does this method need? A
static method needs no object, so it gets none.

**Time.** 10 minutes. **Level.** On-level.

---

## 3. Official documentation: the three tools for Monday and Tuesday

**Python docs, "Built-in Functions"** · `https://docs.python.org/3/library/functions.html` ·
**Opened.**

**What it is.** The reference entries for every built-in. Find three:

- **`property`.** Shows the `@property` decorator and the `.setter` form. The example stores the
  value in `self._x`, with the underscore. That underscore is what keeps the setter from calling
  itself forever, which is Monday's `RecursionError`.
- **`staticmethod`.** A method that receives no automatic first argument. It can be called on the
  class or on an object. The entry ends by pointing to `classmethod` as the variant for creating
  alternate class constructors, which is your `from_record`.
- **`classmethod`.** A method that receives the class, named `cls`, as its first argument, the way
  an instance method receives the object.

**Why this one.** When a tutorial and the reference disagree, the reference wins. Use it to settle
any argument about what a decorator does.

**Time.** 20 minutes. **Level.** On-level.

---

## 4. Official documentation: testing

**Python docs, "unittest"** · `https://docs.python.org/3/library/unittest.html` · **Opened.**

**What it is.** The reference for the testing framework you use on Thursday.

**Why this one.** Read three sections. "Basic example" shows a test class and how to run it.
"Organizing test code" explains why `setUp` builds a fresh object before every test. "Distinguishing
test iterations using subtests" shows `subTest`, which names the value that failed. The
"Command-Line Interface" section shows `python -m unittest -v`, the command you run in your refactor
folder.

**Time.** 25 minutes. **Level.** On-level. The full page is long. Read those sections only.

---

## 5. Official documentation: the naming convention

**PEP 8, "Style Guide for Python Code"** · `https://peps.python.org/pep-0008/` · **Opened.**

**What it is.** The official style guide. Under "Naming Conventions," the sections "Method Names and
Instance Variables" and "Designing for Inheritance" say to use one leading underscore for non-public
methods and instance variables, and explain what two leading underscores do.

**Why this one.** It is where the underscore convention comes from. It also explains why two
underscores exist at all: to avoid name clashes in subclasses. That is a Unit 2 idea, so read it now
and expect it to make more sense in Week 4.

**Time.** 10 minutes. **Level.** Extension.

---

## 6. Video

**"Python OOP Tutorial 6: Property Decorators - Getters, Setters, and Deleters"** ·
`https://www.youtube.com/watch?v=jCzT9XFZ5bw` · **Opened** for the title only. **[VERIFY]** the
channel and the running time before you rely on it. The page's channel name and length did not load
when this file was written. The series is widely credited to Corey Schafer. Confirm that on the page.

**What it is.** A screen-recorded lesson on `@property` and its setter.

**Why this one.** Monday's concept, shown by someone typing it live, the same way your instructor
does. Watch for the moment a value is read with attribute syntax but a method runs. That is the
whole point of a property.

**A second video in the same series, for Tuesday.** "Python OOP Tutorial 3: classmethods and
staticmethods" · `https://www.youtube.com/watch?v=rq8cL2XMM5M` · **Opened** for the title only.
**[VERIFY]** the channel and the running time.

**Level.** On-level, if the running time is under 20 minutes. If either runs longer, treat it as
extension. YouTube may be blocked on the school network. **[VERIFY]** it plays on a lab machine.

---

## 7. Interactive practice

**Predict, then run: two official examples, in your own editor** · from resources 1 and 4 ·
**Opened.**

**What it is.** Two short programs from the official documentation that you copy into `.py` files in
VS Code and run.

1. **Wednesday: the scopes example in tutorial section 9.2.1.** Before you run it, write down the
   four lines you expect it to print. Then run it. For every line you got wrong, write which scope
   level you misjudged.
2. **Thursday: the "Basic example" in the `unittest` page.** It tests Python's own string methods.
   Run it with `-v` and read the output. Then change one expected value in one test so it is wrong,
   run it again, and read the FAIL report line by line. Put the value back. On your own classes you
   break the code instead of the test. Either way, that is Thursday's rule: a test is only worth
   something if you have seen it fail.

**Why this one, and not a practice website.** The practice sites checked for this unit either needed
an account, showed ads, or included an AI chat panel. None of those fit this course. Predict-then-run
is how the Gate 1 TRACE reps work, so this practice builds the same habit.

**Time.** 30 minutes. **Level.** On-level.

---

## 8. Industry connection

**Martin Fowler, "Unit Test"** · `https://martinfowler.com/bliki/UnitTest.html` · **Opened.**

**What it is.** A short essay, dated 2014 and updated since, by a well-known author on software
design. It describes how programmers who write unit tests disagree about what a "unit" is, and names
two styles. **Solitary** tests replace the code a class works with, so only one class is under test.
**Sociable** tests let the class use its real partners. The essay also argues that unit tests must run
fast enough that you run them many times while you work.

**Why this one.** Thursday's lab tests `Machine` and `WorkCell` together, which is the sociable
style. Here is the strongest case each way:

- **For sociable tests.** They test what really runs. They need no fake objects, so there is less
  test code to get wrong. The essay notes that the early practitioners who popularized this kind of
  testing mostly wrote them this way.
- **For solitary tests.** When one fails, you know which class broke. A bug in `Machine` cannot make
  every `WorkCell` test fail at once.

**How to use it.** Write two sentences in your refactor's `TEST_PLAN.md`: which style your tests use,
and one thing that style could hide from you.

**Time.** 15 minutes. **Level.** Extension.

### The current article slot

**Deliberately unfilled.** The essay above is established, not current. No current news article
about testing or encapsulation in industrial software could be opened and honestly described while
this file was written, and this file does not invent one. If your instructor adds one, it goes here,
marked **[VERIFY]**.

---

## 9. Side quest

**SQ-17 · Unit Tests for Something You Already Wrote** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**What it is.** Write a real test suite for an old program. Cover the normal case, the edge cases,
and at least three inputs designed to break it. It is done when the suite runs, at least one test
fails and exposes a real defect you did not know about, and you fixed it. If nothing fails, you have
not tried hard enough. Write nastier tests.

**Why this one.** It is Thursday's skill on code you wrote without tests. Point it at your 145060
Storm Relay or one of your 145060 labs. Do not point it at your refactor, which needs tests anyway.

**Time.** One to two blocks. **Level.** Extension. It is graded under BPA / Credential / Capstone.

**Not yet: SQ-16.** "The Class That Should Not Be a Class" unlocks after inheritance, in Unit 2.

---

## For the refactor project

This week you build the design you committed on Friday, and it is due at the end of this Friday's
commit window. These resources help most:

- **Monday, the first class.** Resource 3's `property` entry for the validated property the project
  requires. Assign through the property inside `__init__`, so a new object gets the same check as a
  changed one. The failure mode to watch for: `__init__` writes `self._value` directly, and a bad
  object is built with no complaint.
- **Tuesday, the rows.** Your pipeline reads CSV rows. Resource 3's `classmethod` entry is the model
  for a `from_row` or `from_record` method. It should call `cls(...)`, so the row goes through the
  same checks as everything else.
- **Wednesday, the scope map.** Resource 1, section 9.2, for the four levels. Look hard at any value
  your 145060 program passed through every function. It probably belongs on an object now.
- **Thursday, the tests.** Resource 4. Plan each case in `TEST_PLAN.md` before you write it. Every
  validated property gets at least one refusal test with `assertRaises`.
- **Every day.** Run the golden check after each change. A refactor that changes what the program
  prints is a rewrite, and the project does not accept it without a written reason.

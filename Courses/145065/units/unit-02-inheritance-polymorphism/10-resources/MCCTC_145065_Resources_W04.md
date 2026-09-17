# Additional Resources · Week 4
## 145065 Object-Oriented Programming · Unit 2 · Week 4
### Topic: inheritance, extending with super(), abstract base classes, frozen dataclasses, and recursion

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**BPA State usually falls this week.** If you are a competitor, resources 1 and 5 are the fastest
way back into Monday and Thursday. Read the week's lecture notes first. These pages come second.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Think Python 3e, chapter 17, "Inheritance" | On-level | 30 min |
| 2 | Python for Everybody, chapter 14, the "Inheritance" section | Remediation | 20 min |
| 3 | Python docs: `super()`, `abc`, and `dataclasses` | On-level | 25 min |
| 4 | Video: Corey Schafer, "Python OOP Tutorial 4: Inheritance" | On-level | 19 min 40 s |
| 5 | Think Python 3e, chapters 5 and 6, the recursion sections | On-level | 30 min |
| 6 | Video: Computerphile, "What on Earth is Recursion?" | Remediation | 9 min 40 s |
| 7 | Python Tutor, stepping through a recursive walk | On-level | 20 min |
| 8 | Raymond Hettinger's blog post on `super()` | Extension | 30 min |
| 9 | Current industry article | Deliberately unfilled | none |
| 10 | Side quest: SQ-16 | Extension | one block |

---

## 1. Primary reading

**Think Python, 3rd edition, chapter 17, "Inheritance"** ·
`https://allendowney.github.io/ThinkPython/chap17.html` · **Opened.**

**What it is.** A free textbook chapter that builds a deck of cards, then makes a `Hand` class that
inherits from `Deck`. Read the sections "Parents and children" and "Specialization" closely.

**Why this one.** It shows a child class that changes its parent's `__init__`, which is Monday's
deliberate error from the other side. It uses a domain you already understand, so the only new idea
is the inheritance.

**Watch for this.** The chapter does not use `super()`. It calls the parent's method by the parent's
name. Both work for one parent. This course uses `super()`, and Tuesday explains why.

**Time.** 30 minutes. **Level.** On-level.

---

## 2. Remediation reading

**Python for Everybody, chapter 14, "Object-oriented programming"** ·
`https://www.py4e.com/html3/14-objects` · **Opened.**

**What it is.** The free book you used in 145060. The chapter includes a section
called "Inheritance," with a `CricketFan` class that extends a `PartyAnimal` class.

**Why this one.** If Monday felt fast, this is the shortest path back. It is slower than Think
Python and uses smaller examples.

**Time.** 20 minutes. **Level.** Remediation. Read it before Tuesday if your Monday exit ticket
missed.

---

## 3. Official documentation

You will read three short entries this week. Each one is the source for one day's concept.

**Built-in functions, `super()`** · `https://docs.python.org/3/library/functions.html#super` ·
**Opened.** The official definition of what `super()` returns. Tuesday's concept.

**`abc`, Abstract Base Classes** · `https://docs.python.org/3/library/abc.html` · **Opened.**
Find the sentence that says a class cannot be instantiated unless all of its abstract methods are
overridden. That sentence is Wednesday's `TypeError`.

**`dataclasses`, Data Classes** · `https://docs.python.org/3/library/dataclasses.html` · **Opened.**
Read the `frozen` and `order` parameters, then the section "Frozen instances." It explains which
exception you get when you try to change a frozen record.

**Why these.** When a tutorial and the documentation disagree, the documentation wins. These three
entries are short enough to read in one sitting.

**Give yourself one question to answer from the pages:** "What exception does Python raise when I
assign to a field of a frozen dataclass, and what does `order=True` add?"

**Also useful.** The Python Tutorial, section 9.5, "Inheritance"
(`https://docs.python.org/3/tutorial/classes.html`, **Opened**), covers `isinstance()` and
`issubclass()`. You will want both in your tests.

**Time.** 25 minutes. **Level.** On-level.

---

## 4. Video, under 20 minutes

**Corey Schafer, "Python OOP Tutorial 4: Inheritance - Creating Subclasses"** ·
`https://www.youtube.com/watch?v=RSl87lqOXDE` · **Opened.** Running time 19 minutes 40 seconds,
read from the page when this file was written.

**What it is.** A screen-recorded tutorial that builds an `Employee` class, then `Developer` and
`Manager` subclasses that call `super().__init__()`.

**Why this one.** It covers Monday and Tuesday in one sitting, with `super()` used the way this
course uses it. It is close to the 20-minute limit, so watch it at home, not in class.

**Level.** On-level. YouTube may be blocked on the school network.

---

## 5. Reading for Thursday: recursion

**Think Python, 3rd edition, chapter 5, "Conditionals and Recursion"** ·
`https://allendowney.github.io/ThinkPython/chap05.html` · **Opened.**
Read the sections "Recursion," "Stack diagrams for recursive functions," and "Infinite recursion."

**Think Python, 3rd edition, chapter 6, "Return Values"** ·
`https://allendowney.github.io/ThinkPython/chap06.html` · **Opened.**
Read "Recursion with return values," "Leap of faith," and "Checking types."

**Why these.** Thursday is the most exam-dense day of the week, and recursion is taught nowhere
else in the course. The stack diagram section is the same drawing you make for the Lab U02-02 trace
table. "Leap of faith" is the habit that makes recursion readable: trust the smaller call to work.

**The failure mode to name now.** "Infinite recursion" describes a missing base case. Thursday's
second error is different. The base case exists, and the data never reaches it. Watch for that.

**Time.** 30 minutes. **Level.** On-level.

---

## 6. Video: recursion, for a second explanation

**Computerphile, "What on Earth is Recursion?"** ·
`https://www.youtube.com/watch?v=Mv9NEXX1VHc` · **Opened.** Running time 9 minutes 40 seconds, read
from the page when this file was written.

**What it is.** A short explainer from the Computerphile channel that works through recursion
with an example.

**Why this one.** If Thursday's stack of calls did not click, a different voice and a different
example often does.

**Level.** Remediation. Watch before Lab U02-02 step 8.

---

## 7. Interactive practice

**Python Tutor** · `https://pythontutor.com/` · **Opened.**

**What it is.** A free tool that runs your code in the browser and draws every frame, variable, and
object as the program runs. The home page lets you start visualizing without signing in.

**Why this one.** Recursion is hard to see. Python Tutor shows each call as its own frame, stacked,
which is exactly the picture Thursday asks you to draw by hand.

**Try this.** Write a nested list that stands for a line: `[["press", "oven"], [["saw"], "rack"]]`.
Write a recursive function that counts the strings in it. Step through it. Count the frames at the
deepest point. Then delete the base case and watch where it fails.

**One rule.** The site also offers an AI tutor chat. Do not use it. This course runs AI on lab
hardware only, and nothing you type here should include anything about you. Use the visualizer
only. Use made-up data, never your own code with your name in it.

**Time.** 20 minutes. **Level.** On-level.

---

## 8. Extension reading

**Raymond Hettinger, a blog post on `super()`** ·
`https://rhettinger.wordpress.com/2011/05/26/super-considered-super/` · **Opened.**

**What it is.** A blog post by a Python core developer, linked from the official `super()` entry.
It explains the search order Python follows when a class has more than one parent.

**Why this one.** Tuesday says `super()` means "the parent." With one parent, that is true. With
several parents, it means "the next class in the search order," and this post shows why that
matters. The post is several Python versions old. Its Python 3 examples use the same `super()` you use.

**Time.** 30 minutes. **Level.** Extension. Read it only after Lab U02-01 reports 14 of 14.

---

## 9. The current article slot

**Deliberately unfilled.** No free, current article was found and opened that connects class
hierarchies to real industry work without being a product advertisement or a paid course.
Articles on this topic age quickly and many are marketing. Pick one the week you teach this, and
**[VERIFY]** it before assigning it. Week 5's resource page fills its slot with a real engineering
team's code review guide, which serves the same purpose.

---

## 10. Side quest

**SQ-16 · The Class That Should Not Be a Class** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**What it is.** Find code, in your own old work or a public project, where a class was used and a
function would have been better. Rewrite it both ways, then argue both sides in writing.

**Why this one.** It unlocks after inheritance, and it trains the question this week keeps asking:
does this design earn its structure? Your 145060 projects are a good place to look. There is no
correct answer. The argument is the grade.

**Another option.** SQ-17, Unit Tests for Something You Already Wrote, fits `layout.py` from
Lab U02-02. Write tests for a cell nested four levels deep.

**Time.** One block. **Level.** Extension.

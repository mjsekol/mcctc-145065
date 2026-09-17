# Additional Resources · Week 6
## 145065 Object-Oriented Programming · Unit 3 · Week 6
### Topic: custom exceptions, JSON serialization, character encoding, guarded loading, and recovery

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**This is the densest week of the unit sequence.** Four concepts, a project, and a problem drop.
Use this page to fill one gap at a time. Do not try to read all of it.

---

## The week at a glance

| # | Resource | Day | Level | Time |
|---|---|---|---|---|
| 1 | Python Tutorial, chapter 8, "Errors and Exceptions" | Mon | On-level | 30 min |
| 2 | Video: Corey Schafer, "Using Try/Except Blocks for Error Handling" | Mon | Remediation | 10 min 34 s |
| 3 | Automate the Boring Stuff 3e, chapters 5, 10, and 18 | Mon to Thu | Remediation | 20 min each |
| 4 | Python docs: the `json` module | Tue, Wed | On-level | 25 min |
| 5 | Python docs: Unicode HOWTO | Tue | On-level | 30 min |
| 6 | Video: Computerphile, "Characters, Symbols and the Unicode Miracle" | Tue | On-level | 9 min 37 s |
| 7 | Python docs: `pickle` warning, and OWASP Deserialization Cheat Sheet | Wed | On-level | 20 min |
| 8 | Python docs: `os.replace`, `os.fsync`, and `pathlib` | Wed, Thu | On-level | 20 min |
| 9 | Python Tutor, watching an exception travel | Mon | On-level | 15 min |
| 10 | NIST SP 800-34, contingency planning | Thu | Extension | 20 min |
| 11 | Side quest: SQ-17, with SQ-04 as a stretch | after Friday | Extension | one to two blocks |

---

## 1. Primary reading for Monday

**The Python Tutorial, chapter 8, "Errors and Exceptions"** ·
`https://docs.python.org/3/tutorial/errors.html` · **Opened.**

**What it is.** The official tutorial chapter on exceptions. Read these sections:

| Section | Why it matters this week |
|---|---|
| 8.3 Handling Exceptions | the order of `except` clauses, Monday's deliberate error |
| 8.4 Raising Exceptions | `raise` with your own classes |
| 8.5 Exception Chaining | `raise ... from error`, which keeps the original cause |
| 8.6 User-defined Exceptions | the naming habit: classes end in `Error` |
| 8.9 Raising and Handling Multiple Unrelated Exceptions | `ExceptionGroup` and `except*`, for the EXTENDED option only |

**Why this one.** In 145060 you caught exceptions other people designed. This week you design your
own. Do not skip section 8.5. It is the section that makes a traceback tell the whole story.

**Give yourself one question to answer from the page:** "What is the difference between
`raise NewError from error` and `raise NewError from None`?"

**Time.** 30 minutes. **Level.** On-level. Section 8.9 is extension.

---

## 2. Video: exceptions, a second explanation

**Corey Schafer, "Python Tutorial: Using Try/Except Blocks for Error Handling"** ·
`https://www.youtube.com/watch?v=NIWwJbo-9_8` · **Opened.** Running time 10 minutes 34 seconds, read
from the page when this file was written.

**What it is.** A screen-recorded tutorial on `try` and `except` blocks.

**Why this one.** It is 145060 review, fast. If Monday's concept felt built on a foundation you do
not remember, watch this first. It does not cover custom exception families. The tutorial chapter
above does.

**Level.** Remediation. YouTube may be blocked on the school network.

---

## 3. The free book you already know

**Automate the Boring Stuff with Python, 3rd edition** · all **Opened.**

| Chapter | Address | Use it for |
|---|---|---|
| 5, "Debugging" | `https://automatetheboringstuff.com/3e/chapter5.html` | raising exceptions and assertions |
| 10, "Reading and Writing Files" | `https://automatetheboringstuff.com/3e/chapter10.html` | `pathlib`, `open()`, and why to pass `encoding='utf-8'` |
| 18, "CSV, JSON, and XML Files" | `https://automatetheboringstuff.com/3e/chapter18.html` | `json.loads()` and `json.dumps()` |

**Why this one.** Chapter 10 names a failure you can hit on a lab machine: Windows does not use
UTF-8 by default when you open a file without `encoding=`. Tuesday's EXTENDED option tests that
on a lab machine. Read the chapter first so you know what you are looking at.

**Time.** 20 minutes per chapter. **Level.** Remediation. Pick only the chapter for the day you
missed.

---

## 4. Official documentation: JSON

**`json`, JSON encoder and decoder** · `https://docs.python.org/3/library/json.html` · **Opened.**

**What it is.** The reference for every function and parameter you use this week.

**Read these four things on the page, in this order.**

1. The warning at the top about parsing JSON from untrusted sources. It recommends limiting the size
   of what you parse. That is why Wednesday checks the file size before reading.
2. `ensure_ascii` under `dumps()`. It decides whether `Á` is written as itself or as an escape
   sequence. Tuesday's demonstration prints both.
3. `parse_constant` under `loads()`. Python's decoder accepts `NaN` and `Infinity` by default, even
   though they are outside the JSON standard. `parse_constant` is the hook you use to refuse them.
4. The section "Standard Compliance and Interoperability." It explains where Python's JSON and the
   standard disagree.

**Why this one.** Item 3 is the most surprising fact of the week. A file your program accepts may
not be valid JSON at all. A `NaN` load value makes `NaN > 1200` and `NaN <= 1200` both `False`, so a
limit check can let it through without a sound.

**Time.** 25 minutes. **Level.** On-level.

---

## 5. Official documentation: character encoding

**Unicode HOWTO** · `https://docs.python.org/3/howto/unicode.html` · **Opened.**

**What it is.** The official explanation of code points, encodings, and UTF-8, with `ord()`,
`chr()`, `str.encode()`, and `bytes.decode()`.

**Why this one.** Tuesday is the only day in the course that teaches character encoding, and 2.3.1
is on the WebXam. The HOWTO states the rule behind Tuesday's byte table: a code point below 128 is
one byte in UTF-8, and anything higher becomes two, three, or four bytes.

**Read this part first.** The introduction to Unicode and the section on encodings. Stop before the
sections on reading and writing files unless you have time.

**Time.** 30 minutes. **Level.** On-level.

---

## 6. Video, under 20 minutes

**Computerphile, "Characters, Symbols and the Unicode Miracle"** ·
`https://www.youtube.com/watch?v=MijmeoH9LT4` · **Opened.** Running time 9 minutes 37 seconds, read
from the page when this file was written.

**What it is.** A short explainer on how computers represent characters, and how Unicode and UTF-8
fit in.

**Why this one.** It gives you the picture before the HOWTO gives you the details. Watch it first if
the byte table in Lab U03-02 step 6 feels like arithmetic without a reason.

**Level.** On-level. YouTube may be blocked on the school network.

---

## 7. Security: why this course never loads a pickle

**`pickle`, Python object serialization** · `https://docs.python.org/3/library/pickle.html` ·
**Opened.**

The warning box at the top of the page is blunt: "Only unpickle data you trust." (Python
documentation, `pickle` module.) The same box says the module is not secure, and that malicious
pickle data can run code while it is being loaded.

**OWASP, "Deserialization Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html` · **Opened.**

**What it is.** A free guide from OWASP, a nonprofit security community, on deserialization
vulnerabilities. It has a Python section that names `pickle` as a dangerous API for untrusted input.

**Why these.** Wednesday says a file is untrusted input. These two pages show that the people who
wrote Python and the people who test application security agree. This is real industry work:
security reviewers look for exactly this.

**Watch for this.** The cheat sheet shows attack examples. Read them. Do not run them. The course's
harmless demonstration runs `print` and nothing else, and that is the only pickle demonstration you
need.

**Time.** 20 minutes. **Level.** On-level.

---

## 8. Official documentation: saving safely

**`os`, `os.replace()` and `os.fsync()`** · `https://docs.python.org/3/library/os.html` · **Opened.**
Use the page search for `os.replace`.

The `os.replace()` entry says that a successful rename is an atomic operation, and names this a
POSIX requirement. The same entry warns that the operation may fail if the two paths are on
different filesystems. That is why Thursday writes the temporary file in the same folder as the real
one. The `os.fsync()` entry tells you to call `f.flush()` first, then `os.fsync(f.fileno())`.

**`pathlib`, object-oriented filesystem paths** · `https://docs.python.org/3/library/pathlib.html` ·
**Opened.**

Read `Path.stat()`, `Path.read_text()`, and `Path.exists()`. The table "Corresponding tools" maps
older `os` functions to their `pathlib` versions, which helps when you read other people's code.

**Why these.** Thursday's four save steps depend on promises the operating system makes. These
entries are where those promises are written down.

**Time.** 20 minutes. **Level.** On-level.

---

## 9. Interactive practice

**Python Tutor** · `https://pythontutor.com/` · **Opened.**

**What it is.** A free tool that runs your code in the browser and draws every frame as it runs.

**Why this one.** An exception leaves a function without a `return`. Python Tutor shows the frames
disappearing as it travels up to the handler that catches it.

**Try this.** Write `ConcertError(Exception)` and `SoldOutError(ConcertError)`. Write
`buy_ticket()` that raises `SoldOutError` when no seats are left, called from `plan_weekend()`,
called from a `try` block. Step through and watch the frames close. Then swap the order of two
`except` clauses and step through again.

**One rule.** The site also offers an AI tutor chat. Do not use it. This course runs AI on lab
hardware only. Use the visualizer only, with made-up data.

**Time.** 15 minutes. **Level.** On-level.

---

## 10. Real industry work: disaster recovery

**NIST Special Publication 800-34 Rev. 1, "Contingency Planning Guide for Federal Information
Systems"** · `https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final` · **Opened.**

**What it is.** A free government guide to planning for the day an information system fails. The
page links to the full PDF.

**Why this one.** Your `RECOVERY_PLAN.md` is a small version of what this guide describes for large
organizations. It comes from a government agency with nothing to sell. Do not read the whole PDF.
Skim its table of contents and find one idea your recovery plan is missing.

**Watch for this.** The guide is written for federal agencies. The ideas scale down. The paperwork
does not.

**Time.** 20 minutes. **Level.** Extension.

**The current article slot.** The OWASP cheat sheet in resource 7 and this NIST guide are this
week's connection to real industry work. No current news article was opened and included. If you
want one, pick it the week you teach this and **[VERIFY]** it. Do not use an incident you cannot
trace to its source.

---

## 11. Side quest

**SQ-17 · Unit Tests for Something You Already Wrote** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**What it is.** A real test suite for code you already wrote, with at least three inputs designed to
break it.

**Why this one.** Point it at your own `storage.py`. Write bad files you did not think of on
Wednesday: an empty file, a file that is one giant string, a file with a byte-order mark, a file
whose numbers are strings. The quest is done only when one of your tests finds a real defect and you
fix it.

**Stretch: SQ-04 · Number Bases by Hand.** Its stretch goal adds ASCII: the character for a number,
and the number for a character. That is Tuesday's `ord()` with the built-in taken away, and it
reinforces 2.3.1 for the WebXam.

**Time.** One to two blocks. **Level.** Extension. Friday is full, so start this next week.

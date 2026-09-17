# Additional Resources · Week 1
## 145065 Object-Oriented Programming · Unit 0 · Week 1
### Topic: the project environment, documentation, and four emerging technologies

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Python tutorial: Virtual Environments and Packages | On-level | 20 min |
| 2 | uv documentation, the overview page | On-level | 15 min |
| 3 | VS Code: Python environments, and Profiles | On-level | 15 min |
| 4 | GitHub Docs: About Projects | On-level | 10 min |
| 5 | Pro Git, chapter 1 review | Remediation | 20 min |
| 6 | Video: "But what is a neural network?" | Extension | under 20 min, [VERIFY] length |
| 7 | Google Machine Learning Crash Course | Extension | 30 min to start |
| 8 | NIST pages for your brief | On-level | 30 min |
| 9 | Side quest: SQ-17 | Extension | one to two blocks |

---

## 1. Primary reading

**The Python Tutorial, "Virtual Environments and Packages"** ·
`https://docs.python.org/3/tutorial/venv.html` · **Confident.**

**What it is.** The official tutorial chapter on why projects get their own environments and how
`venv` makes one.

**Why this one.** It explains Monday's concept in the language's own words, without uv. The companion
reference page, `https://docs.python.org/3/library/venv.html` (**Opened**), states the
`sys.prefix != sys.base_prefix` check the lab uses.

**Time.** 20 minutes. **Level.** On-level. Remediation for anyone whose Monday exit ticket missed.

### For your brief, free books you already know

The three free books from 145060 remain available: Automate the Boring Stuff
(`https://automatetheboringstuff.com/`), Think Python (`https://allendowney.github.io/ThinkPython/`),
and Python for Everybody (`https://www.py4e.com/`), all **Confident**. None covers emerging technology
directly. Use them to refresh 145060 material the Gate 1 reps review.

---

## 2. The lab tool

**uv documentation** · `https://docs.astral.sh/uv/` · **Opened.**

**What it is.** The official documentation for uv, the tool the lab uses to install Python versions,
build environments, and manage packages. The overview page lists `uv init`, `uv add`, `uv run`,
`uv python install`, `uv python pin`, `uv venv`, and `uv sync`.

**Why this one.** It is the primary source for every uv command in this week's notes.

**Time.** 15 minutes. **Level.** On-level.

---

## 3. Official documentation: the editor

**VS Code, "Python environments in VS Code"** ·
`https://code.visualstudio.com/docs/python/environments` · **Opened.**

Explains the **Python: Select Interpreter** command and how VS Code decides which environment to use.

**VS Code, "Profiles"** · `https://code.visualstudio.com/docs/configure/profiles` · **Opened.**

Explains creating a profile from the Profiles editor with **New Profile**, which is how you build your
Gate 1 profile.

**Give students one question to answer from the pages, not the pages:** "How does VS Code show which
interpreter is active, and how do you switch profiles?"

**Time.** 15 minutes. **Level.** On-level.

---

## 4. Official documentation: the task board

**GitHub Docs, "About Projects"** ·
`https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects`
· **Opened.**

Describes GitHub Projects and its table, board, and roadmap layouts. The board layout is Tuesday's
task board.

**Time.** 10 minutes. **Level.** On-level.

---

## 5. Version control review

**Pro Git, 2nd edition** · `https://git-scm.com/book/en/v2` · **Confident.**

Chapter 1 and section 2.2, for any student whose Git habits slipped over the break. Students met this
book in 145060 Week 1.

**Time.** 20 minutes. **Level.** Remediation only. Do not assign it to the whole class.

---

## 6. Video, under 20 minutes

**3Blue1Brown, "But what is a neural network? | Deep learning chapter 1"** ·
`https://www.youtube.com/watch?v=aircAruvnKk` · **Opened** for the title. **[VERIFY]** the running
time is under 20 minutes before assigning it. The page's length did not load when this file was
written.

**What it is.** An animated explanation of what a neural network is, with no code.

**Why this one.** Wednesday's machine learning example was a single learned limit. This shows what
"learning from data" looks like at a larger scale, which helps students writing an ML or LLM brief.

**Level.** Extension. Watch before class, not during it. YouTube may be blocked on the school network.

---

## 7. Interactive practice

**Google Machine Learning Crash Course** ·
`https://developers.google.com/machine-learning/crash-course` · **Opened.**

**What it is.** A free, self-paced course with videos, interactive visualizations, and exercises,
covering fundamentals through large language models and real-world deployment concerns such as
fairness.

**Why this one.** For a student who chose machine learning or a large language model for the brief
and wants to understand the training and inference layers properly.

**Time.** 30 minutes to start. **Level.** Extension. Google-hosted, so check it is reachable on the
school network.

---

## 8. Sources students can use in their briefs

These are government pages, which have no stake in a purchase. All five were **Opened**. Each is a
place to start, not a citation for anything the student has not read on it.

| Technology | Page | What it is |
|---|---|---|
| IoT | `https://csrc.nist.gov/pubs/sp/800/183/final` | NIST SP 800-183, "Networks of 'Things'," on the building blocks of IoT |
| IoT | `https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program` | NIST's Cybersecurity for IoT program |
| Additive manufacturing | `https://www.nist.gov/additive-manufacturing` | NIST's additive manufacturing research hub |
| LLMs and ML | `https://www.nist.gov/itl/ai-risk-management-framework` | the NIST AI Risk Management Framework |
| Any, for the buyer | `https://www.nist.gov/mep` | the Manufacturing Extension Partnership, which supports small and medium manufacturers |

**Two more, for the architecture section.** `https://mqtt.org/` (**Opened**) describes MQTT, a
messaging protocol for IoT. `https://ollama.com/` (**Opened**) is the home page of a tool for running
open models locally, one way the "model server" layer is built.

### The current article slot

**Deliberately unfilled.** Articles about emerging technology age quickly, and many are vendor
marketing. Pick one current piece from a trade publication or a news outlet the week you teach this,
and use it on Thursday as the "news" row of the source table: find the report it summarizes, or show
that you cannot. **[VERIFY]** whatever you choose.

---

## 9. Side quest

**SQ-17 · Unit Tests for Something You Already Wrote** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**Why this one.** It unlocks with this course, and `env_check.py` is a perfect target: its functions
already take their inputs as parameters. Week 3 teaches unit tests formally, so a student who does
this now arrives ahead.

**Time.** One to two blocks. **Level.** Extension.

# Object-Oriented Programming · 145065
## AI Automation & Software Development · Mahoning County Career & Technical Center

Student materials for **145065 Object-Oriented Programming**, junior year, semester 2.
Instructor: Michael Sekol.

Everything here is written to you, the student. Read it, run it, argue with it.

---

## What this course is

Representing programs as objects: data and the behavior that works on it, bundled together and
protected. You learn object-oriented design in Python, build a full web application with a
database, and then move to C#, where the compiler enforces everything Python lets you fake.

You finish having deployed a live web application and built a working industrial interface that
reads real sensor data off a machine and behaves correctly when that machine stops answering.

**You arrive having finished 145060.** You write Python, use Git without thinking about it, handle
errors, consume an API, and have deployed an app. None of that is re-taught.

## Two languages, and why

Python teaches object-oriented ideas softly. There is no real `private`, only a naming convention.
There are no interfaces, only duck typing. Nothing stops you from passing without understanding.

C# checks your work. `private` means private, and an interface is a contract the compiler
enforces. You learn the ideas in Python first, then meet them again in a language that will not let
you fake them. **C# is not better. It is stricter**, and you will see exactly what that buys and
what it costs.

---

## How this course runs

**118-minute block, Periods 1 through 3.** Every day looks like this:

| Minutes | What happens |
|---|---|
| 15 | Bell ringer, then a timed Gate 1 rep. No AI, no autocomplete |
| 15 | Instruction. One concept, live-coded, including a mistake debugged in front of you |
| 35 | Build 1 |
| 5 | Reset |
| 40 | Build 2, hands-on or pair work |
| 8 | Commit and close. Someone demos or names what broke |

**Friday introduces no new content.** Fridays are for Gate 2, quizzes, BPA preparation, credential
work, side quests, and catch-up.

## The three gates

| Gate | AI use | What it is here |
|---|---|---|
| **Gate 1, Closed** | None | Timed reps. In the C# half they include reading compiler errors, which is a different skill from reading a Python traceback. |
| **Gate 2, Adversarial** | AI is the opponent | You review AI-generated object-oriented code with planted design defects: leaky encapsulation, inheritance where composition belongs, interfaces that promise more than they deliver. The code runs. That is what makes it dangerous. |
| **Gate 3, Open** | Full tooling | Ambitious builds. Your decision log names the design you chose and the one you rejected. |

## The industrial part

The employers around here are manufacturers. The interface you build in the C# half is an
**operator panel**, not a phone app: real-time status, high contrast for bad lighting, large
targets for gloved hands, confirmation before anything destructive, and a screen that tells the
operator the difference between **stale** data and **missing** data.

**Hardware safety.** Units 8 and 9 use a Raspberry Pi and sensors. A signed Lab Acceptable Use and
Safety Agreement must be on file before you touch any equipment. ESD precautions are not optional.
The panel you build monitors equipment. It never switches anything on or off.

## The rules that matter most

- **No work is graded that is not in a repository.** Every period ends with a commit.
- **Every project includes an AI usage log and a decision log** that names the design you chose and
  the one you rejected.
- **AI runs locally.** Commercial AI developer APIs require users to be 18 or older, so this course
  never uses them.
- **No personal information, real names, or school data enters any AI tool.**
- **The only way to fail outright is to submit work you cannot explain.**

---

## What is in here

| Unit | Weeks | Title | Language |
|---|---|---|---|
| 0 | 1 | Onboarding & Emerging Technologies | Python |
| 1 | 2-3 | Classes, Objects & Encapsulation | Python |
| 2 | 4-5 | Inheritance & Polymorphism | Python |
| 3 | 6 | Exceptions & Serialization | Python |
| 4 | 7-8 | Flask: Web Application Framework | Python |
| 5 | 9-10 | Databases, CRUD & Deployment | Python |
| 6 | 11-12 | The C# Transition | C# |
| 7 | 13-14 | Event-Driven Programming & WPF | C# |
| 8 | 15-16 | Industrial Human-Machine Interface | C# |
| 9 | 17-18 | Ship, Document & Demonstrate | C# |

Every unit folder is under `Courses/145065/units/` and has the same shape:

```
03-lecture-notes/      read these if you missed class, or before you build
04-slides/             slide outlines from class
05-labs/               the guided labs and the files they use
07-gate2-adversarial/  the weekly AI design reviews and the code to review
09-project/            project briefs, templates, and problem drops
10-resources/          readings, practice, documentation
```

The course runs 18 weeks. **Grading Period 3 is Weeks 1-9** and **Grading Period 4 is Weeks
10-18.** Your CRUD web application deploys in Week 10, and the WebXam post-test is in Week 16.
Everything is scheduled by week and day, so your teacher will tell you how the weeks line up with
this year's calendar.

Units are added here as they are finished. If a folder is not here yet, it is coming.

Plus `Courses/Misc/` for the Side Quest Catalog, the Lab Acceptable Use and Safety Agreement, and
the side quest bundles.

**Lecture notes are written so you can learn a concept from the file alone.** If you were out,
start there rather than asking someone what you missed.

## What is not in here, and why

Answer keys, quizzes, exams, lesson plans, reference implementations, and the instructor's notes
live in a separate private repository. That is not secrecy for its own sake. A published answer key
is not recoverable, and the work is worth more to you unspoiled.

---

## Getting set up

Your 145060 toolchain still applies. This course adds:

- **Python with uv**, the version your instructor sets up on the lab machines
- **Flask**, for the web application
- **A database:** MySQL Workbench to learn, PostgreSQL to deploy
- **.NET and Visual Studio**, for C#
- **A Raspberry Pi with sensors**, on the isolated lab network, in Units 8 and 9

Your instructor sets up hosting and hardware. Nothing here requires an AI account, an API key, or a
credit card, and nothing you write should ever need one.

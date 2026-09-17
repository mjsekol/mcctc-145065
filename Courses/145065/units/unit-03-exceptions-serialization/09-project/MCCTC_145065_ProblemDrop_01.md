# Problem Drop 1: The Midnight Backup
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Friday

**Time:** 40 minutes: 5 to read, 30 to build, 5 to write up and commit. **Mode:** individual.
**Gate:** 3, full tooling, AI usage log required if you use a model.
**What you may use:** anything from this course and 145060. Standard library only.

---

## Read this as though it came to you on the floor

> From: the second-shift lead, Line 3
>
> The die setup program on the office PC keeps losing everything. Twice this month we came in and
> every die setting was gone. The first time, somebody found an old copy on the USB stick in the desk
> drawer and put it back. This time the stick copy is two weeks old, and I know we added dies since
> then.
>
> Somebody on first shift says it is a virus. I do not think so, but I do not know what it is.
>
> The office PC gets shut off at the power strip when the last person leaves, around eleven. It has
> always been that way.
>
> All I want: make the program copy its file to the USB stick every night at midnight, so this never
> happens again.
>
> Attached: the program's log, the file it has right now, and what is on the USB stick.

The request is also in `REQUEST.txt`. Riverside Fabrication is a composite shop. The people, the
dies, and the data are invented.

---

## The files

Your instructor hands out `problem-drop-01-files/` at the start of the block:

| File | What it is |
|---|---|
| `REQUEST.txt` | the message above |
| `tool_log.txt` | the die setup program's log |
| `die_settings.json` | the settings file on the office PC right now |
| `usb_stick/die_settings.json` | the copy on the USB stick |

Copy the folder into `problem-drop-01/` in your repository. **Never change the three data files.**
They are the evidence. Work on copies if you need to.

---

## What you are being asked to do

**Build something in 30 minutes that would actually stop this shop from losing its die settings.**

That is deliberately not the same as "build a midnight backup." The lead told you what hurts and
suggested a fix. Your first job is deciding whether the suggested fix solves what hurts. You are
allowed to build what they asked for. You are also allowed to build something else, if you can show
why.

**You will not finish everything this shop needs in 30 minutes.** Nobody will. Choosing what to leave
out is part of what is graded.

---

## What to hand in

In `problem-drop-01/`:

1. **`PROBLEM.md`**, written first. What is actually happening, with the evidence: line numbers from
   the log, what is in each file, and what the lead's fix would and would not do.
2. **Your artifact**, one or more `.py` files that run with `python` and no installs. It may read the
   evidence files. It must not change them.
3. **`README.md`** with four short sections:
   - **What I built and why.** What it does, and how it addresses the problem in `PROBLEM.md`.
   - **What I left out.** At least one thing the shop needs that you chose not to build.
   - **A real run.** Paste your artifact's output.
   - **`## Tradeoff`.** What your design gives up, and who at the shop would object. Write it even if
     your instructor asks you in person. On a day with a substitute, this section is the tradeoff
     score.
4. **A commit** by minute 105.

## During the block

Your instructor will come to you and ask one question about a choice you made. It takes about a
minute. You do not need a speech. You need to know why you built what you built.

---

## How it is graded

30 points, under Lab & Practice, as the syllabus places problem drops.

| Part | Points | What earns it |
|---|---|---|
| **Problem Identification** | 15 | `PROBLEM.md` names what is actually destroying the settings, supported by the log and the files, not by a guess. |
| **Working Artifact** | 10 | The artifact runs, uses the evidence or fixes the cause, and does what the README says. |
| **Tradeoff** | 5 | You can explain, out loud or in `## Tradeoff`, what your design gives up and who would object. |

**A small artifact aimed at the real problem scores higher than a large one aimed at the wrong
one.**

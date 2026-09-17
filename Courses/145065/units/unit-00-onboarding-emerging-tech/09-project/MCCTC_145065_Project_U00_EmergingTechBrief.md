# Project · The Emerging Technology Brief
## 145065 Object-Oriented Programming · Unit 0 · Week 1

**100 points. Projects category, 35 percent of your grade.**
**Due Week 1, Friday, at the end of the commit window.** BPA State competitors whose pre-submission
is due this week may submit at the start of Week 2, Monday. Your instructor records the extension.

**Gate 3.** Full tooling, AI allowed, AI usage log required, decision log required.

---

## The brief

> From: the operations manager at Riverside Fabrication
>
> Every trade magazine I open says four things are about to change shops like ours: connected
> sensors, AI that writes, machine learning, and 3D printing. The owner keeps forwarding me articles.
> Half of them are selling something.
>
> I need one of those four explained so I can make a decision. I do not need the history. I need to
> know how it would actually plug into what we already run, what it would cost us, and whether it is
> worth it for a shop our size. If the answer is "not yet," that is a fine answer.
>
> Every number you give me, I am going to ask where it came from. If you made it up, tell me you made
> it up and why you picked it. If it came from somewhere, I want to be able to open it.
>
> One page, maybe two. I read the top paragraph and decide whether to read the rest.

Riverside Fabrication is a **composite**, the invented small metal fabrication shop you work with all
semester. You may choose a different buyer you know, such as your school's makerspace or a club, if
you record the choice in your decision log. **No real person's information, and no real company
presented as having done anything, goes in your brief.**

**That is the whole brief.** It does not say which technology, how long "worth it" is, or what the
shop already runs. Deciding those, and writing them down, is the first thing you are graded on.

---

## What you are building

| # | Piece | Form |
|---|---|---|
| 1 | The brief | `brief.md`, 600 to 1500 words, from `project-files/BRIEF_TEMPLATE.md` |
| 2 | A value model | `value_model.py`, from `project-files/value_model_starter.py` |
| 3 | A decision log | `decision-log.md` entries for this project |
| 4 | An AI usage log | every AI use: what you asked, what you kept, what you checked |
| 5 | A README | what the folder holds and how to run the checker and the model |

---

## Technical requirements

1. **One technology** from the four the syllabus names: the Internet of Things, large language
   models, machine learning, or additive manufacturing. A narrower slice of one is allowed, such as
   machine vision inspection as machine learning.
2. **The brief uses the eight template headings**, in order.
3. **The architecture section names at least four layers** in order, what goes in and out of each,
   and what each runs on.
4. **The integration section names a system the buyer already runs** and the exact point where the
   new layer joins it, including what has to be converted or agreed at that boundary.
5. **At least three sources**, each opened by you, each on one numbered line with a URL and a type.
   Not all vendors. **A chatbot answer is never a source.**
6. **Every figure has an owner.** Any percentage, dollar amount, or large count either cites a source
   `[n]` or is marked `(assumption)` in the same paragraph or table row.
7. **`value_model.py` runs**, prints every input with where it came from, and prints a payback period
   in months. No number appears in its calculations. Calculations use named inputs.
8. **Costs and risks name at least three**: one about money, one about people, one about something
   that can go wrong.
9. **The recommendation says how small the first step is** and what would change your mind.
10. **`python brief_check.py brief.md` passes all six checks.**
11. **The decision log** has an entry for the technology (chosen and rejected) and at least one more
    decision.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| No invented statistics | A decision-maker who spends money on a number nobody measured is trusting you, not the number. |
| Your own numbers are labelled `(assumption)` | Labelled estimates are honest and can be challenged by name. |
| No AI-generated citations without opening them | Models produce plausible sources that do not exist. Gate 2 W01 showed one. |
| No personal data, in the brief or in any AI tool | Program rule. Buyers are composites or organizations, never people. |
| AI models are local or not used | Program rule. Commercial AI accounts require users to be 18 or older. |
| 600 to 1500 words | The client reads the top and decides. Short enough to read, long enough to argue. |

---

## Required repository structure

```
oop-semester/
  README.md
  decision-log.md
  unit-00-brief/
    README.md
    brief.md
    value_model.py
    brief_check.py          copied from project-files/, unchanged
    ai-usage-log.md
```

The AI usage log uses the 145060 template you already know, in
`Courses/145060/units/unit-00-onboarding/09-project/MCCTC_145060_Template_AIUsageLog.md`.

---

## DMAIC checkpoints

### Define · Week 1, Wednesday, end of Build 2

Choose the technology and the buyer. **Checkpoint:** a decision log entry naming the technology you
chose and the one you rejected, and one sentence on who the buyer is.

### Measure · Week 1, Thursday, Build 1

Find sources and put numbers on the buyer's situation. **Checkpoint:** a sources log with at least
three rows, each with publisher, type, and what it supports. A list of the inputs your value model
needs, each marked source or assumption.

### Analyze · Week 1, Thursday, Build 2

Draft the architecture and value sections, and write the value model. **Checkpoint:**
`python value_model.py` runs. `brief_check.py` has been run once, and you wrote down how many checks
failed.

### Improve · Week 1, Friday, Build 2

Revise after Gate 2. Work the checker's failures one at a time. This is the sprint: one short plan at
the start ("the three checks I will fix first"), the work, and a last run.

### Control · Week 1, Friday, commit window

**Checkpoint:** `brief_check.py` reports 6 of 6. `value_model.py` runs. Your README says how someone
else runs both. Everything is committed and pushed.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Technology chosen | Week 1 Wed, end of Build 2 | the decision log entry is committed |
| M2 | Sources found | Week 1 Thu, end of Build 1 | three sources logged, at least one not a vendor |
| M3 | Draft and model | Week 1 Thu, end of Build 2 | `value_model.py` runs and the draft is committed |
| **Due** | **Everything** | **Week 1 Fri, commit window** | `brief_check.py` 6 of 6, and the last commit is pushed |

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality.

### Small, and completely finished

**Technology:** IoT temperature monitoring on one oven. **Value model:** payback only, five inputs.

**What makes it full marks:** every figure owned, a clear integration section about the existing log,
three honest sources, and a recommendation that says "count last year's oven stops first."

**The risk:** a thin costs section. Small scope does not shrink the three required risks.

### Medium, and the one most students should aim for

**Technology:** any of the four. **Value model:** payback plus low, likely, and high scenarios for the
input you are least sure of, and one sentence naming which input the answer depends on most.

**What it adds:** the scenarios turn "it pays back in six months" into "it pays back in six months if
this one number is right, so measure that number first." That is a better recommendation.

**The risk:** scenarios chosen to look good. Your low case must be genuinely low.

### Large, and only if the medium version is finished by Thursday

**Technology:** one of the four, with **two deployment options** compared for the same buyer, such as
a language model on shop hardware against one on a hosted service, or printing parts in-house against
ordering them. **Value model:** both options, with scenarios, and a break-even point.

**What it adds:** a real decision between two architectures, with costs and risks for each.

**The risk:** twice the sources and twice the claims to own, in the same word limit. Cut the history.

### Scope calibration

| If you | Aim for |
|---|---|
| finished Lab U00-02 late or are at BPA State pre-submission this week | Small |
| had 4 of 4 on Lab U00-02 during Build 2 | Medium |
| finished M3 early on Thursday and the checker already passes | Large |

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

**Functionality, 25.** The brief does its job: a manager could make a decision from it. The
architecture is correct and layered. The integration section names the join. `value_model.py` runs
and its payback matches the brief. `brief_check.py` passes.

**Code Quality, 20.** `value_model.py` scored on the five-dimension standard: Correctness, Security,
Readability, Performance, Requirements Fit. Right arithmetic with the right units. No personal data.
Names that say what things are. Each value computed once. Every input labelled with where it came
from.

**Documentation, 20.** Every source opened and correctly described. Every figure owned. Technical
writing: recommendation first, one idea per paragraph, numbers in tables. The README lets someone else
run everything.

**Process, 15.** The three milestones met on time. A decision log with real decisions, each naming the
rejected option. An AI usage log that says what you checked. A commit at the end of every period.

**Demonstration, 10.** The three-minute desk demo below.

**Polish, 10.** Reads cleanly for the client, not for you. Template instructions deleted. No
leftover markers.

---

## The three-minute desk demo

Your instructor comes to your desk during Friday Build 2, or during Week 2, Monday Build 1 if you were
not reached. Three minutes, timed.

| Time | What |
|---|---|
| 0:00 to 0:30 | Your recommendation, in one sentence, in the client's terms |
| 0:30 to 1:15 | Point at the layer where your technology joins the buyer's existing system |
| 1:15 to 2:00 | Run `value_model.py`. Name the input the answer depends on most. |
| 2:00 to 2:30 | Your instructor points at one figure in your brief. Open its source, or show its `(assumption)` label and say why you chose that number. |
| 2:30 to 3:00 | One claim you found and left out, and why |

### The demonstration checklist

| # | | Points |
|---|---|---|
| 1 | Recommendation stated in the client's terms | 2 |
| 2 | Integration point named and explained | 2 |
| 3 | Value model run, and its most sensitive input named | 2 |
| 4 | The chosen figure traced to its source or its assumption | 3 |
| 5 | A rejected claim, with the reason | 1 |
| | **Total** | **10** |

Item 4 is the one that matters most. If you cannot trace a figure you wrote, that is the one way to
fail this program outright: submitting work you cannot explain.

---

## Submission checklist

- [ ] `python brief_check.py brief.md` reports 6 of 6
- [ ] `python value_model.py` runs and its payback matches the brief
- [ ] You opened every source you cite
- [ ] Every figure is cited or marked `(assumption)`
- [ ] Decision log: technology chosen and rejected, plus one more decision
- [ ] AI usage log complete
- [ ] README says how to run the checker and the model
- [ ] No personal information anywhere
- [ ] Template instructions and the working sources log deleted from `brief.md`
- [ ] Committed and pushed inside the Friday commit window

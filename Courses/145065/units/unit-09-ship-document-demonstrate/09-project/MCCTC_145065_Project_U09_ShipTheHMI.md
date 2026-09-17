# Project · Ship the HMI
## 145065 Object-Oriented Programming · Unit 9 · Weeks 17-18

**100 points. Projects category, 35 percent of your grade.**
**Everything is due Week 18, Thursday, at the end of the commit window. The final demonstration is Week
18, Friday.**

**Gate 3.** Full tooling, AI allowed, AI usage log required, and a decision log that names the design
choice you made **and the one you rejected**, as every project in this course does.

---

## The brief

> From: the Line 3 Shift Lead, Riverside Fabrication
>
> I've watched your panel run on the bench and it looks right. Now I have to put it in front of
> people who didn't build it, on a shift where you won't be standing next to it.
>
> Before I take it, I need to know exactly which version I'm getting, how it gets installed, and how
> we go back if it misbehaves. I need something my operators can read with gloves on and a machine
> running behind them. Teach me to use it, then watch somebody who has never seen it try, and fix
> what trips them up.
>
> When you hand it over, put it in writing: what I'm getting, what it doesn't do, and who to call.
> Then show me, in five minutes, what it does, why you built it this way, and what you decided not
> to do.
>
> One more thing. It watches the line. It never touches it. I don't want anything in the paperwork
> that suggests otherwise.

Riverside Fabrication and its Line 3 are a **composite**, the invented shop you have worked with all
semester. The shift lead is a role. **In every document you write, people are named by role only.**

**That is the whole brief.** It does not say what "installed" means on your lab PC, how long the
training is, how many people test it, or what counts as a fix. Deciding those, and writing them down,
is part of the grade.

---

## What you are shipping

Your Unit 8 HMI panel, finished and handed off, as a **ship folder** in your repository.

| # | Piece | Where | First drafted |
|---|---|---|---|
| 1 | The panel, with its version written once and shown on screen | `<Version>` in the WPF `.csproj`; the header | Week 17 Mon |
| 2 | A release build you have installed from your own plan | `release/` (never committed) | Week 17 Mon |
| 3 | Implementation plan, including settings (data dictionary), verification, contingency, and rollback | `docs/IMPLEMENTATION_PLAN.md` | Week 17 Mon |
| 4 | User guide for a non-technical operator, with pictures of the real screen | `docs/USER_GUIDE.md`, `docs/screens/` | Week 17 Tue |
| 5 | Every word your panel can show | `docs/screen-words.txt` | Week 17 Tue |
| 6 | Change log and the baseline | `CHANGELOG.md`, tag `v1.0.0` | Week 17 Wed |
| 7 | Change impact note: your interfaces, the baseline, and every change since | `docs/CHANGE_IMPACT.md` | Week 17 Wed |
| 8 | Training plan and record | `docs/TRAINING_PLAN.md` | Week 17 Thu |
| 9 | Handoff letter to the shift lead | `docs/HANDOFF_LETTER.md` | Week 17 Thu |
| 10 | Operator test record and decisions | `docs/OPERATOR_TEST.md` | Week 18 Mon |
| 11 | At least one released change from the operator test, with its tag | code or guide; tag `v1.0.1` or `v1.1.0` | Week 18 Tue |
| 12 | Demo script | `docs/DEMO_SCRIPT.md` | Week 18 Wed |
| 13 | Decision log and AI usage log | `docs/DECISION_LOG.md`, your AI usage log | all unit |

Templates for 3, 4, 6, 7, 8, 9, and the demo score sheet are in `project-files/`. The operator test kit
is in `05-labs/lab-u09-03-files/operator-test-kit/`.

---

## Required repository structure

Your Unit 8 panel folder becomes the ship folder. Add what is missing.

```
oop-semester/
  unit-08-hmi/                     your Unit 8 folder, now the ship folder (keep its name)
    README.md                      what this is, who reads what, how to run it, the version
    CHANGELOG.md
    docs/
      IMPLEMENTATION_PLAN.md
      USER_GUIDE.md
      HANDOFF_LETTER.md
      TRAINING_PLAN.md
      OPERATOR_TEST.md
      CHANGE_IMPACT.md
      DECISION_LOG.md
      DEMO_SCRIPT.md
      screen-words.txt
      screens/                     pictures the guide links to
    <your panel solution>          the .sln and projects from Unit 8
  unit-09-shipcheck/               Lab U09-01
  unit-09-change-impact/           Lab U09-02
  unit-09-tilewords/               Lab U09-03
```

If your Unit 8 folder has a different name, use it and say so in your README. **`release/`, `bin/`, and
`obj/` are listed in `.gitignore` and never committed.**

---

## Technical requirements

1. **One version, one place.** `<Version>` in the WPF project file. The panel's screen shows it. The
   change log's newest entry and the implementation plan name the same version.
2. **A real release build.** Built with `dotnet publish`, its version stamp checked with the command in
   your plan, copied as a whole folder, and started from that folder. Your plan quotes what you saw.
3. **ShipCheck passes 7 of 7** on your ship folder at the deadline. Paste the final report into your
   README.
4. **The implementation plan has eight sections**: what is installed, where, before you start, steps
   (each with what you should see), settings as a data dictionary, verification, contingency and
   rollback, and known limits.
5. **The user guide is organized by what the operator sees**, uses every screen word, links at least
   four pictures of your real panel, and uses none of ShipCheck's jargon.
6. **The guide and the panel agree.** Every control the guide names exists. Every behavior it describes
   is what the panel does. (ShipCheck cannot check this. People can, and will.)
7. **A baseline.** `v1.0.0` is an annotated tag on the commit you trained on, pushed by name:
   `git tag -a v1.0.0 -m "..."` then `git push origin v1.0.0`.
8. **A trained stakeholder.** A classmate from another team plays the shift lead. Your training plan
   follows show, do, check, and records whether they passed an unseen check situation.
9. **An operator test.** At least one person who is not in this class and is not a programmer used your
   panel with only your printed guide. Your record has numbered lines, no names, and at least two
   findings with decisions.
10. **At least one released change.** A finding from the test becomes a change request with a
    prediction table written before the change, then the change, then tests or a check that holds it,
    then a new version, a change log entry, and a tag. A guide-only change counts if the finding was
    about the guide.
11. **A handoff letter** in professional letter form: from and to by role, a subject line, what is
    handed over, what it does not do, how it was checked, known limits, what to do if something goes
    wrong, and a request for written confirmation. One page.
12. **Monitoring only, everywhere.** No document suggests the panel can control equipment.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| People are named by role only, in every file | No personal data enters any record or any AI tool. A role is all a reader needs. |
| The operator test uses the simulator on a lab PC | Visitors and hardware do not mix. Only your instructor runs a station with the lab Pi, under the safety agreement. |
| The facilitator never helps during a session | Help hides exactly the problem you are there to find. |
| Predictions are committed before the change | A prediction written after the result is not evidence. |
| The version lives in one place | Two places disagree eventually. The only question is when. |
| AI tools are allowed, local models only, and logged | Program rule. Commercial AI accounts require users to be 18 or older. |
| Nothing implies the panel controls equipment | It does not, and a reader who believes it does is in danger. |
| The final demo uses the simulator | A room full of people is not the place to unplug a live sensor. |

---

## DMAIC checkpoints

### Define · Week 17, Monday, Build 2

What does "shipped" mean for your panel, and who receives it? **Checkpoint:** a decision log entry that
names the receiver (the shift lead), what they get, and one thing you decided is **not** part of this
release.

### Measure · Week 17, Monday to Tuesday

Where does your ship folder stand? **Checkpoint:** your first ShipCheck report pasted into
`unit-09-shipcheck/RESULTS.md`, with the number of failing checks. Your version stamp read back from a
real release build.

### Analyze · Week 17, Wednesday

What does your panel depend on, and what depends on it? **Checkpoint:** `docs/CHANGE_IMPACT.md` has the
baseline section and your interfaces table. `v1.0.0` is tagged and pushed.

### Improve · Week 17, Thursday, to Week 18, Tuesday

Train, test, fix. This is the sprint.

- **Plan** (Week 17 Thu, start of Build 1): write three to five sprint items on your task board: the
  training, the letter draft, the guide fixes from Gate 2, the operator test, the patch.
- **Daily stand-up** (every commit and close): one sentence each on what you finished, what is next, and
  what blocks you.
- **Review** (Week 18 Tue, end of Build 2): your patch is tagged, and your partner reads your change log
  aloud to you.

**Checkpoints:** training record (Week 17 Thu), revised guide (Week 17 Fri), operator test record
(Week 18 Mon), released change (Week 18 Tue).

### Control · Week 18, Wednesday to Thursday

Can someone else keep this running? **Checkpoint:** ShipCheck 7 of 7. Your rollback tested: start the
previous release folder and read its version on screen. Handoff letter final. Everything pushed, tags
included.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Version on screen, release build, plan draft | Week 17 Mon, end of block | the plan quotes your version stamp |
| M2 | Guide draft, pictures, screen words | Week 17 Tue, end of block | ShipCheck runs on your folder and you recorded the report |
| M3 | Baseline | Week 17 Wed, end of block | `v1.0.0` is pushed and the change log names it |
| M4 | Training record, letter draft | Week 17 Thu, end of block | the record says whether the check situation passed |
| M5 | Guide revised after Gate 2 | Week 17 Fri, end of block | every Gate 2 defect you found in your own guide is fixed |
| M6 | Operator test record | Week 18 Mon, end of block | numbered lines, no names, two or more findings |
| M7 | Released change | Week 18 Tue, end of block | the new tag is pushed and the change log and impact note agree with it |
| M8 | Demo script and one timed rehearsal | Week 18 Wed, end of block | the rehearsal came in under five minutes |
| **Due** | **Everything** | **Week 18 Thu, commit window** | ShipCheck 7 of 7, everything pushed, tags included |
| Demo | Final demonstration | Week 18 Fri | presented and scored |

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality.

### Small, and completely finished

**The panel:** your Unit 8 panel as it stands, with the version added to the window title or header.
**The change:** a guide-only fix from the operator test, released as a PATCH, tagged, and logged.
**Pictures:** screen captures of the real panel in four states, taken with the simulator.

**What makes it full marks:** every document true to the panel, one real visitor, a record with numbered
lines, a clean handoff letter, and a rollback you actually tried.

**The risk:** a thin impact note. A guide-only change still has a prediction table, and it still says
what it did not touch.

### Medium, and the one most students should aim for

**The panel:** version on the header, read from the program's own stamp.
**The change:** a code fix from the operator test, held in place by at least one new test, released and
tagged. The worst-case layout checked after the change.
**Pictures:** captures or rendered pictures, updated after the change.

**What it adds:** a change that crosses code, tests, guide, and pictures, and an impact note whose
predictions were wrong in at least one row, honestly recorded.

**The risk:** the fix grows. Keep the change to what the finding asked for.

### Large, and only if Medium is finished by Week 18, Tuesday

**Adds:** Lab U09-01 EXTENDED (the release stamp check) run on your real release folder, rendered
pictures produced by a harness like the Unit 8 snapshot program, and a deferred finding analyzed in the
impact note with its full cost.

**What it adds:** a ship folder that proves its own consistency, down to the program file.

**The risk:** the tooling becomes the project. The shift lead needs the documents first.

### Scope calibration

| If you | Aim for |
|---|---|
| finished your Unit 8 panel late, or it still has a known bug | Small |
| had Lab U09-01 at 27 of 27 on Tuesday | Medium |
| tagged `v1.0.0` on Wednesday before the reset | Large |

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

**Functionality, 25.** The shipped panel runs from its release folder, shows its version, and behaves
as the guide says in every state, including stale, missing, and alarm through a disconnect. ShipCheck
reports 7 of 7. The rollback works.

**Code Quality, 20.** Your changes this unit, scored on the five-dimension standard. **Correctness:**
the released change does what the finding needed, and your tests pass. **Security:** no personal data
anywhere; nothing implies control; the sensor service stays on the lab network. **Readability:** the
version lives in one place; changes are small and named in the change log. **Performance:** no change
blocks the window. **Requirements Fit:** each change traces to a finding or to the brief.

**Documentation, 20.** Implementation plan, user guide, handoff letter, training plan, change log, and
impact note, each written for its one reader, each true to the panel. The letter meets requirement 11.
Nothing names a person.

**Process, 15.** Milestones on time. Predictions committed before changes. A baseline tag and a release
tag, pushed. A decision log with rejected options. An operator test run by the rules and recorded
honestly, including any rule you broke. An AI usage log. A commit at the end of every period.

**Demonstration, 10.** The score sheet below.

**Polish, 10.** Documents read cleanly for their reader. Pictures match the current release. No
template instructions left behind. No `bin`, `obj`, or `release` committed.

---

## The final demonstration

**Week 18, Friday.** Five minutes, then two minutes of questions. The simulator runs on the class
machine or your lab PC. **No hardware in the demonstration.**

| Time | What | Evidence on screen |
|---|---|---|
| 0:00 to 0:30 | **The one sentence.** What it is, for whom, and that it only watches. | your header |
| 0:30 to 2:00 | **What it does.** Normal, then an alarm, then a failure state. Show that the alarm survives the failure. | the running panel |
| 2:00 to 3:30 | **Why it is built this way.** Three decisions, each pointing at evidence: a requirement, a test, a picture, or a numbered line from your operator test. | your documents |
| 3:30 to 4:30 | **What you rejected.** Two options you did not take, each with the reason and what your choice cost. | your decision log |
| 4:30 to 5:00 | **What is next.** One known limit and what fixing it would take. | your impact note |

A partner runs the simulator from your written card. Rehearse the whole thing once, timed, on
Wednesday.

### Demonstration score sheet (10 points)

| # | The presenter | Points |
|---|---|---|
| 1 | states in one sentence what the panel is, for whom, and that it only watches | 1 |
| 2 | shows normal, alarm, and a failure state live, and the alarm surviving the failure | 3 |
| 3 | gives three design decisions, each tied to evidence shown on screen | 2 |
| 4 | names two rejected options, each with the reason and the cost of the choice made | 3 |
| 5 | answers one question truthfully, including "I don't know" where that is the truth | 1 |
| | **Total** | **10** |

The same sheet is in `project-files/DEMO_SCORE_SHEET.md`, with space for notes.

**Row 4 matters most.** A builder who cannot say what they rejected cannot show they made a decision.
If you cannot explain a choice in your own panel, that is the one way to fail this program outright:
submitting work you cannot explain.

---

## Submission checklist

- [ ] ShipCheck 7 of 7, report pasted into your README
- [ ] Panel header shows the released version; the release folder's stamp matches
- [ ] Rollback tried: the previous release starts and shows its version
- [ ] `v1.0.0` and your release tag pushed by name
- [ ] Implementation plan: eight sections, real commands, real output
- [ ] User guide: by situation, every screen word, four or more pictures of the current release
- [ ] Training record with the check situation result
- [ ] Operator test record: numbered lines, no names, two or more findings, decisions
- [ ] Change request with a prediction committed before the change
- [ ] Change log and impact note agree with the tag
- [ ] Handoff letter, one page, meets requirement 11
- [ ] Demo script and a timed rehearsal
- [ ] Decision log with rejected options, and an AI usage log
- [ ] No person named anywhere; nothing implies the panel controls equipment
- [ ] No `bin`, `obj`, or `release` folders committed
- [ ] Pushed inside the Week 18 Thursday commit window

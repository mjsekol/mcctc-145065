# Project · The HMI PANEL
## 145065 Object-Oriented Programming · Unit 8 · Weeks 15-16

**100 points. Projects category, 35 percent of your grade. Pairs.**
**Demonstration: Week 16, Thursday or Friday, Build 2. Repository due: Week 16, Friday, at the end of the
commit window.**

Riverside Fabrication and its Line 3 are a **composite**: an invented small metal fabrication shop used
all semester. The people and the problems below are invented.

---

## The brief

> From: the Line 3 lead, second shift, Riverside Fabrication
>
> We put sensors on the cure oven, the press, and the coolant tank, and a little computer on the line
> reads them. Right now the only way to see the numbers is to walk over to a laptop and squint. I want a
> screen on the post by the oven exit that my operators can read from where they stand.
>
> My people wear gloves. The lights over that cell bounce off everything. Nobody on my shift is a
> programmer and nobody should have to be.
>
> When something is out of range, I want the screen to say so, loudly, and to keep saying so until
> somebody has actually looked at it. Maintenance and I will argue about where "out of range" starts. I
> want to know why the number is what it is.
>
> Here is what worries me. Last month the little computer froze and nobody noticed for a while, because
> the old numbers sat there looking fine. And carts clip that cable all the time. I do not care how
> the screen looks when everything works as much as I care what it does when things stop working. If it
> does not know something, it has to say it does not know.
>
> One more thing, and I mean it: this screen watches. It does not touch the machines. Ever.

**That is the whole brief.** It does not list requirements. It does not say what "out of range" means,
how old is too old, or what "loudly" looks like. **Turning it into requirements someone can check is the
first thing you are graded on.**

---

## What you are building

A WPF operator panel, in C#, that reads live sensor data from the Line 3 sensor service (the lab Pi, or
the simulator speaking the same contract), shows each sensor as NORMAL, ALARM, STALE, or NO DATA, keeps
every alarm until a person has seen it and the value is back, and never shows an operator a number it
cannot vouch for. With it: the requirements, the hardware needs, a threshold you can defend, a dataflow
diagram, a design review, and a demonstration in which you pull the plug while it runs.

**The panel monitors. It never switches equipment on or off.** The only request it sends is
`GET /api/readings`.

---

## The pieces

You do not start from nothing, and you do not get a finished panel. The starter in
`project-files/HmiPanel/` is a working skeleton built from the course's reference design.

| Piece | Where | Who writes it |
|---|---|---|
| The contract, the reply parser, the thresholds loader, the command line, the clock | `Line3.Hmi.Core/` | given |
| The HTTP client with its timeout and four failure kinds, the polling loop | `Line3.Hmi.Core/SensorClient.cs`, `PollingLoop.cs` | given; you wrote a smaller one in Lab U8-02 |
| The panel's memory: stores results, evaluates each sensor, moves latches, writes events | `Line3.Hmi.Core/PanelMonitor.cs` | given |
| `Decide` and `SensorThreshold.Check` | `StateRules.Truth.cs`, `PanelConfig.cs` | **you**, from Lab U8-03 |
| `CheckFreshness` and the tile's display rules | `StateRules.Freshness.cs`, `SensorTileViewModel.cs` | **you**, from Lab U8-04 |
| The alarm latch and the two-step acknowledge | `AlarmLatch.cs`, three methods in `PanelViewModel.cs` | **you**, from Lab U8-05 |
| **The operator's screen** | `Line3.Hmi.Panel/PanelView.xaml` | **you**, all of it |
| **Your limits, with reasons** | `Line3.Hmi.Panel/thresholds.json` | **your team** |
| The window, startup, the timer, the snapshot harness | `MainWindow`, `App`, `Line3.Hmi.Snapshots/` | given |
| Acceptance tests named for the requirements | `Line3.Hmi.Core.Tests/` | given; you may add more |
| **Every document in `docs/`** | `docs/` | **you** |

The starter's view runs and shows everything, badly on purpose: words only, small text, tiny buttons that
touch. Render it on Monday and list every requirement it fails. That list is your design work.

**If you hand in something shaped like the course's reference panel that you cannot explain, you will be
asked to explain it at the demo.** The only way to fail this program outright is submitting work you
cannot explain. Each partner answers questions alone.

---

## Technical requirements

1. **TR-1.** The solution builds with 0 warnings and 0 errors. Warnings stay errors.
2. **TR-2.** `dotnet test` passes every acceptance test, including `LiveSimulatorTests`.
3. **TR-3.** Each tile shows its state three ways: a word, a shape, and a color. Color alone never
   carries meaning.
4. **TR-4.** A stale value never appears as the big value. It may appear only in its own box, marked not
   live, with its age. A missing value shows no number anywhere.
5. **TR-5.** An alarm survives stale data, missing data, and a pulled cable. Acknowledging opens a
   confirmation that covers the panel; only YES acts; CANCEL and Escape change nothing.
6. **TR-6.** At the 1280 by 800 design size, every button is at least 72 pixels tall, and the two
   confirmation buttons are at least 80 pixels apart.
7. **TR-7.** State text contrast is at least 7:1 against its background. Show your ratios.
8. **TR-8.** Every limit comes from `thresholds.json` with a reason your team wrote. The panel refuses to
   start without one.
9. **TR-9.** The panel sends only `GET /api/readings`. It writes no files and keeps no personal data.
10. **TR-10.** Six PNGs of **your** view, one per scene, rendered by `Line3.Hmi.Snapshots`, are in
    `docs/screens/`, and you have looked at every one.
11. **TR-11.** It runs against the simulator on port 8700 by default, and against the lab Pi with
    `--url` and `--config thresholds.bench.json` [VERIFY on the lab Pi].
12. **TR-12.** No `bin`, `obj`, or `__pycache__` in the repository.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| Monitoring only | Software on this panel never switches equipment. A display with a write path is a hazard. |
| No commercial AI service | This program runs AI on lab hardware only; developer APIs require users to be 18 or older. |
| No personal data anywhere | Lab PCs are shared, and no student or operator data enters any file or tool. |
| Hardware only after the safety brief, with a signed agreement on file, with your instructor present | ESD, power, and wiring hazards. The simulator proves every requirement for grading. |
| No new NuGet packages | The lab's package cache is fixed. Everything you need is already referenced. |
| The contract is fixed | The Pi side and the panel side are built by different people. Change the contract and both break. |
| The design size is 1280 by 800, scaled | Touch targets and proportions stay the same on any screen. |

---

## Required repository structure

```
hmi-panel/
  README.md                    what it is, how to run it, what is not finished
  sensor-service/              copied from 05-labs/sensor-service, unchanged
  HmiPanel/                    the solution from project-files/HmiPanel
    Line3.Hmi.Core/
    Line3.Hmi.Core.Tests/
    Line3.Hmi.Panel/
      PanelView.xaml           your screen
      thresholds.json          your limits and reasons
      thresholds.bench.json
    Line3.Hmi.Snapshots/
    HmiPanel.sln
  docs/
    REQUIREMENTS.md            REQ list with a check for each, constraints, I/O, the workplace
    HARDWARE.md                Pi hardware requirements and the parts and resources list
    THRESHOLDS.md              every limit, its reason, both sides, who agreed
    DATAFLOW.md                the diagram, the I/O table, where each failure is caught
    DESIGN_REVIEW.md           who reviewed, what they asked, what changed
    DEMO_RECORD.md             every demo step, what you saw, the requirement it proves
    decision-log.md            decisions, each naming the pattern chosen and the one rejected
    ai-usage-log.md            every AI tool use, what you kept, what you checked
    screens/                   six PNGs of your view
```

Templates for the first six documents are in `project-files/templates/`. The disconnect demo's script is
`project-files/DISCONNECT_DEMO_RUNBOOK.md`.

**The decision log names a pattern.** This course requires every decision log entry to name the design
pattern you chose and the one you rejected: for example, "commands bound in the view model, rejected
`Click` handlers in code-behind", or "a latch state machine, rejected a Boolean `isAlarm` flag".

---

## DMAIC checkpoints

### Define · Week 15, Monday

Turn the brief into `docs/REQUIREMENTS.md`: at least ten requirements, each with a reason and a check;
the constraints; the inputs and outputs; the operator's workplace at the purpose level, with official
sources marked [VERIFY]. Lab U8-01 gives you `docs/HARDWARE.md`.

### Measure · Week 15, Tuesday and Wednesday

Build and test the starter and record the baseline: how many acceptance tests pass, and which fail.
Measure the simulator: its normal ranges, its drift rate, what each failure mode looks like to your
Lab U8-02 reader. Agree on your limits with evidence (Lab U8-03) and write `docs/THRESHOLDS.md`.

### Analyze · Week 15, Thursday

`docs/DATAFLOW.md`: every layer, the contract on the network arrow, and where each failure is caught
and what it becomes. Render the starter's view and list every requirement it fails. Sketch your screen.

### Improve · Week 15, Friday, through Week 16, Wednesday

Two short sprints, each opened by a two-minute stand-up and closed by a commit.

- **Sprint 1 (Week 15, Friday, to Week 16, Monday):** the design review on Friday; paste in the Lab
  U8-03 and U8-04 pieces; start the view. `docs/DESIGN_REVIEW.md` records every question and what will
  change.
- **Sprint 2 (Week 16, Wednesday):** paste in Lab U8-05; finish the view; render six snapshots; every
  acceptance test green.

Record each stand-up (done, next, blocked) as a line in `README.md` under `## Stand-ups`.

### Control · Week 16, Thursday and Friday

Rehearse the disconnect demo from the run-book and fill `docs/DEMO_RECORD.md`. Demonstrate. Write what
the demo did not prove, for Unit 9.

---

## Milestones

| Milestone | Due | Graded in |
|---|---|---|
| M1 · `REQUIREMENTS.md` draft, `HARDWARE.md` | Week 15 Mon, end of block | Process |
| M2 · `thresholds.json` with your reason, `THRESHOLDS.md`, Lab U8-03 pieces in the project | Week 15 Wed, end of block | Process |
| M3 · `DATAFLOW.md` and a screen sketch | Week 15 Thu, end of Build 1 | Process |
| M4 · design review held, `DESIGN_REVIEW.md` | Week 15 Fri, end of block | Process |
| M5 · every acceptance test passes, six snapshots of your view | Week 16 Wed, end of block | Process |
| M6 · demo rehearsed, `DEMO_RECORD.md` | Week 16 Thu, end of Build 1 | Process |
| **Demonstration** | **Week 16 Thu or Fri, Build 2** | Demonstration |
| **Repository** | **Week 16 Fri, end of the commit window** | all |

The WebXam post-test is Week 16, Tuesday. Plan around it: that day has little build time.

---

## Three worked scope examples

### Small, and completely finished

The starter's view rebuilt to meet TR-3 through TR-7: three tiles with a word, a shape, and a color; the
not-live box; the banner; a full-screen confirmation with big, separated buttons; a status line. The
Line 3 limits with your own oven reason. All documents present and true. The demo on the simulator.

**This earns full marks if it is finished and every document is true.** A finished small panel beats an
unfinished large one every time.

### Medium, and the one most pairs should aim for

Everything in small, plus: the event list on screen; a connection badge whose shape and color change
with the state; limits your team changed from the Line 3 file, with the argument in `THRESHOLDS.md`; the
bench file tested on the lab Pi with your instructor present, including a real alarm from a warmed probe
and the pulled Ethernet cable [VERIFY]; a contrast table for every text color you used.

### Large, and only if both partners were here all of Week 15

Everything in medium, plus one of: a fourth tile for a sensor you add to the **simulator's copy** in your
repository (and to your thresholds, with a reason), with a note in `decision-log.md` about what changing
the contract cost; or a small trend strip showing the last ten live values, never the stale ones; or a
screen-reader pass with every tile announced by its summary. **Nothing in any scope may send a command
to a device.**

### Scope calibration, three signals

- **Too big:** at the end of Week 15, Friday, the design review has not happened, or any acceptance
  test that passed before now fails.
- **Too small:** by Week 16, Monday, the view already meets TR-3 through TR-7 and your plan for the rest
  of the week is "polish".
- **About right:** M5 is done by the end of Week 16, Wednesday, with a day to rehearse.

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

**Functionality, 25.** TR-1 through TR-5 and TR-9: it builds, every acceptance test passes including the
live test, the four states show correctly, and alarms survive a disconnect. The graders also run it
against the simulator and switch modes.

**Code Quality, 20.** Scored on the five-dimension standard: Correctness, Security, Readability,
Performance, Requirements Fit. No `.Result` or `.Wait()`. Nothing in `PanelView.xaml.cs`. Only `GET`.
Comments that agree with the code under them.

**Documentation, 20.** Seven documents, all present, all true, all checkable against the code and the
screens. The requirements each have a check. The thresholds each have both sides argued. The dataflow
shows where each failure is caught.

**Process, 15.** A commit at the end of every period. The milestones on time. The stand-up lines. A
decision log whose entries name the pattern chosen and the pattern rejected. An AI usage log. A design
review that changed something.

**Demonstration, 10.** The five-minute script below, including the disconnect during an alarm and each
partner's answers.

**Polish, 10.** TR-6, TR-7, and TR-10: the screen reads from a few steps away, the buttons suit a
gloved hand, the snapshots are current, and the README says what is not finished.

---

## The five-minute demo script

Five minutes. Timed. You will be stopped. Your instructor runs the simulator's control terminal, or the
lab Pi with you present.

| Minutes | What |
|---|---|
| 0:00 to 0:30 | **The problem, in the Line 3 lead's words.** |
| 0:30 to 1:00 | **Your screen, normal.** Point at one tile and read its three signals: word, shape, color. |
| 1:00 to 1:45 | **Your limit.** Read the oven's reason aloud. Say the strongest case against it. |
| 1:45 to 2:30 | **Drift into alarm.** Read the banner. Press ACKNOWLEDGE, then CANCEL. Say what changed: nothing. |
| 2:30 to 3:15 | **Freeze.** Wait for STALE. Point at the big value: NOT LIVE. Point at the box with the age. |
| 3:15 to 4:15 | **Pull the plug while it is in alarm.** Stop the service (or pull the cable on the Pi). Read the tile and the banner aloud. Then restore, and say what it takes to clear the alarm. |
| 4:15 to 5:00 | **The question.** Your instructor asks each partner one question about code that partner did not write. |

### The ten-point demonstration checklist

1. The problem is stated in the client's terms.
2. A tile's state is read by word, shape, and color.
3. The limit's reason is read, and the case against it is stated.
4. The alarm appears with a banner.
5. CANCEL changes nothing.
6. STALE shows NOT LIVE in the big value.
7. The stale box shows an age.
8. With the service stopped during the alarm, the tile shows no number and the banner stays.
9. Recovery is shown and the clearing rule is stated correctly.
10. Each partner answers a question about the other partner's code.

---

## Safety, again

Read the safety brief in `project-files/DISCONNECT_DEMO_RUNBOOK.md` section 0 aloud before any hardware
step. ESD strap on. Power off before wiring. No mains voltage. Your signed Lab Acceptable Use and Safety
Agreement on file. Your instructor present. **The panel monitors. It never switches equipment on or off.**

## Submission checklist

- [ ] `dotnet build` 0 warnings, 0 errors; `dotnet test` all passed, including the live test
- [ ] `PanelView.xaml` is yours and meets TR-3 through TR-7
- [ ] `thresholds.json` has your team's reasons
- [ ] Seven documents in `docs/`, all true, and six PNGs in `docs/screens/`
- [ ] Decision log entries name the pattern chosen and rejected
- [ ] AI usage log complete
- [ ] Stand-up lines in the README, and a "not finished" section
- [ ] No `bin`, `obj`, or `__pycache__`
- [ ] Pushed before the end of the commit window

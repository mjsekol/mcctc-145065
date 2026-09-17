# Project · The WPF App: A Screen for One Station Job
## 145065 Object-Oriented Programming · Unit 7 · Weeks 13-14

**100 points. Projects category, 35 percent of your grade.**
**Due Week 14, Friday, at the end of the commit window.** BPA Nationals competitors follow the return
plan in the Week 14 lesson plan: due Week 15, Wednesday, at the end of the commit window.

**Gate 3.** Full tooling, AI allowed, AI usage log required, decision log required.

---

## The brief

> From: the Line 3 supervisor at Riverside Fabrication
>
> Half the jobs at my stations still live on paper. Somebody writes on a clipboard, somebody else
> copies it into a spreadsheet at the end of the week, and by then half of it is wrong or smudged.
>
> Pick one of those jobs and give me a screen for it. Something an operator can use with gloves on,
> standing up, without reading a manual. I care about three things: it shows the right number the
> moment something changes, it never locks up on them, and nobody can wipe out a shift's work by
> accident.
>
> Don't connect it to anything yet. No network, no machines. I want to see whether a screen beats
> the clipboard.
>
> Jobs I have in mind, if you need one: tracking when a machine is down and why; the changeover
> checklist when a press gets a new die; recording the first-piece inspection at the start of a run.
> If you know a better one, pitch it.
>
> Show me it working before the end of next week.

Riverside Fabrication is a **composite**, the invented shop you use all semester. You may choose a job
from somewhere you know, such as a club, a team, or a family business, if you record it in your
decision log. **No real person's information goes in your app, your tests, or your screenshots.
Invented names only.**

**That is the whole brief.** It does not say which controls, how many screens, or what "the right
number" means for your job. Turning it into requirements is the first thing you are graded on.

---

## What you are building

| # | Piece | Form |
|---|---|---|
| 1 | The app | a WPF app in three projects: the window, a view model library, and its tests |
| 2 | An event flow diagram | `docs/event-flow.md`, from `project-files/EVENT_FLOW_TEMPLATE.md` |
| 3 | A requirements list | `docs/requirements.md`: numbered, each marked "stated by the client" or "my assumption" |
| 4 | A decision log | `decision-log.md` entries, each naming the option chosen and the option rejected |
| 5 | A README | what it does, how to build, run, and test it, and a picture of the window |
| 6 | An AI usage log | every AI use: what you asked, what you kept, what you checked |

---

## Technical requirements

1. **Three projects.** The window targets `net8.0-windows` with WPF. The view model is a class library
   that targets plain `net8.0`. The tests are an xunit project that references the library.
2. **At least four interactive controls, of at least three different kinds**: for example `Button`,
   `TextBox`, `ComboBox`, `Slider`, `CheckBox`, `RadioButton`, `ListBox`.
3. **Working data binding.** Every value the window shows that can change comes from a view model
   property through `{Binding}`. At least one binding writes back from a control.
4. **Change notification.** The view model implements `INotifyPropertyChanged`, uses `nameof`, and
   announces every property computed from a changed value.
5. **Handlers stay thin.** At least one `Click` handler (or command). Each handler calls the view model,
   and anything else it does is window-only work: asking a person, or talking to a device.
6. **Nothing wipes work by accident.** Every destructive action asks first, through a replaceable
   `Confirm` function like the labs', with No as the default.
7. **Nothing locks up.** No handler waits on anything slow. If your app has slow work, it is awaited.
8. **Built for gloves.** Every button is at least 64 pixels tall, text is at least 18 points, and state
   is shown in words, never by color alone.
9. **Tests.** At least eight passing xunit tests on the view model, including at least one that proves
   a computed property is announced when its source changes.
10. **The event flow diagram** lists every event your app handles and includes one sequence for its
    most important action.
11. **A picture of the window** in the README: a screenshot of the running app, or a picture saved by a
    render check like the labs'.
12. **It builds with no warnings.** Keep `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in the
    window and library projects.

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| No network, no hardware | Unit 8 adds the Raspberry Pi. This unit proves the screen first. |
| The view model has no WPF in it | So every rule has a test that runs without a window. |
| No personal data anywhere | Program rule. Invented names, badge numbers, and records only. |
| AI models are local or not used | Program rule. Commercial AI accounts require users to be 18 or older. |
| Only the NuGet packages the labs use | The lab machines have those. Anything else needs your teacher's approval first. |
| No `bin/` or `obj/` in any commit | Build output belongs to one machine. `dotnet new gitignore` handles it. |

---

## Required repository structure

```
oop-semester/
  decision-log.md
  unit-07-wpf-app/
    README.md
    <App>.sln
    <App>/                  net8.0-windows WPF project
    <App>.Core/             net8.0 view model library
    <App>.Core.Tests/       xunit tests
    docs/
      requirements.md
      event-flow.md
      window.png
    ai-usage-log.md
```

Create the projects from the unit folder:

```
dotnet new wpf -n <App> --framework net8.0
dotnet new classlib -n <App>.Core --framework net8.0
dotnet new xunit -n <App>.Core.Tests --framework net8.0
dotnet add <App> reference <App>.Core
dotnet add <App>.Core.Tests reference <App>.Core
dotnet new sln -n <App> --format sln
dotnet sln add <App> <App>.Core <App>.Core.Tests
```

On the build machine these commands made three projects that built with no warnings, and the test
project's one sample test passed. `--format sln` makes the classic solution file the labs use; without
it, newer SDKs make a `.slnx` file instead. The `net8.0` xunit template already used the labs' package
versions: `xunit` and `xunit.runner.visualstudio` 2.5.3, `Microsoft.NET.Test.Sdk` 17.8.0, and
`coverlet.collector` 6.0.0 [VERIFY on the lab image]. Delete the sample test when you write your own,
and add `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` to the window and library projects.

---

## DMAIC checkpoints

### Define · Week 13, Thursday, last 15 minutes of Build 2

Choose the job. **Checkpoint:** a decision log entry naming the job you chose and one you rejected,
and one sentence on who uses the screen.

### Measure · Week 13, Friday, Build 2

Turn the brief into numbers and requirements. **Checkpoint:** `docs/requirements.md` with at least six
numbered requirements, each marked stated or assumed; a list of every input the operator gives and
every output the screen shows; and a sketch of the window, on paper or in XAML, naming at least four
interactive controls.

### Analyze · Week 14, Monday, Build 2

Design the view model. **Checkpoint:** the library builds, with a property for each output and a
method for each action, and at least four tests pass. Write the dependency table for your view model:
for each value, what else must be announced when it changes.

### Improve · Week 14, Monday to Thursday

This is the sprint. Each day starts with the stand-up question from the lesson plan: what the app does
today, what it will do next, and what is in the way.

- **Tuesday, Build 2:** the window, bound to the view model.
- **Wednesday, Build 2:** notifications, and the test that proves one.
- **Thursday, Build 2:** `docs/event-flow.md`, and the desk demo if you are ready.

### Control · Week 14, Friday, commit window

**Checkpoint:** the build has no warnings, every test passes, the README says how someone else builds,
runs, and tests it, the picture is in `docs/`, and everything is committed and pushed.

---

## Milestones

| # | Milestone | Due | Finished when |
|---|---|---|---|
| M1 | Job chosen | Week 13 Thu, end of Build 2 | the decision log entry is committed |
| M2 | Requirements and sketch | Week 13 Fri, end of Build 2 | `docs/requirements.md` and the sketch are committed |
| M3 | View model and four tests | Week 14 Mon, end of Build 2 | the library builds and four tests pass |
| M4 | Bound window | Week 14 Tue, end of Build 2 | every value on screen comes through a binding |
| M5 | Notifications and the event flow diagram | Week 14 Thu, end of block | a notification test passes and `docs/event-flow.md` is committed |
| **Due** | **Everything** | **Week 14 Fri, commit window** | the submission checklist, every item |

---

## Three worked scope examples

All three can earn full marks. They differ in ambition, not quality.

### Small, and completely finished

**Job:** the changeover checklist. **Controls:** six `CheckBox` steps, a `TextBox` for the die number,
a `Button` that marks the changeover complete (enabled only when every step is checked), and a
`Button` that starts over, which asks first. **View model:** the steps, the die number, a
`StepsDoneText` like `4 of 6 steps done`, and `CanComplete`.

**What makes it full marks:** every check box bound, `StepsDoneText` announced whenever any step
changes, eight tests, and a clear event flow diagram.

**The risk:** you can forget that six different properties feed one computed value. That is the
test to write first.

### Medium, and the one most students should aim for

**Job:** the downtime log. **Controls:** a machine `ComboBox`, STOPPED and RUNNING `Button`s, a reason
`ComboBox`, a note `TextBox`, a `ListBox` of the shift's stops, and a CLEAR SHIFT `Button` that asks
first. A one-second `DispatcherTimer` keeps an open stop's minutes counting.

**What it adds:** time. The view model takes the clock as a parameter, so a test can move time
forward. The timer is a second kind of event, and the diagram shows it.

**The risk:** reading `DateTime.Now` inside the view model makes the minutes untestable. Pass the
clock in.

### Large, and only if the medium version is working by Wednesday

**Job:** the downtime log, plus saving the shift to a JSON file and loading it at startup (the Unit 3
skills), plus commands and keyboard shortcuts (the Lab U07-03 EXTENDED option).

**What it adds:** the app survives being closed, and every save and load has a round-trip test.

**The risk:** a file that fails to load. Decide what the screen shows when it does, write that in the
decision log, and test it.

### Scope calibration

| If you | Aim for |
|---|---|
| finished Lab U07-02 late, or are away for BPA Nationals | Small |
| had 18 of 18 on Lab U07-02 on Thursday | Medium |
| had Lab U07-03 at full marks by Wednesday Build 1 | Large |

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

**Functionality, 25.** The app does the job for the operator. Every control works. Every value on
screen is right the moment something changes. Destructive actions ask first. Nothing freezes. The
build has no warnings, and every test passes.

**Code Quality, 20.** Scored on the five-dimension standard: Correctness (the rules are right and
tested), Security (no data lost by accident, no personal data), Readability (handlers named for what
they handle, `nameof` everywhere, no logic in the code-behind), Performance (nothing slow on the UI
thread, nothing announced that did not change), Requirements Fit (every technical requirement above).

**Documentation, 20.** The requirements list separates what the client said from what you assumed.
The event flow diagram is complete and matches the code. The README lets someone else build, run, and
test the app.

**Process, 15.** The five milestones on time. A decision log with real decisions, each naming the
rejected option. An AI usage log that says what you checked. A commit at the end of every period.

**Demonstration, 10.** The five-minute desk demo below.

**Polish, 10.** It looks like an operator screen: big targets, readable text, words for every state,
nothing cut off. Starter comments and template text removed.

---

## The five-minute desk demo

Your instructor comes to your desk during Week 14, Thursday or Friday, Build 2. Anyone not reached
demos in Week 15, Monday, in the first ten minutes of Build 1. Five minutes, timed.

| Time | What |
|---|---|
| 0:00 to 0:45 | The job, and the operator who does it, in two sentences |
| 0:45 to 2:00 | Use the app as that operator would, start to finish |
| 2:00 to 2:45 | Your instructor presses a destructive button. Show the question, then cancel. |
| 2:45 to 3:45 | Your instructor names a value on screen. Change what it depends on and show it update. Then show the test that proves it is announced. |
| 3:45 to 4:30 | Point at one event in your diagram and at the code that handles it |
| 4:30 to 5:00 | One thing you chose not to build, and why |

### The demonstration checklist

| # | | Points |
|---|---|---|
| 1 | The job and the operator stated clearly | 1 |
| 2 | A full use of the app, with no freeze and no wrong value | 2 |
| 3 | The destructive action asks, and No keeps the work | 2 |
| 4 | The chosen value updates, and its announcement test is shown | 3 |
| 5 | A diagram row matched to its code | 1 |
| 6 | A rejected feature, with the reason | 1 |
| | **Total** | **10** |

Item 4 is the one that matters most. If you cannot show why a value on your screen is right, that is
the one way to fail this program outright: submitting work you cannot explain.

---

## Submission checklist

- [ ] `dotnet build` reports 0 warnings and 0 errors
- [ ] `dotnet test` passes, with at least eight tests, one of them about an announcement
- [ ] At least four interactive controls of at least three kinds
- [ ] Every changing value on screen comes through a binding
- [ ] Every destructive action asks first, with No as the default
- [ ] Every button at least 64 pixels tall; every state shown in words
- [ ] `docs/requirements.md`, `docs/event-flow.md`, and `docs/window.png` committed
- [ ] README: what it does, how to build, run, and test it
- [ ] Decision log: the job chosen and rejected, plus at least two more decisions
- [ ] AI usage log complete
- [ ] No personal information anywhere; no `bin/` or `obj/` committed
- [ ] Pushed inside the Week 14, Friday commit window

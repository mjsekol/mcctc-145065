# Additional Resources · Week 14
## 145065 Object-Oriented Programming · Unit 7 · Week 14
### Topic: data binding, INotifyPropertyChanged, view models, unit tests, and commands

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**About .NET versions.** Microsoft Learn shows the newest .NET by default. The lab targets .NET 8
(`net8.0-windows` for the app, `net8.0` for the view model library). Everything this week covers
works the same way in .NET 8.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Data binding overview, selected sections | On-level | 40 min |
| 2 | How to: Implement Property Change Notification | On-level | 10 min |
| 3 | API reference: `INotifyPropertyChanged`, `ObservableCollection<T>`, `BooleanToVisibilityConverter` | On-level | 20 min |
| 4 | Tutorial: Unit testing C# with dotnet test and xUnit | On-level | 35 min |
| 5 | Video: "XAML Data Binding and MVVM Basics" | On-level | under 20 min, [VERIFY] length |
| 6 | Commands and the MVVM Toolkit | Extension | 20 min |
| 7 | Industry connection: the article slot | On-level | 15 min |
| 8 | For BPA National Leadership Conference competitors | Extension | self-paced |
| 9 | Teacher note: keyboard and screen reader check | On-level | 10 min |
| 10 | Side quest: SQ-17, or SQ-16 | Extension | one to two blocks |

---

## 1. Primary reading

**Microsoft Learn, "Data binding overview"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/` · **Opened.**

**What it is.** The official explanation of WPF data binding: what a binding target and a binding
source are, which way data flows, and when the source gets updated.

**Why this one.** Last week your ShiftTally handlers set `GoodText.Text` by hand. This week the label
updates itself. This page explains how, in the words of the people who built it.

**Read these sections:**

- "What is data binding?"
- "Basic data binding concepts", including "Data context", "Direction of the data flow", and "What
  triggers source updates"
- "Create a binding"
- "Data conversion"
- "Binding to collections", only the part titled "How to implement collections"

**Failure mode to know before Tuesday.** The "What triggers source updates" section says
`TextBox.Text` defaults to updating its source when the box loses focus, not on every keystroke. If
your station name does not reach the view model while you type, this is why. Setting
`UpdateSourceTrigger=PropertyChanged` changes it.

**Time.** 40 minutes. **Level.** On-level. The sections on collection views, data templating, and
validation are extension.

---

## 2. Short reading: the notification pattern

**Microsoft Learn, "How to: Implement Property Change Notification"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/how-to-implement-property-change-notification`
· **Opened.**

**What it is.** A one-page example of a class that implements `INotifyPropertyChanged` with an
`OnPropertyChanged` method and `[CallerMemberName]`.

**Why this one.** It is the shortest correct version of Wednesday's pattern.

**Read it critically.** The example's setter raises `PropertyChanged` every time, even when the new
value equals the old one. The API reference example in section 3 checks for a change first. Decide
which your view model should do, and write one sentence in your decision log saying why. This is a
good Gate 2 habit: official samples are teaching code, not always production code.

**Time.** 10 minutes. **Level.** On-level.

---

## 3. Official documentation

**.NET API reference, `INotifyPropertyChanged` interface (System.ComponentModel)** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.inotifypropertychanged` ·
**Opened.**

**What it is.** The reference page for the interface. It has one member, the `PropertyChanged`
event. The Remarks say a bound type should either implement this interface, which the page calls
preferred, or provide a change event for each property, and not do both.

**Know this before you assign it.** The page's full example is a Windows Forms app with a
`DataGridView`, not WPF. The `DemoCustomer` class inside it is the part that transfers. Tell
students to skip the form code.

**.NET API reference, `ObservableCollection<T>` class** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.collections.objectmodel.observablecollection-1`
· **Opened.** The page describes it as a collection that sends notifications when items are added or
removed, or when the whole list is refreshed. That is why a list on screen that grows during a
shift, such as a list of machine stops, uses it instead of `List<T>`.

**.NET API reference, `BooleanToVisibilityConverter` class** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.windows.controls.booleantovisibilityconverter`
· **Opened.** The Remarks say `true` becomes `Visible` and `false` becomes `Collapsed`, and that
`Collapsed` reserves no space in the layout. Know that before your scrap rate line makes the rest
of the screen jump.

**Give students one question to answer from the pages, not the pages:** "Which of these three types
needs WPF, and which two can a plain `net8.0` view model library use?" The answer comes from the
Assembly line at the top of each page. `BooleanToVisibilityConverter` lives in PresentationFramework,
which is WPF, so it belongs in the app project, not the library.

**Time.** 20 minutes. **Level.** On-level.

---

## 4. Hands-on practice: testing a plain library

**Microsoft Learn, "Unit testing C# code in .NET using dotnet test and xUnit"** ·
`https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-xunit` · **Opened.**

**What it is.** A tutorial that builds a solution with a class library and an xUnit test project from
the dotnet CLI. It covers `dotnet new classlib`, `dotnet new xunit`, adding a project reference,
`[Fact]`, `[Theory]`, `[InlineData]`, and `dotnet test`.

**Why this one.** It is the same shape as this week's build. Your view model lives in a plain class
library so a test project can reference it without opening a window. Work the tutorial once with its
prime number example. Then repeat the steps with your ShiftTally view model as the library.

**One failure mode to expect.** The tutorial follows test-driven development, so its first test is
supposed to fail. A red result on the first run is the tutorial working, not your machine breaking.

**Time.** 35 minutes. **Level.** On-level.

---

## 5. Video, under 20 minutes

**James Montemagno, "XAML Data Binding and MVVM Basics (.NET MAUI, WPF, UWP, Xamarin.Forms)"** ·
`https://www.youtube.com/watch?v=sAn4RVsroF4` · **Opened** for the title and channel name.
**[VERIFY]** the running time is under 20 minutes before assigning it. The page's length did not
load when this file was written.

**What it is.** A video on the channel of James Montemagno about data binding and the MVVM pattern
across several XAML frameworks, WPF among them.

**Why this one.** It shows the view, view model, and binding relationship moving on screen, which is
hard to get from reading. The title names WPF, but it covers several frameworks. Watch for the ideas,
not for exact syntax. Where the video and this week's notes differ, the notes win.

**Level.** On-level. Watch before class, not during it. YouTube may be blocked on the school network.

**Backup hosted on Microsoft Learn.** ".NET MAUI Data Binding with MVVM & XAML [5 of 8]" ·
`https://learn.microsoft.com/en-us/shows/dotnet-maui-for-beginners/dotnet-maui-data-binding-with-mvvm-xaml-5-of-8-dotnet-maui-for-beginners`
· **Opened** for the title and description. **[VERIFY]** the length. The description says it
introduces MVVM and uses the .NET Community Toolkit. It is about .NET MAUI, not WPF, so the binding
ideas transfer but some syntax does not.

---

## 6. Extension: commands and the MVVM Toolkit

**.NET API reference, `ICommand` interface (System.Windows.Input)** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.windows.input.icommand` · **Opened.**

**What it is.** The reference page for the command interface. It lists two methods, `CanExecute` and
`Execute`, and one event, `CanExecuteChanged`.

**Why this one.** A command moves a button's work, such as ShiftTally's +1 GOOD, out of code-behind
and into the view model, where a test can reach it. `CanExecute` is how a button greys itself out
when its action is not allowed, such as UNDO LAST with nothing to undo. That is a fail-safe default
an operator can see. Lab U07-03's EXTENDED option builds exactly this.

**Microsoft Learn, "Introduction to the MVVM Toolkit"** ·
`https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/` · **Opened.**

**What it is.** The documentation for the `CommunityToolkit.Mvvm` package. The page says Microsoft
maintains it, it is part of the .NET Foundation, and it works with WPF. It includes
`ObservableObject` and `RelayCommand`.

**Why this one.** Professional teams rarely hand-write `OnPropertyChanged` in every class. They use a
library like this.

**The honest tradeoff.** Writing the pattern by hand this week is more verbose. It also means you know
what the library generates when something breaks. Build it by hand first. Do not add the package to
a lab project without your teacher's approval.

**Time.** 20 minutes. **Level.** Extension.

---

## 7. Industry connection

### The current article slot

**Deliberately unfilled.** This file found no current, free article about data-driven operator screens
that could be opened and trusted while it was written. Pick one current piece from ISA, a government
agency such as NIST, or a well-known trade publication the week you teach this. Look for one that
shows an operator screen updating from live machine data, which is the job binding does in ShiftTally.
**[VERIFY]** whatever you choose, and check that it is free to read.

The ISA-101 page listed in the Week 13 resources file,
`https://www.isa.org/standards-and-publications/isa-standards/isa-101-standards` (**Opened**), still
applies. Use it to remind students that operator screen design has a published standard. The standard
itself is sold, so do not assign it.

**Time.** 15 minutes. **Level.** On-level.

---

## 8. For BPA National Leadership Conference competitors

The National Leadership Conference usually falls in Week 14. **Confirm this year's date** before you
plan around it.

**Business Professionals of America** · `https://www.bpa.org` · **Opened.**

**What it is.** The organization's home page. The page describes BPA as a Career and Technical Student
Organization.

**How to prepare for event 330, C# Programming.** Get the current event guidelines from the BPA site
through your chapter advisor. Do not rely on last year's copy. Then study from this unit's own
materials:

- Gate 1 rep prompts from Weeks 11-14, which your teacher can print, done in a plain editor under time
- the `Dispatcher` reference page from the Week 13 resources file and the `INotifyPropertyChanged`
  page above
- the xUnit tutorial in section 4, so you can prove your code works before a judge asks
- the Tour of C# listed in the Week 13 resources file, for fast syntax review

**Time.** Self-paced. **Level.** Extension. Competitors who travel miss class time. Collect the Week 14
packet before you leave, and follow the return plan your teacher confirms with you.

---

## 9. Teacher note: a keyboard and screen reader check

This is not a side quest. It is a five-minute check to run on Thursday or Friday.

Ask each student to unplug the mouse and run ShiftTally with the keyboard only. Can they reach every
button with Tab? Is the order sensible? Then turn on Narrator, the screen reader built into Windows,
and listen to what it announces for the counts and the status line. A label that Narrator reads as
nothing useful is a defect. An operator wearing gloves, or one who cannot see the screen well, meets
the same problem.

**Time.** 10 minutes. **Level.** On-level.

---

## 10. Side quest

**SQ-17 · Unit Tests for Something You Already Wrote** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**Why this one.** This week you test a view model you wrote today. This quest asks you to test code
you wrote weeks ago, which is harder and more honest. Your Week 12 C# port is a good target. The
catalog's rule applies: at least one test must fail and expose a real defect you did not know about,
and you fix it. If nothing fails, write nastier tests.

**Time.** One to two blocks. **Level.** Extension.

**Alternative: SQ-16 · The Class That Should Not Be a Class** · same catalog.

**Why this one.** A view model is a class that exists so a window can bind to it. Ask whether every
class in your project earns its place the same way. The catalog asks you to find a class that should
have been a function, rewrite it both ways, and argue both sides in writing. There is no correct
answer and the argument is the grade.

**Time.** One block. **Level.** Extension.

# Additional Resources · Week 13
## 145065 Object-Oriented Programming · Unit 7 · Week 13
### Topic: event-driven programming, XAML, layout panels, event handlers, and the UI thread

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**About .NET versions.** Microsoft Learn shows the newest .NET by default. The lab targets .NET 8
(`net8.0-windows`). Everything this week covers works the same way in .NET 8. When a tutorial tells
you to pick a newer framework, pick .NET 8 instead so your project matches the lab.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | WPF overview and XAML language overview | On-level | 35 min |
| 2 | Threading Model and Routed events overview | On-level | 40 min |
| 3 | Tutorial: Create a WPF app with Visual Studio | On-level | 30 min |
| 4 | API reference: `Dispatcher` class | On-level | 15 min |
| 5 | Video: "Introduction To Async, Await, And Tasks" | On-level | [VERIFY] length |
| 6 | Asynchronous programming, the breakfast article | Extension | 25 min |
| 7 | C# review: Tour of C# and Get started with C# | Remediation | 20 to 40 min |
| 8 | Industry connection: ISA-101 and the article slot | On-level | 15 min |
| 9 | Side quest: SQ-15 | Extension | two blocks |

---

## 1. Primary reading

**Microsoft Learn, "What is Windows Presentation Foundation"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/overview/` · **Opened.**

**What it is.** The official overview of WPF for .NET. It says WPF runs only on Windows, and that
XAML defines how an app looks while code-behind defines how it behaves.

**Why this one.** Monday's question is how a program that waits for clicks differs from a program
that runs top to bottom. This page shows the whole shape in one place: a window in XAML, a `Click`
handler in C#, and the `InitializeComponent` call that joins them.

**Read these sections:** "Program with WPF", "Markup and code-behind", and "Layout". The Layout
section names `Grid`, `StackPanel`, and `DockPanel`, three of Tuesday's four panels. `UniformGrid` is
not in that list. Find it in the API reference if you want it early.

**Microsoft Learn, "XAML language overview"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/xaml/` · **Opened.**

**What it is.** The official explanation of XAML syntax as WPF uses it.

**Why this one.** It states the idea behind Tuesday: each XAML object element creates an instance
of a real class. Your ShiftTally window is a tree of objects, not a picture.

**Read these sections:** "XAML syntax in brief", "Named elements", and "Events and XAML
code-behind". Named elements is where `x:Name` turns a XAML element into a field you can use in C#.

**Time.** 35 minutes for both. **Level.** On-level.

---

## 2. Reading for Thursday and Friday: the UI thread and event routing

**Microsoft Learn, "Threading Model"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model` · **Opened.**

**What it is.** The official explanation of the WPF UI thread and the dispatcher.

**Why this one.** This is the hardest idea of the week. A handler that blocks freezes the whole
window, and an operator on Line 3 sees a screen that stopped counting parts. This page explains why.

**Read these sections:** "Overview and the dispatcher", "Single-threaded app with a long-running
calculation", and "Handle a blocking operation with Task.Run". Skip "Multiple windows, multiple
threads" and "Technical details and stumbling points" unless you are reading for extension.

**Microsoft Learn, "Routed events overview"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/events/routed-events-overview` · **Opened.**

**What it is.** The official explanation of how an event such as `Button.Click` travels through the
element tree.

**Why this one.** It settles a question students ask on Wednesday: what is the difference between
`sender` and `e.Source`? The page says `Source` is the element that raised the event and `sender`
is the element whose handler is running. They are the same object only when you handle the event
on the element that raised it.

**Read these sections:** "What is a routed event?" and "The concept of handled".

**Time.** 40 minutes for both. **Level.** On-level. The rest of the routed events page is extension.

---

## 3. Hands-on practice

There is no free in-browser simulator for WPF. The practice is a guided tutorial you run on the lab
machine in Visual Studio 2026.

**Microsoft Learn, "Create a WPF app with Visual Studio tutorial"** ·
`https://learn.microsoft.com/en-us/dotnet/desktop/wpf/get-started/create-app-visual-studio` ·
**Opened.**

**What it is.** A step-by-step tutorial that builds a small app which adds names to a list box. It
uses a `Grid` with row and column definitions, a `StackPanel`, `x:Name`, and a `Click` handler.

**Why this one.** It rehearses every Tuesday and Wednesday skill on a program with no stakes. The
page tells you to select .NET 10 in the Framework box. Choose .NET 8 on the lab machines. If .NET 8
is not in the list, tell your teacher before you continue.

**One failure mode to expect.** The tutorial's app adds names typed by the user. Type part names
such as "bracket" or "hinge". Do not type classmates' names into anything you build.

**Second option.** Visual Studio's own tutorial, "Hello World app with WPF in C#" ·
`https://learn.microsoft.com/en-us/visualstudio/get-started/csharp/tutorial-wpf?view=visualstudio`
· **Opened.** Its last section opens the **Live Visual Tree** window on a running app. That window
shows you Tuesday's point: the window really is a tree of objects.

**Time.** 30 minutes. **Level.** On-level. Remediation for anyone whose Wednesday handler did not
build.

---

## 4. Official documentation

**.NET API reference, `Dispatcher` class (System.Windows.Threading)** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.windows.threading.dispatcher` · **Opened.**

**What it is.** The reference page for the class that holds the UI thread's queue of work. The page
lists .NET for Windows desktop 8.0 among the versions it applies to.

**Why this one.** The Remarks section says it plainly: a background thread cannot update a `Button`
that belongs to the UI thread. It must hand the work to the dispatcher. The Methods table shows
`Invoke`, `BeginInvoke`, and `InvokeAsync`.

**Give students one question to answer from the page, not the page:** "What does the page say is
the difference between `Invoke` and `BeginInvoke`?" The Remarks answer it: `Invoke` is synchronous
and `BeginInvoke` is asynchronous.

**Time.** 15 minutes. **Level.** On-level.

---

## 5. Video, under 20 minutes

**Microsoft Learn Shows, "Introduction To Async, Await, And Tasks | C# Advanced [5 of 8]"** ·
`https://learn.microsoft.com/en-us/shows/c-advanced/introduction-to-async-await-and-tasks--c-advanced-5-of-8`
· **Opened** for the title and description. **[VERIFY]** the running time is under 20 minutes
before assigning it. The page's length did not load when this file was written.

**What it is.** An episode of Microsoft's C# Advanced video series. Its description says it shows
how well-written async code reads like a sequence of operations while the compiler handles the
asynchronous execution.

**Why this one.** Thursday's fix for a frozen window is `async` and `await` in the event handler. This
video explains the keywords before you use them. It is not about WPF, so you supply the connection:
a handler that awaits gives the UI thread back to the dispatcher while it waits.

**Level.** On-level. Watch before class, not during it. The video is hosted on Microsoft Learn
rather than YouTube, which may help if YouTube is blocked on the school network. Check that it plays
on a student account first.

---

## 6. Extension reading: asynchronous programming

**Microsoft Learn, "Asynchronous programming"** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/` · **Opened.**

**What it is.** The official C# article that teaches `async` and `await` with a breakfast example:
coffee, eggs, hash browns, and toast.

**Why this one.** The section "Don't block, await instead" compares blocking code to staring at the
toaster while ignoring everything else in the kitchen. That is exactly what a blocking `Click`
handler does to your window. The article also says client apps should stay responsive to user input
and should not freeze while data downloads.

**Time.** 25 minutes. **Level.** Extension. The examples are console programs, not WPF.

---

## 7. C# review, for anyone still shaky from Weeks 11-12

**Microsoft Learn, "Interactive tutorials: A tour of C#"** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/tutorials/` · **Opened.**

**What it is.** A short sequence of lessons: Hello world, numbers, tuples and types, branches and
loops, the List collection, and pattern matching. The page says a student coming from another
language can skim the first two lessons.

**Know this before you assign it.** The page says the lessons run in GitHub Codespaces or with the
.NET SDK installed. Use the SDK on the lab machine. The page also says the lessons use file-based
apps, a newer SDK feature. **[VERIFY]** that the lab SDK runs them, or have students paste each
snippet into a console project.

**Microsoft Learn training path, "Write your first code using C# (Get started with C#, Part 1)"** ·
`https://learn.microsoft.com/en-us/training/paths/get-started-c-sharp-part-1/` · **Opened.**

**What it is.** A six-module beginner path covering syntax, variables, string formatting, and basic
operations, with two guided projects. Do not have students create accounts to use it. Check that
the module pages open without signing in.

**Time.** 20 to 40 minutes. **Level.** Remediation only. Do not assign it to the whole class.

---

## 8. Industry connection: operator panels

**What professionals use.** Process plants design operator screens against a published standard.
The best known in North America is ISA-101.

**ISA, "ISA-101 Series of Standards"** ·
`https://www.isa.org/standards-and-publications/isa-standards/isa-101-standards` · **Opened.**

**What the page says.** ISA-101 guides how HMIs are designed, implemented, operated, and maintained
in process automation, with attention to safety, usability, efficiency, and operator training. The
page says it applies to continuous, batch, and discrete industries.

**What the page does not give you.** The standard itself is sold. The page says ISA members can view
it and others must buy it or join. Do not buy it for this unit. Use the page only to show students
that operator screen design is a professional discipline with its own standard.

**Discussion prompt for Monday.** A consumer app wants you to keep scrolling. An operator panel wants
you to notice one thing fast and act. Name one design choice that follows from each goal.

### The current article slot

**Deliberately unfilled.** This file found no current, free article about operator panel design that
could be opened and trusted while it was written. An ISA InTech magazine article about ISA-101
appeared in a search, but it seemed to require a login, so it is not listed here. Pick one current
piece from ISA, a government agency such as NIST, or a well-known trade publication the week you
teach this. Use it on Monday as a real-world example of event-driven software on a shop floor.
**[VERIFY]** whatever you choose, and check that it is free to read.

**Time.** 15 minutes. **Level.** On-level.

---

## 9. Side quest

**SQ-15 · Same Program, Two Languages** · from
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**Why this one.** Monday compares a program that runs top to bottom with one that waits for events.
This quest makes you feel that difference. Take one of your Python programs from last semester and
rewrite it in C#. Same behavior, same output. If you pick a program that asks questions in a loop,
your README has a ready-made section: what changes when the loop becomes a window that waits.

**Done when** (from the catalog): both versions produce identical output on the same inputs, and your
README says what was harder in each language and what each one made obvious.

**Time.** Two blocks. **Level.** Extension.

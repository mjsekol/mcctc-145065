# Lecture Notes: The Build Output Is a Review
## 145065 Object-Oriented Programming · Unit 6 · Week 12, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W12_BuildAsReviewer.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W12_BuildAsReviewer.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competencies:** 5.6.13 perform code reviews (peer walkthrough, static analysis) · 5.7.1 explain
version management and interface control · 5.7.3 analyze the impact of changes.

Every output and error below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python
outputs are from Python 3.13.7.

---

## Why this exists

All week, the build has told you more than "passed" or "failed." Yellow warnings scrolled past, and
the program ran anyway. Today you find out what those warnings were trying to say, why teams turn
them into errors, and how to read an error list after a change as a map of everything the change
touched.

This is also the half of configuration management that the exam asks about: when you change a
contract other code depends on, who breaks, and how do you know before you ship?

---

## The concept in plain language

**A warning is static analysis.** The compiler studied your code without running it, found
something suspicious, and built the program anyway. Static analysis is a code review done by a
program.

**`TreatWarningsAsErrors` is a team decision** that a warning stops the build. It lives in the
project file:

```xml
<TreatWarningsAsErrors>true</TreatWarningsAsErrors>
```

**Silencing is not fixing.** The null-forgiving operator `!` and `#pragma warning disable` make a
warning disappear. Neither changes what the program does.

**An error list after an interface change is an impact analysis.** Every class that promised the
interface and no longer keeps the promise is listed, in every folder, before anything runs.
Controlling that list, deciding which changes are allowed and when, is interface control.

---

## Worked example 1: a warning, then the same warning as an error

```csharp
string? badge = FindBadge("L3-PRS-02");
Console.WriteLine(badge.ToUpper());

static string? FindBadge(string tag) => tag == "L3-PRS-01" ? "tech-07" : null;
```

`string?` says the value may be null. With the default project settings:

```
w12thu_a_nullable_warning.cs(4,19): warning CS8602: Dereference of a possibly null reference.
```

The build succeeds. The program runs and throws:

```
Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.
```

The same file, with `TreatWarningsAsErrors` on:

```
w12thu_b_same_as_error.cs(4,19): error CS8602: Dereference of a possibly null reference.
```

Nothing runs. The crash was found at the desk.

Python, for the same mistake, raises
`AttributeError: 'NoneType' object has no attribute 'upper'` on the day the press is not locked
out.

The fix decides what "no badge" means:

```csharp
Console.WriteLine(badge is null ? "not locked out" : badge.ToUpper());
```

It builds with warnings as errors, 0 warnings, and prints `not locked out`.

---

## Worked example 2: warnings that point at code nobody needs

```csharp
int alarms = 0;
double limit = 240;
return;
Console.WriteLine(alarms);

static int Unused()
{
    int spare;
    return 1;
}
```

```
w12thu_f_unused_and_unreachable.cs(5,1): warning CS0162: Unreachable code detected
w12thu_f_unused_and_unreachable.cs(9,9): warning CS0168: The variable 'spare' is declared but never used
w12thu_f_unused_and_unreachable.cs(3,8): warning CS0219: The variable 'limit' is assigned but its value is never used
w12thu_f_unused_and_unreachable.cs(7,12): warning CS8321: The local function 'Unused' is declared but never used
```

None of these crash. Each one is a reviewer asking a question: why is this here? A `limit` that is
set and never read is often a threshold somebody forgot to use.

---

## Worked example 3: the impact list

Three classes implement `IReadingSource`. One line is added to the interface:

```csharp
interface IReadingSource
{
    string Name { get; }
    double? Next();
    int Remaining { get; }
}
```

```
w12thu_e_impact_list.cs(22,30): error CS0535: 'SimulatedOven' does not implement interface member 'IReadingSource.Remaining'
w12thu_e_impact_list.cs(10,31): error CS0535: 'ScriptedSource' does not implement interface member 'IReadingSource.Remaining'
w12thu_e_impact_list.cs(16,31): error CS0535: 'TextLineSource' does not implement interface member 'IReadingSource.Remaining'
```

Read the whole list. It is not in file order, and the first line is not the most important one.
Every class that promised the old contract is listed. Code that only **calls** the interface is not
listed, because it still compiles.

In a real project the list spans folders. The plant model port in this course lists `Equipment`,
`Cell`, and `Sensor`, in three folders, for a one-line change.

Python, for the same change, reports nothing until something asks for `remaining`, and then only for
that one object:

```
201.5
AttributeError: 'ScriptedSource' object has no attribute 'remaining'
```

**What you do with the list** is the decision. Implement the member everywhere, or decide the change
is wrong. A live sensor cannot know how many readings remain, so this member promises more than
every source can keep. The right call here is to take it back out, or to put it in a separate,
narrower interface that only finite sources implement.

---

## The wrong version: silencing instead of fixing

```csharp
string? badge = FindBadge("L3-PRS-02");
Console.WriteLine(badge!.ToUpper());
```

With `TreatWarningsAsErrors` on, this builds with **0 warnings**. It still throws
`System.NullReferenceException` when it runs.

```csharp
#pragma warning disable CS8602
Console.WriteLine(badge.ToUpper());
#pragma warning restore CS8602
```

Same result: a clean build, the same crash.

The `!` tells the analyzer "trust me, this is not null." It adds no check. It is only honest when
something the analyzer cannot see really does guarantee a value. In a review, every `!` and every
`#pragma` gets the same question: **where is the proof?**

---

## Why the wrong version is tempting

The build is red, the fix the error suggests is one character, and a clean build feels like
success. Teams that turn warnings into errors see this happen, which is why reviewers search for `!`
and `#pragma` on purpose.

---

## The human half: a peer walkthrough

Static analysis reads code without running it. A walkthrough is the same idea done by people. The
author demonstrates, then stays quiet while a reviewer asks questions and a recorder writes down
findings. The author writes a decision for every finding: fixed, deferred with a reason, or kept
with a reason.

Questions a compiler cannot ask, and a reviewer can:

1. Which member did you make more visible than it needs to be, and why?
2. What does your interface promise that one implementation cannot keep?
3. Which hand-written check did you keep, and what would happen without it?
4. Where is the proof behind each `!`?
5. What does your code do with a missing value?

---

## Configuration management, in one table (5.7.1, 5.7.3)

| Term | In this course |
|---|---|
| **Version management** | Every change is a commit. The deployed CRUD app in Week 10 was tagged as a baseline |
| **Interface control** | A published interface is a promise to people you may never meet. Changes to it are decided on purpose, never typed in on a whim |
| **Impact of a change** | Everything that must change because of this change. For an interface, the compiler lists it |
| **Baseline** | A version everyone agrees to measure from, such as the Week 10 release tag |

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Static analysis** | Checking code without running it. Compiler warnings are one kind |
| **Warning** | A static analysis finding that does not stop the build |
| **`TreatWarningsAsErrors`** | A project setting that makes every warning stop the build |
| **Nullable reference types** | `string?` means "may be null." The compiler tracks it and warns |
| **Null-forgiving operator** | `!` after an expression. Silences the warning. Adds no check |
| **`#pragma warning disable`** | Turns a warning off for the lines that follow |
| **Impact analysis** | Finding everything a change affects |
| **Peer walkthrough** | A review where the author presents and others question |

---

## Self-check

**Question 1.** A build has three warnings and succeeds. The team turns on `TreatWarningsAsErrors`.
What happens to the next build, and what does the team get in exchange for the inconvenience?

**Question 2.** You add one member to an interface that four classes implement, and a fifth class
only calls the interface. How many CS0535 errors appear, and which class is not listed?

**Question 3.** Write the review comment for `Console.WriteLine(badge!.ToUpper());` in a panel's
alarm handler.

---

### Answers

**1.** The next build fails with three errors, the same three messages. In exchange, no suspicious
code can reach the program unnoticed: a possible null, an unused threshold, or an unreachable line
has to be fixed or explained before anything ships.

**2.** Four, one for each implementing class. The class that only calls the interface still compiles
and is not listed, until it calls the new member.

**3.** Something like: "`badge` is `string?`, so it is null whenever the press is not locked out. The
`!` removes the warning, not the null, and this line will throw inside the alarm handler. Decide what
the handler shows when there is no badge, and check for null before calling `ToUpper()`."

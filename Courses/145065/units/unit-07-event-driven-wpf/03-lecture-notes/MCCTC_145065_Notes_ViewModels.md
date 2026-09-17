# Lecture Notes: A View Model You Can Test
## 145065 Object-Oriented Programming · Unit 7 · Week 14, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W14_ViewModels.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W14_ViewModels.md --export pptx`

If you missed class, including for BPA Nationals, you can learn this concept from this file alone. You
need the .NET SDK and the Lab U07-03 files.

**Competencies:** 5.3.12 write code that creates classes, objects, and methods. 5.1.4 compare
object-oriented and event-driven programming.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

Look at last week's ShiftTally code-behind. The rules of the shift (what UNDO takes back, how the
scrap rate is computed, when the target is reached) are mixed into handlers that also write to
`TextBlock` controls.

That has two costs. First, **you cannot test a rule without opening a window.** Second, the rules
cannot be reused: Unit 8's operator panel needs the same kind of logic on a different screen.

A **view model** pulls the rules and the state out of the window into an ordinary class. The window
keeps only the jobs that belong to a window: talking to the operator and to devices.

---

## The concept in plain language

A view model is a class that holds **everything the window shows, as properties**, and does
**everything the buttons do, as methods**.

| In the window | In the view model |
|---|---|
| `GoodText.Text = $"Good: {good}";` | `public int Good { get; }` |
| the scrap rate arithmetic inside `ShowCounts` | `public string ScrapRateText { get; }` |
| `good++; history.Push(true);` inside a handler | `public void AddGood()` |
| a message box asking a question | stays in the window |
| a printer call | stays in the window |

The view model goes in its own project that targets plain `net8.0`, **not** `net8.0-windows`. That
library cannot see any WPF type. Its tests run with no window, no thread rules, and no dispatcher.

The window's handlers shrink:

```csharp
// Lab U07-02: the handler does the counting, the bookkeeping, and the drawing.
private void OnGoodClick(object sender, RoutedEventArgs e)
{
    good++;
    history.Push(true);
    ShowCounts();
    StatusText.Text = "Counted one good part.";
}

// Lab U07-03: the handler passes the press to the view model.
private void OnGoodClick(object sender, RoutedEventArgs e) => Tally.AddGood();
```

The window owns one view model:

```csharp
public TallyViewModel Tally { get; } = new();
```

---

## Worked example 1: the rules, with no window at all

A console program using `TallyViewModel` from the Lab U07-03 solution:

```csharp
ShiftTally.Core.TallyViewModel tally = new() { Target = 150 };
for (int i = 0; i < 37; i++)
{
    tally.AddGood();
}

for (int i = 0; i < 3; i++)
{
    tally.AddScrap();
}

Console.WriteLine(tally.Heading);
Console.WriteLine($"Good {tally.Good}, scrap {tally.Scrap}, total {tally.Total}");
Console.WriteLine(tally.ProgressText);
Console.WriteLine($"Progress bar value: {tally.Progress.ToString("0.00", CultureInfo.InvariantCulture)}");
Console.WriteLine(tally.ScrapRateText);
Console.WriteLine(tally.Status);
```

Output:

```
Press 2: Hinge bracket
Good 37, scrap 3, total 40
37 of 150 good parts
Progress bar value: 24.67
Scrap rate: 7.5 %
Counted one scrap part. Tag it before it goes in the bin.
```

Every value the window will show exists here, computed, before any window is involved.

---

## Worked example 2: the members of the view model

From the Lab U07-03 solution, trimmed to the counting rules:

```csharp
public int Total => Good + Scrap;

public bool CanUndo => history.Count > 0;

/// <summary>The slider binds here. Values outside the range are pulled back into it.</summary>
public int Target
{
    get => target;
    set
    {
        int clamped = Math.Clamp(value, MinimumTarget, MaximumTarget);
        if (Set(ref target, clamped))
        {
            Changed(nameof(Progress));
            Changed(nameof(ProgressText));
        }
    }
}

/// <summary>0 to 100, for the progress bar. Only good parts count toward the target.</summary>
public double Progress => Math.Min(100.0, 100.0 * Good / Target);

public string ScrapRateText => Total == 0
    ? "Scrap rate: no parts yet"
    : string.Format(CultureInfo.InvariantCulture, "Scrap rate: {0:0.0} %", 100.0 * Scrap / Total);

public void AddGood()
{
    history.Push(true);
    Good++;
    Status = "Counted one good part.";
}
```

`Set` and `Changed` are Wednesday's topic. Today, notice that `Total`, `Progress`, and
`ScrapRateText` are **computed** properties: they have no field of their own, and each one is always
right because it is worked out from the counts every time it is read.

---

## Worked example 3: a rule, tested

From `ShiftTally.Core.Tests`, adapted from the course's anchor tests:

```csharp
[Fact]
public void ScrapRateUsesFloatingPointDivision()
{
    TallyViewModel tally = new();
    for (int i = 0; i < 7; i++)
    {
        tally.AddGood();
    }

    tally.AddScrap();
    // 1 of 8 is 12.5 percent. Integer division would give 0.
    Assert.Equal("Scrap rate: 12.5 %", tally.ScrapRateText);
}

[Theory]
[InlineData(10, 50)]
[InlineData(50, 50)]
[InlineData(250, 250)]
[InlineData(9000, 500)]
public void TheTargetStaysInRange(int asked, int expected)
{
    TallyViewModel tally = new() { Target = asked };
    Assert.Equal(expected, tally.Target);
}
```

Against the Lab U07-03 solution, `dotnet test` on the view model tests reported:

```
Passed!  - Failed:     0, Passed:    23, Skipped:     0, Total:    23, Duration: 111 ms - ShiftTally.Core.Tests.dll (net8.0)
```

Twenty-three checks in about a tenth of a second, with no window. The window checks, which open the
real window on a test thread, take seconds.

---

## Worked example 4: what stays in the window

```csharp
private void OnResetClick(object sender, RoutedEventArgs e)
{
    if (Confirm(Tally.ResetQuestion))
    {
        Tally.Reset();
    }
    else
    {
        Tally.Status = "Reset cancelled. The counts are kept.";
    }
}
```

Asking a person is the window's job, so the question stays here. The **wording** of the question is
a rule ("say how many parts will be lost"), so it lives in the view model as `ResetQuestion`, where a
test checks it:

```
Reset 3 counted parts to zero? This cannot be undone.
```

---

## The wrong version, and the error it produces

Try to give the view model a control:

```csharp
using System.Windows.Controls;

public sealed class TallyViewModel
{
    public TextBlock? GoodText { get; set; }
}
```

In a `net8.0` library, the build stops:

```
Program.cs(1,22): error CS0234: The type or namespace name 'Controls' does not exist in the namespace 'System.Windows' (are you missing an assembly reference?)
Program.cs(7,12): error CS0246: The type or namespace name 'TextBlock' could not be found (are you missing a using directive or an assembly reference?)
```

(The build machine's reproduction used a file named `Program.cs`; yours names your file.) **This error
is the design working.** The library cannot see WPF, so no rule can quietly start depending on a
window. The fix is never to add WPF to the library. The fix is a property the window binds to.

---

## Why the wrong version is tempting

Writing to a `TextBlock` is what you did all last week, and it worked. Moving code into another
project feels like extra files for no gain, until the first time you want to test a rule and
discover the only way to reach it is to open a window and click.

There is an honest cost. A view model means two projects, a project reference, and a property for
everything the window shows. For a window with one button, that is more code than it saves. For an
operator panel, it is the only way to test the rules that decide what an operator sees.

---

## Vocabulary

| Term | What it means |
|---|---|
| **View** | the window: XAML and code-behind |
| **View model** | a class holding what the view shows and doing what its buttons do |
| **Code-behind** | the window's C# file |
| **Computed property** | a property with no field, worked out each time it is read |
| **Class library** | a project that builds a `.dll` for other projects to use |
| **`net8.0` versus `net8.0-windows`** | plain .NET, which runs anywhere, versus .NET with Windows desktop libraries such as WPF |
| **Unit test** | a small, automatic check of one behavior |
| **MVVM** | Model-View-ViewModel, a family of designs built on this split |

---

## Self-check

**Question 1.** Sort these into "view model" or "window": the scrap rate arithmetic, a Yes/No
message box, the list of part types, a call to the label printer, the rule that UNDO does nothing
when there is nothing to undo.

**Question 2.** `Progress` has no field. Why is it never out of date when you read it?

**Question 3.** A teammate adds `using System.Windows;` to `ShiftTally.Core` so the view model can
show a `MessageBox`. The build fails. Should they change the project to `net8.0-windows`? Argue it.

---

### Answers

**1.** View model: the scrap rate arithmetic, the list of part types, the UNDO rule. Window: the
message box and the printer call.

**2.** It is computed from `Good` and `Target` every time it is read, so it always matches them.
(Whether the **screen** re-reads it is Wednesday's topic.)

**3.** First, what fails: the `using` line is accepted, because plain .NET has a few types under
`System.Windows`. The call fails: `error CS0103: The name 'MessageBox' does not exist in the current
context`. Should they switch? No. Changing the target would let the view model show dialogs, and then its tests would pop up
windows and wait for a person. Keep the question's wording in the view model (`ResetQuestion`) and
the dialog in the window (`Confirm`). The strongest case for the change is that it is one line and
makes the code shorter today; the case against is that every test of that rule now needs a person.

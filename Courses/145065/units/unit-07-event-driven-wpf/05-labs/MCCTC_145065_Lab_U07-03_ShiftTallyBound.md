# Lab U07-03: Shift Tally Bound
## 145065 Object-Oriented Programming · Unit 7 · Week 14

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday, Tuesday, and Wednesday, Build 1
and the first 15 minutes of Build 2 each day. The rest of each Build 2 is project time.
**Competencies:** 5.3.12 (classes, objects, and methods), 5.5.6 (format output), 5.4.2 (write and
edit code in the IDE), 5.4.7 (debug logic errors), 5.1.4 (object-oriented and event-driven design).

Files: `lab-u07-03-files/`, which holds `ShiftTally.sln`, `ShiftTally` (the Lab U07-02 solution, now
owning a `TallyViewModel`), `ShiftTally.Core` (the view model library), `ShiftTally.Core.Tests`,
`ShiftTally.SelfCheck`, and `extended/CommandChecks.cs`.

**Riverside Fabrication is a composite**, an invented shop. The label printer is simulated.

**Where the files came from.** Adapted from the course's HMI anchor project, where ShiftTally's
finished view model lives. This lab moves the view model into a separate `net8.0` library so its
tests need no window.

**Away for BPA Nationals?** Every step here works from the Week 14 lecture notes alone. Do Part 1 on
your first day back and Parts 2 and 3 on the second.

---

## The scenario

ShiftTally works, but its rules live inside the window. The supervisor wants the scrap rate
arithmetic checked every time the code changes, and a person clicking through the app is not a check.
Unit 8's operator panel is built the same way you will build this, so the pattern matters beyond
this app.

## What you will build

ShiftTally again, with its state and rules in a tested view model and every value on screen coming
through a data binding.

---

## Starter code

Copy `lab-u07-03-files/` into your repository. It builds and runs, and it works exactly like your
Lab U07-02 app.

- `ShiftTally.Core/TallyViewModel.cs` targets plain `net8.0`. The station and part members are
  written. Every other member throws `NotImplementedException` with the step number that writes it.
- `ShiftTally.Core.Tests` tests the view model with no window. Its `LogicTests` are Monday's work.
  Its `NotificationTests` are Wednesday's.
- `ShiftTally/MainWindow.xaml.cs` is the Lab U07-02 solution plus one property:
  `public TallyViewModel Tally { get; } = new();`. The window still counts in its own fields.
- `ShiftTally.SelfCheck` opens the window. `BindingChecks` are Tuesday's work. `LiveScreenChecks` check
  what the screen shows after presses.

---

## Part 1 · Monday · The view model

### Step 1. Build and check the starter

```
dotnet build ShiftTally.sln
dotnet test ShiftTally.sln
```

**Observable result:** two summaries.

```
Failed!  - Failed:    20, Passed:     3, Skipped:     0, Total:    23, ... ShiftTally.Core.Tests.dll (net8.0)
Failed!  - Failed:    22, Passed:     8, Skipped:     0, Total:    30, ... ShiftTally.SelfCheck.dll (net8.0)
```

Eight window checks already pass, because last week's code-behind writes the screen itself. Watch
what happens to them on Tuesday.

### Step 2. The counts, the target, and what is computed from them

In `TallyViewModel.cs`, at the step 2 comment, add fields for the good count, the scrap count, and the
target, which starts at 200. Replace the members that throw:

```csharp
public int Good
{
    get => good;
    private set => good = value;
}
```

`private set` means only this class can change the count. Write `Scrap` the same way. Then:

- `Total` is good plus scrap.
- `Target` stores `Math.Clamp(value, MinimumTarget, MaximumTarget)`, so 9000 becomes 500.
- `Progress` is `Math.Min(100.0, 100.0 * Good / Target)`.
- `ProgressText` reads `37 of 150 good parts`.
- `ScrapRateText` reads `Scrap rate: no parts yet` when the total is 0. Otherwise it is
  `string.Format(CultureInfo.InvariantCulture, "Scrap rate: {0:0.0} %", 100.0 * Scrap / Total)`. Add
  `using System.Globalization;`.

**Observable result:** the project builds. `dotnet test ShiftTally.Core.Tests` shows
`TheTargetStaysInRange` passing for all four targets.

### Step 3. What the buttons do

Replace the four methods that throw:

- `AddGood` pushes `true` onto `history`, adds one to `Good`, and sets `Status` to
  `Counted one good part.`
- `AddScrap` pushes `false`, adds one to `Scrap`, and sets `Status` to
  `Counted one scrap part. Tag it before it goes in the bin.`
- `Undo` pops the most recent entry, if there is one, takes one from the matching count, and sets
  `Status` to `Took back the last count.` With nothing to undo, it does nothing at all.
- `Reset` clears `history`, sets both counts to 0, and sets `Status` to `Counts reset.`

**Observable result:** `StartsEmpty`, `GoodAndScrapEachCountOne`, `UndoTakesBackTheLastKindCounted`,
`ResetClearsCountsAndHistory`, and `TheStatusLineSaysWhatJustHappened` pass.

### Step 4. The text the handlers need

`ResetQuestion` reads `Reset 3 counted parts to zero? This cannot be undone.` with the real total.
`SummaryText` reads `Press 4 | Cover plate | good 2 | scrap 1 | target 100`, using `StationName`.

**Observable result:** `dotnet test ShiftTally.Core.Tests` reports `Passed: 15` of 23. Every
`LogicTests` check passes. The 8 `NotificationTests` fail, and they should, until Wednesday.

### Step 5. The window uses the view model

In `MainWindow.xaml.cs`, delete the four fields `history`, `good`, `scrap`, and `target`. Then:

- Each counting handler calls the view model and redraws. For example:

  ```csharp
  private void OnGoodClick(object sender, RoutedEventArgs e)
  {
      Tally.AddGood();
      ShowCounts();
  }
  ```

- `OnResetClick` asks `Confirm(Tally.ResetQuestion)`. On yes it calls `Tally.Reset()`; on no it sets
  `Tally.Status = "Reset cancelled. The counts are kept.";`. Either way it ends with `ShowCounts()`.
- `OnPrintClick` sets `Tally.Status` instead of `StatusText.Text`, prints `Tally.SummaryText`, and calls
  `ShowCounts()` after each status change.
- The change handlers store into the view model first: `Tally.Target = (int)e.NewValue;`,
  `Tally.Station = StationBox.Text;`, `Tally.PartType = PartName();`, and
  `Tally.ShowScrapRate = ShowRateBox.IsChecked == true;`.
- `ShowCounts` reads everything from `Tally`:

  ```csharp
  GoodText.Text = $"Good: {Tally.Good}";
  ScrapText.Text = $"Scrap: {Tally.Scrap}";
  TotalText.Text = $"Total: {Tally.Total}";
  TargetText.Text = $"Shift target: {Tally.Target}";
  ShiftProgress.Value = Tally.Progress;
  ProgressText.Text = Tally.ProgressText;
  RateText.Text = Tally.ScrapRateText;
  RateText.Visibility = Tally.ShowScrapRate ? Visibility.Visible : Visibility.Collapsed;
  UndoButton.IsEnabled = Tally.CanUndo;
  StatusText.Text = Tally.Status;
  ```

- `ShowHeading` sets `HeadingText.Text = Tally.Heading;`.
- Remove `using System.Globalization;` from the window if nothing uses it now.

**Observable result:** the project builds with no errors.

### Step 6. Check and commit

**Observable result:** `ShiftTally.Core.Tests` 15 of 23, and `ShiftTally.SelfCheck` 12 of 30. The
app still counts when you run it. Commit.

---

## Part 2 · Tuesday · Bindings

### Step 7. Add a converter

In `MainWindow.xaml`, inside `Grid.Resources`, add:

```xml
<BooleanToVisibilityConverter x:Key="Visible" />
```

**Observable result:** the project builds.

### Step 8. Bind every value

Change these controls. **Keep every `x:Name`.** Remove the static `Text` or `Value` each binding
replaces, and remove the `TextChanged`, `SelectionChanged`, `ValueChanged`, `Checked`, and `Unchecked`
attributes: the two-way bindings now carry those changes to the view model. Keep the five `Click`
attributes. Replace `PartBox`'s three `ComboBoxItem` children with `ItemsSource`.

| Control | Binding |
|---|---|
| `HeadingText` | `Text="{Binding Heading}"` |
| `StationBox` | `Text="{Binding Station, UpdateSourceTrigger=PropertyChanged}"` |
| `PartBox` | `ItemsSource="{Binding PartTypes}" SelectedItem="{Binding PartType}"` |
| `UndoButton` | `IsEnabled="{Binding CanUndo}"` |
| `GoodText` | `Text="{Binding Good, StringFormat=Good: {0}}"` |
| `ScrapText` | `Text="{Binding Scrap, StringFormat=Scrap: {0}}"` |
| `TotalText` | `Text="{Binding Total, StringFormat=Total: {0}}"` |
| `TargetText` | `Text="{Binding Target, StringFormat=Shift target: {0}}"` |
| `TargetSlider` | `Value="{Binding Target}"` |
| `ShiftProgress` | `Value="{Binding Progress, Mode=OneWay}"` |
| `ProgressText` | `Text="{Binding ProgressText}"` |
| `ShowRateBox` | `IsChecked="{Binding ShowScrapRate}"` |
| `RateText` | `Text="{Binding ScrapRateText}"` and `Visibility="{Binding ShowScrapRate, Converter={StaticResource Visible}}"` |
| `StatusText` | `Text="{Binding Status}"` |

**Observable result:** the XAML builds. `ProgressBar.Value` needs `Mode=OneWay` because `Progress` has
no setter.

### Step 9. Let the bindings work

In `MainWindow.xaml.cs`:

1. In the constructor, after `Confirm = AskYesNo;`, add `DataContext = Tally;`.
2. Delete `ShowCounts`, `ShowHeading`, `PartName`, the `windowBuilt` field and its assignment, and all
   four change handlers.
3. Make the three counting handlers one line each:
   `private void OnGoodClick(object sender, RoutedEventArgs e) => Tally.AddGood();`
4. In `OnResetClick` and `OnPrintClick`, delete the `ShowCounts()` calls.
5. Delete any `using` the file no longer needs.

**Observable result:** the project builds. The code-behind is about a third of its Monday length.

### Step 10. Check the bindings

**Observable result:** `EveryDisplayedValueIsBound` passes for all 15 rows, and
`NoBindingPathIsMisspelled` passes. `TheWindowShowsItsOwnViewModel`, `TheScreenStartsWithTheViewModelsValues`,
`TheSliderWritesBackToTheViewModel`, `TypingWritesBackOnEveryKeystroke`, and
`ThePartListComesFromTheViewModel` pass.

### Step 11. Predict, then run

**Before you run anything**, write in your notes what you expect the window checks to report, and
what you expect the picture to show.

Then run `dotnet test` and open
`ShiftTally.SelfCheck/bin/Debug/net8.0-windows/window-pictures/ShiftTally-U07-03.png`.

**Observable result:** `ShiftTally.SelfCheck` reports 24 of 30. The six failures are all
`LiveScreenChecks`: `PressingAButtonUpdatesTheScreen`, `UndoUpdatesTheScreenAndTurnsItselfOff`,
`TheHeadingFollowsTheStationBox`, `ProgressFollowsTheSlider`, `ResetStillAsksFirst`, and
`PrintingStillKeepsTheWindowWorking`. The picture shows `Good: 0`, `Scrap: 0`, and `Total: 0`,
although the check that made it added 37 good and 3 scrap parts to `Tally`.

Write two sentences in your notes: what the view model holds, and why the screen does not show it.

### Step 12. One odd result, then commit

Run the app and drag the slider. Then press +1 GOOD.

**Observable result:** the "Shift target" text follows the slider. The counts do not move when you
press. Write one sentence on why the target text updates when nothing else does. The Tuesday lecture
note's last section and slide 9 of the Tuesday deck explain it. Commit.

---

## Part 3 · Wednesday · Announcing changes

### Step 13. Implement the interface

At the top of `TallyViewModel.cs` add `using System.ComponentModel;` and
`using System.Runtime.CompilerServices;`. Change the class line to
`public sealed class TallyViewModel : INotifyPropertyChanged`, and add:

```csharp
public event PropertyChangedEventHandler? PropertyChanged;

/// <summary>Stores a value and announces it, unless nothing changed.</summary>
private bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
{
    if (EqualityComparer<T>.Default.Equals(field, value))
    {
        return false;
    }

    field = value;
    Changed(name);
    return true;
}

private void Changed(string? name) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
```

**Observable result:** view model tests 16 of 23, and window checks **23** of 30.
`SettingTheSameValueAnnouncesNothing` now passes. `TheCheckBoxHidesTheScrapRate`, which passed
yesterday, now fails. Write down why in your notes: once a class says it announces its changes, WPF
stops watching for changes in any other way.

### Step 14. Announce the counts and the status

Change the `Good` setter:

```csharp
private set
{
    if (Set(ref good, value))
    {
        CountsChanged();
    }
}
```

Do the same for `Scrap`. Add `CountsChanged`, which announces every bound property computed from the
counts:

```csharp
private void CountsChanged()
{
    Changed(nameof(Total));
    Changed(nameof(Progress));
    Changed(nameof(ProgressText));
    Changed(nameof(ScrapRateText));
    Changed(nameof(CanUndo));
}
```

Change the `Status` setter to `set => Set(ref status, value ?? string.Empty);`. In `Reset`, after both
counts are set to 0, add `Changed(nameof(CanUndo));` so the UNDO button hears about the cleared
history even when the counts were already zero.

**Observable result:** view model tests 20 of 23, window checks 27 of 30. The counts move on screen.

### Step 15. Announce the target

In the `Target` setter, store the clamped value with `Set`, and when it really changed, announce
`Progress` and `ProgressText`.

**Observable result:** 21 of 23 and 28 of 30. `ProgressFollowsTheSlider` passes.

### Step 16. Announce the station, the part, and the check box

The `Station` setter uses `Set` and, when it changed, announces `StationName`, `StationIsValid`, and
`Heading`. The `PartType` setter uses `Set` and announces `Heading`. The `ShowScrapRate` setter becomes
`set => Set(ref showScrapRate, value);`.

**Observable result:** both summaries show every check passing.

### Step 17. Look again

Run `dotnet test` and open the picture again.

**Observable result:**

```
Passed!  - Failed:     0, Passed:    23, Skipped:     0, Total:    23, ... ShiftTally.Core.Tests.dll (net8.0)
Passed!  - Failed:     0, Passed:    30, Skipped:     0, Total:    30, ... ShiftTally.SelfCheck.dll (net8.0)
```

The picture now shows `Good: 37`, `Scrap: 3`, `Total: 40`, `Shift target: 150`, `37 of 150 good parts`,
and `Scrap rate: 7.5 %`. Compare it with Tuesday's picture.

### Step 18. Break one line on purpose, then commit

Delete `Changed(nameof(ScrapRateText));` from `CountsChanged` and run the tests.

**Observable result:** two view model tests fail with a message that begins
`ScrapRateText changed but was never announced.` and one window check reports
`Expected: "Scrap rate: 33.3 %"` and `Actual:   "Scrap rate: no parts yet"`. Nothing crashed. Put the
line back, run the tests to full marks, and commit.

### Acceptance criteria, full lab

- [ ] `ShiftTally.Core.Tests`: 23 of 23
- [ ] `ShiftTally.SelfCheck`: 30 of 30
- [ ] `ShiftTally.Core` has no reference to WPF
- [ ] Every value on screen comes through a binding; each Click handler is one call, except RESET and PRINT
- [ ] Your notes hold the Tuesday prediction, the two Tuesday sentences, the step 12 sentence, and the
      step 13 explanation
- [ ] Committed at the end of each day

---

## If it breaks

### 1. A control in the view model library

```
error CS0234: The type or namespace name 'Controls' does not exist in the namespace 'System.Windows' (are you missing an assembly reference?)
```

**Cause:** `using System.Windows.Controls;` in `ShiftTally.Core`. The library targets plain `net8.0`
and cannot see WPF, on purpose. Give the view model a property instead, and bind to it.

### 2. A misspelled binding path

The build succeeds, the text is blank, and the debug output shows a line like:

```
System.Windows.Data Error: 40 : BindingExpression path error: 'Goood' property not found on 'object' ''TallyViewModel' ...
```

**Cause:** the name inside `{Binding ...}` does not match a property. `NoBindingPathIsMisspelled` lists
every such line. In Visual Studio, these appear in the Output window while debugging [VERIFY].

### 3. A test that says the view model does not announce

```
TallyViewModel does not implement INotifyPropertyChanged yet, so no binding can hear it change (step 13).
```

**Cause:** step 13 is not done. Every `NotificationTests` check fails with this until it is.

### 4. A stale value with no error anywhere

```
ScrapRateText changed but was never announced. A control bound to it keeps showing the old value. Announced: Good, Total, Progress, ProgressText, CanUndo, Status
```

**Cause:** a dependent property is missing from `CountsChanged` or from a setter. The last part of the
message lists what **was** announced, so you can see what is missing.

### Also likely: a property that still throws

```
System.NotImplementedException : Lab U07-03 step 3: AddGood
```

**Cause:** that member still has the starter's `throw`. The message names the step and the member.

### Also likely: the heading lags one step behind while typing

**Cause:** `StationBox`'s binding is missing `UpdateSourceTrigger=PropertyChanged`, so the view model
only hears the name when the box loses focus. `TypingWritesBackOnEveryKeystroke` fails.

---

## Stretch goal

Add `ToolTip="{Binding SummaryText}"` to `PrintButton`. Press +1 GOOD twice, then hover over PRINT
SUMMARY. On the build machine, a check that did exactly this found the tooltip still reading
`Press 2 | Hinge bracket | good 0 | scrap 0 | target 200` while `Tally.SummaryText` said `good 2`.
Explain why in your notes. Then fix it: `SummaryText` depends on the counts, the station, the part, and
the target, so every one of those setters must announce it. Add a view model test that proves a good
part announces `SummaryText`.

---

## Submission checklist

- [ ] 23 of 23 and 30 of 30
- [ ] Notes: Tuesday prediction and sentences, step 12, step 13
- [ ] The window's code-behind has no `ShowCounts` and no count fields
- [ ] Pushed at the end of Monday, Tuesday, and Wednesday
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Fewer than 15 of 23 view model tests at the end of Monday, or a returning competitor starting late | SCAFFOLDED |
| Steady progress, questions about which property depends on which | STANDARD |
| 23 of 23 and 30 of 30 before Wednesday Build 2 | EXTENDED |
| The student asks why anyone separates a window from its logic | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** your teacher gives you a different `ShiftTally.Core/TallyViewModel.cs`, a
  finished `MainWindow.xaml.cs`, and a `MainWindow.xaml` with half its bindings written. The view model
  already implements the interface and has `Set` and `Changed`, but its setters do not use them yet.
  It starts at 12 of 23 and 13 of 30.
- **Steps:** four checkpoints marked `TODO` in the files: (1) `Undo` and `ScrapRateText`, (2) run the
  tests, (3) the remaining bindings in the XAML, (4) every setter uses `Set`, and `CountsChanged`
  announces the five dependent properties.
- **Checkpoints:** show your teacher the test summaries after checkpoints 1 and 3.

**Acceptance criteria:** 23 of 23 and 30 of 30, and the step 18 observation in your notes.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a WPF feature the unit has not taught: commands.

**Added requirement.** Replace the Click handlers for +1 GOOD, +1 SCRAP, and UNDO LAST with commands
on the view model: `AddGoodCommand`, `AddScrapCommand`, and `UndoCommand`. UNDO LAST must grey itself
out through the command when there is nothing to undo. Add keyboard shortcuts to the window: `F2` for
a good part, `F3` for scrap, and `Ctrl+Z` for undo, each running the **same command object** as its
button. Use function keys, not letters: a window-wide `G` would also fire while the operator types a
station name. RESET and PRINT keep their Click handlers, because they talk to a person and a device.

Copy `extended/CommandChecks.cs` into `ShiftTally.SelfCheck`. Until the commands exist, it does not
compile, and the compiler's message names what is missing.

**Hint, not the answer.** Read the `ICommand` interface reference on Microsoft Learn
(`https://learn.microsoft.com/en-us/dotnet/api/system.windows.input.icommand`), and look up
`Window.InputBindings` and `KeyBinding` in the WPF documentation [VERIFY]. `ICommand` ships with plain
.NET, so it can live in `ShiftTally.Core`. Ask yourself how the command tells the button that
`CanExecute` has changed.

**Acceptance criteria:** 23 of 23 view model tests and 38 of 38 window checks with `CommandChecks.cs`
copied in; the three Click handlers are gone.

**Grading:** same scale.

---

## APPLIED

**For the student who asks why anyone separates a window from its logic.** The same skill, somewhere
else.

**Changed scenario.** A school library wants a book-return counter at the drop box: returned on time,
returned late, a daily goal slider, a late-return rate, and UNDO. No borrower information of any kind:
the counter counts books, never people.

**What you build.** A `net8.0` library with a view model and at least eight tests, including one that
proves the late-return rate is announced when a late book is counted, and a WPF window bound to it.
Write the dependency table first.

**Acceptance criteria:** your tests pass; every value on screen is bound; your dependency table
matches your announcements. You may adapt `ShiftTally.SelfCheck` to your window, and your teacher
gives credit for doing so.

**Grading:** same scale. Requirements Fit is judged on whether the library staff could trust the rate
on screen.

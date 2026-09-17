# Lab U07-02: Shift Tally Handlers
## 145065 Object-Oriented Programming · Unit 7 · Week 13

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Wednesday Build 1 and Build 2
(Part 1), Thursday Build 1 and the first 25 minutes of Build 2 (Part 2).
**Competencies:** 5.3.12 (classes, objects, and methods), 5.4.2 (write and edit code in the IDE),
5.4.7 (debug logic errors), 5.1.4 (event-driven programming).

Files: `lab-u07-02-files/`, which holds `ShiftTally.sln`, the `ShiftTally` starter (the Lab U07-01
window, plus `LabelPrinter.cs`), `ShiftTally.SelfCheck`, and `extended/ExtendedChecks.cs`.

**Riverside Fabrication is a composite**, an invented shop. Every count is invented. The label printer
is simulated: there is no printer and no hardware.

**Where the files came from.** ShiftTally is adapted from the course's HMI anchor project. The
starter window is the Lab U07-01 solution, so you can start clean even if yesterday went badly.

---

## The scenario

The Press 2 window from yesterday looks right and does nothing. The operator needs every button to
count, a reset that cannot wipe a shift by accident, and a printed summary at the end of the shift.
The label printer takes about three seconds per label, and the operator keeps working while it prints.

## What you will build

Event handlers that make ShiftTally count, confirm, and print, without ever freezing the window.

---

## Starter code

Copy `lab-u07-02-files/` into your repository. It builds and runs. Nothing responds.

Read these three pieces of `ShiftTally/MainWindow.xaml.cs` before you write anything:

- **`windowBuilt`.** WPF raises some events while `InitializeComponent` is still building the window,
  before every control exists. This flag is `false` until the constructor finishes. `ShowCounts`
  returns early while it is `false`. **Do not remove it.** Section "If it breaks" shows what happens
  without it.
- **`Confirm`.** A function that asks the operator a yes-or-no question. In the running app it shows a
  message box with **No** as the default. The self-check replaces it with its own answer, so no dialog
  appears while the checks run. **Call `Confirm`, never `MessageBox`, from your handler.**
- **`Printer`.** The simulated `LabelPrinter`. Read `LabelPrinter.cs`: `Print` makes the caller wait,
  and `PrintAsync` does not. Step 11 uses the first. Step 13 uses the second.

---

## Part 1 · Wednesday · Handlers that count

### Step 1. Build and check the starter

```
dotnet build ShiftTally.sln
dotnet test ShiftTally.sln
```

**Observable result:** `Failed!  - Failed:    17, Passed:     1, Skipped:     0, Total:    18`. The one
that passes saves a picture.

### Step 2. Add the shift's state

In `MainWindow.xaml.cs`, at the comment "Step 3: add the fields", add:

```csharp
private readonly Stack<bool> history = new();   // true = a good part, false = scrap
private int good;
private int scrap;
private int target = 200;
```

A `Stack` remembers the order parts were counted, so UNDO takes back the most recent one.

**Observable result:** four fields in the class. **Do not build yet.** This project treats warnings
as errors, and the compiler complains about fields that nothing uses. Steps 3 and 4 use them.

### Step 3. Show the counts, then count good parts

Inside `ShowCounts`, after the `windowBuilt` check, write the counts onto the screen:

```csharp
int total = good + scrap;
GoodText.Text = $"Good: {good}";
ScrapText.Text = $"Scrap: {scrap}";
TotalText.Text = $"Total: {total}";
TargetText.Text = $"Shift target: {target}";
UndoButton.IsEnabled = history.Count > 0;
```

At the comment "Steps 4 to 12", write the first handler:

```csharp
private void OnGoodClick(object sender, RoutedEventArgs e)
{
    good++;
    history.Push(true);
    ShowCounts();
    StatusText.Text = "Counted one good part.";
}
```

Attach it in `MainWindow.xaml` by adding `Click="OnGoodClick"` to `GoodButton`. Now build.

**Observable result:** the build fails with one error, which on the build machine read:

```
MainWindow.xaml.cs(26,17): error CS0649: Field 'MainWindow.scrap' is never assigned to, and will always have its default value 0
```

Read it. The compiler is right: nothing changes `scrap` yet. Step 4 fixes that.

### Step 4. Count scrap

Write `OnScrapClick` with the same four steps: add one to `scrap`, push `false`, call `ShowCounts`,
and set the status to `Counted one scrap part. Tag it before it goes in the bin.` Attach it to
`ScrapButton`. Build and test.

**Observable result:** the build succeeds. `dotnet test` reports `Passed: 4` of 18:
`GoodAddsOneAndShowsIt`, `ScrapAddsOneAndShowsIt`, `EachPressCountsExactlyOnce`, and the picture. Run
the app with `dotnet run --project ShiftTally` and press both buttons: the counts, the total, and the
status line change.

### Step 5. Undo

Write `OnUndoClick`. Take the most recent entry off `history` with `TryPop`. If there is none, return.
If it was a good part, take one from `good`; otherwise take one from `scrap`. Call `ShowCounts` and set
the status to `Took back the last count.` Attach it to `UndoButton`.

**Observable result:** `Passed: 6` of 18. `UndoTakesBackTheLastKindCounted` and
`UndoIsEnabledOnlyWhenThereIsSomethingToUndo` now pass. In the running app, UNDO LAST turns on after
the first count and off again when nothing is left.

### Step 6. Commit

**Observable result:** a commit whose message says the counting handlers work.

### Step 7. Reset, with a question first

Write `OnResetClick`:

1. Ask `Confirm($"Reset {good + scrap} counted parts to zero? This cannot be undone.")`.
2. If the answer is `false`, set the status to `Reset cancelled. The counts are kept.` and return.
3. Otherwise set both counts to 0, clear `history`, call `ShowCounts`, and set the status to
   `Counts reset.`

Attach it to `ResetButton`.

**Observable result:** `ResetAsksFirstAndKeepsTheCountsOnNo` and `ResetClearsEverythingOnYes` pass. In
the running app, RESET SHIFT shows a Yes/No box, and pressing Enter chooses No [VERIFY on the lab
machine].

### Step 8. The target and the progress

Add `ValueChanged="OnTargetChanged"` to `TargetSlider`, and write:

```csharp
private void OnTargetChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    target = (int)e.NewValue;
    ShowCounts();
}
```

In `ShowCounts`, add two lines. The progress bar's value is `100.0 * good / target`, but never more
than 100 (use `Math.Min`). The progress text reads like `37 of 150 good parts`. The target text is
already there from step 3.

**Observable result:** `TheSliderChangesTheTargetAndTheProgress` and
`ProgressCountsGoodPartsOnlyAndStopsAtOneHundred` pass.

### Step 9. The scrap rate and the check box

In `ShowCounts`, set `RateText.Text` to `Scrap rate: no parts yet` when the total is 0. Otherwise:

```csharp
string.Format(CultureInfo.InvariantCulture, "Scrap rate: {0:0.0} %", 100.0 * scrap / total)
```

Add `using System.Globalization;` at the top. Then set `RateText.Visibility` to
`Visibility.Visible` when `ShowRateBox.IsChecked == true`, and `Visibility.Collapsed` otherwise.

Write `OnShowRateChanged(object sender, RoutedEventArgs e)`, which calls `ShowCounts`, and attach it
to **both** `Checked` and `Unchecked` on `ShowRateBox`.

**Observable result:** `ScrapRateUsesFloatingPointDivision` shows `Scrap rate: 12.5 %` for 7 good and 1
scrap, and `TheCheckBoxHidesAndShowsTheScrapRate` passes.

### Step 10. The heading follows the station and the part

Add a helper and a method like `ShowCounts`:

```csharp
private string PartName() =>
    PartBox.SelectedItem is ComboBoxItem item ? item.Content as string ?? "" : "";
```

Write `ShowHeading`: return early if the window is not built; otherwise take `StationBox.Text.Trim()`.
If it is not empty, the heading is `{station}: {PartName()}`. If it is empty, the heading is
`(name the station): {PartName()}`. Add `using System.Windows.Controls;` at the top.

Write `OnStationChanged(object sender, TextChangedEventArgs e)` and
`OnPartChanged(object sender, SelectionChangedEventArgs e)`, each calling `ShowHeading`. Attach them
with `TextChanged` on `StationBox` and `SelectionChanged` on `PartBox`. Call `ShowHeading()` at the end
of the constructor too.

**Observable result:** `dotnet test` reports `Passed: 16` of 18. The two that fail are the printing
checks. Commit.

---

## Part 2 · Thursday · Printing without freezing

### Step 11. Print the slow way first

Add a summary helper:

```csharp
private string SummaryText() =>
    $"{StationBox.Text.Trim()} | {PartName()} | good {good} | scrap {scrap} | target {target}";
```

Write the print handler with the **blocking** method, and attach it to `PrintButton`:

```csharp
private void OnPrintClick(object sender, RoutedEventArgs e)
{
    PrintButton.IsEnabled = false;
    StatusText.Text = "Printing the shift summary...";
    printer.Print(SummaryText());
    StatusText.Text = "Summary printed.";
    PrintButton.IsEnabled = true;
}
```

Run `dotnet test`.

**Observable result:** 17 of 18. The one failure is `PrintingDoesNotFreezeTheWindow`, and its message
begins `The PRINT handler held the UI thread for` about 1000 ms (the check shortens the printer's delay
to one second). Read the rest of the message.

### Step 12. Feel the freeze

Run the app. Press PRINT SUMMARY. During the next three seconds, press +1 GOOD twice.

**Observable result:** write down, in your lab notes, exactly what the window did during those three
seconds, whether the words "Printing the shift summary..." ever appeared, and what happened to your
two presses when the freeze ended [VERIFY on the lab machine before class]. If Windows labelled the
window "Not Responding", write that down too.

### Step 13. Await instead

Change the handler to:

```csharp
private async void OnPrintClick(object sender, RoutedEventArgs e)
{
    PrintButton.IsEnabled = false;
    StatusText.Text = "Printing the shift summary...";
    await printer.PrintAsync(SummaryText());
    StatusText.Text = "Summary printed.";
    PrintButton.IsEnabled = true;
}
```

**Observable result:** `dotnet test` reports 18 of 18. In the running app, press PRINT SUMMARY and then
+1 GOOD: the count changes while the label prints, and PRINT SUMMARY is greyed out until it finishes.

### Step 14. Break it twice, and read what the build says

1. Remove `async` from the handler and build. Copy the error line into your notes. It is **CS4033**.
2. Put `async` back. Remove `await` from the print line and build. Copy the error. It is **CS4014**.
3. Put `await` back and build until it succeeds.

**Observable result:** two error lines in your notes, each with one sentence in your own words saying
what it means for an operator.

### Step 15. Finish and look

Run `dotnet test` and open `ShiftTally.SelfCheck/bin/Debug/net8.0-windows/window-pictures/ShiftTally-U07-02.png`.

**Observable result:** `Passed!  - Failed:     0, Passed:    18, Skipped:     0, Total:    18`. The
picture shows `Good: 37`, `Scrap: 3`, `Total: 40`, a target of 150, a progress bar about a quarter
full, `37 of 150 good parts`, and `Scrap rate: 7.5 %`. Commit and push.

### Acceptance criteria, full lab

- [ ] `dotnet test ShiftTally.sln` reports 18 of 18
- [ ] Every handler is attached once, in the XAML, and nowhere else
- [ ] RESET calls `Confirm` before changing anything
- [ ] The scrap rate uses floating-point division
- [ ] PRINT SUMMARY awaits `PrintAsync` and is disabled while it prints
- [ ] Your notes describe the freeze from step 12 and hold the two error lines from step 14
- [ ] The `windowBuilt` guard is still in place
- [ ] Committed at the end of Wednesday and at the end of Thursday

---

## If it breaks

### 1. The window never opens

```
System.NullReferenceException: Object reference not set to an instance of an object.
```

The stack trace names one of your handlers, often `OnStationChanged` or `OnTargetChanged`.

**Cause:** WPF raised `TextChanged` or `ValueChanged` while `InitializeComponent` was still building
the window, and your handler touched a control that did not exist yet. With the `windowBuilt` guard
removed from the solution, all 18 checks failed this way. Make sure every method that touches
controls from a change handler starts with `if (!windowBuilt) { return; }`.

### 2. A handler with the wrong parameters

```
MainWindow.xaml(7,39): error CS0123: No overload for 'OnCountClick' matches delegate 'RoutedEventHandler'
```

**Cause:** the method's parameters do not match the event. `Click` needs
`(object sender, RoutedEventArgs e)`. A slider's `ValueChanged` needs
`(object sender, RoutedPropertyChangedEventArgs<double> e)`. The line and column point at the event
attribute in your XAML.

### 3. A double where an int belongs

```
MainWindow.xaml.cs(16,18): error CS0266: Cannot implicitly convert type 'double' to 'int'. An explicit conversion exists (are you missing a cast?)
```

**Cause:** slider values are `double`. Write `target = (int)e.NewValue;`. The slider snaps to ticks of
50, so the cast loses nothing.

### 4. `await` without `async`, or the reverse

```
MainWindow.xaml.cs(112,9): error CS4033: The 'await' operator can only be used within an async method. Consider marking this method with the 'async' modifier and changing its return type to 'Task'.
```

```
MainWindow.xaml.cs(112,9): error CS4014: Because this call is not awaited, execution of the current method continues before the call is completed. Consider applying the 'await' operator to the result of the call.
```

**Cause:** the first means `async` is missing. For an event handler, add `async` and **keep `void`**.
The advice about `Task` is for ordinary methods. The second means `await` is missing, so the handler
would say "Summary printed." before anything printed. Your line numbers will differ.

### Also likely: a misspelled event name

```
MainWindow.xaml(7,71): error MC3072: The property 'Clik' does not exist in XML namespace 'http://schemas.microsoft.com/winfx/2006/xaml/presentation'. Line 7 Position 71.
```

**Cause:** an event attribute is spelled wrong. Events are checked like properties.

### Not an error, and the one that matters most: `async` with the blocking call

Mark the handler `async` but keep `printer.Print(...)`. On the build machine's SDK this compiled with
**no warning at all**, and the window froze exactly as in step 11. The check caught it:
`The PRINT handler held the UI thread for 1004 ms.` The word `async` does not make anything
asynchronous. Only `await` on a method that returns a `Task` does.

### Not an error: one press counts two

If a handler is attached twice, once in the XAML and once with `+=` in the constructor, every press
runs it twice. With `GoodButton.Click += OnGoodClick;` added to the solution, 10 of the 18 checks
failed, and `EachPressCountsExactlyOnce` reported:

```
Assert.Equal() Failure: Values differ
Expected: Tuple ("Good: 3", "Scrap: 2", "Total: 5")
Actual:   Tuple ("Good: 6", "Scrap: 2", "Total: 8")
```

Remove the `+=` line.

---

## Stretch goal

Add a keyboard shortcut: pressing the `G` key anywhere in the window counts one good part. Look up
the `KeyDown` event on `Window`. Your handler receives `KeyEventArgs`. What must your handler do so
typing a `G` into the station box does **not** count a part? Write the answer in your notes.

---

## Submission checklist

- [ ] `dotnet test ShiftTally.sln`: 18 of 18
- [ ] Notes: the freeze from step 12, the two errors from step 14
- [ ] No `+=` for any handler that the XAML already attaches
- [ ] Pushed at the end of Wednesday and Thursday
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Fewer than 6 of 18 at the end of Wednesday Build 1, or no handler attached yet | SCAFFOLDED |
| Steady progress, questions about which event to use | STANDARD |
| 18 of 18 before Thursday Build 2 | EXTENDED |
| The student asks what a counter has to do with real jobs | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** your teacher gives you a different `ShiftTally` folder. Every event is already
  attached in the XAML, every handler exists, and `OnGoodClick` is finished as your model. The other
  handler bodies hold comments that list their steps. It starts at 6 of 18.
- **Steps:** work through the five checkpoints in the file's comments instead of steps 2 to 11.
  Checkpoint 5 is the print handler, which starts in its blocking form, so steps 12 to 15 are
  unchanged.
- **Checkpoints:** show your teacher `dotnet test` after checkpoints 2 and 4.

**Acceptance criteria:** 18 of 18, the step 12 notes, and the step 14 error lines.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a failure the lab has not taught.

**Added requirement.** The real label printer runs out of labels. In the simulation, set
`Printer.OutOfLabels = true` and `PrintAsync` throws `InvalidOperationException` after its delay.
Right now that exception closes the whole app: on the build machine it ended with
`Unhandled exception. System.InvalidOperationException: The label printer is out of labels.` Make
the handler survive it. The status must read exactly:

```
Print failed: The label printer is out of labels. Load labels and press PRINT SUMMARY again.
```

and PRINT SUMMARY must work again afterward.

Copy `extended/ExtendedChecks.cs` into `ShiftTally.SelfCheck`. While it sits in the `extended` folder,
nothing compiles it.

**Hint, not the answer.** Read about `try`, `catch`, and `finally` in the C# language reference on
Microsoft Learn: `https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/exception-handling-statements`
[VERIFY]. Ask yourself which statement runs whether printing worked or not, and which exception type
the printer throws. The exception's `Message` is the middle of the status text.

**Acceptance criteria:** all STANDARD criteria; `dotnet test` reports 20 of 20 with the extended
checks copied in.

**Grading:** same scale.

---

## APPLIED

**For the student who asks what a counter has to do with real jobs.** The same skill, somewhere else.

**Changed scenario.** The school's booster club runs a concession stand at games. Build a sales
counter for one register: `+1 HOT DOG`, `+1 DRINK`, `UNDO LAST`, and `END OF GAME` (which asks first),
a slider for the expected crowd size with a progress bar of sales against it, and a `PRINT TOTALS`
button whose simulated printer takes three seconds. Invented item names and prices only. No customer
information of any kind.

**What you build.** Copy `lab-u07-02-files/` and change the window and handlers. Keep the
`windowBuilt` guard, the `Confirm` seam, and `LabelPrinter`. Write down which of your handlers needs
`await`, and why.

**Acceptance criteria:** every button works in the running app; END OF GAME asks first; PRINT TOTALS
does not freeze the window; your notes answer the `await` question. You may adapt
`HandlerChecks.cs` to your control names, and your teacher gives credit for doing so.

**Grading:** same scale. Requirements Fit is judged on whether a volunteer could run the stand with
it.

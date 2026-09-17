# Lab U07-01: First Window
## 145065 Object-Oriented Programming · Unit 7 · Week 13

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1 and Build 2 (Part 1),
Tuesday Build 1 and Build 2 (Part 2).
**Competencies:** 5.1.4 (procedural, object-oriented, and event-driven programming), 5.4.2 (write and
edit code in the IDE), 5.3.12 (classes and objects).

Files: `lab-u07-01-files/`, which holds `ShiftTally.sln`, the `TallyConsole` project, the `ShiftTally`
starter, and the `ShiftTally.SelfCheck` project.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every station, part, and count in this lab is invented. No hardware and no network are used.

**Where the files came from.** ShiftTally is adapted from the course's HMI anchor project, the
Week 13 starter app the instructor keeps. This lab gives you its window in pieces.

---

## The scenario

Press 2 on Line 3 counts good and scrapped parts on a clipboard, and the tally is often wrong by the
end of the shift. The supervisor wants a touch screen at the station with big buttons an operator in
gloves can press. Before any button can count, somebody has to build the window.

## What you will build

A WPF window, described in XAML, with every control the ShiftTally counter needs, named so that next
week's code can find it.

---

## Starter code

Copy `lab-u07-01-files/` into your repository. Add a `.gitignore` for .NET if your repository does not
have one:

```
dotnet new gitignore
```

`bin/` and `obj/` hold build output. They never go in a commit.

The starter builds and runs. `ShiftTally/MainWindow.xaml` shows a navy heading and the station row,
and nothing else. Its comments mark where rows 2 to 5 go. `MainWindow.xaml.cs` holds one method, the
constructor, which calls `InitializeComponent()`. `ShiftTally.SelfCheck` is a test project that opens
your window on a test thread and measures it.

**Read `MainWindow.xaml` before you change it.** Rows 0 and 1 show every idea you need today.

---

## Part 1 · Monday · A program that waits

### Step 1. Check the environment

In a terminal:

```
dotnet --list-sdks
dotnet --list-runtimes
```

**Observable result:** at least one SDK line, and a line that starts `Microsoft.WindowsDesktop.App 8.`
[VERIFY the versions on the lab image]. Paste both outputs into your lab notes. If the
`WindowsDesktop` line is missing, tell your teacher before you go on.

### Step 2. Create a WPF project

**In Visual Studio 2026:** File, New, Project. Choose "WPF Application" for C#. Name it `HelloLine3`.
Choose .NET 8 as the framework [VERIFY the menu path and template name on the lab image].

**Or from a terminal**, in your repository folder:

```
dotnet new wpf -n HelloLine3 --framework net8.0
```

**Observable result:** a `HelloLine3` folder holding `App.xaml`, `App.xaml.cs`, `AssemblyInfo.cs`,
`HelloLine3.csproj`, `MainWindow.xaml`, and `MainWindow.xaml.cs`.

### Step 3. Run the empty window

```
dotnet run --project HelloLine3
```

**Observable result:** an empty window titled `MainWindow`. The terminal does not return until you
close the window. Close it.

### Step 4. Make it count

Replace the whole of `HelloLine3/MainWindow.xaml` with:

```xml
<Window x:Class="HelloLine3.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Hello, Line 3" Height="300" Width="400">
    <StackPanel Margin="20">
        <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
        <Button x:Name="CountButton" Content="+1 PART" MinHeight="64" Click="OnCountClick" />
    </StackPanel>
</Window>
```

Replace the whole of `HelloLine3/MainWindow.xaml.cs` with:

```csharp
using System.Windows;

namespace HelloLine3;

public partial class MainWindow : Window
{
    private int parts;

    public MainWindow()
    {
        InitializeComponent();
    }

    private void OnCountClick(object sender, RoutedEventArgs e)
    {
        parts++;
        CountText.Text = $"Parts: {parts}";
    }
}
```

Run it and press the button three times.

**Observable result:** the text reads `Parts: 1`, `Parts: 2`, then `Parts: 3`. The build reported no
errors.

### Step 5. Break it on purpose

In the XAML, change `Click="OnCountClick"` to `Click="OnCountClik"`. Build:

```
dotnet build HelloLine3
```

**Observable result:** the build fails with an error that begins
`MainWindow.xaml(7,82): error CS1061: 'MainWindow' does not contain a definition for 'OnCountClik'`.
Copy the whole line into your lab notes. Under it, write one sentence: which file does the error
name, and why that file? Then fix the spelling and build again until it succeeds.

### Step 6. Run the procedural version

Run `TallyConsole` and type these keys, pressing Enter after each: `g`, `g`, `s`, `x`, `g`, `q`.

```
dotnet run --project TallyConsole
```

Then run it again with the keys coming from a file. PowerShell changes text sent through a pipe, so
use `cmd`:

```
cmd /c "dotnet run --project TallyConsole < TallyConsole\keys.txt"
```

**Observable result:** both runs print the same lines, ending with:

```
> Good: 3  Scrap: 1  Total: 4
> Shift over. 4 parts counted.
```

### Step 7. Compare the two programs

Copy this table into your lab notes. Fill every cell from the two programs you ran, not from memory.

| Question | TallyConsole | HelloLine3 |
|---|---|---|
| Which of the four styles does it use? (procedural, structured, object-oriented, event-driven) | | |
| Who decides what runs next? | | |
| Where is the program when nobody touches anything? | | |
| What happens if two inputs arrive at once? | | |
| How does it end? | | |

**Observable result:** ten filled cells. The "where is the program" row names a line of code for one
program and something other than your code for the other.

### Step 8. Sketch the event flow

On paper or in your notes, list every event `HelloLine3` responds to. For each: what raises it, what
handles it, and what changes. Include the app starting, the button press, and the window closing.

**Observable result:** at least three rows. The button row names `OnCountClick` and the two things it
changes. Commit `HelloLine3`, your notes, and the sketch.

---

## Part 2 · Tuesday · The ShiftTally window

### Step 9. Build and check the starter

From `lab-u07-01-files/`:

```
dotnet build ShiftTally.sln
dotnet test ShiftTally.sln
```

**Observable result:** the build succeeds. The test summary ends with
`Failed!  - Failed:    24, Passed:     4, Skipped:     0, Total:    28`. The first run restores
packages and takes longer. In Visual Studio, the Test Explorer shows the same checks
[VERIFY: Test, Test Explorer].

### Step 10. Read the plan

This is the window you are building, 900 by 600 pixels:

```
+------------------------------------------------------------------------+
| Press 2: Hinge bracket                                     (row 0, done) |
+------------------------------------------------------------------------+
| Station [Press 2      ]    Part [Hinge bracket            v] (row 1, done) |
| [ +1 GOOD ] [ +1 SCRAP ] [ UNDO LAST ] [ RESET SHIFT ]           (row 2) |
| Good: 0          Scrap: 0          Total: 0                      (row 3) |
| Shift target: 200   ----o-----------------------------          (row 4) |
| [==========                                     ]  progress            |
| 0 of 200 good parts                                                    |
| [x] Show scrap rate                                                    |
| Scrap rate: no parts yet                                               |
|                                                                        |
| Count each part as it leaves the station.        [ PRINT SUMMARY ] (row 5) |
+------------------------------------------------------------------------+
```

Every control below needs **exactly** this `x:Name`. Next week's handlers and the self-check find
controls by name.

| Row | `x:Name` | Type | Starts with |
|---|---|---|---|
| 0 | `HeadingText` | `TextBlock` | done |
| 1 | `StationBox`, `PartBox` | `TextBox`, `ComboBox` | done |
| 2 | `GoodButton` | `Button` | `Content="+1 GOOD"`, `Background="#DDE8F7"` |
| 2 | `ScrapButton` | `Button` | `Content="+1 SCRAP"`, `Background="#F6DADF"` |
| 2 | `UndoButton` | `Button` | `Content="UNDO LAST"`, `IsEnabled="False"` |
| 2 | `ResetButton` | `Button` | `Content="RESET SHIFT"` |
| 3 | `GoodText`, `ScrapText`, `TotalText` | `TextBlock` | `Good: 0`, `Scrap: 0`, `Total: 0` |
| 4 | `TargetText` | `TextBlock` | `Shift target: 200`, `Width="200"` |
| 4 | `TargetSlider` | `Slider` | `Minimum="50" Maximum="500" Value="200" TickFrequency="50" IsSnapToTickEnabled="True"` |
| 4 | `ShiftProgress` | `ProgressBar` | `Minimum="0" Maximum="100" Value="0" Height="34"` |
| 4 | `ProgressText` | `TextBlock` | `0 of 200 good parts` |
| 4 | `ShowRateBox` | `CheckBox` | `Content="Show scrap rate" IsChecked="True"` |
| 4 | `RateText` | `TextBlock` | `Scrap rate: no parts yet` |
| 5 | `PrintButton` | `Button` | `Content="PRINT SUMMARY"`, docked right |
| 5 | `StatusText` | `TextBlock` | `Count each part as it leaves the station.` |

**Observable result:** you can point at the XAML comment where each row goes.

### Step 11. Row 2: the counting buttons

Replace the row 2 comment with a `UniformGrid` in `Grid.Row="2"` with `Rows="1"` and
`Margin="14,16,14,0"`, holding the four buttons from the table, in order. Do not give the buttons a
height: the style in `Grid.Resources` already makes every button at least 64 pixels tall.

**Observable result:** `dotnet test` reports `Passed: 9` of 28, including
`TheFourCountingButtonsShareOneRowAtEqualWidths`.

### Step 12. Row 3: the counts

Replace the row 3 comment with a `StackPanel` in `Grid.Row="3"` with `Orientation="Horizontal"` and
`Margin="20,16,20,0"`. Inside, the three count `TextBlock` elements, each with `FontSize="28"` and
`Width="220"`. Make the good and scrap counts bold with `FontWeight="Bold"`.

**Observable result:** `Passed: 13` of 28, including `TheCountsStartAtZero`.

### Step 13. Row 4: the target, progress, and rate

Replace the row 4 comment with a `StackPanel` in `Grid.Row="4"` with `Margin="20,16,20,0"`. Inside, in
this order:

1. A `DockPanel` holding `TargetText` and then `TargetSlider`. Add `TickPlacement="BottomRight"` and
   `VerticalAlignment="Center"` to the slider. A `DockPanel` gives its last child the rest of the
   width, so the slider stretches.
2. `ShiftProgress`, with `Margin="0,12,0,0"` and `Foreground="#57A1EB"`.
3. `ProgressText`, with `Margin="0,4,0,0"`.
4. `ShowRateBox`, with `FontSize="18"` and `Margin="0,12,0,0"`.
5. `RateText`, with `FontSize="24"`, `FontWeight="SemiBold"`, and `Margin="0,6,0,0"`.

**Observable result:** `Passed: 21` of 28, including `TheSliderFollowsTheShiftRules` and
`ProgressAndScrapRateStartEmpty`.

### Step 14. Row 5: the status line and PRINT

Replace the row 5 comment with a `DockPanel` in `Grid.Row="5"` with `Margin="14,0,14,8"` and
`VerticalAlignment="Bottom"`. Put `PrintButton` first, with `DockPanel.Dock="Right"`. Then
`StatusText`, with `Foreground="#5A5A5A"`, `VerticalAlignment="Center"`, and `TextWrapping="Wrap"`.

**Observable result:** `dotnet test` ends with
`Passed!  - Failed:     0, Passed:    28, Skipped:     0, Total:    28`.

### Step 15. Look at your window

The check `SavesAPictureOfYourWindow` wrote a picture. Find it under
`ShiftTally.SelfCheck/bin/Debug/net8.0-windows/window-pictures/ShiftTally-U07-01.png` and open it.
Then run the app itself:

```
dotnet run --project ShiftTally
```

**Observable result:** the picture and the running window match the plan in step 10. UNDO LAST is
greyed out. Nothing responds when you press it. That is tomorrow. Close the window.

### Step 16. Use the designer once

In Visual Studio, open `MainWindow.xaml` in the designer. Click `+1 GOOD` on the design surface.
In the Properties window, change its `Background` to another color [VERIFY the panel names in
Visual Studio 2026]. Look at the XAML.

**Observable result:** the designer changed the `Background` attribute in the XAML. Write one
sentence in your notes about what the designer did to the file. Change the color back to `#DDE8F7`,
run `dotnet test` again for 28 of 28, and commit.

### Acceptance criteria, full lab

- [ ] Your notes hold the `dotnet --list-sdks` output and the CS1061 line with your sentence
- [ ] `HelloLine3` counts presses and is committed without `bin/` or `obj/`
- [ ] The comparison table has ten filled cells
- [ ] The `HelloLine3` event flow sketch has at least three rows
- [ ] `dotnet test ShiftTally.sln` reports 28 of 28
- [ ] Every control has the exact `x:Name` from step 10
- [ ] Your notes say what the designer did to the XAML
- [ ] Committed and pushed at the end of both days

---

## If it breaks

### 1. A handler name that matches nothing

```
MainWindow.xaml(7,82): error CS1061: 'MainWindow' does not contain a definition for 'OnCountClik' and no accessible extension method 'OnCountClik' accepting a first argument of type 'MainWindow' could be found (are you missing a using directive or an assembly reference?)
```

**Cause:** the event attribute names a method the class does not have. Check the spelling in both
files. The numbers in brackets are the line and column in the XAML.

### 2. Two elements where one belongs

```
MainWindow.xaml(6,6): error MC3089: The object 'Window' already has a child and cannot add 'Button'. 'Window' can accept only one child. Line 6 Position 6.
```

**Cause:** a `Window` (or a `Border`) holds exactly one child. Put the elements inside a panel. In
ShiftTally, every row goes inside the `Grid`, never directly inside the `Window`.

### 3. A misspelled attribute

```
MainWindow.xaml(7,38): error MC3072: The property 'Contnet' does not exist in XML namespace 'http://schemas.microsoft.com/winfx/2006/xaml/presentation'. Line 7 Position 38.
```

**Cause:** there is no property with that name. XAML attribute names are checked like method names.

### 4. A tag that does not close

```
MainWindow.xaml(8,7): error MC3000: 'The 'TextBlock' start tag on line 6 position 10 does not match the end tag of 'StackPanel'. Line 8, position 7.' XML is not valid.
```

**Cause:** an element that should end with `/>` ends with `>`. The message names the line where the
parser noticed (8) and the line where the mistake is (6). Fix line 6.

### Also likely: the same name twice

```
MainWindow.xaml(8,49): error CS0102: The type 'MainWindow' already contains a definition for 'CountText'
```

**Cause:** two elements share an `x:Name`. Each name becomes a field, and a class cannot have two
fields with one name.

### Not an error: a check that says a control is missing

```
No control named TargetSlider. Check the x:Name in MainWindow.xaml.
```

**Cause:** the self-check could not find that name. Look for a spelling or capitalization
difference. `targetSlider` is not `TargetSlider`.

---

## Stretch goal

Add a fifth counting button, `ReworkButton`, reading `+1 REWORK`, to row 2, and run `dotnet test`.
All 28 checks still pass. Open the picture: the five buttons share the row, and the labels barely
fit. Write in your notes why no check noticed the new button, and describe a check that would fail if
a label were cut off. Then remove the button.

---

## Submission checklist

- [ ] `HelloLine3` committed, with a `.gitignore` that excludes `bin/` and `obj/`
- [ ] Lab notes: SDK output, the CS1061 line and sentence, the comparison table, the event flow sketch,
      the designer sentence
- [ ] `dotnet test ShiftTally.sln`: 28 of 28
- [ ] Pushed at the end of Monday and at the end of Tuesday
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At the start of Tuesday Build 2, the student has fewer than 13 of 28 checks passing | SCAFFOLDED |
| Steady progress through the rows, questions about panel behavior | STANDARD |
| 28 of 28 before Tuesday Build 2 is half over | EXTENDED |
| The student asks why anyone builds a window for a factory | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** your teacher gives you rows 2 and 3 already written. You write rows 4 and 5.
- **Steps:** skip step 16. Do steps 13 and 14 with the table in step 10 open beside you.
- **Checkpoints:** show your teacher `dotnet test` after step 13 (21 of 28) and after step 14.

**Acceptance criteria:** 28 of 28, the Part 1 notes, and a commit at the end of each day.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a layout rule the lab has not taught.

**Added requirement.** Operators on Line 3 sometimes run the panel on a smaller screen. At the
window's minimum size the layout breaks in a way the self-check does not notice: rendered at 700 by
560, the labels `UNDO LAST` and `RESET SHIFT` are cut off, and all 28 checks still pass. A real window
is worse, because its frame takes some of that space. Make the window usable at its minimum size with
every label readable. You may not change `MinWidth` or `MinHeight`, and you may not remove a control.

**Hint, not the answer.** Look up `Viewbox` and `ScrollViewer` in the WPF controls documentation on
Microsoft Learn, starting from `https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/`
[VERIFY]. One of them scales its content. The other lets content scroll. Decide which suits an
operator in gloves, and write the decision and the rejected option in your decision log.

**Acceptance criteria:** all STANDARD criteria still pass at 900 by 600; the running window, dragged
to its smallest size, shows every control with every label readable; a decision log entry names the
option you chose and the one you rejected. To check the smaller size without dragging, change `Width`
and `Height` at the top of `WpfTestHost.cs` to 700 and 560 in a copy, and open the picture.

**Grading:** same scale.

---

## APPLIED

**For the student who asks why anyone builds a window for a factory.** The same skill, somewhere else.

**Changed scenario.** The school's robotics club tracks practice runs on a whiteboard: runs completed,
runs that failed, and a target for the session. Build the window for a tablet by the practice field.
Use invented robot names only. No student names appear anywhere.

**What you build.** A window with the same six-row structure: a heading, a robot picker (a
`ComboBox`), four big buttons (`+1 RUN`, `+1 FAILED RUN`, `UNDO LAST`, `RESET SESSION`), three counts,
a target slider with a progress bar, and a status line with a `SAVE NOTES` button. Name every control.
Write a table like the one in step 10 for your window before you write XAML.

**Acceptance criteria:** the window builds and shows every control; your table matches your XAML
names; every button is at least 64 pixels tall. You may copy `ShiftTally.SelfCheck` and change the
names in `LayoutChecks.cs` to check your own window, and your teacher gives credit for doing so.

**Grading:** same scale. Requirements Fit is judged on whether the layout would work for a person
standing at a practice field.

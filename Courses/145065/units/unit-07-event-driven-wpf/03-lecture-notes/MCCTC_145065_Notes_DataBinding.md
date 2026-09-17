# Lecture Notes: Binding a Control to a Property
## 145065 Object-Oriented Programming · Unit 7 · Week 14, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W14_DataBinding.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W14_DataBinding.md --export pptx`

If you missed class, including for BPA Nationals, you can learn this concept from this file alone. You
need the .NET SDK and the Lab U07-03 files.

**Competencies:** 5.5.6 format output. 5.4.2 write and edit code in the IDE.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

After Monday, the view model holds every value. Something still has to copy those values onto the
screen, and last week that was `ShowCounts`: ten lines of `SomeText.Text = ...` that had to be
called after every change, in every handler. Forget one call and the screen is wrong.

**Data binding** replaces that copying. You tell each control, once, which property it shows. WPF
does the copying.

---

## The concept in plain language

A binding connects a **target** (a property on a control, such as `TextBlock.Text`) to a **source**
(a property on an object, such as `TallyViewModel.Good`).

```xml
<TextBlock Text="{Binding Good, StringFormat=Good: {0}}" />
```

Read it as: "this TextBlock's `Text` is the `Good` property of my data, shown as `Good: 3`."

Four ideas make bindings work:

1. **`DataContext` is where bindings look.** Set it once on the window, and every element inside
   inherits it. In ShiftTally: `DataContext = Tally;` after `InitializeComponent()`.
2. **Direction.** Most bindings are one-way: source to screen. A `TextBox`'s `Text`, a `Slider`'s
   `Value`, a `CheckBox`'s `IsChecked`, and a `ComboBox`'s `SelectedItem` are two-way by default, so
   the operator's change is written back to the source.
3. **Timing.** A two-way `TextBox` writes back when it **loses focus**, unless you add
   `UpdateSourceTrigger=PropertyChanged`, which writes back on every keystroke.
4. **Formatting.** `StringFormat` shapes the text. A **converter** changes the type, such as
   `BooleanToVisibilityConverter`, which turns `true` into `Visible` and `false` into `Collapsed`.

| What the operator sees | The binding |
|---|---|
| `Good: 37` | `Text="{Binding Good, StringFormat=Good: {0}}"` |
| the station name, editable | `Text="{Binding Station, UpdateSourceTrigger=PropertyChanged}"` |
| the part list and the chosen part | `ItemsSource="{Binding PartTypes}" SelectedItem="{Binding PartType}"` |
| the target slider | `Value="{Binding Target}"` |
| the progress bar | `Value="{Binding Progress, Mode=OneWay}"` |
| UNDO greyed out when there is nothing to undo | `IsEnabled="{Binding CanUndo}"` |
| the scrap rate, hidden by the check box | `Visibility="{Binding ShowScrapRate, Converter={StaticResource Visible}}"` |

The `Visible` converter is declared once in the window's resources:
`<BooleanToVisibilityConverter x:Key="Visible" />`.

---

## Worked example 1: a one-way binding with a format

`Shift` here is a plain class with `Station`, `Scrap`, and `Target` properties.

```csharp
Shift shift = new() { Station = "Press 2", Scrap = 3 };
TextBlock scrapText = new() { DataContext = shift };
scrapText.SetBinding(TextBlock.TextProperty, new Binding("Scrap") { StringFormat = "Scrap: {0}" });
TextBlock stationText = new() { DataContext = shift };
stationText.SetBinding(TextBlock.TextProperty, new Binding("Station"));
Console.WriteLine(scrapText.Text);
Console.WriteLine(stationText.Text);
```

Output:

```
Scrap: 3
Press 2
```

`SetBinding` in C# is what `{Binding ...}` does in XAML. Nobody wrote `scrapText.Text = ...`.

---

## Worked example 2: two-way bindings, and why the trigger matters

```csharp
Shift shift = new() { Station = "Press 2" };

TextBox lazyBox = new() { DataContext = shift };
lazyBox.SetBinding(TextBox.TextProperty, new Binding("Station"));
lazyBox.Text = "Press 4";
Console.WriteLine($"Default trigger, after typing:        Station = {shift.Station}");

TextBox eagerBox = new() { DataContext = shift };
eagerBox.SetBinding(TextBox.TextProperty,
    new Binding("Station") { UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged });
eagerBox.Text = "Press 5";
Console.WriteLine($"PropertyChanged trigger, after typing: Station = {shift.Station}");

Slider slider = new() { Minimum = 50, Maximum = 500, DataContext = shift };
slider.SetBinding(RangeBase.ValueProperty, new Binding("Target"));
slider.Value = 300;
Console.WriteLine($"Slider moved to 300:                   Target = {shift.Target}");
```

Output:

```
Default trigger, after typing:        Station = Press 2
PropertyChanged trigger, after typing: Station = Press 5
Slider moved to 300:                   Target = 300
```

The first box changed its text, and the source did not hear about it: that box never lost focus.
The heading in ShiftTally depends on the station name, so the lab's box uses `PropertyChanged`. The
slider wrote back at once, and WPF converted the slider's `double` to the property's `int` for you.

---

## Worked example 3: bindings written in XAML

```csharp
string xaml = """
    <StackPanel xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
        <TextBlock Text="{Binding Station}" />
        <TextBlock Text="{Binding Scrap, StringFormat=Scrap: {0}}" />
        <TextBlock Text="{Binding Target, StringFormat=Shift target: {0}}" />
    </StackPanel>
    """;
StackPanel panel = (StackPanel)XamlReader.Parse(xaml);
panel.DataContext = new Shift { Station = "Press 2", Scrap = 3, Target = 150 };
RunQueue();   // bindings made by the XAML reader connect on the dispatcher's next pass
foreach (TextBlock line in panel.Children)
{
    Console.WriteLine(line.Text);
}
```

`RunQueue` is a three-line helper in the unit's verification program: it lets the dispatcher work
through its queue once, the way a running window does. Output:

```
Press 2
Scrap: 3
Shift target: 150
```

Two things to see. The three TextBlocks never set `DataContext`; they inherited it from the panel.
And the build machine's first attempt printed three blank lines, because it read the text before the
dispatcher had connected the bindings. In a running window that pass happens before the operator
sees anything.

---

## Worked example 4: the ShiftTally window, bound

From the Lab U07-03 solution:

```xml
<TextBlock x:Name="HeadingText" Text="{Binding Heading}"
           FontSize="30" FontWeight="Bold" Foreground="White" />

<TextBox x:Name="StationBox" MaxLength="20" FontSize="20" Padding="6"
         Text="{Binding Station, UpdateSourceTrigger=PropertyChanged}" />

<ComboBox x:Name="PartBox" FontSize="20" Padding="6"
          ItemsSource="{Binding PartTypes}" SelectedItem="{Binding PartType}" />

<Button x:Name="UndoButton" Content="UNDO LAST" Click="OnUndoClick"
        IsEnabled="{Binding CanUndo}" />

<TextBlock x:Name="GoodText" Text="{Binding Good, StringFormat=Good: {0}}"
           FontSize="28" FontWeight="Bold" Width="220" />
```

```csharp
public MainWindow()
{
    InitializeComponent();
    Confirm = AskYesNo;
    DataContext = Tally;
}
```

`ShowCounts`, `ShowHeading`, and the `windowBuilt` flag are gone. The Lab U07-03 self-check confirms
15 bound properties with `BindingOperations.IsDataBound`.

---

## The wrong version, and what it produces

Misspell a binding path:

```csharp
TextBlock scrapText = new() { DataContext = new Shift { Scrap = 3 } };
scrapText.SetBinding(TextBlock.TextProperty, new Binding("Scarp") { StringFormat = "Scrap: {0}" });
Console.WriteLine($"The TextBlock shows: \"{scrapText.Text}\"");
```

**The build succeeds.** The program runs. The text is blank, and WPF writes a line to the debug
output:

```
System.Windows.Data Error: 40 : BindingExpression path error: 'Scarp' property not found on 'object' ''Shift' (HashCode=45638969)'. BindingExpression:Path=Scarp; DataItem='Shift' (HashCode=45638969); target element is 'TextBlock' (Name=''); target property is 'Text' (type 'String')
The TextBlock shows: ""
```

The compiler cannot check a path inside `{Binding ...}`; it is a string. Visual Studio shows these
lines in the Output window while the app runs under the debugger [VERIFY, and look for a "XAML
Binding Failures" window in Visual Studio 2026]. The Lab U07-03 self-check listens for them in
`NoBindingPathIsMisspelled`. The `HashCode` numbers change from run to run.

**The other thing that goes wrong on Tuesday is not a mistake.** Bind everything, press +1 GOOD,
and the count does not change on screen, although `Tally.Good` went up. The binding read `Good`
once, and nothing told it to read again. That is Wednesday.

**One control will seem to work anyway.** Drag the slider, and the "Shift target" text follows it.
That change went through a binding, so WPF told the other binding on the same property of the same
object. The progress text, which is computed from `Target`, does not move. Nothing told WPF that it
depends on `Target`. The Lab U07-03 check `ProgressFollowsTheSlider` found exactly that: the target
text read `Shift target: 100` while the progress text still read `0 of 200 good parts`.

---

## Why the wrong version is tempting

A binding path looks like code, so it feels checked. It is text that WPF looks up at run time. A
typo fails quietly and shows an empty space, which on a busy screen goes unnoticed.

The habit that prevents it: after you add bindings, run with the debugger and read the Output window
before you look at the screen. An empty Output window is a better sign than a screen that looks
right.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Data binding** | a connection that copies a source property into a control property |
| **Target** | the control property a binding sets |
| **Source** | the object property a binding reads, and may write back to |
| **`DataContext`** | the default source for bindings, inherited by child elements |
| **Path** | the name of the source property, such as `Good` |
| **One-way, two-way** | copies to the screen only, or also back from the screen |
| **`UpdateSourceTrigger`** | when a two-way binding writes back: on focus loss or on every change |
| **`StringFormat`** | a format pattern such as `Good: {0}` |
| **Converter** | an object that changes a value's type or form, such as `BooleanToVisibilityConverter` |

---

## Self-check

**Question 1.** `Target` is 150. What does `Text="{Binding Target, StringFormat=Shift target: {0}}"`
show?

**Question 2.** A student binds the station box as `Text="{Binding Station}"`. The heading updates
only after the student clicks somewhere else. Why, and what one change fixes it?

**Question 3.** After binding everything, a student presses +1 GOOD five times. The debugger shows
`Tally.Good` is 5. The screen says `Good: 0`. The Output window has no binding errors. What is
missing?

---

### Answers

**1.** `Shift target: 150`.

**2.** A two-way `TextBox` binding writes back when the box loses focus by default. Add
`UpdateSourceTrigger=PropertyChanged` so it writes back on every keystroke.

**3.** The view model never announced that `Good` changed, so the binding never read it again. It
needs `INotifyPropertyChanged`, Wednesday's concept. No binding error appears because the path is
correct.

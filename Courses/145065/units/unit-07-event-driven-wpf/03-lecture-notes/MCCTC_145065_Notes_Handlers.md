# Lecture Notes: A Handler Is a Method WPF Calls for You
## 145065 Object-Oriented Programming · Unit 7 · Week 13, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W13_Handlers.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W13_Handlers.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and the
Lab U07-02 files.

**Competencies:** 5.3.12 write code that creates classes, objects, and methods. 5.4.2 write and edit
code in the IDE.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

A window that only shows things is a poster. The operator has to be able to change something: count
a part, move a target, type a station name. Each of those is an event, and each needs code that runs
when it happens.

That code has rules the compiler enforces and one rule it cannot: **WPF may call your handler at
moments you did not expect**, including while the window is still being built.

---

## The concept in plain language

A handler is an ordinary method on the window class. Two things make it a handler:

1. **An event attribute names it.** `Click="OnGoodClick"` on a button. The build connects the two.
2. **Its parameters match the event.** Every WPF event passes two things:
   - `sender`: the control that raised the event, typed as `object`.
   - `e`: the details. For `Click` it is `RoutedEventArgs`. For a slider's `ValueChanged` it is
     `RoutedPropertyChangedEventArgs<double>`, which carries `OldValue` and `NewValue`.

| Control | Event you will use | What it tells you |
|---|---|---|
| `Button` | `Click` | it was pressed |
| `Slider` | `ValueChanged` | `e.NewValue` and `e.OldValue` |
| `TextBox` | `TextChanged` | read the box's `Text` |
| `ComboBox` | `SelectionChanged` | read the box's `SelectedItem` |
| `CheckBox` | `Checked` and `Unchecked` | read the box's `IsChecked` |

A handler usually does three things: change the state, update what the screen shows, and tell the
operator what happened. The Lab U07-02 `OnGoodClick`:

```csharp
private void OnGoodClick(object sender, RoutedEventArgs e)
{
    good++;
    history.Push(true);
    ShowCounts();
    StatusText.Text = "Counted one good part.";
}
```

**You can attach a handler in XAML or in C#**, but never both for the same event. XAML is the usual
place. `GoodButton.Click += OnGoodClick;` in code does the same job, and doing both runs the handler
twice per press.

---

## Worked example 1: one handler, three buttons

`sender` tells a shared handler which button was pressed:

```csharp
int burr = 0;
int bent = 0;
int hole = 0;
Button burrButton = new() { Name = "BurrButton", Content = "+1 BURR" };
Button bentButton = new() { Name = "BentButton", Content = "+1 BENT" };
Button holeButton = new() { Name = "HoleButton", Content = "+1 WRONG HOLE" };

void OnReasonClick(object sender, RoutedEventArgs e)
{
    Button pressed = (Button)sender;
    switch (pressed.Name)
    {
        case "BurrButton":
            burr++;
            break;
        case "BentButton":
            bent++;
            break;
        case "HoleButton":
            hole++;
            break;
    }

    Console.WriteLine($"{pressed.Content}: burr {burr}, bent {bent}, hole {hole}");
}

burrButton.Click += OnReasonClick;
bentButton.Click += OnReasonClick;
holeButton.Click += OnReasonClick;

burrButton.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
holeButton.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
burrButton.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
```

Output:

```
+1 BURR: burr 1, bent 0, hole 0
+1 WRONG HOLE: burr 1, bent 0, hole 1
+1 BURR: burr 2, bent 0, hole 1
```

`sender` arrives as `object`, so the handler casts it to `Button` before reading its name. The
`RaiseEvent` lines stand in for three presses.

---

## Worked example 2: events that carry a value

```csharp
Slider target = new() { Minimum = 50, Maximum = 500, Value = 200 };
target.ValueChanged += (sender, e) =>
    Console.WriteLine($"ValueChanged: {e.OldValue} to {e.NewValue}");

TextBox station = new();
station.TextChanged += (sender, e) =>
    Console.WriteLine($"TextChanged: \"{((TextBox)sender).Text}\"");

target.Value = 350;
target.Value = 9000;
station.Text = "P";
station.Text = "Pr";
```

Output:

```
ValueChanged: 200 to 350
ValueChanged: 350 to 500
TextChanged: "P"
TextChanged: "Pr"
```

Two things to notice. The slider refused 9000 and reported 500, its `Maximum`. And `TextChanged`
fires on every change, one character at a time, which is what a live heading needs.

In the lab, the slider's handler stores the new target. Slider values are `double`, so it casts:

```csharp
private void OnTargetChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    target = (int)e.NewValue;
    ShowCounts();
}
```

---

## Worked example 3: a handler attached twice runs twice

```csharp
int good = 0;
Button goodButton = new() { Content = "+1 GOOD" };
void OnGoodClick(object sender, RoutedEventArgs e) => good++;

goodButton.Click += OnGoodClick;   // as if the XAML attached it
goodButton.Click += OnGoodClick;   // and the constructor attached it again

goodButton.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
Console.WriteLine($"One press, good is {good}");

goodButton.Click -= OnGoodClick;
goodButton.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
Console.WriteLine($"After removing one, the next press makes good {good}");
```

Output:

```
One press, good is 2
After removing one, the next press makes good 3
```

No error, no warning. An event keeps a list of handlers, and the same method can be on the list
twice. A test that presses once and checks for exactly one change is how you catch it.

---

## Worked example 4: a destructive handler asks first

RESET throws away a shift's counts, so it asks. The lab calls a replaceable `Confirm` function
instead of a message box directly, so the self-check can answer for the operator:

```csharp
private void OnResetClick(object sender, RoutedEventArgs e)
{
    int total = good + scrap;
    if (!Confirm($"Reset {total} counted parts to zero? This cannot be undone."))
    {
        StatusText.Text = "Reset cancelled. The counts are kept.";
        return;
    }

    good = 0;
    scrap = 0;
    history.Clear();
    ShowCounts();
    StatusText.Text = "Counts reset.";
}
```

In the running app, `Confirm` shows a Yes/No message box with **No** as the default, so a stray
Enter key does not wipe a shift. The Lab U07-02 checks `ResetAsksFirstAndKeepsTheCountsOnNo` and
`ResetClearsEverythingOnYes` pass against this handler.

---

## The wrong version, and the errors it produces

**A handler with the wrong parameters.** Write `private void OnCountClick()` with no parameters:

```
MainWindow.xaml(7,39): error CS0123: No overload for 'OnCountClick' matches delegate 'RoutedEventHandler'
```

`RoutedEventHandler` is the shape `Click` requires: `(object sender, RoutedEventArgs e)`.

**A handler that runs before the window exists.** This is the one that surprises everyone. A slider
declared above the text it updates:

```xml
<Slider x:Name="TargetSlider" Minimum="50" Maximum="500" Value="200" ValueChanged="OnTargetChanged" />
<TextBlock x:Name="TargetText" Text="Shift target: 200" />
```

```csharp
private void OnTargetChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    TargetText.Text = $"Shift target: {(int)e.NewValue}";
}
```

The window never opens. Creating it throws:

```
System.NullReferenceException: Object reference not set to an instance of an object.
```

Nobody touched the slider. While `InitializeComponent` built the slider, setting `Minimum="50"`
moved its value from 0 to 50, and that raised `ValueChanged`. The handler ran before `TargetText`
existed. A logging line in the handler recorded `ValueChanged 0 -> 50` and `TargetText null=True`.

The lab's fix is a flag the constructor sets when the window is finished:

```csharp
private readonly bool windowBuilt;

public MainWindow()
{
    InitializeComponent();
    Confirm = AskYesNo;
    windowBuilt = true;
    ShowCounts();
}

private void ShowCounts()
{
    if (!windowBuilt)
    {
        return;   // still inside InitializeComponent: some controls do not exist yet
    }

    // ...
}
```

With that guard removed from the Lab U07-02 solution, all 18 self-checks failed with the same
exception, thrown from `OnStationChanged`: the station box's `Text="Press 2"` fires `TextChanged`
during construction too.

---

## Why the wrong version is tempting

The mental picture is "handlers run when the operator does something." That is true after the
window opens. During construction, WPF sets each property you wrote in XAML, one at a time, and a
property change is an event. The XAML looks like a finished screen, so it is hard to imagine it half
built.

Week 14 removes most of this risk. When handlers stop writing to controls and bindings do the work
instead, there is no half-built control for a handler to touch.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Event attribute** | a XAML attribute such as `Click="OnGoodClick"` that attaches a handler |
| **`sender`** | the object that raised the event |
| **Event arguments** | the second parameter, carrying details such as `NewValue` |
| **Delegate** | a type that describes a method's shape, such as `RoutedEventHandler` |
| **`+=` and `-=`** | attach and detach a handler in C# |
| **Seam** | a replaceable piece, such as `Confirm`, that lets a test stand in for a person |

---

## Self-check

**Question 1.** Which parameter tells a shared handler which button was pressed, and what type does
it arrive as?

**Question 2.** A student's GOOD button adds 2 per press. The handler body is `good++; ShowCounts();`.
Name the two places to look.

**Question 3.** Why does this handler, attached to a slider declared at the top of the window, crash
the app before it opens, and what are two fixes?

```csharp
private void OnTargetChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    ProgressText.Text = $"{good} of {(int)e.NewValue} good parts";
}
```

---

### Answers

**1.** `sender`, which arrives as `object`. Cast it to `Button` to read its `Name` or `Content`.

**2.** The XAML, for `Click="OnGoodClick"`, and the C#, for a `GoodButton.Click += OnGoodClick;` line.
If both exist, the handler runs twice.

**3.** Setting the slider's `Minimum` during `InitializeComponent` raises `ValueChanged` before
`ProgressText` exists, so `ProgressText` is `null`. Fixes: guard the handler with a flag set at the end
of the constructor, or attach the handler in code after `InitializeComponent()`.

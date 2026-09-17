# Lecture Notes: Programs That Wait
## 145065 Object-Oriented Programming · Unit 7 · Week 13, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W13_ProgramsThatWait.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W13_ProgramsThatWait.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and the
Lab U07-01 files.

**Competencies:** 5.1.4 describe, compare, and contrast procedural, structured, object-oriented, and
event-driven programming. 5.4.2 write and edit code in the IDE.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described.

---

## Why this exists

Every program you have written so far was in charge. A script ran from the top. A loop asked a
question, waited for the answer, and decided what to do next.

An operator panel cannot work that way. The operator might press any button, in any order, at any
moment. A sensor reading might arrive in the middle of a press. A program that asks one question at
a time would miss everything else.

**An event-driven program gives up control on purpose.** It sets things up, then waits for things to
happen, and reacts to each one. Every desktop app, phone app, and web page you use works this way.

---

## The concept in plain language

There are four ways to organize a program, and the WebXam asks you to tell them apart.

| Style | Who decides what runs next | Where the program waits | Example you have written |
|---|---|---|---|
| **Procedural** | your code, top to bottom, with calls to functions | wherever your code asks for input | a 145060 script with functions |
| **Structured** | your code, using only sequence, selection, and loops (no jumps) | the same places | every loop you have written |
| **Object-oriented** | your code, calling methods on objects that bundle data and behavior | the same places | your Unit 2 class hierarchy |
| **Event-driven** | **the event loop**, which calls your methods when events happen | **inside the event loop, which you did not write** | today's window |

The styles combine. A WPF app is object-oriented (the window is an object) and event-driven (the
window waits for events), and each handler inside it is structured code.

**An event** is something that happens: a click, a key, a timer tick, a window opening. **A handler**
is a method you attach to an event. **The event loop** waits for the next event, calls every handler
attached to it, one at a time, and waits again. In WPF the event loop is called the **dispatcher**.

---

## Worked example 1: a procedural program waits in one place

`TallyConsole` in the Lab U07-01 files:

```csharp
int good = 0;
int scrap = 0;

Console.WriteLine("Shift tally for Press 2.");
Console.WriteLine("Type g for a good part, s for scrap, q to quit.");

while (true)
{
    Console.Write("> ");
    string? input = Console.ReadLine();   // the program waits here, and only here

    if (input is null || input == "q")
    {
        break;
    }

    if (input == "g")
    {
        good++;
    }
    else if (input == "s")
    {
        scrap++;
    }
    else
    {
        Console.WriteLine("Unknown key. Type g, s, or q.");
        continue;
    }

    Console.WriteLine($"Good: {good}  Scrap: {scrap}  Total: {good + scrap}");
}

Console.WriteLine($"Shift over. {good + scrap} parts counted.");
```

With the keys `g g s x g q` typed in, it printed:

```
Shift tally for Press 2.
Type g for a good part, s for scrap, q to quit.
> Good: 1  Scrap: 0  Total: 1
> Good: 2  Scrap: 0  Total: 2
> Good: 2  Scrap: 1  Total: 3
> Unknown key. Type g, s, or q.
> Good: 3  Scrap: 1  Total: 4
> Shift over. 4 parts counted.
```

The loop is yours. The program can only ever be waiting at `Console.ReadLine()`. Nothing else can
happen while it waits there.

---

## Worked example 2: an event without a window

C# has events built in. This `Sensor` class raises one each time it takes a reading:

```csharp
public sealed class Sensor
{
    public event EventHandler<double>? ReadingTaken;

    public void Take(double value) => ReadingTaken?.Invoke(this, value);
}
```

Two handlers attach to it with `+=`:

```csharp
Sensor oven = new();
oven.ReadingTaken += ShowOnPanel;
oven.ReadingTaken += WriteToLog;
Console.WriteLine("Subscribed. Nothing has happened yet.");
oven.Take(212.4);
oven.Take(236.0);

static void ShowOnPanel(object? sender, double value) => Console.WriteLine($"Panel: {value} C");
static void WriteToLog(object? sender, double value) => Console.WriteLine($"Log:   {value} C");
```

Output:

```
Subscribed. Nothing has happened yet.
Panel: 212.4 C
Log:   212.4 C
Panel: 236 C
Log:   236 C
```

Attaching a handler runs nothing. Each event runs every attached handler, in the order they were
attached. The sensor does not know or care who is listening. (`236.0` prints as `236` because C#
drops a zero decimal part when it turns a `double` into text.)

---

## Worked example 3: a WPF button is an event source

A `Button` raises `Click`. Here the click is raised in code so you can see the output:

```csharp
Button good = new() { Content = "+1 GOOD" };
int count = 0;
good.Click += (sender, e) =>
{
    count++;
    Console.WriteLine($"Click handled. Count is {count}.");
};
Console.WriteLine($"Handler attached. Count is {count}.");
good.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
good.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
```

Output:

```
Handler attached. Count is 0.
Click handled. Count is 1.
Click handled. Count is 2.
```

In a real window you never call `RaiseEvent`. A mouse press does, through WPF.

---

## Worked example 4: the event loop runs one item at a time

The dispatcher keeps a queue. `BeginInvoke` adds work to the end of it:

```csharp
Dispatcher ui = Dispatcher.CurrentDispatcher;
ui.BeginInvoke(() => Console.WriteLine("3. the first queued item runs"));
ui.BeginInvoke(() => Console.WriteLine("4. the second queued item runs"));
Console.WriteLine("1. still running the current item");
Console.WriteLine("2. the current item ends");
```

After the dispatcher is allowed to run its queue, the output is:

```
1. still running the current item
2. the current item ends
3. the first queued item runs
4. the second queued item runs
```

Queued work waits until the current work finishes. **A click is queued work too.** That fact is
Thursday's whole lesson.

---

## Worked example 5: your first window

`dotnet new wpf -n HelloLine3 --framework net8.0` makes a project. Its window, after you edit it:

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

```csharp
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

There is no loop in either file. `App.xaml` names this window, WPF opens it, and WPF waits. Each
press queues a `Click`, and the dispatcher calls `OnCountClick`.

---

## The wrong version, and the error it produces

A handler must have the shape the event expects. `ReadingTaken` passes a sender and a value:

```csharp
Sensor oven = new();
oven.ReadingTaken += ShowOnPanel;
oven.Take(212.4);

static void ShowOnPanel(double value) => Console.WriteLine($"Panel: {value} C");
```

The build stops:

```
Program.cs(2,1): error CS0123: No overload for 'ShowOnPanel' matches delegate 'EventHandler<double>'
```

`EventHandler<double>` means "a method that takes an `object?` sender and a `double`." The fix is
the two-parameter version in worked example 2.

In WPF the same mistake points at the XAML. Misspell the handler as `Click="OnCountClik"` and the
build reports:

```
MainWindow.xaml(7,82): error CS1061: 'MainWindow' does not contain a definition for 'OnCountClik' and no accessible extension method 'OnCountClik' accepting a first argument of type 'MainWindow' could be found (are you missing a using directive or an assembly reference?)
```

The file is `MainWindow.xaml`, line 7, column 82. The build compiles your XAML into C#, so a name in
the XAML must match a method in the class.

---

## Why the wrong version is tempting

In Python, any function could be passed anywhere, and a mismatch failed only when it ran. C# checks
the shape at build time. The error feels like the compiler being fussy. It is the compiler refusing
to wire a handler that would have crashed on the first event.

The worse mistake does not produce an error at all: **forgetting to attach the handler.** The event
still happens, nobody is listening, and nothing runs. When a button does nothing, check the event
attribute before you check the method.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Procedural programming** | code organized as steps and function calls, deciding its own order |
| **Structured programming** | code built only from sequence, selection, and repetition |
| **Object-oriented programming** | code organized as objects that bundle data with the methods that use it |
| **Event-driven programming** | code organized as handlers that run when events happen |
| **Event** | something that happens that code can react to |
| **Handler** | a method attached to an event |
| **Event loop** | the loop that waits for events and calls their handlers |
| **Dispatcher** | WPF's event loop, which runs on the UI thread |
| **Subscribe** | attach a handler, with `+=` in C# or an event attribute in XAML |

---

## Self-check

**Question 1.** In `TallyConsole`, where is the program when nobody is typing? In `HelloLine3`, where
is it when nobody is touching the mouse?

**Question 2.** A WPF app is described as both object-oriented and event-driven. Give one piece of
`HelloLine3` that shows each.

**Question 3.** Predict the output:

```csharp
Sensor press = new();
press.Take(3.1);
press.ReadingTaken += (s, v) => Console.WriteLine($"got {v}");
press.Take(7.4);
```

---

### Answers

**1.** `TallyConsole` is inside `Console.ReadLine()`, on a line you wrote. `HelloLine3` is inside
WPF's dispatcher, waiting for the next event. None of your code is running.

**2.** Object-oriented: `MainWindow` is a class with a field (`parts`) and a method that changes it.
Event-driven: `OnCountClick` runs only when the `Click` event happens, called by WPF.

**3.** One line: `got 7.4`. The first reading happened before anyone subscribed, so no handler ran
for it.

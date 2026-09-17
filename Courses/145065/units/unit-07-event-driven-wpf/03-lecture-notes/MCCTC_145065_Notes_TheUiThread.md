# Lecture Notes: The UI Thread Does One Thing at a Time
## 145065 Object-Oriented Programming · Unit 7 · Week 13, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W13_TheUiThread.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W13_TheUiThread.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and the
Lab U07-02 files.

**Competencies:** 5.4.7 debug logic errors. 5.1.4 describe event-driven programming.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

A label printer takes a few seconds. A sensor across the network takes a moment to answer. Saving a
file to a slow drive takes time. Every real app has work that is slow.

If a handler waits for that work, the window stops. It does not repaint. No button works. An
operator sees a panel that looks normal and ignores them. On a shop floor, **a frozen panel is worse
than a crashed one**, because a crash is obvious.

This is the most important idea of Week 13, and Unit 8's live sensor panel depends on it.

---

## The concept in plain language

WPF runs every handler on **one thread, the UI thread**. The dispatcher (Monday's event loop) takes
the next item from its queue, runs it to the end, and only then takes the next one. Repainting the
window is an item. A click is an item. So:

**While your handler runs, nothing else in the window can happen.**

A handler that calls `Thread.Sleep(3000)`, or a method that sleeps inside, holds the UI thread for
three seconds. Clicks made during that time wait in the queue.

The fix has two parts:

1. **Start the slow work in a way that returns at once.** Methods ending in `Async` return a `Task`,
   an object that represents work still in progress.
2. **`await` the task.** `await` gives the UI thread back to the dispatcher. When the work finishes,
   the rest of the handler runs, **back on the UI thread**, so it may update controls.

A handler that uses `await` must be marked `async`. Handlers are the one place `async void` is
allowed, because an event decides a handler's return type.

---

## Worked example 1: the same two seconds, waited and awaited

```csharp
Button slow = new();
slow.Click += (sender, e) =>
{
    Thread.Sleep(2000);   // pretend the label printer takes two seconds
    Console.WriteLine("blocking handler: label printed");
};

Button awaited = new();
awaited.Click += async (sender, e) =>
{
    await Task.Delay(2000);   // the same two seconds, awaited
    Console.WriteLine("awaiting handler: label printed");
};

Stopwatch clock = Stopwatch.StartNew();
slow.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
Console.WriteLine($"blocking handler gave the thread back after {clock.ElapsedMilliseconds / 100 * 100} ms");

clock.Restart();
awaited.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent));
Console.WriteLine($"awaiting handler gave the thread back after {clock.ElapsedMilliseconds / 100 * 100} ms");
```

Output, with the dispatcher left running afterward so the second handler can finish:

```
blocking handler: label printed
blocking handler gave the thread back after 2000 ms
awaiting handler gave the thread back after 0 ms
awaiting handler: label printed
```

(The times are rounded down to the nearest 100 ms so they print the same every run.) The blocking
handler kept the thread for two seconds. The awaiting handler gave it back at once and finished two
seconds later.

---

## Worked example 2: where the code after `await` runs

```csharp
Button print = new();
print.Click += async (sender, e) =>
{
    Console.WriteLine($"before await: UI thread? {print.Dispatcher.CheckAccess()}");
    await Task.Delay(300);
    Console.WriteLine($"after await:  UI thread? {print.Dispatcher.CheckAccess()}");
    await Task.Run(() =>
        Console.WriteLine($"inside Task.Run: UI thread? {print.Dispatcher.CheckAccess()}"));
    Console.WriteLine($"after Task.Run: UI thread? {print.Dispatcher.CheckAccess()}");
};
```

`CheckAccess()` answers "is this code running on the thread that owns the button?" Output:

```
before await: UI thread? True
after await:  UI thread? True
inside Task.Run: UI thread? False
after Task.Run: UI thread? True
```

`Task.Run` moves work to another thread. After `await`, the handler is back on the UI thread. That
return trip is what lets the lab's handler set `StatusText.Text` after printing.

---

## Worked example 3: the lab's print handler

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

Disabling the button is part of the design: while one label prints, a second press would queue a
second label. The Lab U07-02 self-check timed this handler: `The PRINT handler gave the window back
after 0 ms.`, and +1 GOOD worked while the label printed.

---

## Worked example 4: a control belongs to one thread

```csharp
TextBlock status = new() { Text = "Printing..." };
try
{
    Task.Run(() => status.Text = "Printed.").Wait();
}
catch (AggregateException problem)
{
    Console.WriteLine(problem.InnerException!.GetType().Name + ": " + problem.InnerException.Message);
}

Console.WriteLine($"The status still says: {status.Text}");
```

Output:

```
InvalidOperationException: The calling thread cannot access this object because a different thread owns it.
The status still says: Printing...
```

Work you send to another thread may compute, wait, and read files. It may not touch a control. Do the
slow part there, `await` it, and update the screen after the `await`.

---

## The wrong version, and the errors it produces

**The freeze.** Wire PRINT SUMMARY to the blocking method:

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

It builds. It runs. The window freezes for the printer's delay. "Printing..." never appears, because
the window cannot repaint until the handler ends. The self-check reports:

```
The PRINT handler held the UI thread for 1010 ms. While it waits, no button works. Await PrintAsync instead of calling Print.
```

**`await` without `async`:**

```
MainWindow.xaml.cs(112,9): error CS4033: The 'await' operator can only be used within an async method. Consider marking this method with the 'async' modifier and changing its return type to 'Task'.
```

For a handler, add `async` and keep `void`. The "change its return type to `Task`" advice is for
ordinary methods.

**`PrintAsync` without `await`:**

```
MainWindow.xaml.cs(112,9): error CS4014: Because this call is not awaited, execution of the current method continues before the call is completed. Consider applying the 'await' operator to the result of the call.
```

This is a warning that the lab projects treat as an error. Without `await`, the handler says
"Summary printed." before anything printed.

**`async` with the blocking call inside.** Mark the handler `async` but keep `printer.Print(...)`. On
the build machine's SDK (10.0.401) this compiled with **no warning at all**, and it froze exactly like
the first version. Older compilers warn about an `async` method with no `await` [VERIFY on the lab's
Visual Studio]. The word `async` in the signature does not make anything asynchronous.

**An exception that escapes.** If `PrintAsync` throws (the EXTENDED option's printer runs out of
labels) and the handler does not catch it, the whole app ends. On the build machine the app closed
with:

```
Unhandled exception. System.InvalidOperationException: The label printer is out of labels.
```

---

## Why the wrong version is tempting

The blocking version reads top to bottom like every program you have written, and on a fast
machine with a fast printer it might seem fine. Testing with a short delay hides the freeze. The
`async` version looks backwards: the handler "finishes" before the work does.

The habit that prevents it: **for any handler that waits on anything outside the program, ask what
the operator can do while it waits.** If the answer is "nothing," the handler needs `await`.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Thread** | a path of execution; WPF's controls belong to one, the UI thread |
| **UI thread** | the thread that runs the dispatcher, every handler, and every repaint |
| **Blocking** | making the current thread wait until work is done |
| **`Task`** | an object representing work that may still be running |
| **`async`** | marks a method that may use `await` |
| **`await`** | gives the thread back until a task finishes, then continues |
| **`async void`** | allowed only for event handlers; exceptions from it end the app |
| **`Task.Run`** | runs work on another thread |
| **Not Responding** | what Windows may show when a window's UI thread stays busy too long |

---

## Self-check

**Question 1.** A handler calls a method that takes four seconds. During those four seconds, the
operator presses STOP on the same window. When does the STOP handler run?

**Question 2.** Why can the lab's print handler set `StatusText.Text` after `await`, when worked
example 4 shows that another thread cannot?

**Question 3.** This builds with no warning on SDK 10.0.401. Is the window responsive while it
prints? Explain.

```csharp
private async void OnPrintClick(object sender, RoutedEventArgs e)
{
    printer.Print(SummaryText());
    StatusText.Text = "Summary printed.";
}
```

---

### Answers

**1.** Not until the first handler finishes. The STOP press is queued behind it, because the UI
thread runs one item at a time. On an operator panel, that delay is the danger.

**2.** After `await`, the rest of an `async` handler runs back on the UI thread, which owns
`StatusText`. Code inside `Task.Run` runs on a different thread, which does not.

**3.** No. `async` only allows `await`. There is no `await`, so `Print` runs on the UI thread and
blocks it for the whole delay. The fix is `await printer.PrintAsync(SummaryText());`.

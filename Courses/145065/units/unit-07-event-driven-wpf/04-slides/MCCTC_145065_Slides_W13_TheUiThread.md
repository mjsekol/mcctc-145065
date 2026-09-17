# The UI Thread Does One Thing at a Time
---
## Slide 1: The panel that looked fine
- The operator presses PRINT SUMMARY
- Then presses STOP on the same screen
- Nothing happens for three seconds
- The screen looks completely normal
Speaker notes: Here is the failure that scares people who build operator panels. A slow button, then an urgent one. For three seconds the second press does nothing, and the screen gives no sign that anything is wrong. A crash is obvious. A frozen panel that looks normal is not. Today you cause this on purpose, then fix it.
Image: An operator pressing a red STOP button on a panel with a small clock icon showing three seconds.
---
## Slide 2: One thread runs every handler
- The dispatcher runs on the UI thread
- It runs one item to the end
- Repainting is an item, and so is a click
- A slow handler holds everything behind it
Speaker notes: Monday's sentence comes back. The dispatcher runs one item at a time, on one thread. While your handler runs, the window cannot repaint and no other handler can start. Presses made during that time wait in line.
Image: A single-lane road with one slow truck and a line of cars labeled click, repaint, and timer.
---
## Slide 3: Waited, and awaited
```csharp
slow.Click += (sender, e) =>
{
    Thread.Sleep(2000);   // pretend the label printer takes two seconds
    Console.WriteLine("blocking handler: label printed");
};

awaited.Click += async (sender, e) =>
{
    await Task.Delay(2000);   // the same two seconds, awaited
    Console.WriteLine("awaiting handler: label printed");
};
```
Speaker notes: Two buttons, the same two seconds of work. The first one waits. The second one awaits. The difference is one word and one keyword, and it changes everything about what the operator experiences.
Image: None. This slide is code.
---
## Slide 4: What the stopwatch said
```
blocking handler: label printed
blocking handler gave the thread back after 2000 ms
awaiting handler gave the thread back after 0 ms
awaiting handler: label printed
```
Speaker notes: The blocking handler kept the UI thread for two full seconds. The awaiting handler gave it back immediately and printed its line two seconds later. While it waited, the dispatcher was free to repaint and to run other handlers.
Image: None. This slide is code.
---
## Slide 5: What await does
- Starts the slow work
- Gives the UI thread back to the dispatcher
- Comes back when the work finishes
- Runs the rest of the handler on the UI thread
Speaker notes: await does not make work faster. It lets the thread do other things while the work happens somewhere else. When the work finishes, the rest of your handler runs back on the UI thread, which is why you can set StatusText right after the await. A handler that uses await must be marked async, and async void is allowed for event handlers and nowhere else.
Image: A relay runner handing a baton back to the track and picking it up again later.
---
## Slide 6: The lab's print handler
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
Speaker notes: Disable the button so one press prints one label. Say what is happening. Await the printer. Say it is done. Turn the button back on. The self-check timed this handler at zero milliseconds before it gave the window back, and plus one GOOD worked while the label printed.
Image: None. This slide is code.
---
## Slide 7: The wrong way, and what the check says
```
The PRINT handler held the UI thread for 1010 ms. While it waits, no button works. Await PrintAsync instead of calling Print.
```
- The code built with no error
- The window froze for the whole delay
- Printing... never appeared on screen
Speaker notes: This is the blocking version. It compiled cleanly. It froze the window. The status line never showed Printing, because the window could not repaint until the handler ended. And one more trap: on the build machine's compiler, marking the method async while still calling the blocking Print produced no warning at all. The word async does not make anything asynchronous.
Image: A frozen window with a stopwatch overlay reading about one second.
---
## Slide 8: A control belongs to one thread
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
```
```
InvalidOperationException: The calling thread cannot access this object because a different thread owns it.
```
Speaker notes: Task dot Run moves work to another thread. That thread may wait, compute, and read files. It may not touch a control, because the control belongs to the UI thread. Do the slow part elsewhere, await it, and update the screen after the await.
Image: None. This slide is code.
---
## Slide 9: Two build errors you will meet today
- await without async: error CS4033
- PrintAsync without await: error CS4014
- For a handler, add async and keep void
- Without await, it says done before it prints
Speaker notes: Forget async and the build says await can only be used within an async method. Its advice to change the return type to Task is for ordinary methods, not handlers. Forget await and the lab projects turn the warning CS4014 into an error, because the handler would announce Summary printed before anything printed.
Image: Two error cards side by side, each with a one-word fix under it.
---
## Slide 10: What you are about to build
- Lab U07-02 Part 2: printing without freezing
- Wire PRINT to the blocking method first
- Press other buttons during the freeze
- Write down what happened, then fix it
Speaker notes: First you build the freeze on purpose and press other buttons while the window ignores them. Write down exactly what happens to those presses. Then switch to await, disable the button while it prints, and run the self-check to eighteen of eighteen. In the last fifteen minutes, read the project handout and choose your station job.
Image: The ShiftTally window with the PRINT SUMMARY button greyed out and a status line reading Printing.

# Programs That Wait
---
## Slide 1: Who decides what happens next
- A panel shows three buttons and a live number
- The operator can press any button, any time
- A reading can arrive in the middle of a press
- Your old programs asked one question at a time
Speaker notes: Picture the operator panel you will build in Unit 8. Three big buttons and a number that changes on its own. The operator can press anything, in any order, and a new reading can arrive at the same moment. Every program you have written so far asked one question, waited for one answer, and decided what came next. That will not work here. Today is about programs that give up control on purpose.
Image: An operator's gloved hand reaching toward a touch panel with three large buttons and a live temperature, navy and launch blue.
---
## Slide 2: Four ways to organize a program
- Procedural: your code decides the order
- Structured: sequence, selection, and loops only
- Object-oriented: objects bundle data with behavior
- Event-driven: a loop you did not write calls you
Speaker notes: The WebXam asks you to tell these apart, so here they are. Procedural code decides its own order and calls functions. Structured code uses only sequence, selection, and loops. Object-oriented code bundles data with the methods that use it. Event-driven code hands control to a loop it did not write, and that loop calls your methods when something happens. A WPF app is object-oriented and event-driven at the same time.
Image: A four-row table with one icon per row: a list, a loop arrow, a class box, and a bell.
---
## Slide 3: A procedural program waits in one line
```csharp
while (true)
{
    Console.Write("> ");
    string? input = Console.ReadLine();   // the program waits here, and only here

    if (input is null || input == "q")
    {
        break;
    }

    // ... count g and s, or complain about any other key ...

    Console.WriteLine($"Good: {good}  Scrap: {scrap}  Total: {good + scrap}");
}
```
Speaker notes: This is the heart of TallyConsole from your lab folder. Find the one line where it waits. It is Console dot ReadLine. While it sits there, nothing else can happen. The loop is yours, and your code picks what comes next every time.
Image: None. This slide is code.
---
## Slide 4: An event, with no window at all
```csharp
Sensor oven = new();
oven.ReadingTaken += ShowOnPanel;
oven.ReadingTaken += WriteToLog;
Console.WriteLine("Subscribed. Nothing has happened yet.");
oven.Take(212.4);
```
```
Subscribed. Nothing has happened yet.
Panel: 212.4 C
Log:   212.4 C
```
Speaker notes: C# has events built in. The plus equals attaches a handler. Attaching runs nothing, which is why the first line prints before anything else. When the sensor takes a reading, every attached handler runs, in the order it was attached. The sensor does not know who is listening.
Image: None. This slide is code.
---
## Slide 5: The event loop runs one item at a time
- WPF's loop is called the dispatcher
- It takes the next item from a queue
- It runs that item to the end
- Clicks, repaints, and timers are all items
Speaker notes: In WPF the loop you did not write is the dispatcher. It keeps a queue. It takes one item, runs it to the end, then takes the next. A click is an item. Repainting the window is an item. Hold on to that sentence, one item at a time, because Thursday is built on it.
Image: A conveyor belt carrying labeled boxes into a single machine, one box inside at a time.
---
## Slide 6: Your first window
```xml
<StackPanel Margin="20">
    <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
    <Button x:Name="CountButton" Content="+1 PART" MinHeight="64" Click="OnCountClick" />
</StackPanel>
```
```csharp
private void OnCountClick(object sender, RoutedEventArgs e)
{
    parts++;
    CountText.Text = $"Parts: {parts}";
}
```
Speaker notes: Here is HelloLine3. The XAML says there is a button, and its Click event should call OnCountClick. The C# is the method. Look for the loop. There is no loop in either file. WPF opens the window and waits, and each press queues a Click.
Image: None. This slide is code.
---
## Slide 7: The wrong way, and what the build says
```
MainWindow.xaml(7,82): error CS1061: 'MainWindow' does not contain a definition for 'OnCountClik' and no accessible extension method 'OnCountClik' accepting a first argument of type 'MainWindow' could be found (are you missing a using directive or an assembly reference?)
```
- One letter wrong in the XAML
- The error names the XAML file
Speaker notes: I misspelled the handler name in the XAML as OnCountClik. The build stops. Read the file name at the front of the message. It is the XAML file, line 7, column 82. The build turns your XAML into C#, so a name in the XAML has to match a real method. Python would have waited until the click to complain.
Image: A XAML line with the misspelled word circled in launch red.
---
## Slide 8: The worse mistake makes no sound
- Forget to attach the handler
- The button still presses
- The event still happens
- Nothing is listening, so nothing runs
Speaker notes: The misspelling was the kind mistake. The compiler caught it. Here is the unkind one. Forget the Click attribute entirely. The button presses, the event happens, and no handler is attached, so nothing runs and nothing complains. When a button does nothing, check the attachment before you stare at the method.
Image: A button being pressed with sound waves drawn but no listener in the room.
---
## Slide 9: Where each program is right now
- TallyConsole: inside Console.ReadLine, on your line
- HelloLine3: inside WPF's dispatcher, waiting
- Your code runs only when WPF calls it
- The constructor once, then a handler per event
Speaker notes: Here is the exit ticket answer, so you can check yourself tonight. When nobody is typing, TallyConsole is inside a line you wrote. When nobody is touching the mouse, HelloLine3 is not running any of your code. It is inside the dispatcher. Your code runs at two kinds of moments: once in the constructor, and once per event.
Image: Two side-by-side diagrams, one with a pointer on a code line, one with a pointer on a loop labeled dispatcher.
---
## Slide 10: What you are about to build
- Lab U07-01 Part 1: First Window
- Create HelloLine3, run it, break it, fix it
- Compare it with TallyConsole
- Sketch its event flow
Speaker notes: In Build 1 you check your environment and create HelloLine3 yourself, then break the handler name on purpose and read the error. In Build 2 you run TallyConsole with typed keys and with a keys file, fill in the comparison table, and sketch every event HelloLine3 handles. That sketch is the first version of the event flow diagram your project needs next week.
Image: A small window with one big button beside a hand-drawn event flow sketch with three arrows.

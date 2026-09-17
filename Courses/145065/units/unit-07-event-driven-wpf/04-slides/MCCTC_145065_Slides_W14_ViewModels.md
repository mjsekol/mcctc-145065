# A View Model You Can Test
---
## Slide 1: How do you test a rule you cannot reach
- The scrap rate math lives in a handler
- The handler lives in a window
- To test it, open the window and click
- Every test needs a person
Speaker notes: Last week's scrap rate is a rule a supervisor depends on. Where does it live? Inside ShowCounts, inside the window. To check it, somebody opens the app and clicks. A rule that only a person can check gets checked rarely. Today it moves somewhere a test can reach in a tenth of a second.
Image: A student clicking a button over and over while a stopwatch runs.
---
## Slide 2: A view model holds what the window shows
- Every displayed value becomes a property
- Every button's job becomes a method
- It knows nothing about controls
- It lives in a plain net8.0 library
Speaker notes: A view model is an ordinary class. What the window shows, it holds as properties. What the buttons do, it does as methods. It never touches a TextBlock. It lives in its own project that targets plain net8.0, so it cannot even see WPF. That is how its tests run with no window at all.
Image: Two boxes, a window and a view model, with an arrow labeled calls from the window and none going back.
---
## Slide 3: The handler shrinks
```csharp
// Lab U07-02
private void OnGoodClick(object sender, RoutedEventArgs e)
{
    good++;
    history.Push(true);
    ShowCounts();
    StatusText.Text = "Counted one good part.";
}

// Lab U07-03
private void OnGoodClick(object sender, RoutedEventArgs e) => Tally.AddGood();
```
Speaker notes: Top, last week. Bottom, this week. The counting, the history, and the status message all move into the view model's AddGood method. The handler's only job is to pass the press along.
Image: None. This slide is code.
---
## Slide 4: The rules, with no window
```csharp
ShiftTally.Core.TallyViewModel tally = new() { Target = 150 };
for (int i = 0; i < 37; i++) { tally.AddGood(); }
for (int i = 0; i < 3; i++) { tally.AddScrap(); }
Console.WriteLine(tally.ProgressText);
Console.WriteLine(tally.ScrapRateText);
```
```
37 of 150 good parts
Scrap rate: 7.5 %
```
Speaker notes: A console program, no window anywhere, using the lab's view model. Every value the window will show already exists, computed, before any window is involved. The lecture note has the longer version that prints the heading, the counts, and the status too.
Image: None. This slide is code.
---
## Slide 5: What stays in the window
- Asking the operator a question
- Talking to the label printer
- Starting a timer
- Anything a test cannot do without a person
Speaker notes: Some jobs belong to the window. A message box needs a person. A printer is a device. The window keeps those. But notice the split inside RESET: the wording of the question is a rule, so it lives in the view model as ResetQuestion, where a test checks it. Showing the question is the window's job.
Image: A window icon holding a speech bubble and a printer, and a view model icon holding a calculator.
---
## Slide 6: A rule, tested
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
    Assert.Equal("Scrap rate: 12.5 %", tally.ScrapRateText);
}
```
```
Passed!  - Failed:     0, Passed:    23, Skipped:     0, Total:    23, Duration: 111 ms - ShiftTally.Core.Tests.dll (net8.0)
```
Speaker notes: One of the twenty-three view model tests. Seven good, one scrap, twelve point five percent. Integer division would say zero, and this test would catch it. All twenty-three ran in about a tenth of a second against the solution, with no window.
Image: None. This slide is code.
---
## Slide 7: The wrong way: a control in the library
```
Program.cs(1,22): error CS0234: The type or namespace name 'Controls' does not exist in the namespace 'System.Windows' (are you missing an assembly reference?)
```
- The library cannot see WPF
- This error is the design working
- The fix is a property, not a reference
Speaker notes: I tried to give the view model a TextBlock. The build stopped: Controls does not exist. Resist the urge to fix this by adding WPF to the library. The library cannot see a window on purpose. If the view model needs to show something, it gets a property, and the window binds to it tomorrow.
Image: A locked door between two rooms labeled library and window.
---
## Slide 8: The honest cost
- Two projects instead of one
- A property for everything on screen
- More files for a one-button window
- Worth it once a rule matters
Speaker notes: This design is not free. You now have two projects, a project reference, and a property for every value on screen. For a window with one button, that is more code than it saves. For a panel whose numbers an operator trusts, it is the only way to test the rules. Present both sides when someone asks.
Image: A balance scale with extra files on one side and a green test result on the other.
---
## Slide 9: Monday's numbers, before you start
- View model tests: 15 of 23 by the end
- The 8 notification tests fail until Wednesday
- Window checks: 12 of 30 by the end
- The app still counts when you run it
Speaker notes: Here is what done looks like today, so a red result does not scare you. The logic tests pass. The eight notification tests fail on purpose until Wednesday. The window checks show twelve of thirty, because the bindings come tomorrow. And the app still works, because ShowCounts now reads from the view model.
Image: A test summary bar, mostly green with a labeled red section marked Wednesday.
---
## Slide 10: What you are about to build
- Lab U07-03 Part 1: TallyViewModel
- Counts, target, progress, and rate
- AddGood, AddScrap, Undo, and Reset
- Then your own app's view model and four tests
Speaker notes: In Build 1 you write the members of TallyViewModel that throw NotImplementedException, one test group at a time. In Build 2 the handlers start calling Tally, and ShowCounts reads from it. Then you start your own project's view model, with at least four tests that pass.
Image: A class diagram of TallyViewModel with its properties and four methods.

# A Handler Is a Method WPF Calls for You
---
## Slide 1: A window that only shows things
- The counts are on screen
- The operator presses +1 GOOD
- Nothing happens
- A window with no handlers is a poster
Speaker notes: Yesterday's window looks finished. Press any button and nothing happens, because nothing is attached. Today every control that should respond gets a handler: a method that WPF calls when its event happens. By the end of the day the counts move.
Image: A framed poster of the ShiftTally window hanging on a wall.
---
## Slide 2: What makes a method a handler
- An event attribute names it
- Its parameters match the event
- sender is the control that raised it
- e carries details, such as NewValue
Speaker notes: Two things. The XAML names the method, for example Click equals OnGoodClick. And the method has the parameters the event expects: sender, the control that raised the event, typed as object, and e, the details. For a slider, e carries the old and new values.
Image: A Button tag with a dotted line to a method signature, labeled sender and e.
---
## Slide 3: The GOOD handler
```xml
<Button x:Name="GoodButton" Content="+1 GOOD" Background="#DDE8F7" Click="OnGoodClick" />
```
```csharp
private void OnGoodClick(object sender, RoutedEventArgs e)
{
    good++;
    history.Push(true);
    ShowCounts();
    StatusText.Text = "Counted one good part.";
}
```
Speaker notes: Change the state, remember it for UNDO, redraw, and tell the operator what happened. Almost every handler you write this week has those four steps. You never call this method yourself. WPF does, once per press.
Image: None. This slide is code.
---
## Slide 4: One handler, three buttons
```csharp
void OnReasonClick(object sender, RoutedEventArgs e)
{
    Button pressed = (Button)sender;
    switch (pressed.Name)
    {
        case "BurrButton": burr++; break;
        case "BentButton": bent++; break;
        case "HoleButton": hole++; break;
    }
}
```
```
+1 BURR: burr 1, bent 0, hole 0
+1 WRONG HOLE: burr 1, bent 0, hole 1
+1 BURR: burr 2, bent 0, hole 1
```
Speaker notes: sender tells a shared handler which button was pressed. It arrives as object, so cast it to Button first. Three presses, burr, wrong hole, burr, produce these three lines. The lecture note has the full version with the line that prints.
Image: None. This slide is code.
---
## Slide 5: Events that carry a value
- Slider ValueChanged: e.NewValue, e.OldValue
- TextBox TextChanged: read the box's Text
- ComboBox SelectionChanged: read SelectedItem
- CheckBox Checked and Unchecked: read IsChecked
Speaker notes: Different controls, different events. A slider hands you the new value directly. Setting a slider to 9000 when its maximum is 500 reported 350 to 500, because the slider refused the value. TextChanged fires on every keystroke, which is what a live heading needs. Slider values are doubles, so cast to int when you store a whole-number target.
Image: Four controls in a column, each with a small speech bubble naming its event.
---
## Slide 6: Attached twice, runs twice
- XAML attaches OnGoodClick
- The constructor attaches it again with +=
- One press counts two
- No error, no warning
Speaker notes: An event keeps a list of handlers, and the same method can be on that list twice. The verification run showed one press, good is 2. Attach in XAML or in C#, never both for the same event. A test that presses once and checks for exactly one change catches it.
Image: Two identical arrows pointing from one button into one method box.
---
## Slide 7: The wrong way: a handler before the window exists
```xml
<Slider x:Name="TargetSlider" Minimum="50" Maximum="500" Value="200" ValueChanged="OnTargetChanged" />
<TextBlock x:Name="TargetText" Text="Shift target: 200" />
```
```
System.NullReferenceException: Object reference not set to an instance of an object.
```
Speaker notes: Nobody touched the slider, and the window never opened. While InitializeComponent built the slider, setting Minimum to 50 moved its value from 0 to 50, and that raised ValueChanged. The handler wrote to TargetText, which did not exist yet. WPF raises events while it is still building the window.
Image: None. This slide is code.
---
## Slide 8: The guard the lab gives you
- windowBuilt is false during InitializeComponent
- The constructor sets it true at the end
- ShowCounts returns early until then
- Without it, all 18 checks failed
Speaker notes: The starter has a flag named windowBuilt. The constructor sets it to true after InitializeComponent. ShowCounts and ShowHeading return early while it is false. When the build machine removed that guard, every one of the eighteen self-checks failed with the same exception, thrown from OnStationChanged.
Image: A gate across a road labeled still building, lifted after the window finishes.
---
## Slide 9: A destructive handler asks first
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
Speaker notes: RESET throws away a shift. So it asks. Confirm is a function the lab gives you. In the running app it shows a Yes or No box with No as the default, so a stray Enter does not wipe a shift. The self-check swaps in its own answer, so no dialog pops up while it runs.
Image: None. This slide is code.
---
## Slide 10: What you are about to build
- Lab U07-02 Part 1: Shift Tally Handlers
- GOOD, SCRAP, and UNDO
- RESET with a confirmation
- The slider, the check box, and the heading
Speaker notes: Build 1 is the state fields and the three counting handlers, then UNDO. Build 2 is RESET, the slider and progress bar, the check box that hides the scrap rate, and the heading that follows the station name. By the commit, sixteen of the eighteen checks should pass. The last two are about printing, and printing is tomorrow.
Image: The ShiftTally window with arrows from each button to a handler name.

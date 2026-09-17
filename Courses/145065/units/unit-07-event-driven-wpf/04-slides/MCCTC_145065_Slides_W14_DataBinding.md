# Binding a Control to a Property
---
## Slide 1: Ten lines you have to remember
- ShowCounts writes every value by hand
- Every handler must call it
- Forget one call and the screen is wrong
- Nothing warns you
Speaker notes: Look at ShowCounts from last week. Ten lines that copy values onto the screen, and every handler has to remember to call it. Miss one call in one handler and the screen shows an old value. Today you delete ShowCounts. Each control will say once which property it shows, and WPF does the copying.
Image: A sticky note reading call ShowCounts stuck to every button on the ShiftTally window.
---
## Slide 2: A binding in one line
- Target: a control property, like Text
- Source: a view model property, like Good
- DataContext: where bindings look
- StringFormat: how the text is shaped
Speaker notes: A binding connects a target to a source. The target is a property on a control. The source is a property on your view model. DataContext, set once on the window, tells every binding where to look, and every element inside inherits it. StringFormat shapes the number into words.
Image: A TextBlock and a view model joined by a cable labeled Binding.
---
## Slide 3: The ShiftTally bindings
```xml
<TextBlock x:Name="GoodText" Text="{Binding Good, StringFormat=Good: {0}}" />
<TextBox x:Name="StationBox" Text="{Binding Station, UpdateSourceTrigger=PropertyChanged}" />
<ComboBox x:Name="PartBox" ItemsSource="{Binding PartTypes}" SelectedItem="{Binding PartType}" />
<Slider x:Name="TargetSlider" Minimum="50" Maximum="500" Value="{Binding Target}" />
<Button x:Name="UndoButton" Content="UNDO LAST" Click="OnUndoClick" IsEnabled="{Binding CanUndo}" />
```
```csharp
DataContext = Tally;
```
Speaker notes: Five controls, five bindings, and one line of C#. The text box, the combo box, and the slider also write back, so the operator's changes reach the view model. UNDO's enabled state comes from CanUndo. The heading, the counts, and the rate follow the same pattern.
Image: None. This slide is code.
---
## Slide 4: Direction and timing
- Most bindings copy source to screen
- TextBox, Slider, CheckBox, ComboBox also write back
- A TextBox writes back when it loses focus
- Unless you ask for every keystroke
Speaker notes: Most bindings only read. Controls the operator changes also write back. The trap is timing. A TextBox writes back only when it loses focus, unless you add UpdateSourceTrigger equals PropertyChanged. Your heading depends on the station name, so it needs every keystroke.
Image: Two arrows between a text box and a view model, one solid and one dashed labeled on focus loss.
---
## Slide 5: What the trigger changes
```csharp
TextBox lazyBox = new() { DataContext = shift };
lazyBox.SetBinding(TextBox.TextProperty, new Binding("Station"));
lazyBox.Text = "Press 4";

TextBox eagerBox = new() { DataContext = shift };
eagerBox.SetBinding(TextBox.TextProperty,
    new Binding("Station") { UpdateSourceTrigger = UpdateSourceTrigger.PropertyChanged });
eagerBox.Text = "Press 5";
```
```
Default trigger, after typing:        Station = Press 2
PropertyChanged trigger, after typing: Station = Press 5
```
Speaker notes: Same source, two text boxes. The first one changed its text to Press 4, and the source still says Press 2, because the box never lost focus. The second one wrote back at once. SetBinding in C# is what a curly-brace binding does in XAML.
Image: None. This slide is code.
---
## Slide 6: Converters change the type
- IsChecked is a bool
- Visibility is Visible or Collapsed
- BooleanToVisibilityConverter translates
- Declare it once in the window's resources
Speaker notes: The check box gives you true or false. The rate text's Visibility wants Visible or Collapsed. A converter translates between them. You declare one BooleanToVisibilityConverter in the resources with a key, then use it in the binding with Converter equals StaticResource and that key.
Image: A small machine with true going in one side and Visible coming out the other.
---
## Slide 7: The wrong way: a misspelled path
```
System.Windows.Data Error: 40 : BindingExpression path error: 'Scarp' property not found on 'object' ''Shift' (HashCode=45638969)'. BindingExpression:Path=Scarp; DataItem='Shift' (HashCode=45638969); target element is 'TextBlock' (Name=''); target property is 'Text' (type 'String')
```
- The build succeeded
- The text on screen is blank
Speaker notes: I spelled Scrap as Scarp inside the binding. The build did not complain, because a binding path is text that WPF looks up at run time. The screen shows nothing, and this line appears in the debug output. Run with the debugger and read the Output window before you trust the screen. Your self-check listens for exactly this line.
Image: A blank label on the window and a magnifying glass over the Output window.
---
## Slide 8: Tuesday's surprise, predicted
- Press +1 GOOD five times
- The view model holds 5
- The screen still says Good: 0
- No error anywhere
Speaker notes: Here is what will happen at the end of Build 1, so you are not surprised. The bindings are right. The view model is right. The screen does not move. The binding read Good once, and nothing told it to read again. Your window picture will show zeros while the view model holds thirty-seven parts. Write down why. That is tomorrow's concept.
Image: A split screen: a debugger watch showing Good equals 5 beside a window showing Good: 0.
---
## Slide 9: One thing will update anyway
- Drag the slider to 100
- Shift target: 100 appears
- The progress text does not change
- One changed through a binding, one did not
Speaker notes: One detail confuses people. The slider's label updates even today, because the slider changed Target through a binding, and WPF told the other binding on the same property. The progress text is computed from Target, and nothing told WPF about it. Keep this in your head for tomorrow.
Image: A slider at 100 with its label updated and a progress bar still at its old value.
---
## Slide 10: What you are about to build
- Lab U07-03 Part 2: bind the window
- Set DataContext and bind all 15 values
- Delete ShowCounts and ShowHeading
- Predict, then read, 24 of 30
Speaker notes: In Build 1 you set DataContext and bind every value the window shows. ShowCounts, ShowHeading, and the windowBuilt flag get deleted. In Build 2 you predict the self-check result, run it, and explain the six failures in writing. Then you bind your own app's window to its view model.
Image: The ShiftTally window with a binding label on each control.

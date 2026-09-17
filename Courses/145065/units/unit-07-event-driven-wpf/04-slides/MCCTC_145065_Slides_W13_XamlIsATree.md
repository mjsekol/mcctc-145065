# XAML Is a Tree of Objects
---
## Slide 1: The screen you inherit
- Someone else built the Line 3 panel
- You must add one button by Friday
- The layout is four hundred lines of code
- Where does your button even go
Speaker notes: Imagine you inherit a panel built entirely in C#, one new after another, four hundred lines. Your job is one button. You cannot see the shape of the screen anywhere in that code. XAML exists so the shape of a screen is visible in the file. Nesting in the file is nesting on the screen.
Image: A long scroll of code on one side and a clean window layout on the other, with a question mark between them.
---
## Slide 2: Three rules explain most XAML
- Every element is an object
- Every attribute sets a property
- Nesting means holds
- x:Name makes a field your C# can use
Speaker notes: Three rules. Button in angle brackets means new Button. Content equals plus one GOOD means set the Content property. An element inside a StackPanel is one of its children. And x colon Name gives you a field with that name in your code-behind, filled in by InitializeComponent.
Image: A XAML tag with arrows labeling the element as object, an attribute as property, and x:Name as field.
---
## Slide 3: The same tree, two ways
```xml
<StackPanel Margin="20">
    <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
    <Button x:Name="CountButton" Content="+1 PART" MinHeight="64" />
</StackPanel>
```
```csharp
StackPanel panel = new() { Margin = new Thickness(20) };
panel.Children.Add(new TextBlock { Name = "CountText", Text = "Parts: 0", FontSize = 28 });
panel.Children.Add(new Button { Name = "CountButton", Content = "+1 PART", MinHeight = 64 });
```
Speaker notes: Top half, XAML. Bottom half, the C# that builds exactly the same objects. Same types, same properties, same parent and children. When the build compiles your XAML, it produces code that does what the bottom half does. XAML is the shorter way to write it.
Image: None. This slide is code.
---
## Slide 4: Panels decide where children go
- StackPanel: one after another
- Grid: rows and columns
- DockPanel: pinned to edges, last child fills
- UniformGrid: every cell the same size
Speaker notes: A panel holds many children and arranges them. StackPanel stacks. Grid uses rows and columns, and a child says which row with Grid dot Row. DockPanel pins children to edges and gives the rest to the last one. UniformGrid makes every cell equal, which is how your four counting buttons get equal widths.
Image: Four small diagrams of boxes arranged as a stack, a grid, a docked layout, and an even grid.
---
## Slide 5: A Grid, measured
```csharp
grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Star) });
```
```
row 0: top 0, height 40
row 1: top 40, height 64
row 2: top 284, height 16
```
Speaker notes: This is the row setup from a longer program in today's lecture note, which adds a heading, a button, and a status line and measures them. Two Auto rows and one star row, measured in a 400 by 300 area. Auto rows are exactly as tall as their content. The star row takes everything left over, and the status text sits at its bottom, at 284. Resize the window and only the star row changes.
Image: None. This slide is code.
---
## Slide 6: The ShiftTally counting row
```xml
<UniformGrid Grid.Row="2" Rows="1" Margin="14,16,14,0">
    <Button x:Name="GoodButton" Content="+1 GOOD" Background="#DDE8F7" />
    <Button x:Name="ScrapButton" Content="+1 SCRAP" Background="#F6DADF" />
    <Button x:Name="UndoButton" Content="UNDO LAST" IsEnabled="False" />
    <Button x:Name="ResetButton" Content="RESET SHIFT" />
</UniformGrid>
```
Speaker notes: This is row 2 of the window you build today. Four buttons, one row, equal widths, because UniformGrid makes every cell the same. A style higher up sets every button to at least 64 pixels tall, for gloved fingers. UNDO starts disabled, because there is nothing to undo yet.
Image: None. This slide is code.
---
## Slide 7: The wrong way: two things in a window
```
MainWindow.xaml(6,6): error MC3089: The object 'Window' already has a child and cannot add 'Button'. 'Window' can accept only one child. Line 6 Position 6.
```
- A window holds exactly one object
- Wrap the controls in a panel
Speaker notes: I deleted the StackPanel, so the window tried to hold a TextBlock and a Button directly. The build says a window can accept only one child. That one child is usually a Grid or another panel, and the panel holds everything else. The designer hides this from you, because the new-window template already contains a Grid.
Image: A window frame with two controls trying to squeeze through one door.
---
## Slide 8: XAML mistakes the compiler catches
- A misspelled property: error MC3072
- A tag that never closes: error MC3000
- A handler name with no method: error CS1061
- Two x:Name values the same: error CS0102
Speaker notes: XAML looks like a document, and documents forgive spelling. XAML does not. Contnet with the letters swapped is error MC3072, property does not exist. A tag that never closes is MC3000, XML is not valid. The line number in each message points at the XAML. Read it before you change anything.
Image: A checklist of four error codes, each with a small XAML fragment beside it.
---
## Slide 9: A mistake the compiler cannot catch
- MinHeight equals tall builds without complaint
- Opening the window throws XamlParseException
- The inner exception says what happened
- Tall string cannot be converted to Length
Speaker notes: Some values are only checked when the window is built. MinHeight equals the word tall passed the build. When the window opened, it threw a XAML parse exception. The useful part is the inner exception: tall string cannot be converted to Length. When a window crashes on open, read the inner exception first.
Image: A stack of two error cards, the inner card highlighted in launch red.
---
## Slide 10: What you are about to build
- Lab U07-01 Part 2: the ShiftTally layout
- Rows 2 to 5, with the names the lab lists
- Run dotnet test until 28 of 28 pass
- Open the saved picture of your window
Speaker notes: The starter has rows 0 and 1. You write rows 2 through 5: the counting buttons, the counts, the target slider and progress, and the status line with the print button. Every control needs the exact x colon Name the lab lists, because next week's code finds them by name. The self-check measures your layout and saves a picture of it. Compare the picture with your sketch.
Image: The finished ShiftTally window with its six rows outlined and numbered.

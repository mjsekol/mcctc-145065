# Lecture Notes: XAML Is a Tree of Objects
## 145065 Object-Oriented Programming · Unit 7 · Week 13, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W13_XamlIsATree.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W13_XamlIsATree.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and the
Lab U07-01 files.

**Competencies:** 5.4.2 write and edit code in the IDE, including XAML and the visual designer.
5.3.12 write code that creates classes, objects, and methods.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

You could build a window entirely in C#, one `new` at a time. For a real operator screen that is
hundreds of lines where the shape of the screen is buried in the code.

XAML puts the shape on the page. Nesting in the file is nesting on the screen. A designer, a
teammate, or you next month can read the layout at a glance, and Visual Studio's designer can edit
the same file you type.

**The trap:** XAML looks like a drawing, so people treat it like one. It is not a drawing. It is a
list of objects to build, and the compiler checks every name in it.

---

## The concept in plain language

Three rules explain almost every XAML file.

1. **Every element is an object.** `<Button />` means `new Button()`.
2. **Every attribute sets a property.** `Content="+1 GOOD"` means `button.Content = "+1 GOOD"`.
3. **Nesting means "holds."** An element inside a `StackPanel` is one of the panel's children.

Three more things make it practical:

- **Panels arrange their children.** `StackPanel` stacks them. `Grid` puts them in rows and columns.
  `DockPanel` pins children to an edge and gives the rest to the last one. `UniformGrid` makes every
  cell the same size.
- **Attached properties** are set on a child but read by its parent: `Grid.Row="2"` tells the
  surrounding `Grid` which row the child goes in.
- **`x:Name` makes a field.** `x:Name="GoodText"` means your C# can write `GoodText.Text = ...`. The
  build writes that field for you, and `InitializeComponent()` fills it.

**The visual designer** in Visual Studio shows the window and lets you drag controls from the
Toolbox and set properties in the Properties window [VERIFY the panel names in Visual Studio 2026].
Every drag writes XAML. Read what it wrote: dragged controls often get a fixed `Margin` that breaks
the layout when the window is resized.

---

## Worked example 1: the same tree, in XAML and in C#

The XAML:

```xml
<StackPanel Margin="20">
    <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
    <Button x:Name="CountButton" Content="+1 PART" MinHeight="64" />
</StackPanel>
```

The same objects, built in C#:

```csharp
StackPanel panel = new() { Margin = new Thickness(20) };
panel.Children.Add(new TextBlock { Name = "CountText", Text = "Parts: 0", FontSize = 28 });
panel.Children.Add(new Button { Name = "CountButton", Content = "+1 PART", MinHeight = 64 });

foreach (object child in LogicalTreeHelper.GetChildren(panel))
{
    FrameworkElement element = (FrameworkElement)child;
    Console.WriteLine($"{element.GetType().Name} named {element.Name}");
}
```

Output:

```
TextBlock named CountText
Button named CountButton
```

Same objects, same properties, same parent and children. XAML is the shorter way to write it.

---

## Worked example 2: reading XAML at run time shows the tree

`XamlReader.Parse` builds objects from a XAML string, the same job the build does for your window.
A short method walks the result and prints each object, indented by depth:

```csharp
string xaml = """
    <StackPanel xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
        <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
        <UniformGrid Rows="1">
            <Button x:Name="GoodButton" Content="+1 GOOD" />
            <Button x:Name="ScrapButton" Content="+1 SCRAP" />
        </UniformGrid>
    </StackPanel>
    """;
object root = XamlReader.Parse(xaml);
Print(root, 0);

static void Print(object node, int depth)
{
    string name = node is FrameworkElement { Name.Length: > 0 } fe ? $" ({fe.Name})" : "";
    Console.WriteLine($"{new string(' ', depth * 2)}{node.GetType().Name}{name}");
    if (node is DependencyObject parent)
    {
        foreach (object child in LogicalTreeHelper.GetChildren(parent))
        {
            if (child is DependencyObject)
            {
                Print(child, depth + 1);
            }
        }
    }
}
```

Output:

```
StackPanel
  TextBlock (CountText)
  UniformGrid
    Button (GoodButton)
    Button (ScrapButton)
```

The indentation of the output matches the indentation of the XAML. That is the tree.

---

## Worked example 3: a Grid decides where each row goes

```csharp
Grid grid = new();
grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Star) });

TextBlock heading = new() { Text = "Press 2", FontSize = 30 };
Button good = new() { Content = "+1 GOOD", MinHeight = 64 };
TextBlock status = new() { Text = "Ready", VerticalAlignment = VerticalAlignment.Bottom };
Grid.SetRow(heading, 0);
Grid.SetRow(good, 1);
Grid.SetRow(status, 2);
grid.Children.Add(heading);
grid.Children.Add(good);
grid.Children.Add(status);

grid.Measure(new Size(400, 300));
grid.Arrange(new Rect(0, 0, 400, 300));
foreach (FrameworkElement child in grid.Children)
{
    Point top = child.TranslatePoint(new Point(0, 0), grid);
    Console.WriteLine($"row {Grid.GetRow(child)}: top {top.Y:0}, height {child.ActualHeight:0}");
}
```

Output, for a 400 by 300 area:

```
row 0: top 0, height 40
row 1: top 40, height 64
row 2: top 284, height 16
```

`Auto` rows are as tall as their content. The `*` row takes everything left over, and the status text
sits at its bottom. In XAML, `Grid.SetRow(good, 1)` is written `Grid.Row="1"`, and the rows are
`<RowDefinition Height="Auto" />` and `<RowDefinition Height="*" />`.

---

## Worked example 4: the ShiftTally counting row

From the Lab U07-01 solution. Four buttons in one row, at equal widths, with a style that makes every
button tall enough for a gloved finger:

```xml
<Grid.Resources>
    <Style TargetType="Button">
        <Setter Property="MinHeight" Value="64" />
        <Setter Property="FontSize" Value="22" />
        <Setter Property="FontWeight" Value="Bold" />
    </Style>
</Grid.Resources>

<UniformGrid Grid.Row="2" Rows="1" Margin="14,16,14,0">
    <Button x:Name="GoodButton" Content="+1 GOOD" Background="#DDE8F7" />
    <Button x:Name="ScrapButton" Content="+1 SCRAP" Background="#F6DADF" />
    <Button x:Name="UndoButton" Content="UNDO LAST" IsEnabled="False" />
    <Button x:Name="ResetButton" Content="RESET SHIFT" />
</UniformGrid>
```

The Lab U07-01 self-check measured this row at 900 pixels wide: all four buttons share one top edge,
have equal widths, and are at least 64 pixels tall. `UNDO LAST` starts disabled because there is
nothing to undo yet.

---

## The wrong version, and the errors it produces

**A window holds one object.** Put two elements straight inside a `Window`:

```xml
<Window ...>
    <TextBlock x:Name="CountText" Text="Parts: 0" FontSize="28" />
    <Button x:Name="CountButton" Content="+1 PART" MinHeight="64" Click="OnCountClick" />
</Window>
```

```
MainWindow.xaml(6,6): error MC3089: The object 'Window' already has a child and cannot add 'Button'. 'Window' can accept only one child. Line 6 Position 6.
```

The fix is a panel around them. A window's `Content` is one object; panels exist to hold many.

**A misspelled property is a build error:**

```
MainWindow.xaml(7,38): error MC3072: The property 'Contnet' does not exist in XML namespace 'http://schemas.microsoft.com/winfx/2006/xaml/presentation'. Line 7 Position 38.
```

**A tag that does not close is not XML at all.** Writing `FontSize="28">` where `FontSize="28" />`
belongs gives:

```
MainWindow.xaml(8,7): error MC3000: 'The 'TextBlock' start tag on line 6 position 10 does not match the end tag of 'StackPanel'. Line 8, position 7.' XML is not valid.
```

The error names line 8, where the parser noticed, and line 6, where the mistake is.

**A value the property cannot use builds fine and fails at run time.** `MinHeight="tall"` passed the
build on the build machine. Creating the window threw a `System.Windows.Markup.XamlParseException`
with this message:

```
'Provide value on 'System.Windows.Baml2006.TypeConverterMarkupExtension' threw an exception.' Line number '7' and line position '38'.
```

Its inner exception was a `System.FormatException` with this message:

```
'tall' string cannot be converted to Length.
```

The inner exception is the useful part. Read it first. Visual Studio shows it under "Inner
Exception" when the app stops [VERIFY the label in Visual Studio 2026].

---

## Why the wrong version is tempting

The designer lets you drop two controls on a window and shows them both, so it feels like a window
holds many things. It does not. The new-window template already contains an empty `Grid`, so
dropped controls land inside it. When you type XAML yourself and delete that `Grid`, nothing holds
them.

Typos are tempting for a different reason: XAML looks like a document, and documents forgive
spelling. XAML is code. `Contnet` is not a property, the same way `Consle.WriteLine` is not a method.

---

## Vocabulary

| Term | What it means |
|---|---|
| **XAML** | a markup language that describes objects and their properties |
| **Element** | one object in XAML, written as a tag |
| **Attribute** | a property setting inside a tag |
| **Panel** | an element that holds and arranges children: `Grid`, `StackPanel`, `DockPanel`, `UniformGrid` |
| **Attached property** | a property set on a child and read by its parent, such as `Grid.Row` |
| **`x:Name`** | gives an element a name and makes a field for it in the code-behind |
| **Code-behind** | the C# half of a window, `MainWindow.xaml.cs` |
| **`InitializeComponent()`** | the generated method that builds everything the XAML describes |
| **Logical tree** | the objects and their parent-child links, as the XAML nests them |

---

## Self-check

**Question 1.** Rewrite this C# as one line of XAML:
`Button reset = new() { Name = "ResetButton", Content = "RESET SHIFT", IsEnabled = false };`

**Question 2.** A window has a `Grid` with rows `Auto`, `Auto`, `*`. The status text is in row 2 with
`VerticalAlignment="Bottom"`. The window grows taller. Which row gets the extra height, and where does
the status text go?

**Question 3.** This builds, but the first click crashes with `NullReferenceException` at the line
that sets `CountText.Text`. What was removed from the constructor, and why does it matter?

```csharp
public MainWindow()
{
}
```

---

### Answers

**1.** `<Button x:Name="ResetButton" Content="RESET SHIFT" IsEnabled="False" />`

**2.** Row 2, the `*` row, gets all the extra height. The status text stays at the bottom of that row,
so it moves down with the window's bottom edge.

**3.** `InitializeComponent();` was removed. That call builds every object in the XAML and fills the
`x:Name` fields. Without it, `CountText` is still `null`, so the first handler that uses it throws.
The build machine reproduced this: the click threw `System.NullReferenceException: Object reference
not set to an instance of an object.` from `OnCountClick`.

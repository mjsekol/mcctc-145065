# Lecture Notes: Announcing Every Change
## 145065 Object-Oriented Programming · Unit 7 · Week 14, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W14_ChangeNotification.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-07-event-driven-wpf/04-slides/MCCTC_145065_Slides_W14_ChangeNotification.md --export pptx`

If you missed class, including for BPA Nationals, you can learn this concept from this file alone. You
need the .NET SDK and the Lab U07-03 files.

**Competencies:** 5.4.7 debug logic errors. 5.3.12 write code that creates classes, objects, and
methods.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented shop.

---

## Why this exists

Tuesday ended with a screen that showed the right values once and then stopped changing. The view
model held 37 good parts. The window said zero.

That is the most dangerous bug in this unit, because **nothing crashes and nothing warns**. An
operator trusts a number that is no longer true. In Unit 8, the same bug would show a temperature
from ten minutes ago as if it were live.

---

## The concept in plain language

A binding reads its source property once. It reads again **only when the source object announces
that the property changed**, by name. An object announces through one interface:

```csharp
public interface INotifyPropertyChanged
{
    event PropertyChangedEventHandler? PropertyChanged;
}
```

That is the whole contract: one event whose argument carries a property name. WPF subscribes to it
when it binds, and when the event arrives with a name it is bound to, it reads that property again.

Three rules follow.

1. **Announce after you change a stored value.** Every setter that changes a field raises the event
   with its own name.
2. **Announce what depends on it.** If `Total` is computed from `Good`, then a change to `Good` must
   also announce `Total`. Nothing figures that out for you.
3. **Do not announce what did not change.** Setting 200 when the value is already 200 announces
   nothing. Every announcement makes bound controls redraw.

A small helper handles rules 1 and 3 for every property. From the Lab U07-03 solution:

```csharp
private bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
{
    if (EqualityComparer<T>.Default.Equals(field, value))
    {
        return false;
    }

    field = value;
    Changed(name);
    return true;
}

private void Changed(string? name) => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
```

`[CallerMemberName]` fills in the name of the property that called `Set`, so a setter can write
`Set(ref good, value)` without typing `"Good"`.

Rule 2 is a table you write by hand:

| When this changes | Also announce |
|---|---|
| `Good` or `Scrap` | `Total`, `Progress`, `ProgressText`, `ScrapRateText`, `CanUndo` |
| `Target` | `Progress`, `ProgressText` |
| `Station` | `StationName`, `StationIsValid`, `Heading` |
| `PartType` | `Heading` |

---

## Worked example 1: the same binding, silent and announced

`Shift` has no notifications. `LoudShift` implements `INotifyPropertyChanged`.

```csharp
Shift quiet = new() { Scrap = 3 };
TextBlock quietText = new() { DataContext = quiet };
quietText.SetBinding(TextBlock.TextProperty, new Binding("Scrap") { StringFormat = "Scrap: {0}" });
quiet.Scrap = 4;
Console.WriteLine($"No announcement:  object holds {quiet.Scrap}, screen shows \"{quietText.Text}\"");

LoudShift loud = new() { Scrap = 3 };
TextBlock loudText = new() { DataContext = loud };
loudText.SetBinding(TextBlock.TextProperty, new Binding("Scrap") { StringFormat = "Scrap: {0}" });
loud.Scrap = 4;
Console.WriteLine($"With announcement: object holds {loud.Scrap}, screen shows \"{loudText.Text}\"");
```

Output:

```
No announcement:  object holds 4, screen shows "Scrap: 3"
With announcement: object holds 4, screen shows "Scrap: 4"
```

Same binding, same change. Only the announcement differs.

---

## Worked example 2: the dependent property

`LoudShift` announces `Scrap` always, and `Total` only when its `AnnounceTotal` switch is on:

```csharp
private void SetCount(ref int field, int value, [CallerMemberName] string? name = null)
{
    if (field == value)
    {
        return;   // nothing changed, so nothing to announce
    }

    field = value;
    PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    if (AnnounceTotal)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Total)));
    }
}
```

A TextBlock bound to `Total`, before and after scrap goes from 0 to 2 with 5 good parts:

```csharp
foreach (bool announceTotal in new[] { false, true })
{
    LoudShift shift = new() { Good = 5, AnnounceTotal = announceTotal };
    TextBlock totalText = new() { DataContext = shift };
    totalText.SetBinding(TextBlock.TextProperty, new Binding("Total") { StringFormat = "Total: {0}" });
    shift.Scrap = 2;
    Console.WriteLine($"Announce Total too? {announceTotal,-5}  object total {shift.Total}, screen shows \"{totalText.Text}\"");
}
```

Output:

```
Announce Total too? False  object total 7, screen shows "Total: 5"
Announce Total too? True   object total 7, screen shows "Total: 7"
```

`Total` was always right when read. The screen did not read it until it was told to.

---

## Worked example 3: listening to the announcements

```csharp
LoudShift shift = new() { AnnounceTotal = true };
shift.PropertyChanged += (_, e) => Console.WriteLine($"announced: {e.PropertyName}");
shift.Scrap = 1;
shift.Scrap = 1;
Console.WriteLine("(the second assignment announced nothing)");
```

Output:

```
announced: Scrap
announced: Total
(the second assignment announced nothing)
```

This is how the lab's `NotificationTests` work: subscribe, change something, and check the list of
names heard. From `ShiftTally.Core.Tests`:

```csharp
[Fact]
public void AGoodPartAnnouncesEveryPropertyComputedFromTheCounts()
{
    TallyViewModel tally = new();
    List<string?> heard = Listen(tally);
    tally.AddGood();
    AssertAnnounced(heard, "Good", "Total", "Progress", "ProgressText", "ScrapRateText", "CanUndo", "Status");
}
```

---

## Worked example 4: the whole counting property

From the Lab U07-03 solution:

```csharp
public int Good
{
    get => good;
    private set
    {
        if (Set(ref good, value))
        {
            CountsChanged();
        }
    }
}

private void CountsChanged()
{
    Changed(nameof(Total));
    Changed(nameof(Progress));
    Changed(nameof(ProgressText));
    Changed(nameof(ScrapRateText));
    Changed(nameof(CanUndo));
}
```

`private set` means only the view model's own methods (`AddGood`, `Undo`, `Reset`) can change the
count. `Set` returns `false` when nothing changed, so `CountsChanged` runs only for a real change.
With this in place, the Lab U07-03 window checks went from 24 of 30 to 30 of 30.

---

## The wrong version, and what it produces

**A misspelled name in a string.** This compiles and runs:

```csharp
public void AddScrap()
{
    scrap++;
    PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Scarp"));
}
```

A listener shows exactly what happened:

```
announced: Scarp
Scrap is 1
```

Nobody is bound to `Scarp`, so nothing redraws. No error appears anywhere.

**The same mistake with `nameof`** does not compile:

```csharp
PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Scarp)));
```

```
Program.cs(17,75): error CS0103: The name 'Scarp' does not exist in the current context
```

`nameof` turns a spelling mistake into a build error. Use it for every announcement.

**The forgotten dependent.** Delete `Changed(nameof(ScrapRateText));` from `CountsChanged`. Press
+1 SCRAP three times. The counts update. The scrap rate keeps its old value. The build is clean, the
Output window is empty, and the Lab U07-03 test
`AGoodPartAnnouncesEveryPropertyComputedFromTheCounts` fails with:

```
ScrapRateText changed but was never announced. A control bound to it keeps showing the old value.
```

followed by the list of names that were announced.

---

## Why the wrong version is tempting

Computed properties feel automatic: `Total => Good + Scrap` is always right, so it seems the screen
must be too. The screen is a separate copy, and copies only refresh when asked.

The forgotten dependent is also invisible in a quick test. You press the button, the big number
changes, and you move on. The small number in the corner is the one that is wrong.

The habit that prevents it: **write the dependency table before you write the setters**, and write
one test per row.

---

## Vocabulary

| Term | What it means |
|---|---|
| **`INotifyPropertyChanged`** | the interface a class implements to announce property changes |
| **`PropertyChanged`** | the interface's one event; its argument names the property |
| **Announce** | raise `PropertyChanged` for a property |
| **Dependent property** | a property computed from another one |
| **Dependency table** | the list of what must be announced when each value changes |
| **`[CallerMemberName]`** | fills a parameter with the name of the calling property or method |
| **`nameof`** | turns a name into a string, checked by the compiler |
| **Stale display** | a screen showing an old value while the object holds a new one |

---

## Self-check

**Question 1.** A view model has `Temperature` and a computed `AlarmText` that says "HIGH" above 230.
The `Temperature` setter announces only `Temperature`. The reading goes from 225 to 236. What does a
TextBlock bound to `AlarmText` show?

**Question 2.** Why does the `Set` helper compare the old and new values before announcing?

**Question 3.** Write the dependency table rows for this class:

```csharp
public int Good { get; private set; }
public int Scrap { get; private set; }
public int Target { get; set; }
public int Total => Good + Scrap;
public bool TargetReached => Good >= Target;
public string Summary => $"{Good} good of {Total}";
```

---

### Answers

**1.** Whatever it showed at 225, which is not "HIGH". `AlarmText` was never announced, so the
binding never read it again. This is exactly the kind of stale display Unit 8 must never allow.

**2.** Announcing a change that did not happen makes every bound control read and redraw for
nothing. It also means a two-way binding that writes back an unchanged value triggers another
announcement for no reason.

**3.**

| When this changes | Also announce |
|---|---|
| `Good` | `Total`, `TargetReached`, `Summary` |
| `Scrap` | `Total`, `Summary` |
| `Target` | `TargetReached` |

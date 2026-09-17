# Announcing Every Change
---
## Slide 1: The number that lied
- The view model holds 37 good parts
- The screen says 0
- Nothing crashed
- An operator would trust the 0
Speaker notes: Yesterday ended with this picture. The object was right. The screen was wrong. There was no error to read. In Unit 8, the same bug shows a temperature from ten minutes ago as if it were live. Today you learn the one interface that prevents it, and the discipline it needs.
Image: The ShiftTally window showing Good: 0 beside a debugger tooltip reading 37.
---
## Slide 2: One interface, one event
```csharp
public interface INotifyPropertyChanged
{
    event PropertyChangedEventHandler? PropertyChanged;
}
```
Speaker notes: That is the whole contract. One event, and its argument carries a property name. WPF subscribes when it binds. When the event arrives with a name it is bound to, it reads that property again. No event, no read.
Image: None. This slide is code.
---
## Slide 3: Three rules
- Announce a stored value when it changes
- Announce everything computed from it
- Announce nothing that did not change
- nameof, never a typed string
Speaker notes: One: every setter that changes a field announces its own name. Two: if Total is computed from Good, a change to Good also announces Total. Nothing does that for you. Three: setting the same value again announces nothing. And always use nameof, so the compiler checks the spelling.
Image: Three numbered cards and a fourth card showing nameof with a green check.
---
## Slide 4: The helper and the table
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

private void CountsChanged()
{
    Changed(nameof(Total));
    Changed(nameof(Progress));
    Changed(nameof(ProgressText));
    Changed(nameof(ScrapRateText));
    Changed(nameof(CanUndo));
}
```
Speaker notes: Set handles rules one and three for every property. CallerMemberName fills in the property's name for you. CountsChanged is rule two, written by hand: everything that depends on a count. The Good and Scrap setters call it only when Set says something really changed.
Image: None. This slide is code.
---
## Slide 5: Silent and announced
```
No announcement:  object holds 4, screen shows "Scrap: 3"
With announcement: object holds 4, screen shows "Scrap: 4"
Announce Total too? False  object total 7, screen shows "Total: 5"
Announce Total too? True   object total 7, screen shows "Total: 7"
```
Speaker notes: Four lines from the verification program. Same binding, same change. Without the announcement the screen stays at 3. With it, 4. The second pair is the dependent property: Total was always right when read, but the screen did not read it until it was told to.
Image: None. This slide is code.
---
## Slide 6: Write the table first
- Good or Scrap: Total, Progress, ProgressText, ScrapRateText, CanUndo
- Target: Progress, ProgressText
- Station: StationName, StationIsValid, Heading
- PartType: Heading
Speaker notes: Before you write setters, write this table for your own app. Each row says what else must be announced when that value changes. Then write one test per row. A table on paper takes two minutes. A stale number in production can take a day to find.
Image: A hand-drawn dependency table with arrows from each input to its dependents.
---
## Slide 7: The wrong way: a typo in a string
```csharp
PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Scarp"));
```
```
announced: Scarp
Scrap is 1
```
- Compiles, runs, updates nothing
- nameof(Scarp) would not compile: error CS0103
Speaker notes: A misspelled string compiles and runs. The event fires for a property called Scarp, which nobody is bound to, so nothing redraws. Write nameof instead and the same mistake stops the build with error CS0103, the name Scarp does not exist in the current context.
Image: A mailbox labeled Scarp overflowing with unread letters.
---
## Slide 8: The forgotten dependent
- Delete one line: ScrapRateText
- Press +1 SCRAP: the counts move
- The rate stays where it was
- A test names exactly what is missing
Speaker notes: Here is today's deliberate error. Remove the ScrapRateText line from CountsChanged. The counts update. The rate does not. The build is clean and the Output window is empty. The lab's test fails with a message: ScrapRateText changed but was never announced, followed by the list of names that were announced.
Image: The ShiftTally window with updated counts and a rate line wrapped in launch red tape.
---
## Slide 9: Wednesday's numbers
- View model tests: 23 of 23
- Window checks: 30 of 30
- The picture matches the view model
- Anyone done starts commands and shortcuts
Speaker notes: With announcements in place, the eight notification tests pass and the six live screen checks come back, so the window goes from twenty-four of thirty to thirty of thirty. Open the picture. It should show thirty-seven good parts now. The EXTENDED option replaces the Click handlers with commands and adds keyboard shortcuts.
Image: A fully green test summary bar and the ShiftTally picture showing 37 good parts.
---
## Slide 10: What you are about to build
- Lab U07-03 Part 3: make TallyViewModel announce
- Implement the interface and the Set helper
- Announce the counts, target, station, and part
- Then your app's table and one test per row
Speaker notes: Build 1 is the interface, the helper, and every announcement in the dependency table. Build 2 is the full self-check and the picture. Then turn to your own app: write its dependency table, add the announcements, and write at least one test that proves a dependent property is announced.
Image: A dependency table beside a green test run.

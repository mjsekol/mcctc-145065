# What the Build Is Telling You
---
## Slide 1: A clean build that crashes
- One exclamation point added
- The yellow warning disappeared
- Zero warnings, zero errors
- NullReferenceException on the next shift
Speaker notes: A teammate had one yellow warning. They added one character, an exclamation point, and the warning went away. The build was perfectly clean. On the next shift the panel threw a null reference exception. Today is about what warnings are, why teams turn them into errors, and why making a warning disappear is not the same as fixing it.
Image: A spotless build report pinned next to a crash report.
---
## Slide 2: A warning is a review
- The compiler studied the code without running it
- It found something suspicious
- It built the program anyway
- That is static analysis
Speaker notes: A warning is a code review done by a program. The compiler studied your code without running it, found something suspicious, and let the build succeed anyway. That is static analysis, and it is one half of a code review. The other half is people, and you do that half in build two.
Image: A robot inspector with a clipboard leaning over a page of code.
---
## Slide 3: The warning, and what it meant
```csharp
string? badge = FindBadge("L3-PRS-02");
Console.WriteLine(badge.ToUpper());
```
```
warning CS8602: Dereference of a possibly null reference.
Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.
```
Speaker notes: String with a question mark says badge may be null. The compiler warned: you are calling a method on something that may be null. The build succeeded anyway. Then it ran, the press was not locked out, badge was null, and it crashed. The warning told us exactly what would happen.
Image: None. This slide is code.
---
## Slide 4: The team decides warnings stop the build
```xml
<TreatWarningsAsErrors>true</TreatWarningsAsErrors>
```
```
error CS8602: Dereference of a possibly null reference.
```
Speaker notes: One line in the project file. Now the same warning is an error, and nothing runs. The crash was found at the desk. This is a team decision, not a compiler rule, and it costs something: every warning now has to be fixed or explained before anyone can run anything.
Image: None. This slide is code.
---
## Slide 5: Silencing is not fixing
```csharp
Console.WriteLine(badge!.ToUpper());
```
- Builds with warnings as errors, zero warnings
- Still throws NullReferenceException
- The exclamation point adds no check
- Reviewers ask: where is the proof?
Speaker notes: Here is the wrong way. The exclamation point is the null forgiving operator. It tells the analyzer to trust you. The build is clean, even with warnings as errors, and the program still throws, exactly as before. Pragma warning disable does the same thing. Every time you see either one in a review, ask where the proof is that the value exists.
Image: None. This slide is code.
---
## Slide 6: The fix decides what nothing means
```csharp
Console.WriteLine(badge is null ? "not locked out" : badge.ToUpper());
```
Speaker notes: The real fix makes a decision. What should the panel say when there is no badge? Not locked out. Now the null case is handled, the warning is gone because there is nothing left to warn about, and the program prints not locked out. That is the difference between silencing and fixing.
Image: None. This slide is code.
---
## Slide 7: Add one line to an interface
```
error CS0535: 'SimulatedOven' does not implement interface member 'IReadingSource.Remaining'
error CS0535: 'ScriptedSource' does not implement interface member 'IReadingSource.Remaining'
error CS0535: 'TextLineSource' does not implement interface member 'IReadingSource.Remaining'
```
Speaker notes: One line added to IReadingSource: an int called Remaining. Three errors, one for every class that promised the old contract. Not in file order, so read the whole list. Code that only calls the interface is not on it. This list is an impact analysis. It is everything your one-line change breaks, found before anything runs.
Image: None. This slide is code.
---
## Slide 8: Interface control is a decision
- The list shows who breaks
- You decide whether the change should happen
- A live sensor cannot count what remains
- Revert, or add a narrower interface
Speaker notes: The list tells you who breaks. It does not tell you whether to make the change. That is the decision, and it is called interface control. A live sensor cannot know how many readings remain, so this member promises more than every source can keep. The right call is to take it back out, or to put it in a separate, narrower interface.
Image: A change request form with "impact" filled in and "approved" left unchecked.
---
## Slide 9: The human half
- The author demonstrates, then stays quiet
- The reviewer asks, the recorder writes
- Every finding gets a decision
- Fixed, deferred, or kept, with a reason
Speaker notes: The other half of a review is people. A peer walkthrough. The author gives a three minute demo, then stops defending. The reviewer asks questions a compiler cannot, like what your interface promises that one class cannot keep. The recorder writes every finding. Before the period ends, the author writes a decision for each one.
Image: Three students at a table: one pointing at a screen, one asking, one writing.
---
## Slide 10: What you are about to build
- Lab U06-03, Part 4: warnings become errors
- Fix the two real bugs they found
- Add Remaining, read the list, decide
- Then the same two steps on your port
Speaker notes: Build one is the last part of the lab. Turn on warnings as errors, and the two warnings you have ignored all week stop the build. Fix them properly, no exclamation points. Then add Remaining to the interface, record the list, decide, and write IMPACT dot md. Then do both steps on your own port. Build two is the peer walkthrough and your demo.
Image: A build log going from two yellow lines to a clean green line.
---

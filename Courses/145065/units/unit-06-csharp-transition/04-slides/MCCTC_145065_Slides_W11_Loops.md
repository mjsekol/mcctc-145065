# Four Loops and One Crash
---
## Slide 1: The summary that crashed at the end
- Thirty minutes of oven readings
- The loop printed all thirty
- Then the program crashed
- The build had zero warnings
Speaker notes: Here is a shift summary that printed every one of its thirty readings, and then crashed. The build was perfectly clean. By the end of this segment you will be able to find that bug in about three seconds, and you will know why no compiler on earth could have warned you about it.
Image: A printout of thirty numbered readings with a torn edge after the last line and a red crash symbol.
---
## Slide 2: You already know all four
- for i in range(n) becomes a for loop
- for x in items becomes foreach
- while stays while
- do while runs the body at least once
Speaker notes: Good news first. There is nothing new in the idea of a loop. A Python range loop becomes a C# for loop. Looping over items becomes foreach. While is still while. The only new one is do while, which checks its condition after the body, so the body always runs at least once.
Image: A two-column matching chart, Python loops on the left and C# loops on the right, connected by lines.
---
## Slide 3: for and foreach
```csharp
double[] temps = { 199.2, 212.5, 216.0, 208.1 };

for (int i = 0; i < temps.Length; i++)
{
    Console.WriteLine($"minute {i + 1} is {temps[i]}");
}

int over = 0;
foreach (double t in temps)
{
    if (t > 210) { over++; }
}
```
Speaker notes: The for loop has three parts in the parentheses. Start at zero. Keep going while i is less than the length. Add one each time. Use it when you need the position number. The foreach loop gives you each reading, typed as a double, and you never touch an index. That makes foreach the safer choice whenever the position does not matter.
Image: None. This slide is code.
---
## Slide 4: while and do
```csharp
int minute = 0;
while (minute < temps.Length && temps[minute] < 215)
{
    minute++;
}

int tries = 0;
do
{
    tries++;
} while (tries < 0);
```
Speaker notes: The while loop stops at the first reading at or above 215. Look at the order in the condition. The index check comes first. The double ampersand stops as soon as the left side is false, so the array is never read past its end. The do loop runs once even though tries less than zero is false from the start.
Image: None. This slide is code.
---
## Slide 5: Three rules Python never had
- The loop variable has a type
- The condition must be a real bool
- A variable dies at its closing brace
Speaker notes: Here is what the compiler checks in every loop. The loop variable has a declared type. The condition must be true or false, so while remaining, with a number, does not build. And a variable declared inside the braces does not exist after them. Python keeps loop variables alive after the loop. C# does not.
Image: A loop drawn as a fenced yard, with a variable inside the fence unable to walk out the gate.
---
## Slide 6: The compiler catches this one
```csharp
double total;
foreach (double reading in temps)
{
    total += reading;
}
```
```
error CS0165: Use of unassigned local variable 'total'
```
Speaker notes: Here is the wrong way with the real error. The running total was never given a starting value, and total plus equals reading reads it. CS0165, use of unassigned local variable. The fix is one word on the declaration line: equals zero. The compiler found this one at your desk.
Image: None. This slide is code.
---
## Slide 7: The compiler cannot catch this one
```csharp
for (int i = 0; i <= temps.Length; i++)
{
    Console.WriteLine($"Minute {i + 1}: {temps[i]}");
}
```
```
Unhandled exception. System.IndexOutOfRangeException: Index was outside the bounds of the array.
```
Speaker notes: This is the summary from slide one. Less than or equal. An array of three has indexes zero, one, and two, and this loop asks for three. It builds with zero warnings, prints every reading, and crashes. The compiler cannot warn you, because the array's length is only known when the program runs. Python does the same thing with range of length plus one.
Image: None. This slide is code.
---
## Slide 8: Skip one, stop early
- continue skips to the next pass
- break leaves the loop entirely
- Both work exactly as in Python
- A null reading is a good reason to continue
Speaker notes: Continue and break work the way you remember. In the lab, a missing reading is a null, and you skip it with continue rather than counting it as zero. A reading above the maximum is a reason to break and report. Missing is not zero. Say it every time.
Image: A conveyor with one empty slot being skipped and a red stop bar at the end.
---
## Slide 9: Habits that prevent every bug today
- Write i less than Length, every time
- Give every total a start value
- Declare a variable where you need it
- Put the index check first
Speaker notes: Four habits, and they prevent every bug on these slides. Less than, never less than or equal, when you count up to a length. A starting value on the line that declares a running total. Declare a variable at the level where you will use it. And when a condition reads an array, check the index first.
Image: Four checkboxes on a clipboard, all ticked.
---
## Slide 10: What you are about to build
- Lab U06-01, Part 3: the oven summary
- Average and highest with foreach
- First drift with for, steady minutes with while
- Break it with less than or equal, on purpose
Speaker notes: Build one finishes the Shift Summary. You compute the average and the highest reading with foreach, the first minute out of tolerance with for, and the steady minutes with while, index check first. Step ten asks you to break your own for loop with less than or equal, watch the crash, write down what printed, and fix it. Then your output must match the lab line for line.
Image: A finished shift summary with an oven temperature chart beside it.
---

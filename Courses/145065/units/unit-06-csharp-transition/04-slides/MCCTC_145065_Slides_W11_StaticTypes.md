# Zero Percent Uptime
---
## Slide 1: The press that never ran
- Press 1 ran 437 of 480 minutes
- The new C# report says 0 percent uptime
- No error, no warning, no crash
- The Python report said 91 percent
Speaker notes: Here is a real kind of report. Press 1 was scheduled for 480 minutes and ran 437. The Python version of the report said 91 percent uptime. Somebody ported it to C#, the build was clean, and the report now says zero. Nobody got an error. By the end of this segment you will know exactly why, and you will never write it again.
Image: A shift report card with "Uptime: 0%" circled in red and a press running happily in the background.
---
## Slide 2: One type, forever
- Every C# variable has one type
- The compiler fixes it when it builds
- var still means one type
- Python names can change type anytime
Speaker notes: In Python a name can hold a number now and a string later. In C#, every variable has one type, decided when the program is compiled. You can write the type, or write var and let the compiler work it out from the first value. Either way it never changes. That is what static typing means.
Image: A label maker printing "int" onto a storage bin, with the bin bolted to a shelf.
---
## Slide 3: The types you will use
- int, long: whole numbers
- double: fractions, approximately
- decimal: exact fractions, for money
- bool, char, string: true or false, one character, text
- double?: a number or nothing
Speaker notes: Here are the types for this unit. int for counts, long when a count gets huge. double for measurements. decimal for money, because it is exact. bool, char with single quotes, and string with double quotes. And double with a question mark, which is a number that might be missing. You will lean on that one all semester.
Image: A parts bin organizer with one labeled drawer per type.
---
## Slide 4: Same digits, different answers
```csharp
Console.WriteLine(7 / 2);       // 3
Console.WriteLine(7 / 2.0);     // 3.5
Console.WriteLine(7 % 2);       // 1
Console.WriteLine(-7 / 2);      // -3
Console.WriteLine(0.1m + 0.2m); // 0.3
```
Speaker notes: Predict each line before I run it. Seven divided by two is three, because both are ints, so the fraction is thrown away. Make one side a double and you get three point five. Percent is the remainder. Negative seven over two is negative three in C#, where Python's floor division gives negative four. And the m suffix makes decimals exact.
Image: None. This slide is code.
---
## Slide 5: The type is forever, even with var
```csharp
var partsMade = 1250;
partsMade = "twelve hundred fifty";
```
```
error CS0029: Cannot implicitly convert type 'string' to 'int'
```
Speaker notes: This is the wrong way, with the real error. var made partsMade an int on the first line. The second line tries to put text in it, and the compiler refuses with CS0029. The same two lines in Python run without a word. This is a mistake C# catches for you.
Image: None. This slide is code.
---
## Slide 6: The line that compiles and lies
```csharp
int runMinutes = 437;
int scheduledMinutes = 480;
double uptimePercent = runMinutes / scheduledMinutes * 100;
Console.WriteLine(uptimePercent);   // 0
```
Speaker notes: This is the report from slide one. It builds with zero warnings. It prints zero. Four hundred thirty seven divided by four hundred eighty, both ints, is zero. Zero times one hundred is zero. Only then does the zero go into the double. Declaring the variable as double did not help, because the division was already over.
Image: None. This slide is code.
---
## Slide 7: Why your Python habit caused it
- Python 3: slash always gives a float
- C#: int slash int is integer division
- Your formula was right in Python
- The compiler cannot know you meant a fraction
Speaker notes: This is not a careless mistake. Your Python was correct. In Python 3, the slash always gives a float, so run over scheduled times one hundred is ninety one point zero four. You carried a correct habit into a language with a different rule, and the compiler has no way to know you wanted a fraction. Consistent is not the same as right.
Image: A passport stamped "Python" being handed to a border officer labeled "C#" who shrugs.
---
## Slide 8: The fix
```csharp
double fixedPercent = runMinutes * 100.0 / scheduledMinutes;
Console.WriteLine(fixedPercent);   // 91.04166666666667
```
Speaker notes: Make the arithmetic a double before any division happens. Multiplying by one hundred point zero turns the whole expression into doubles, and now we get ninety one point zero four. The habit: every time you divide, say the types of both sides out loud. If both are whole numbers, ask yourself whether you want a whole number back.
Image: None. This slide is code.
---
## Slide 9: One value, three spellings
- 0x2C is hexadecimal, 0b0010_1100 is binary
- Both are the number 44
- ToString("X") prints hex
- Convert.ToString(value, 2) prints binary
Speaker notes: One more thing from 145060. You converted bases by hand in Week 4. C# writes hex with zero x and binary with zero b, the same as Python. The press controller sends a status word, and it is forty four whether you write it in hex, in binary, or in decimal. Only the text changes, never the value.
Image: One gear drawn three times with labels "44", "0x2C", and "00101100".
---
## Slide 10: What you are about to build
- Lab U06-01, Part 2: the shift numbers
- Uptime, full boxes, parts left over
- The status word in three bases
- Make the zero percent bug on purpose
Speaker notes: Build one is Part 2 of the Shift Summary. You calculate uptime, full boxes, and leftover parts, and you print the status word three ways. Step six asks you to write the zero percent bug on purpose, see it, and write one sentence in your build log about why no error appeared. Then you fix it. Integer division is exactly right for full boxes, so think before you change every int.
Image: A shift summary printout with uptime, boxes, and a status word in three bases.
---

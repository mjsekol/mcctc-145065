# A Promise the Compiler Checks
---
## Slide 1: The loop that crashed halfway
- The line inspects every machine
- Four machines already started
- The rack has no start method
- AttributeError, halfway through
Speaker notes: In Unit 2, a loop called the same method on every machine. It worked because every class happened to have that method. Then someone added a class without it. The loop started four machines, reached the rack, and crashed. Half an operation on real equipment is worse than none. Today you learn how to make that promise checkable.
Image: A row of five machines, four with green lights, the fifth with a red question mark.
---
## Slide 2: An interface is a list of promises
```csharp
interface IReadingSource
{
    string Name { get; }
    double? Next();
}
```
Speaker notes: This is an interface. It lists members and has no code at all. Any reading source must have a name and a Next method that returns a reading that might be missing. The capital I at the front is the naming convention. On its own, this does nothing. It becomes useful when classes promise to keep it.
Image: None. This slide is code.
---
## Slide 3: Keeping the promise
```csharp
sealed class ScriptedSource : IReadingSource
{
    private readonly double?[] _values;
    private int _index;

    public ScriptedSource(string name, double?[] values)
    {
        Name = name;
        _values = values;
    }

    public string Name { get; }

    public double? Next() => _index < _values.Length ? _values[_index++] : null;
}
```
Speaker notes: The colon IReadingSource is the promise. This class supplies both members, with exactly the promised types. It replays a list of values and returns null when it runs out. A second class, TextLineSource, parses pasted log lines instead. Completely different code, the same promise.
Image: None. This slide is code.
---
## Slide 4: Code that trusts only the promise
```csharp
foreach (IReadingSource source in sources)
{
    Console.WriteLine(source.Name);
    double? value = source.Next();
    Console.WriteLine(value is double v ? $"  {v}" : "  missing");
}
```
Speaker notes: This loop never asks what kind of source it holds. It works with the scripted source, the log source, and a live Raspberry Pi source that nobody has written yet. Value is double v checks for a reading and unwraps it in one step. A missing reading prints missing, never zero.
Image: None. This slide is code.
---
## Slide 5: Skip a member
```csharp
sealed class ScriptedSource : IReadingSource
{
    public string Name => "bench script";
}
```
```
error CS0535: 'ScriptedSource' does not implement interface member 'IReadingSource.Next()'
```
Speaker notes: Here is the wrong way with the real error. The class promised the interface and skipped Next. CS0535, at build time. Python's version of this mistake builds, runs, and crashes when the loop reaches that object. This is the halfway crash from slide one, found at your desk instead.
Image: None. This slide is code.
---
## Slide 6: Promise less, and it still fails
- Interface: double? Next()
- Class: double Next()
- CS0738: the return type does not match
- A double can never say missing
Speaker notes: A sneakier version. The class returns a plain double instead of a nullable one. Every double fits in a double question mark, so it seems close enough. The compiler says CS0738. The contract promised callers a value that can say missing. A plain double never can, so the class does not keep the promise.
Image: A delivery form with a box labeled "missing" that the sender removed.
---
## Slide 7: You only see the contract
- ScriptedSource also has Rewind
- Through IReadingSource, Rewind does not exist
- CS1061 if you try
- That keeps code working with any source
Speaker notes: The scripted source has an extra method, Rewind. If your variable's type is the interface, Rewind is not there, and calling it is CS1061. That feels annoying for about a minute. Then you notice it guarantees your code will still work when someone hands it a live sensor that cannot rewind.
Image: A universal remote with only the buttons every TV supports.
---
## Slide 8: Interface or base class
- Interface: shares a promise, no code
- Base class: shares code and one "is a"
- A class can keep many interfaces
- A class has only one parent
Speaker notes: When do you use which? A base class shares code and says what a thing is, and a class gets only one. An interface shares only a promise, and a class can keep several. A battery and a tool kit can both be checkable without being tools. That is interface territory.
Image: A Venn diagram: "shares code" on one side, "shares a promise" on the other, a class keeping several promises in the middle.
---
## Slide 9: Promise only what everyone can keep
- A script knows how many readings remain
- A live sensor does not
- Remaining in the interface forces a lie
- Or a NotSupportedException at run time
Speaker notes: The hardest design rule of the day. An interface should promise only what every implementation can keep. A scripted source knows how many readings remain. A live sensor never does. Put Remaining in the interface and the live sensor must invent a number or throw at run time, which is the crash interfaces were supposed to prevent.
Image: A contract with one clause crossed out in red.
---
## Slide 10: What you are about to build
- Lab U06-03, Part 2: the reading contract
- ScriptedSource and LogLineSource
- One contract test runs against both
- ShiftMonitor never names either class
Speaker notes: Build one is Part 2 of the lab. You write the interface, a scripted source, and a log line source that turns unreadable lines into missing readings. One set of contract tests runs against both classes. Then ShiftMonitor summarizes any source, and it may not mention either class by name. In build two, your port gets its own interface and two classes that keep it.
Image: Two different machines plugged into the same labeled socket.
---

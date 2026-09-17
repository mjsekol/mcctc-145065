# Who May Touch What
---
## Slide 1: Five hundred degrees, and fine
- The oven reads 500 degrees
- The panel says it is under maximum
- Someone raised the maximum to 9999
- Every test passed
Speaker notes: Here is an oven class. The oven reads five hundred degrees, and the panel says it is below its maximum. How? Some other piece of code set the maximum to nine thousand nine hundred ninety nine. The class had public fields, so anyone could. Every test passed, because every test used the class correctly. Today is about making that impossible.
Image: An oven gauge in the red zone with a sticky note on the limit dial reading "9999."
---
## Slide 2: The leak
```csharp
class LeakyOven
{
    public double TemperatureC;
    public double MaxC;

    public bool IsOverMaximum => TemperatureC > MaxC;
}
```
Speaker notes: Two public fields. Any caller can set either one to anything. Set the temperature to NaN and IsOverMaximum is false, because NaN compares false with everything. Raise MaxC and a real overheat is false too. It builds with zero warnings. Python behaves exactly the same. This is the dangerous design that works today.
Image: None. This slide is code.
---
## Slide 3: Four modifiers
- public: anyone, the contract
- private: this class only, subclasses too
- protected: this class and its subclasses
- internal: this project only
Speaker notes: Four words. Public is the contract, what callers may rely on. Private is this class only, and that includes subclasses. Protected adds subclasses. Internal means any code in the same project. In Python, one underscore asked people to stay out. In C#, the compiler makes them.
Image: A building with four doors: a front door, a locked office, a staff-only hallway, and a badge-only wing.
---
## Slide 4: Read it, but do not change it
```csharp
public bool IsRunning { get; private set; }
```
- Anyone can read IsRunning
- Only Start and Stop can change it
- The rules live in those two methods
Speaker notes: This one line does most of the work in this unit. The get is public and the set is private. Anyone can ask whether the press is running. Only code inside the class can change it, and that code is Start and Stop, which is exactly where the guard check and the lockout check live. Nobody can skip the rules by writing to the property.
Image: A glass display case: everyone can look, only the curator has the key.
---
## Slide 5: Every choice, on purpose
```csharp
abstract class PoweredEquipment
{
    private string? _lockoutHolder;

    protected PoweredEquipment(string assetTag) => AssetTag = assetTag;

    public string AssetTag { get; }
    public bool IsRunning { get; private set; }
    public string? LockedOutBy => _lockoutHolder;

    public void LockOut(string badge)
    {
        Stop();
        _lockoutHolder = badge;
    }
}
```
Speaker notes: Walk through each modifier with me. The lockout holder is private, so not even a subclass can clear a lockout. The constructor is protected, so only a subclass calls it. AssetTag has no setter, so a machine can never be retagged. LockedOutBy lets anyone read who holds the lockout without being able to change it.
Image: None. This slide is code.
---
## Slide 6: The compiler refuses
```
error CS0272: The property or indexer 'Press.IsRunning' cannot be used in this context because the set accessor is inaccessible
error CS0200: Property or indexer 'Press.AssetTag' cannot be assigned to -- it is read only
error CS0122: 'PoweredEquipment._lockoutHolder' is inaccessible due to its protection level
```
Speaker notes: Here is the wrong way, three times, with the real errors. Setting IsRunning from outside is CS0272: a setter exists and you may not use it. Retagging the press is CS0200: there is no setter at all. Reaching the private field is CS0122. Read each message and ask what it says the author decided.
Image: None. This slide is code.
---
## Slide 7: The same line, another project
- Inside the project: CS0272
- From another project: CS0200, read only
- The compiler shows what you may see
- Lab U06-03 proves it with Intruder
Speaker notes: This surprises everyone once, so here it is before the lab. If the code that sets IsRunning lives in another project, the error is CS0200, read only, not CS0272. From outside, the private setter is invisible, so the property looks read only. The lab has a project called Intruder that shows you this for real.
Image: Two people looking at the same door, one inside the building who sees a locked door, one outside who sees a wall.
---
## Slide 8: Python's back door
- Name mangling blocks the plain name
- _PoweredEquipment__lockout_holder still works
- A lockout cleared from outside
- C# has no back door
Speaker notes: Python did try. Two underscores mangle the name, so a subclass typing the plain name fails. But the mangled name still works from anywhere, and a lockout can be cleared while a technician may still be inside the machine. In C#, private has no back door.
Image: A padlocked front gate next to a wide open side gate.
---
## Slide 9: Naming that matches
- _camelCase for private fields
- PascalCase for properties, methods, classes
- camelCase for parameters and locals
- I plus PascalCase for interfaces
Speaker notes: The underscore survives in C#, as a naming convention for private fields, so a reader can tell storage from a property at a glance. It is not the protection. The private keyword is. Properties, methods, and classes are PascalCase. Parameters and locals are camelCase. Interfaces start with a capital I, which is tomorrow.
Image: A name badge template with four example badges filled in.
---
## Slide 10: What you are about to build
- Lab U06-03, Part 1: lock down Reading
- Run Intruder before, and save what it prints
- Lock it down, run Intruder again
- Paste the three errors as evidence
Speaker notes: Build one is Part 1 of Lab U06-03. Reading has three public fields. First, build and run the Intruder project and write down what it prints, because that is the damage. Then lock Reading down, with validation in the constructor. Build Intruder again. It must fail, and its three errors are your evidence. In build two, you give your own port the same treatment.
Image: A before and after pair: a console line full of garbage, then three red error lines.
---

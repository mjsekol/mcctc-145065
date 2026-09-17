# Declaring the Whole Shape
---
## Slide 1: Next Friday, your hierarchy speaks C#
- Your Unit 2 classes, ported to C#
- Due Friday of next week
- Today is the translation table
- And the three things C# makes you write down
Speaker notes: In Unit 2 you built a class hierarchy in Python. Next Friday it is due again, in C#. Today is the translation table you will use for every class in it. And today you will see why C# asks you to write down things Python let you leave out, and what that buys you.
Image: A Python class diagram on the left and the same diagram on the right with type labels added.
---
## Slide 2: Python builds an object as it goes
- Attributes appear when __init__ runs
- Nothing lists them anywhere else
- A forgotten super call fails later
- Somewhere else, in some other method
Speaker notes: Think about how a Python object gets its attributes. They appear as init runs. There is no list of them anywhere else. So if a subclass forgets to call super dot init, the object still gets built, and the crash happens later, in some other method, with an error that points at the symptom instead of the cause.
Image: A house being framed while people already move furniture in.
---
## Slide 3: C# declares everything first
- Fields and properties, with types
- Constructors, named after the class
- The parent class, after a colon
- The compiler checks every use against this
Speaker notes: A C# class declares its whole shape up front. Its fields and properties with their types. Its constructors, which have the class's name and no return type. Its parent, after a colon. Then the compiler checks every use of the class against that declaration, before anything runs.
Image: A blueprint with every room labeled before any wall goes up.
---
## Slide 4: The parent
```csharp
abstract class Equipment
{
    protected Equipment(string assetTag, string name)
    {
        AssetTag = assetTag;
        Name = name;
    }

    public string AssetTag { get; }
    public string Name { get; }
    public abstract string Kind { get; }

    public virtual string Describe() => $"{AssetTag} {Name} ({Kind})";
}
```
Speaker notes: Abstract class is Python's ABC. Nobody can build a plain Equipment. The constructor is init. AssetTag with only a get is a property with no setter, so only the constructor can set it. Kind is abstract, so every concrete subclass must supply it. Describe is virtual, which means a subclass is allowed to replace it.
Image: None. This slide is code.
---
## Slide 5: The child
```csharp
sealed class StorageRack : Equipment
{
    private double _loadKg;

    public StorageRack(string assetTag, string name, double capacityKg)
        : base(assetTag, name)
    {
        CapacityKg = capacityKg;
    }

    public double CapacityKg { get; }
    public override string Kind => "rack";
}
```
Speaker notes: The colon Equipment says what the rack is. The colon base line runs the parent's constructor first, which is super dot init. The underscore field is private, so only the rack can touch it. Override on Kind supplies what the parent demanded. Sealed means nothing may inherit from a rack.
Image: None. This slide is code.
---
## Slide 6: Validation lives in set
- Python: @property plus a setter method
- C#: one property with get and set
- value is whatever was assigned
- Check first, assign last
Speaker notes: In Python, validated state was a property and a setter, two methods. In C# it is one property with a get block and a set block. Inside set, the word value is whatever the caller assigned. Check it first and assign it last, so a refused value never touches your field.
Image: A bouncer at a door labeled "set," checking each value before it enters.
---
## Slide 7: Forget the base call
```csharp
public StorageRack(string assetTag, string name, double capacityKg)
{
    CapacityKg = capacityKg;
}
```
```
error CS7036: There is no argument given that corresponds to the required parameter 'assetTag' of 'Equipment.Equipment(string, string)'
```
Speaker notes: Here is the wrong way, with the real error. I deleted the colon base line. CS7036. Read it slowly. With no base call, C# tried to call a parent constructor with no arguments. Equipment does not have one. The message names the parent's constructor and its first parameter. Compare that to the Python version, which fails somewhere else, later.
Image: None. This slide is code.
---
## Slide 8: Python habits the compiler refuses
- self.Id: the name self does not exist
- A method named __init__ is an ordinary method
- A skipped abstract member: CS0534
- Overriding a non-virtual method: CS0506
Speaker notes: Your fingers will type self dot. There is no self in C#, so that is CS0103. A method named underscore underscore init builds as an ordinary method, not a constructor. A subclass that skips the abstract Kind gets CS0534. And overriding a method the parent did not mark virtual gets CS0506. The parent's author decides what you may change.
Image: A stack of four rejected sticky notes, each with one error code.
---
## Slide 9: A warning is still a bug
- A property never set in the constructor
- Warning CS8618, and the build succeeds
- Then NullReferenceException when it runs
- Read your warnings
Speaker notes: One more, and it is only a warning. A string property that the constructor never sets gets CS8618. The build succeeds, and the program throws a null reference exception when it reads the name. Yellow does not mean optional. Next Thursday is about what teams do with warnings like this one.
Image: A yellow warning light on a dashboard that the driver has covered with tape.
---
## Slide 10: What you are about to build
- Lab U06-02: port a piece of Line 3
- Part A: the Sensor class, tests provided
- Part B: Equipment and StorageRack
- Part C: ToolCart, written from nothing
Speaker notes: Build one is Lab U06-02, Part A. You port the Python Sensor class, and the tests are already written, so your job is to make them pass. Build two is Parts B and C. You port Equipment and StorageRack, then you write a ToolCart class with no starter at all. Step eleven switches on its tests before the class exists, so your build fails on purpose. Read that error before you fix it.
Image: A test runner going from red to green, with a small tool cart icon.
---

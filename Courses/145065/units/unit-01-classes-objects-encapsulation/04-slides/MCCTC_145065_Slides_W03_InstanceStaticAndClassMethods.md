# Instance, Static, and Class Methods
---
## Slide 1: Code that is about machines but needs no machine
- Is "L3-OVN-01" a valid tag?
- How many machines has this program built?
- Build a machine from a row in a file
- None of these needs one existing machine
Speaker notes: Last Wednesday you learned two homes for code. Method if it needs this object, function if it needs no object. Here are three jobs that fall in between. Checking a tag format needs no machine, but it is clearly about machines. Counting machines built needs the class, not any single machine. And building a machine from a file row needs the class's own rules. Python has a method kind for each one.
Image: Three task cards floating between a Machine class box and a loose functions file.
---
## Slide 2: Choose by what the method needs
- Needs this object: instance method, self
- Needs the class: @classmethod, cls
- Needs neither: @staticmethod, nothing passed
- The decorator states the need out loud
Speaker notes: Here is the rule. Choose by what the method needs. If it needs this one object, it is an instance method, and it gets self. If it needs the class but no particular object, it is a class method, and it gets cls. If it needs neither, it is a static method, and Python passes nothing. The decorator line is documentation that Python enforces.
Image: A three-row table with the columns needs, kind, first parameter, in navy and launch blue.
---
## Slide 3: All three in one class
```python
class Machine:
    _machines_created = 0                       # class attribute: one shared count

    def __init__(self, asset_tag, rated_kw):
        if not Machine.is_valid_asset_tag(asset_tag):
            raise ValueError(f"asset tag {asset_tag!r} does not match L3-ABC-00")
        self.asset_tag = asset_tag
        self.rated_kw = float(rated_kw)
        Machine._machines_created += 1

    @staticmethod
    def is_valid_asset_tag(tag):
        return isinstance(tag, str) and _TAG_PATTERN.fullmatch(tag) is not None

    @classmethod
    def machines_created(cls):
        return cls._machines_created

    @classmethod
    def from_record(cls, record):
        return cls(record["tag"].strip().upper(), float(record["kw"]))

    def describe(self):
        return f"{self.asset_tag}: {self.rated_kw:g} kW"
```
Speaker notes: The static method checks a tag and touches nothing else. The first class method reads a class attribute, one count shared by every machine. We only need a quick look at class attributes today, because tomorrow is all about where names live. The second class method is an alternative constructor. And describe is an ordinary instance method.
Image: None. This slide is code.
---
## Slide 4: Calling each kind
```python
print(Machine.is_valid_asset_tag("L3-OVN-01"), Machine.is_valid_asset_tag("oven"))
press = Machine("L3-PRS-01", 15)
conveyor = Machine.from_record({"tag": " l3-cnv-01 ", "kw": "3"})
print(press.describe(), "|", conveyor.describe())
print("Machines built:", Machine.machines_created())
print(press.is_valid_asset_tag("L3-PRS-02"))
```
```
True False
L3-PRS-01: 15 kW | L3-CNV-01: 3 kW
Machines built: 2
True
```
Speaker notes: The static method answers through the class with no machine at all, and it also works through an object on the last line. From record took a messy row, spaces, lower case, a rating stored as text, cleaned it, and built a real machine. The count is two.
Image: None. This slide is code.
---
## Slide 5: An alternative constructor keeps the rules
- from_record cleans the row, then calls cls(...)
- cls(...) runs __init__ and every check in it
- A bad row is refused by the class itself
- The counter only counts machines that passed
Speaker notes: This is the part that matters for your refactor project, where your 145060 data arrives as rows. An alternative constructor cleans the row and then calls cls, which runs init. So every validation rule still applies. Load a file with a row that says press three and the class refuses it, with no extra checking code in the loader. And the counter stays honest, because it only goes up after the checks pass.
Image: A CSV row passing through a cleaning step and then a checkpoint labelled __init__.
---
## Slide 6: Loading a file
```
Skipped a row: asset tag 'PRESS THREE' does not match L3-ABC-00
L3-CNV-01: 3 kW
L3-PRS-02: 22 kW
Machines built: 2
```
Speaker notes: This is the output of the loader in your notes. It reads three rows with csv DictReader and hands each one to from record. Two machines were built. The third row was refused by the rules in init, and the loader only had to catch the error and report it. Three rows in, two machines out, and the count agrees.
Image: None. This slide is code.
---
## Slide 7: Watch me forget the decorator
```python
class Machine:
    def is_valid_asset_tag(tag):          # no @staticmethod
        return tag.startswith("L3-")

press = Machine()
print(Machine.is_valid_asset_tag("L3-PRS-01"))
print(press.is_valid_asset_tag("L3-PRS-01"))
```
```
True
Traceback (most recent call last):
  File "...\static_forgot.py", line 7, in <module>
    print(press.is_valid_asset_tag("L3-PRS-01"))
          ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
TypeError: Machine.is_valid_asset_tag() takes 1 positional argument but 2 were given
```
Speaker notes: I left off at static method. Through the class, it works. Through an object, Python passes the object first, like it does for every normal method. Two arguments, the object and the tag, and room for one. If you only ever test through the class, this bug waits for the first teammate who uses an object. The dangerous design is the one that works today.
Image: None. This slide is code.
---
## Slide 8: Honest judgment calls
- A static method could often be a module function
- Static fits when every caller uses this class
- Two classes need it: move it out
- Never write a self you do not use
Speaker notes: This is a judgment call, and I want you to hear both sides. A static method is really a function that lives in the class. That is right when everyone who needs it is already using this class. If a second class needs it, a module-level function is the better home. What is never right is an instance method with a self it never touches. It runs, but it hides what the method needs.
Image: A balance scale with a static method on one side and a module function on the other.
---
## Slide 9: What you are about to build
- Build 1: Lab U01-03 GuardTheState, Part 2
- Static: is_valid_asset_tag for the Oven
- Class method: ovens_created, with its counter
- Alternative constructor: from_record
- Build 2: refactor Improve, one method kind with a reason
Speaker notes: Build 1 is Lab U01-03, Guard the State, Part 2. Your Oven gets a static tag check, a class method that counts ovens built, and a from record constructor that refuses bad rows through the normal rules. Build 2 is your refactor project. You need at least one static or class method, and a sentence in your class boundaries file saying why you chose that kind.
Image: An Oven class box with three highlighted methods, each tagged with its kind.

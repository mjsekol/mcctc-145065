# Let the Standard Library Enforce the Design
---
## Slide 1: A grinder that passes every inspection
- New class: Grinder
- It forgot to report anything
- Every inspection comes back clean
- The comment said "subclasses must do this"
Speaker notes: Someone adds a grinder to the model. They never write the method that reports problems. So every inspection of the grinder comes back empty, and empty looks like safe. There was a comment telling them to write it. A comment is a request. Today you turn requests into rules Python enforces.
Image: A clipboard with a clean checklist and a grinder behind it throwing sparks.
---
## Slide 2: Reuse libraries
- Code someone else wrote, tested, and maintains
- The standard library ships with Python
- Nothing to install
- abc and dataclasses do design work
Speaker notes: A reuse library is code you build on instead of rewriting. The standard library comes with Python. Two modules in it do design work for you. abc makes a rule enforceable. dataclasses writes the boring parts of a record class, correctly.
Image: A toolbox with two labeled tools, abc and dataclasses.
---
## Slide 3: An abstract base class
```python
from abc import ABC, abstractmethod


class Equipment(ABC):
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def inspect(self):
        """The template: shared checks first, then this kind's own."""
        return self.common_findings() + self._kind_findings()

    def common_findings(self):
        return []

    @abstractmethod
    def _kind_findings(self):
        """Every concrete kind must answer this."""
```
Speaker notes: Inherit from ABC and mark a method abstract. Now Python refuses to build an Equipment, and refuses to build any subclass that has not written kind findings. Inspect is the template: shared checks first, then the kind's own. A subclass never writes inspect, so it cannot forget the shared part.
Image: None. This slide is code.
---
## Slide 4: The rule, enforced
```
['L3-RCK-01: overloaded']
TypeError: Can't instantiate abstract class Equipment without an implementation for abstract method '_kind_findings'
```
Speaker notes: The rack wrote its answer, so it builds and reports it is overloaded. Equipment has no answer, so Python refuses it and says exactly which method is missing.
Image: None. This slide is code.
---
## Slide 5: A record, written for you
```python
@dataclass(frozen=True)
class Finding:
    asset_tag: str
    severity: str
    message: str
```
```
Finding(asset_tag='L3-PRS-02', severity='stop', message='guard is open')
True True
FrozenInstanceError: cannot assign to field 'severity'
```
Speaker notes: Three lines. The dataclass writes init, equals, and repr from the fields. Frozen equals true means nobody can change a finding after it is made, which is right for a record of something that already happened. Compare the twelve hand-written lines in the notes.
Image: None. This slide is code.
---
## Slide 6: When a record should check itself
- __post_init__ runs right after the written __init__
- Refuse a bad value there
- Frozen records can go in a set
Speaker notes: Sometimes a field needs checking. The dataclass calls post init right after its own init, so that is where the check goes. And because frozen records never change, Python can hash them, so they work in sets and as dictionary keys.
Image: A stamped form with a checkmark and a rejected form with a launch red X.
---
## Slide 7: The wrong way: the old method name
```
Traceback (most recent call last):
  File "...\oven_forgot.py", line 42, in <module>
    oven = Oven("L3-OVN-01", 200)
TypeError: Can't instantiate abstract class Oven without an implementation for abstract method '_kind_findings'
```
Speaker notes: The oven still has the old method name, problems. With abc, this error appears the moment someone builds an oven. Without abc, the oven would build, report nothing, and an overheating oven would pass inspection. This red text is the good outcome.
Image: None. This slide is code.
---
## Slide 8: Why people skip the library
- Renames get done halfway
- Quick tests call the old name directly
- Hand-written records look finished
- The library catches both, every time
Speaker notes: Renaming a method across a family of classes often gets done halfway, and a quick test that calls the old name still passes. Hand-written record classes look fine until one equals method compares the wrong field. The library does these the same way every time.
Image: A half-painted fence with a paint roller, and a finished fence labeled standard library.
---
## Slide 9: Where you already use them
- Finding in the plant model is a frozen dataclass
- Equipment in the plant model is an ABC
- Your project will use at least one
Speaker notes: Both appear in the Line 3 plant model. The class hierarchy project requires at least one of them, because that is how this unit earns the reuse library competency.
Image: The Line 3 class diagram with Equipment and Finding highlighted in launch blue.
---
## Slide 10: What you are about to build
- Lab U02-01, Part 3
- Equipment becomes an abstract base class
- inspect() becomes a template method
- Finding becomes a frozen dataclass
- Self-check target: 14 of 14
Speaker notes: Part 3 finishes the lab. You make Equipment abstract, replace each class's problems method with kind findings, write the frozen Finding record, and then break it on purpose in step sixteen. Fourteen of fourteen by the end of Build 1. Build 2 starts your project.
Image: The finished three-level hierarchy with an abstract label on the top two boxes.

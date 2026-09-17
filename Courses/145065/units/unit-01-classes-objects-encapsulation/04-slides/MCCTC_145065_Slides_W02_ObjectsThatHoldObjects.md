# Objects That Hold Objects
---
## Slide 1: Two presses with the same tag
- A cell lists L3-PRS-01 twice
- The power total is now wrong
- Nobody knows which line added the second one
- A plain list let it happen
Speaker notes: Here is a real kind of bug. A work cell on Line 3 lists the same press twice. Now the total power for the cell is wrong, and the maintenance report is wrong, and nobody can tell which line of code added the duplicate. The machines lived in a plain list, and any part of the program could append to it. This is Monday's problem again, one level up. Today one object guards a whole collection.
Image: A cell dashboard listing the same press tag twice, the total kW figure circled in launch red.
---
## Slide 2: A container owns the rules for its collection
- One way in: add, and it refuses bad members
- Ways out return a copy, never the real collection
- It answers len, in, and for loops
- Diagram: WorkCell "1" o-- "0..*" Machine
Speaker notes: A container object keeps its members in an internal collection and controls every way in and out. There is one way in, add, and it checks. Every way out hands back a copy. And three special methods let it answer questions Python already knows how to ask. In Tuesday's diagram language, this is aggregation. One cell holds zero or more machines.
Image: A WorkCell box with a single entry door labelled add and a window labelled copy.
---
## Slide 3: The way in
```python
class WorkCell:
    def __init__(self, name):
        self.name = name
        self._machines = {}              # keyed by asset tag

    def add(self, machine):
        if not isinstance(machine, Machine):
            raise TypeError(f"a cell holds Machine objects, not {type(machine).__name__}")
        if machine.asset_tag in self._machines:
            raise ValueError(f"{machine.asset_tag} is already in cell {self.name}")
        self._machines[machine.asset_tag] = machine
        return machine

    def machines(self):
        return tuple(self._machines.values())   # a copy
```
Speaker notes: Two checks in add. Is it a machine at all, and is its tag already here. Only then does it go in. The collection is a dictionary keyed by asset tag, and that is a review of 145060 Unit 5. You look machines up by tag constantly, a dictionary finds one without a scan, and a duplicate is one membership test. Dictionaries also keep insertion order. And machines returns a tuple copy.
Image: None. This slide is code.
---
## Slide 4: Answering Python's questions
```python
    def __len__(self):
        return len(self._machines)

    def __contains__(self, asset_tag):
        return asset_tag in self._machines

    def __iter__(self):
        return iter(self.machines())
```
Speaker notes: When you write len of forming, Python calls this double underscore len method. When you write a tag in forming, Python calls contains. When you write a for loop over forming, Python calls iter. You are teaching your object to answer questions Python already knows how to ask. Notice that iter loops over the copy, not the real dictionary.
Image: None. This slide is code.
---
## Slide 5: It works, and it refuses
```
2 machines, 37.0 kW
True ['L3-PRS-01']
Refused: L3-PRS-01 is already in cell Forming
Refused: a cell holds Machine objects, not str
```
Speaker notes: Two machines, thirty-seven kilowatts. The in check finds a tag. Then two bad adds. The duplicate is refused even though it was a different object with a different rating, because on this line the tag is what makes a machine unique. The string is refused because a cell holds machines.
Image: None. This slide is code.
---
## Slide 6: What the copy protects
- The tuple cannot gain or lose members
- snapshot.append fails with an AttributeError
- The machines inside are the real objects
- Each Machine still guards its own rules
- Each object guards its own level
Speaker notes: Be precise here, because this is where people get confused. The tuple protects the collection. Nobody can add or swap members through it. But the machines inside are the same objects the cell holds, so starting one through the snapshot really starts the press. That is fine. Machine guards its own rules. The cell guards the collection. Each object guards its own level.
Image: A glass case holding machine icons, with a lock on the case and each machine carrying its own small lock.
---
## Slide 7: Watch me leak it
```python
    def machines(self):
        return self._machines            # the real dict

forming.machines()["L3-PRS-03"] = "Press 3"   # no add(), no checks
print(len(forming), "machines")
print(forming.total_rated_kw())
```
```
2 machines
AttributeError: 'str' object has no attribute 'rated_kw'
```
Speaker notes: I changed one line. Machines now returns the real dictionary. So a caller writes straight into it, with no add and no checks, and puts a string in. Length says two. Then total rated kilowatts crashes. Look where. Not on the bad line. In a method that did nothing wrong, one call later. In a real program that could be a day later. That distance is what makes a leak expensive.
Image: None. This slide is code.
---
## Slide 8: Python asks for each ability separately
```
Traceback (most recent call last):
  File "...\no_iter.py", line 12, in <module>
    for machine in forming:
                   ^^^^^^^
TypeError: 'WorkCell' object is not iterable
```
Speaker notes: One more you will hit. This class had double underscore len and no double underscore iter. Len worked fine two lines earlier. The for loop failed. Python does not assume your object can do something because it can do something else. You give it each ability on purpose.
Image: None. This slide is code.
---
## Slide 9: What you are about to build
- Build 1: Lab U01-02 ToolCrib, Part 3
- A ToolCrib container that refuses bad tools
- Hands out copies, answers len, in, and loops
- Build 2: refactor UML final, CLASS_BOUNDARIES draft
Speaker notes: Build 1 is Lab U01-02, Tool Crib, Part 3. You write the ToolCrib container. It refuses anything that is not a tool and any duplicate tag, it never hands out its real collection, and it answers len, in, and for loops. Build 2 is the refactor project. Finish your class diagram and start CLASS_BOUNDARIES dot md, where you justify every class, every function that stayed a function, and the collection each class holds. Both are due tomorrow, before any class code.
Image: A tool crib shelf with tagged tools, and a checkout counter labelled add.

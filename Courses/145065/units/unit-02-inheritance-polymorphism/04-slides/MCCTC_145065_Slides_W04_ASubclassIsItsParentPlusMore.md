# A Subclass Is Its Parent, Plus More
---
## Slide 1: The fix that reached one copy
- The lockout rule changed last month
- Someone fixed it in Press
- Oven had the same code, copied
- Nobody fixed Oven
- A locked-out oven keeps running
Speaker notes: Here is a story from our composite shop, Riverside Fabrication. The lockout rule changed. Somebody updated the press. The oven had a copy of the same code, and nobody remembered it. So now a technician locks out the oven, and it keeps running. Nothing crashed. Today is about making sure a rule lives in exactly one place.
Image: Two identical code blocks side by side, one highlighted as fixed, the other with a launch red outline.
---
## Slide 2: Copied code drifts
- Every copy is a place a fix can be missed
- The copies look identical until they are not
- Tests on one copy prove nothing about the other
Speaker notes: Open the lab starter and put Press and Oven side by side. Most of the lines match. Your job today is to find the one method where they do not match, and then make it impossible for that to happen again.
Image: Three sheets of paper photocopied from each other, the last one slightly faded and changed.
---
## Slide 3: Inheritance means is a
- A press is powered equipment
- Powered equipment is equipment
- A rack is equipment, with no power
- Say the sentence out loud before you write it
Speaker notes: Inheritance models one relationship, is a. Say it out loud. A press is a piece of powered equipment: true. A rack is a piece of powered equipment: false, it has no power at all. If the sentence is false, the inheritance is wrong, no matter how much code it would save.
Image: A family tree with Equipment at the top, PoweredEquipment and StorageRack below, and Press under PoweredEquipment, navy boxes.
---
## Slide 4: The parent sets up its part
```python
class Equipment:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name

    def describe(self):
        return f"{self.asset_tag} {self.name}"


class PoweredEquipment(Equipment):
    def __init__(self, asset_tag, name, rated_kw):
        super().__init__(asset_tag, name)  # the parent sets up its part
        self.rated_kw = rated_kw           # the child adds its own
        self.running = False

    def start(self):
        self.running = True
```
Speaker notes: The child names its parent in parentheses. The first line of the child's init is super, init. That runs the parent's init, so the parent creates asset tag and name. Then the child adds its own attributes. Describe is written once, in Equipment, and every powered machine gets it.
Image: None. This slide is code.
---
## Slide 5: What the child can do
```python
oven = PoweredEquipment("L3-OVN-01", "Cure Oven", 45)
oven.start()
print(oven.describe())                     # written once, in Equipment
print(oven.rated_kw, oven.running)
print(isinstance(oven, Equipment), isinstance(oven, PoweredEquipment))
```
```
L3-OVN-01 Cure Oven
45 True
True True
```
Speaker notes: The oven uses describe, which it never wrote. It has its own rated kW and running state. And isinstance says it is both kinds of object at once, because a powered piece of equipment is a piece of equipment.
Image: None. This slide is code.
---
## Slide 6: Three levels, searched in order
- Press, then PoweredEquipment, then Equipment, then object
- Python stops at the first class with the name
- That order is the method resolution order
- StorageRack sits beside PoweredEquipment, not under it
Speaker notes: When you ask a press for something, Python looks in Press first, then climbs. The first class that has the name wins. That order has a name, the method resolution order, and you can print it with double underscore m r o. The rack sits at level two, next to powered equipment, because of the sentence test.
Image: A ladder with four labeled rungs, Press at the bottom and object at the top, a launch blue arrow climbing.
---
## Slide 7: The wrong way: forgetting super
```python
class Press(PoweredEquipment):
    def __init__(self, asset_tag, name, rated_kw, tonnage):
        self.tonnage = tonnage             # forgot super().__init__(...)


press = Press("L3-PRS-01", "Press 1", 15, 60)
print("built, tonnage", press.tonnage)
press.start()
print("started")
print(press.describe())
```
Speaker notes: This press sets its tonnage and never calls super init. Predict what happens. Does it fail when it is built, when it starts, or somewhere else?
Image: None. This slide is code.
---
## Slide 8: The error shows up somewhere else
```
built, tonnage 60
started
Traceback (most recent call last):
  File "...\press_no_super.py", line 30, in <module>
    print(press.describe())
          ~~~~~~~~~~~~~~^^
  File "...\press_no_super.py", line 8, in describe
    return f"{self.asset_tag} {self.name}"
              ^^^^^^^^^^^^^^
AttributeError: 'Press' object has no attribute 'asset_tag'
```
Speaker notes: It built. It even started, because start only sets an attribute. The crash comes in describe, and it names asset tag, which the parent was supposed to create. The mistake is in Press init. The error points at Equipment. Errors that point far from their cause are the expensive ones.
Image: None. This slide is code.
---
## Slide 9: The habit
- First line of every child init: super().__init__(...)
- Pass exactly what the parent asks for
- Run the sentence test before class B(A)
- Delete the copy once the parent has it
Speaker notes: Four habits for today. Super init first, every time. Give the parent exactly the arguments it asks for. Say the sentence before you write the class. And once a parent does something, delete every copy of it in the children, or the drift starts again.
Image: A checklist with four boxes, each checked in launch blue.
---
## Slide 10: What you are about to build
- Lab U02-01, Line Hierarchy, Part 1
- Find the copy that drifted
- Build Equipment and PoweredEquipment
- Make Press, Oven, and the rack inherit
- Self-check target: 7 of 14
Speaker notes: The lab gives you three classes written by copying. First find the one method whose copies do not match, and write down what it does. Then build the two parent classes and make every class inherit. Delete every copied line. Your self-check should say seven of fourteen by the end of the day.
Image: A before and after diagram, three separate boxes on the left and a three-level tree on the right.

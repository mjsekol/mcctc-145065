# Where a Name Lives
---
## Slide 1: Three starts, and the count says zero
- Every press start should add one to a shared count
- Three presses started today
- The shared count says 0
- No error anywhere
Speaker notes: Here is the quietest bug in this unit. You want one count shared by every machine on the line. You write the line that looks right to everyone. The presses start three times. The shared count says zero, and Python never complains. By the end of this segment you will be able to say exactly why, and you will have a tool that catches it before it happens.
Image: A shift board reading Starts today: 0 above three presses with green RUNNING lights.
---
## Slide 2: Four levels a name can live at
- Module: top of the file, shared by everything
- Class: in the class body, shared by every object
- Instance: through self, one per object
- Local: inside a function, gone after it returns
Speaker notes: In 145060 you had two levels, local and global. Classes add two more. Module level is the top of the file. Class level is inside the class body but outside any method, and every object shares it. Instance level is anything you assign through self, one copy per object. Local is inside a function and disappears when the call returns. This is competency 5.2.2 on the state exam.
Image: Four nested boxes labelled module, class, instance, local, from outermost to innermost.
---
## Slide 3: All four in one file
```python
SITE_NAME = "Riverside Fabrication"          # module (global) scope

class Machine:
    line_name = "Line 3"                     # class scope

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag           # instance scope

    def label(self):
        text = f"{SITE_NAME}, {self.line_name}, {self.asset_tag}"   # local scope
        return text
```
```
Riverside Fabrication, Line 3, L3-PRS-01
Outside the method: name 'text' is not defined
```
Speaker notes: One method reads a module name, a class name, and an instance name, and makes a local. Outside the method, text does not exist. And one more thing from the notes. When I reassign SITE NAME later in the file, Python lets me. Capitals mean constant by agreement, the same kind of promise as the underscore.
Image: None. This slide is code.
---
## Slide 4: Reading and assigning follow different rules
- Reading self.name: check the object, then the class
- Assigning self.name: always writes on the object
- The object's copy now shadows the class value
- In a function, assigning makes the name local
Speaker notes: This is the rule that explains slide one. When you read self dot name, Python checks the object first, and if it is not there, it checks the class. When you assign self dot name, Python does not look anywhere. It writes on that object. From then on, that object's copy shadows the class value. Functions have the same shape. Assign a name anywhere in a function and it is local for the whole function.
Image: Two arrows: a read arrow travelling from object to class, an assign arrow stopping at the object.
---
## Slide 5: Watch the count go wrong
```python
class Machine:
    starts_today = 0                         # meant to be one shared count

    def __init__(self, asset_tag):
        self.asset_tag = asset_tag

    def start(self):
        self.starts_today += 1               # the deliberate mistake

press1, press2 = Machine("L3-PRS-01"), Machine("L3-PRS-02")
press1.start()
press1.start()
press2.start()
print("press1:", press1.starts_today, "press2:", press2.starts_today, "class:", Machine.starts_today)
print(vars(press1), vars(press2))
```
```
press1: 2 press2: 1 class: 0
{'asset_tag': 'L3-PRS-01', 'starts_today': 2} {'asset_tag': 'L3-PRS-02', 'starts_today': 1}
```
Speaker notes: Plus equals is a read and then an assign. The read finds the class value, zero. The assign writes one onto that press. Every later start reads the press's own copy. The class count is never touched. Vars shows each object's own attributes, and there are the stray copies.
Image: None. This slide is code.
---
## Slide 6: Name the class when you change class data
```python
    def start(self):
        Machine.starts_today += 1            # name the class, not self
```
```
press1: 3 press2: 3 class: 3
{'asset_tag': 'L3-PRS-01'} {'asset_tag': 'L3-PRS-02'}
```
Speaker notes: The fix is one word. Change class data through the class name, or through cls in a class method like yesterday. Now every press reads the one shared count, and no object has a stray copy. The same shadowing happens from outside, too. Press two dot line name equals Line 9 moves one press to Line 9 and leaves every other press on Line 3.
Image: None. This slide is code.
---
## Slide 7: The function version crashes instead
```python
alarms_today = 0

def record_alarm(asset_tag):
    alarms_today += 1                # the deliberate mistake
    return f"{asset_tag}: alarm {alarms_today}"
```
```
UnboundLocalError: cannot access local variable 'alarms_today' where it is not associated with a value
```
Speaker notes: Same shape, in a function. Plus equals assigns, so Python decides that alarms today is local for the whole function, and then the line tries to read a local with no value yet. The message says exactly that. Notice the contrast. With self, you get a wrong number. With a function, you get a crash. The crash is the kinder of the two.
Image: None. This slide is code.
---
## Slide 8: global works. Avoid it anyway.
- global alarms_today makes the function assign the module name
- Now any function in the file can change it
- Finding who changed it means reading every function
- Pass the value in and return the new value
- State that belongs to something lives in that object
Speaker notes: The global keyword fixes the crash. It tells Python to assign the module name. It works, and you should still avoid it, because now any function in the file can change that value, and when it is wrong you have to read all of them. Pass the count in and return the new count, so the change is visible at the call. Better still, state that belongs to something lives in that object.
Image: A module-level variable with arrows coming in from many functions, a question mark over each arrow.
---
## Slide 9: The scope map
- A table: every important name and its level
- Add one line saying why it lives there
- A row that is hard to fill means the design is unsettled
- Your refactor project requires one
Speaker notes: Here is the tool. A scope map is a short table, at the top of your file or in your README. Name, level, and why it lives there. Site name, module, one value for the program. Starts today, class, one shared count. Asset tag, instance, each machine has its own. If you cannot fill in a row easily, you have not decided the design yet. Your refactor project needs one.
Image: A three-column table titled Scope map with four filled rows.
---
## Slide 10: What you are about to build
- Build 1: Lab U01-04 ScopeAndTests, Part 1
- Scope hunt in a shift counter program
- Find every shadowed and misplaced name
- Build 2: refactor Improve, encapsulation pass and scope map
Speaker notes: Build 1 is Lab U01-04, Scope and Tests, Part 1. It is a scope hunt. A shift counter program has names at every level and some of them are in the wrong place. You map every name, find the bugs this lesson predicts, and fix them. Build 2 is your refactor project. Make an encapsulation pass, underscores and at least one validated property, and write your scope map.
Image: A magnifying glass over a code file with four names highlighted in four colours.

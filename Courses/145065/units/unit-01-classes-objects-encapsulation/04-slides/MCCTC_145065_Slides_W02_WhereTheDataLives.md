# Where the Data Lives
---
## Slide 1: The press was locked out. It is running.
- Your code refused to start a locked-out press
- One line later, the press is running anyway
- No error, no warning, no red text
- Where the data lives decided this
Speaker notes: Welcome to Unit 1. Picture this. Your program checks for a lockout and correctly refuses to start a press. Then one line somewhere else in the program sets running to true, and the press runs with a technician's lock still on it. Nothing crashed. Today is about why that was possible and how an object makes it much harder. Riverside Fabrication is a made-up shop we use all semester, but the problem is real.
Image: A shop-floor press with a red lockout tag on its switch and a status screen reading RUNNING, navy and launch blue.
---
## Slide 2: You have done this already
- 145060 Unit 5: Data Pipeline, no classes allowed
- Data in dictionaries, rules in loose functions
- 145060 Unit 7: Storm Relay v4 had real classes
- Today: what a class protects
Speaker notes: You are not starting from zero. You built the Data Pipeline with no classes, so your data lived in dictionaries and lists. Then Storm Relay v4 gave you Room, Player, and Game. You know init and self. Today we go deeper and ask a harder question. What does a class actually protect, and what does it not?
Image: Two file icons side by side, pipeline.py with dictionary braces and storm_relay.py with a class keyword.
---
## Slide 3: The 145060 way
```python
press = {"tag": "L3-PRS-01", "running": False, "locked_by": None}

def start(machine):
    if machine["locked_by"] is not None:
        print(machine["tag"], "is locked out and cannot start")
        return
    machine["running"] = True

lock_out(press, "tech-07")
start(press)                 # refused, correctly
press["running"] = True      # any line in the program can do this
print(press)
```
Speaker notes: Here is the press as a dictionary with loose functions. The start function has a correct rule. Now read the second to last line. Nothing forces anyone to call start. Predict what the last line prints before I run it.
Image: None. This slide is code.
---
## Slide 4: The rule worked, then got skipped
```
L3-PRS-01 is locked out and cannot start
{'tag': 'L3-PRS-01', 'running': True, 'locked_by': 'tech-07'}
```
Speaker notes: The first line is the rule doing its job. The second line is a locked-out press that is running. Both are true at the same time. This is the thread for the whole course. The dangerous design is the one that works today. It worked on the day it was written. It fails on the day somebody adds one line.
Image: None. This slide is code.
---
## Slide 5: An object keeps data and rules together
- The data and its allowed operations live together
- The object checks its inputs when it is built
- State changes only through its methods
- The object guards its own rules
Speaker notes: Here is the idea for today. An object bundles its data with the only operations allowed to change that data. It checks its inputs in init, so it can never exist in a bad state. After that, the state changes only through its methods. Say it with me. The object guards its own rules.
Image: A box labelled Machine with its data inside and three doors labelled start, stop, lock_out.
---
## Slide 6: The same press as an object
```python
class Machine:
    def __init__(self, asset_tag, rated_kw):
        if isinstance(rated_kw, bool) or not isinstance(rated_kw, (int, float)):
            raise TypeError(f"rated_kw must be a number, not {type(rated_kw).__name__}")
        if rated_kw <= 0:
            raise ValueError(f"rated_kw must be above 0, not {rated_kw}")
        self.asset_tag = asset_tag
        self.rated_kw = float(rated_kw)
        self._running = False       # internal: change me only through my methods
        self._locked_by = None

    def start(self):
        if self._locked_by is not None:
            raise RuntimeError(f"{self.asset_tag} is locked out by {self._locked_by}")
        self._running = True

    def is_running(self):
        return self._running
```
Speaker notes: Three things to notice. Init refuses a bad rating, and it checks for bool first because True counts as a number in Python. The running flag has a leading underscore, which in this course means internal, change me only through my methods. Python does not enforce that, and next Monday I show you exactly what it does not stop. And we read state with is_running, a method. Properties come in Week 3.
Image: None. This slide is code.
---
## Slide 7: Refused, and still stopped
```
Refused: L3-PRS-01 is locked out by tech-07
Machine(asset_tag='L3-PRS-01', rated_kw=15.0) running: False
Refused 'L3-PRS-02', -5: rated_kw must be above 0, not -5
Refused 'L3-PRS-03', True: rated_kw must be a number, not bool
```
Speaker notes: The refusal is an exception now, not a print a caller can ignore. The press stays stopped. And the last two lines show the object refusing to be built wrong. A negative rating is refused. A rating of True is refused. Without that bool check, True would have quietly become one kilowatt.
Image: None. This slide is code.
---
## Slide 8: Watch me break it
```python
    def start(self):
        _running = True          # no "self."

press = Machine("L3-PRS-01")
press.start()
print("running:", press.is_running())
```
```
running: False
```
Speaker notes: I am going to make the most common class mistake on purpose. I left off self dot. Watch the output. Running is False after start. No error. Without self dot, that line made a local variable that vanished when the method returned. Leave off self in the parameter list instead and you get a TypeError that says zero positional arguments but one was given. That one is the object Python hands every method.
Image: None. This slide is code.
---
## Slide 9: Four ways to organize a program
- Procedural: functions receive data and act on it
- Structured: sequence, selection, loops, one way in and out
- Object-oriented: data bundled with the behavior that changes it
- Event-driven: wait, then run a handler when something happens
- Real programs mix all four
Speaker notes: The exam asks you to compare these. Procedural is the dictionary version. Structured is every Python program you have written, because there is no goto. Object-oriented is today. Event-driven is your phone running the snooze code when you tap Snooze, and it is Unit 7 in C#. They are not rivals. A method is structured code inside an object.
Image: A four-column comparison grid with a small icon for each style, navy headers.
---
## Slide 10: What you are about to build
- Build 1: Lab U01-01 MachineRules, Part 1
- A Machine class that refuses bad data
- Build 2: Part 2, rewrite the tracker to use it
- The rogue line must no longer work quietly
Speaker notes: Build 1 is Lab U01-01, Machine Rules, Part 1. You take a procedural press tracker where a rogue line runs a locked-out press, and you write a Machine class that validates on construction and changes state only through start, stop, lock out, release lockout, and record run. Build 2 is Part 2. You rewrite the tracker to use your class. If you were absent for the Unit 0 quiz or still owe a desk demo, your teacher will tell you when that happens today. Commit before you leave.
Image: A before-and-after split: a dictionary on the left, a Machine class box on the right, launch blue arrow between.

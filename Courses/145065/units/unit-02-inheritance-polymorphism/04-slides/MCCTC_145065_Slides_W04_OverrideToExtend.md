# Override to Extend, and Keep the Parent's Promise
---
## Slide 1: A locked-out press that starts
- A technician locks out Press 1
- Someone closes the guard
- Someone presses start
- The press starts
Speaker notes: Picture this on our composite shop floor. A technician has Press 1 locked out and is working near it. Someone else closes the guard and hits start. The press starts. No error, no warning. The code for the press was written by someone who thought they were adding a safety rule. Today you will see how adding a rule can delete one.
Image: A press with a padlock tag hanging on it and a green running light, launch red outline around the light.
---
## Slide 2: Overriding a method
- Same method name in the child
- Python finds the child's version first
- The parent's version does not run
- Unless the child asks for it
Speaker notes: When a child writes a method with the same name as the parent, the child's version wins. That is the method resolution order from yesterday. The parent's version is still there. It only runs if the child calls it.
Image: Two stacked boxes labeled Press start and PoweredEquipment start, an arrow stopping at the first box.
---
## Slide 3: Replacing throws the parent away
```python
class Press(PoweredEquipment):
    def __init__(self, asset_tag):
        super().__init__(asset_tag)
        self.guard_closed = False

    def start(self):                      # REPLACES the parent's start()
        if not self.guard_closed:
            raise RuntimeError(f"{self.asset_tag} guard is open")
        self.running = True


press = Press("L3-PRS-01")
press.lock_out("tech-07")
press.guard_closed = True
press.start()
print("running:", press.running, "| locked by:", press.locked_by)
```
```
running: True | locked by: tech-07
```
Speaker notes: This start checks the guard and sets running. It never calls the parent. The lockout check lived only in the parent's start, so it is gone. Running true, locked by tech zero seven. That is the slide one story, in code.
Image: None. This slide is code.
---
## Slide 4: Extending keeps both rules
```python
    def start(self):                      # EXTENDS the parent's start()
        if not self.guard_closed:
            raise RuntimeError(f"{self.asset_tag} guard is open")
        super().start()                   # the lockout rule still runs

    def open_guard(self):
        self.guard_closed = False
        self.stop()                       # whatever stop() means for this object
```
Speaker notes: Same check for the guard, then super start. Now the parent's lockout rule still runs after the press adds its own. And look at open guard. It does not set running to false itself. It calls self dot stop, so whatever stop means for this object is what happens.
Image: None. This slide is code.
---
## Slide 5: The lockout rule, working
```
RuntimeError: L3-PRS-01 is locked out by tech-07
```
Speaker notes: Lock it out, close the guard, start it. This time the start is refused, by the parent's rule, reached through super. That red text is the program doing its job. Some errors are the safety system working.
Image: None. This slide is code.
---
## Slide 6: Every method makes a promise
- stop() promises: afterward, not running
- lock_out() depends on that promise
- open_guard() depends on it too
- An override must keep the promise
Speaker notes: A method is a promise to everyone who calls it. Stop promises the machine is stopped afterward. Lock out calls stop and trusts that promise. Open guard does the same. If a child overrides stop and breaks the promise, both of those methods break, and nobody touched them.
Image: A handshake between two boxes labeled lock_out and stop.
---
## Slide 7: The wrong way: a stop that does nothing
```python
class LazyPress(Press):
    def stop(self):
        pass                              # "the ram returns by itself"


press = LazyPress("L3-PRS-01")
press.guard_closed = True
press.start()
press.open_guard()
print("guard closed:", press.guard_closed, "| running:", press.running)
press.lock_out("tech-07")
print("locked by:", press.locked_by, "| running:", press.running)
```
```
guard closed: False | running: True
locked by: tech-07 | running: True
```
Speaker notes: This child overrides stop with pass. Run it. The guard is open and the press is running. Then it gets locked out, and it is still running. There is no error message anywhere. That is the most dangerous kind of wrong in this course: it works today.
Image: None. This slide is code.
---
## Slide 8: Two questions for every override
- Does my version still call super()?
- What did the parent promise?
- Does my version still promise it?
Speaker notes: Before you commit any override, ask these out loud. Most broken overrides fail the first question. The rest fail the second.
Image: A magnifying glass over a method signature, launch blue.
---
## Slide 9: Extending works on text too
- A child can add to what the parent builds
- Call super().describe(), then add your part
- A parent change reaches every child
Speaker notes: Extending is not only for safety rules. In the lab, powered equipment builds its description by calling super describe and adding the power and state. If the parent's description ever changes, every child's description changes with it.
Image: A text label with a base part in navy and an added part in launch blue.
---
## Slide 10: What you are about to build
- Lab U02-01, Part 2
- Press.start() that extends, not replaces
- open_guard() that calls stop()
- describe() built once per level
- Then break a promise on purpose
Speaker notes: In Part 2 you rewrite the press's start so the lockout rule still runs, make open guard call stop, and move describe up into the parents. Then step eleven asks you to write a stop that does nothing and record what happens. Self-check target: ten of fourteen.
Image: A checklist with the four lab steps, the last one marked with a launch red tag.

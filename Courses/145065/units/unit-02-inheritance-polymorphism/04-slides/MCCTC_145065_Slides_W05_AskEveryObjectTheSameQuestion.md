# Ask Every Object the Same Question
---
## Slide 1: The report that broke on a Tuesday
- A new kind of assignment arrives
- The grade report crashes
- The class worked fine
- The if/elif chain never heard of it
Speaker notes: Picture a grade tool. Someone adds project as a new kind of assignment, writes the class, tests it, and it works. Then the weekly report runs and crashes, because a function somewhere has an if elif chain that lists every kind by name, and project is not on the list. Today is about getting rid of that list.
Image: A report page with a launch red error banner across it.
---
## Slide 2: The chain has three costs
- Every new kind edits the chain
- A forgotten kind fails at run time
- The rules live far from the class
Speaker notes: An if elif chain on kind is a conditional control structure, the kind you have written since last semester. It works. It also means every new kind edits it, every forgotten kind fails in front of a user, and nobody reading the class can see its rules.
Image: A long chain with each link labeled with a kind, one link cracked.
---
## Slide 3: Polymorphism: one call, many answers
- Ask every object the same question
- Each class answers in its own way
- The loop never asks what kind
- Python picks the method by class
Speaker notes: Polymorphism means many shapes. You ask every object the same question, and each class answers for itself. The decision did not disappear. It moved into Python's method lookup, the resolution order you already know.
Image: One question mark pointing to three different boxes, each with its own answer.
---
## Slide 4: One question, three answers
```python
    def final_score(self, days_late):
        return max(0, self.score - self.penalty(days_late))

    @abstractmethod
    def penalty(self, days_late):
        """Points taken off. Each kind answers for itself."""


class Quiz(Assignment):
    kind = "quiz"

    def penalty(self, days_late):
        return self.score if days_late > 0 else 0     # a late quiz earns nothing


class Essay(Assignment):
    kind = "essay"

    def penalty(self, days_late):
        return 10 * days_late                         # 10 points a day


class Lab(Assignment):
    kind = "lab"

    def penalty(self, days_late):
        return min(15, 5 * days_late)                 # 5 a day, at most 15
```
Speaker notes: Final score is written once, in the base class. It calls penalty, which each kind answers differently. A late quiz earns nothing, an essay loses ten a day, a lab loses five a day up to fifteen. No if about kinds anywhere.
Image: None. This slide is code.
---
## Slide 5: The new kind, both ways
```python
class Project(Assignment):
    kind = "project"

    def penalty(self, days_late):
        return 0 if days_late <= 1 else 20            # one grace day, then 20 points


work = [Quiz("Unit 2 quiz", 36), Essay("Design analysis", 88), Lab("Layout walk", 95),
        Project("Class hierarchy", 91)]
print("polymorphic:", [item.final_score(2) for item in work])
print("chain:      ", [final_score_by_kind(item, 2) for item in work])
```
```
polymorphic: [0, 68, 85, 71]
```
Speaker notes: Project arrives with one grace day. The polymorphic line asks all four and gets four answers. Now watch the chain on the same list.
Image: None. This slide is code.
---
## Slide 6: The wrong way: the chain meets the new kind
```
  File "...\late_work_chain.py", line 47, in final_score_by_kind
    raise ValueError(f"no late rule for kind {item.kind!r}")
ValueError: no late rule for kind 'project'
```
Speaker notes: The chain never heard of projects. It fails at run time, inside a report. With polymorphism, the only file that changed was the new class. With the chain, you would have to find every function shaped like this one.
Image: None. This slide is code.
---
## Slide 7: abc catches the forgetful class early
- A new class with no answer cannot be built
- The error comes when it is created
- Not when a report runs
Speaker notes: What if the new class forgets to write penalty? Because penalty is abstract, Python refuses to create the object at all. The person who wrote the class finds out, not the person reading the report.
Image: A factory gate stopping a box with a missing part.
---
## Slide 8: The loop that never asks
```python
def inspect_all(items):
    findings = []
    for item in items:              # never asks what kind item is
        findings.extend(item.inspect())
    return findings
```
```
['L3-PRS-02: guard is open', 'L3-RCK-01: overloaded', 'L3-WLD-01: wire low']
```
Speaker notes: Here is the same idea on Line 3. Inspect all is five lines and never checks a kind. A welder class was added after it was written, and its finding is in the list.
Image: None. This slide is code.
---
## Slide 9: The disguised chain
- isinstance() inside the loop is the chain again
- So is if item.kind == inside the loop
- Ask which class the branch belongs to
Speaker notes: Watch for the chain in disguise. Someone keeps the polymorphic loop and adds one isinstance check for the kind that behaves differently. That is the chain, back again. When you catch yourself writing it, ask which class that branch belongs in.
Image: A chain hidden inside a loop diagram, partly visible.
---
## Slide 10: What you are about to build
- Lab U02-03, Inspect Without Asking
- Move each branch into its class
- Write inspect_all() in five lines
- Prove it matches the chain
- Add a welder without touching the loop
Speaker notes: The lab hands you the real Line 3 chain. You move each kind's branch into its own class, write the polymorphic loop, and prove the findings are identical. Then you add a welder and show the chain breaks while your loop does not. Build 2 starts your project's first sprint.
Image: A before and after: a long function on the left, four small class boxes and a short loop on the right.

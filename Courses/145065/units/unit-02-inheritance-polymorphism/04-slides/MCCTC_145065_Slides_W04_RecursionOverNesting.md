# Recursion Over a Nested Structure
---
## Slide 1: How deep does the line go
- Line 3 holds cells
- Finishing holds a cell called Transfer
- Next year Transfer may hold a cell
- How many loops do you write?
Speaker notes: Our composite line has cells inside cells. Today it is two levels deep in one place. Next year it could be three. If you write two nested loops, you handle two levels and silently miss the third. So how many loops do you write? The honest answer is: you cannot know.
Image: A tree diagram of Line 3 with one branch trailing off into a question mark.
---
## Slide 2: A function that calls itself
- Recursion: solve the problem using a smaller copy of it
- Fits anything that contains more of itself
- Folders, comment threads, cells
Speaker notes: A recursive function calls itself on a smaller piece. It fits any structure that contains more of its own kind. Your phone's folders, a reply thread, and our cells all work this way.
Image: A folder containing a smaller folder containing a smaller folder, launch blue outlines.
---
## Slide 3: Two parts, always
- Base case: answer without calling yourself
- Recursive case: call yourself on each smaller piece
- Every call must move toward the base case
Speaker notes: Every recursive function has a base case and a recursive case. For counting machines, a machine counts one and has nothing inside: that is the base case. A cell counts whatever its items count: that is the recursive case. Each call goes one level deeper, and every path ends at a machine.
Image: A staircase going down with the bottom step labeled base case.
---
## Slide 4: Counting at any depth
```python
def count_machines(node):
    if isinstance(node, Machine):
        return 1                                                   # base case
    return sum(count_machines(child) for child in node.items)      # recursive case


print(count_machines(line))
print(count_machines(line.items[1]))
print(count_machines(Machine("L3-PRS-09")))
```
```
5
2
1
```
Speaker notes: Base case first. Then the recursive case: add up the count for every child. Five machines on the line. Two in Finishing, one of them inside Transfer. And one machine alone counts one.
Image: None. This slide is code.
---
## Slide 5: Walking and indenting
```
Line 3
  Forming
    L3-PRS-01
    L3-PRS-02
  Finishing
    L3-OVN-01
    Transfer
      L3-CNV-01
  Staging
    L3-RCK-01
```
Speaker notes: The show function passes depth down and adds one on every call, so each level indents two more spaces. Nobody wrote handle three levels. The data decided how deep to go.
Image: None. This slide is code.
---
## Slide 6: The wrong way: no base case
```python
def count_machines(node):
    return sum(count_machines(child) for child in node.items)      # no base case


print(count_machines(line))
```
```
    return sum(count_machines(child) for child in node.items)      # no base case
                                                  ^^^^^^^^^^
AttributeError: 'Machine' object has no attribute 'items'
```
Speaker notes: Delete the base case and every node gets asked for items. Cells have items. The first machine does not, and this is the error. The fix is the base case, before the line that reads items.
Image: None. This slide is code.
---
## Slide 7: The other wrong way: a loop in the data
- The function has its base case
- The line was added inside its own cell
- Every path goes around forever
- RecursionError: maximum recursion depth exceeded
Speaker notes: Here the function is correct. The data is not a tree any more: someone put the line inside one of its own cells. No path ever reaches a machine, so Python stops after about a thousand calls with a recursion error. The fix belongs where things are added: refuse the loop in add.
Image: A circular arrow looping back on a tree branch, launch red.
---
## Slide 8: Trace it on paper
- count(Finishing) asks count(Oven) and count(Transfer)
- count(Oven) returns 1
- count(Transfer) asks count(Conveyor), gets 1
- Finishing returns 1 plus 1
Speaker notes: Before you trust recursion, trace one call by hand. Finishing asks its two items. The oven is a machine, one. Transfer is a cell, so it asks the conveyor, one, and returns one. Finishing adds them, two. The lab asks you to write this table in your README.
Image: A stack of index cards, each labeled with one call and its return value.
---
## Slide 9: Where it shows up on the exam
- Nested structures and recursion: competency 5.3.8
- Outcome 5.3 is about a quarter of the WebXam
- This week is the only recursion lesson
Speaker notes: Recursion is taught once in this course, today. It is part of the heaviest outcome on the WebXam. Expect a question that asks you to trace a recursive call. The Gate 1 reps this week include one.
Image: A pie chart with a quarter slice highlighted in launch blue.
---
## Slide 10: What you are about to build
- Lab U02-02, Layout Walk
- count_equipment, walk, outline, total_rated_kw
- contains_cell, then refuse loops
- Break it twice on purpose
- Self-check target: 9 of 9
Speaker notes: The lab gives you the Line 3 layout and five stubs. You write each recursive function, then the loop guard, then break it twice, once without a base case and once with a loop. The trace table goes in your README. Nine of nine by the end of the day.
Image: The Line 3 layout tree with each function name attached to the part it walks.

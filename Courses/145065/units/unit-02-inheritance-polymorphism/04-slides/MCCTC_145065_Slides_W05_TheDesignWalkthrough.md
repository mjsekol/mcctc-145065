# The Design Walkthrough
---
## Slide 1: The cheapest bug you will ever fix
- On a diagram: minutes
- After twenty tests depend on it: an afternoon
- After it ships: much more
- The designer is the worst person to find it
Speaker notes: A design mistake is cheapest while it is still a line on a diagram. Once other code depends on it, it costs an afternoon. Once it ships, it costs far more. And the person least able to see it is the person who designed it, because they already know what they meant.
Image: A rising cost curve from diagram to shipped product, launch blue line.
---
## Slide 2: Two roles
- Author: shows the design, listens, records
- Reviewer: asks questions, names findings
- Findings are about the design, never the person
Speaker notes: A walkthrough has two roles. The author walks through the design and mostly listens. The reviewer asks questions and names findings. Every finding is about a class or a relationship. Never about the person.
Image: Two chairs facing a shared screen with a class diagram on it.
---
## Slide 3: Questions that test something
- What happens when a new kind arrives?
- Which class owns this rule?
- Say the sentence test for this class line
- What if this collection is changed from outside?
Speaker notes: Looks good finds nothing. Good questions test the design against something. These four come from this unit. Bring three of your own to every walkthrough.
Image: Four question cards fanned out, launch blue.
---
## Slide 4: A question that found a problem
```python
    def label(self):
        """Each kind shows its own detail."""
        if isinstance(self, Press):
            return f"{self.tag} press, {self.tonnage:g} t"
        if isinstance(self, Oven):
            return f"{self.tag} oven, {self.setpoint_c:g} C"
        return f"{self.tag} equipment"
```
```
L3-PRS-01 press, 60 t
L3-OVN-01 oven, 200 C
L3-GRD-01 equipment
```
Speaker notes: The reviewer asked what happens when a new kind arrives. The author added a grinder and ran it. The grinder lost its detail, because the base class names its subclasses. The docstring says each kind shows its own detail. The code disagrees. One question, one finding.
Image: None. This slide is code.
---
## Slide 5: Listening is a skill
- Let the reviewer finish
- Repeat the point back in your words
- Answer a finding with a question
- Face them, hands off the keyboard
Speaker notes: Active listening, which the state standards name directly. Let the person finish. Say their point back so they know you heard it. Your first reply to a finding is a question, not a defense. And your body talks too: face them, stop typing, write the finding down.
Image: Two people talking, one with a notepad, hands off a laptop.
---
## Slide 6: The wrong way to be reviewed
- Reviewer: Why is Line a subclass of Cell?
- Author: explains for a full minute
- Author: it works, all my tests pass
- Reviewer: OK.
Speaker notes: This is what a failed walkthrough sounds like. The reviewer asked a good question. The author answered a different one, does it work, and talked until the reviewer gave up. The finding on the next slide was one test away, and it never got written down.
Image: A speech bubble filling the whole frame, a small OK bubble in the corner.
---
## Slide 7: The test that settled it
```python
line = Line("Line 3")
line.add_cell(Cell("Forming"))
line.add(Press("L3-PRS-09"))             # inherited add() skips the rule
print([type(item).__name__ for item in line.items])
try:
    line.add_cell(Press("L3-PRS-10"))
except TypeError as error:
    print("TypeError:", error)
```
```
['Cell', 'Press']
TypeError: a line holds cells
```
Speaker notes: When the pair disagreed, they agreed on a test instead of a winner. Can a loose machine get onto the line? Add cell refuses a press. The inherited add accepts one. The requirement says a line holds only cells. The test settled it.
Image: None. This slide is code.
---
## Slide 8: Disagreeing well
- Each side states its strongest case
- Find what would settle it
- A test, a requirement, or a reversible choice
- Record the decision and what was rejected
Speaker notes: Negotiation and conflict resolution, also named in the state standards. Each person states the best version of their side. Then you look for something that settles it: a test you can write, a requirement that decides it, or a choice you can undo later. The record names the decision and the option you rejected, so nobody reargues it next month.
Image: Two arrows meeting at a signed record card.
---
## Slide 9: The record
- Findings, one per line
- The disagreement, both positions
- What settled it
- What the author will change
Speaker notes: Every walkthrough ends with a written record. The template is in your project files. The author commits to the changes, and tomorrow's build time is for making them.
Image: A filled-in form with four labeled sections.
---
## Slide 10: What you are about to build
- A walkthrough packet: design, questions, one doubt
- Two rounds, 18 minutes each
- 12 minutes talking, 6 writing the record
- Swap roles for round two
Speaker notes: Build 1 is your packet: your design updated to match your code, three questions you want answered, one decision you are unsure of, and your test output. Build 2 is two rounds with an assigned partner. Twelve minutes of walkthrough, six to write the record, then swap.
Image: A timer split into a twelve-minute and a six-minute segment, twice.

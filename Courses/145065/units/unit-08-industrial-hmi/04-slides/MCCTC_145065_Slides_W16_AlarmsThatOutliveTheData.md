# Alarms That Outlive the Data
---
## Slide 1: The alarm that vanished
- The oven runs hot, the tile turns red
- A cart clips the Pi's cable
- The tile goes dark
- The next shift sees no warning
Speaker notes: The oven runs hot and the tile turns red. A minute later a cart clips the Pi's cable, and the tile goes dark. If your panel decides alarm from the current value, the next person to walk past sees nothing. The one moment the operator most needs a warning is the moment it disappears. Today an alarm stops being a color and becomes a memory.
Image: A dark screen tile beside a warm oven door.
---
## Slide 2: An alarm is a memory
- Something happened
- A person has not dealt with it yet
- Only the right events may change it
- Not knowing changes nothing
Speaker notes: An alarm is a memory. Something happened, and a person has not dealt with it yet. Memory needs a structure that only the right events can change. On your panel, only two kinds of event may move it: a live value, inside or outside its limits, and a person acknowledging it. Stale and missing data move nothing, because I do not know is never a reason to forget.
Image: A sticky note on a fridge that stays until someone takes it down.
---
## Slide 3: A memory with three states
```
9%               Quiet   -> Unseen
no reading       Unseen  -> Unseen
no reading       Unseen  -> Unseen
pilot taps SEEN  Unseen  -> Seen
7%               Seen    -> Seen
31%              Seen    -> Quiet
```
Speaker notes: A drone controller's low battery warning has three states: quiet, unseen, and seen. Nine percent raises it. The radio link drops, no reading, twice, and the warning stays unseen. The pilot taps seen. Another low reading does not undo that. Thirty one percent ends it. The panel's latch has one more state, for an alarm that ended before anyone saw it, and the same shape.
Image: None. This slide is code.
---
## Slide 4: Write the table first
- One row per state, one column per event
- The no-reading column copies its row
- Fill the panel's table on paper
- Then the switch copies the table
Speaker notes: A state machine is clearest to check as a table: one row per current state, one column per event. In the drone's table, every cell in the no reading column equals its row's state. If one differs, the design forgets on a lost link. In the lab you fill in the panel's table on paper, four by four, before you write any code. Then the switch is a copy of the table, and the tests are a copy of its cells.
Image: A hand-drawn grid with one column highlighted.
---
## Slide 5: Acknowledge is not clear
- Acknowledge: a person has seen it
- Still out of limits: still an alarm
- The banner changes its words and stays
- Clearing needs a person and a live normal value
Speaker notes: Acknowledging is not clearing. When the operator acknowledges, it means a person has seen the alarm. If the oven is still too hot, it is still an alarm. The banner changes its words, acknowledged, not cleared, and it stays. An alarm clears only when a person has seen it and a live value is back inside its limits.
Image: A banner reading ACKNOWLEDGED, NOT CLEARED across a red tile.
---
## Slide 6: The question before the action
```
DELETE  question OPEN    save Slot 2: Chapter 7
CANCEL  question closed  save Slot 2: Chapter 7
DELETE  question OPEN    save Slot 2: Chapter 7
YES     question closed  save (empty)
YES     question closed  save (empty)
```
Speaker notes: Deleting a saved game works the way acknowledging should. The button opens a question. Cancel changes nothing. Only yes acts. A second yes, with no question open, changes nothing either. The question closes before the action, so it can never sit over something that already changed. On the panel, a gloved hand that brushes the screen must never dismiss an alarm.
Image: None. This slide is code.
---
## Slide 7: The wrong way: an alarm as a Boolean
```csharp
bool isAlarm = latest > 230.0;
```
```
oven 236.0    alarm banner: UP
oven no data  alarm banner: none
```
Speaker notes: Here is the wrong way. An alarm computed from the latest value. It compiles with zero warnings and never throws. In C sharp, comparing a missing number with greater than gives false, so the banner vanished the moment the data did. Inside a latch, the same mistake is a discard arm that returns Clear. In the lab's shift replay, the Pi freezes at step three and the latch reads Clear.
Image: None. This slide is code.
---
## Slide 8: A switch with no discard
- The compiler warns CS8509: not exhaustive
- It names the missing pattern: Stale
- Ignore it and it throws at run time
- SwitchExpressionException on the first stale reading
Speaker notes: Leave out the discard arm entirely, and the compiler warns CS8509. The switch expression does not handle all possible values, and it names the one it found: sensor state stale. Ignore the warning, and the first stale reading throws a switch expression exception. The compiler told you before it ran. A discard arm that returns the current state is the safe default.
Image: A yellow warning triangle over a list of states with one missing.
---
## Slide 9: What you are about to build
- Lab U8-05: Next and Acknowledge
- Request, confirm, and cancel
- Twenty-three self-checks and ShiftReplay
- Then the panel view and six snapshots
Speaker notes: In build one you write the latch in Lab U8-05: Next, then Acknowledge, then the three methods behind the two-step question. The self-check makes twenty three checks, and ShiftReplay plays a stretch of a shift through your code. In build two you paste it all into the project and build your panel view, with word, shape, and color on every tile. Then render the six snapshots and read every one.
Image: A panel mockup with an alarm banner and a confirmation dialog.
---

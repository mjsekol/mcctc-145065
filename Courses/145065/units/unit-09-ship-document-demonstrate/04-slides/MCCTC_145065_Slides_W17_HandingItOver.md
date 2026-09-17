# Handing It Over
---
## Slide 1: The panel is about to stop being yours
- Tomorrow the shift lead owns it
- You will not be there on second shift
- What has to cross from you to them?
Speaker notes: Starting tomorrow, your panel belongs to someone else. The shift lead decides when it runs and who uses it, and you will not be standing next to it on second shift. So what exactly has to cross from you to them? Today you find out, and you do it.
Image: A panel on a post with a sticky note labeled new owner.
---
## Slide 2: Two things cross in a handoff
- A skill: they can run it
- A responsibility: they know what they own
- The skill crosses by training
- The responsibility crosses in writing
Speaker notes: A handoff moves two things. A skill, so the shift lead can use the panel and teach an operator. And a responsibility, so they know what they own, what it does not do, and who to call. Training carries the first. A letter carries the second.
Image: Two arrows from a developer to a shift lead, labeled skill and responsibility.
---
## Slide 3: Show, do, check
- Tell what it is for
- Show each situation once
- Do: the trainee drives, you stay quiet
- Check: a new situation, no hints
Speaker notes: This is the method. Tell them what it is for. Show each situation once. Then hand over the screen and be quiet while they do it. Last, a check situation they have never seen. The check is the step everyone skips, and it is the only one that proves understanding instead of copying.
Image: Four steps in a row with a hand moving from the trainer to the trainee.
---
## Slide 4: The Do situations
```
python sim_control.py --port 8705 mode drift
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}

python sim_control.py --port 8705 mode freeze
200 {"mode": "freeze", "meaning": "the service answers, but sequence and sampled_at stop advancing (STALE)"}
```
Speaker notes: You switch the simulator from a second terminal while the trainee watches the panel, not you. This is real output from the build PC, which uses port 8705. In the lab you use 8660. Write down what the trainee did in each situation, not whether they did well.
Image: None. This slide is code.
---
## Slide 5: The Check situation
```
python sim_control.py --port 8705 mode silent
200 {"mode": "silent", "meaning": "the service accepts connections and never answers (MISSING, by timeout)"}

python sim_control.py --port 8705 read
No answer from http://127.0.0.1:8705: timed out
```
Speaker notes: The trainee has seen an alarm and has seen lost data, never both at once. Start drift, wait for the alarm, then go silent. A passing answer is: the oven is still in alarm, the screen cannot see it, check the oven by hand. If they say the alarm stopped, train that situation again.
Image: None. This slide is code.
---
## Slide 6: The wrong way: a command from memory
```
python sim_control.py --port 8705 mode drop-sensor coolant-level
usage: sim_control.py [-h] --port PORT [--host HOST] [--timeout TIMEOUT]
                      {mode,read} ...
sim_control.py: error: unrecognized arguments: coolant-level
```
Speaker notes: This happens mid-training. You type a mode from memory and forget the sensor flag. The panel does not change, the trainee stands there, and your training time shrinks. Write every command on a card before the session and read them from it.
Image: None. This slide is code.
---
## Slide 7: The bigger wrong way: the tour
- You drive the screen for twenty minutes
- The trainee nods along
- "Make sense?" "Yes."
- Nothing was proven
Speaker notes: The tour feels like training. You know the panel, so the demonstration is smooth, and the trainee nods. But nothing was tested. The first time they meet a situation alone is the first time they meet it at all. Hand over the screen, and stay quiet.
Image: A trainer pointing at a screen while the trainee stands back with folded arms.
---
## Slide 8: The handoff letter
- From and to, by role, with a subject
- What is handed over, and its version
- What it does, and does not do
- Known limits, and what to do if it fails
- A request for written confirmation
Speaker notes: The letter is professional correspondence. Sender and receiver by role. A subject with the product and version. What it does and, equally important, what it does not do. Known limits. Where to look when something fails. And the part a document never has: a request that the reader act and answer.
Image: A one-page letter with a signature line at the bottom highlighted.
---
## Slide 9: Why the wrong way is tempting
- Showing feels like teaching
- Watching someone struggle is uncomfortable
- A letter feels like a formality
Speaker notes: A smooth demo feels like progress, but it is progress for you. Staying quiet while someone struggles is hard, and it is the skill. And the letter feels like paperwork, until a month later, when it is the only part of the handoff anyone can still find.
Image: A trainer with a hand hovering over a mouse, holding back.
---
## Slide 10: What you are about to build
- Build 1: your training plan, then train a classmate
- Swap: you become someone else's shift lead
- Build 2: your handoff letter, one page
- Record what the trainee did, not how it felt
Speaker notes: In Build 1 you write your outcomes and your command card, then train a classmate from another team playing the shift lead, show, do, check. Then you swap and become their trainee. In Build 2 you write your handoff letter. Your record says what the trainee did and whether the check situation passed.
Image: Two students at a panel, one driving, one watching with a clipboard.

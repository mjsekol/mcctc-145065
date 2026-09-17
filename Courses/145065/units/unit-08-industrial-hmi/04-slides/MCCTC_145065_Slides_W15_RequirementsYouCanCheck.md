# Requirements You Can Check
---
## Slide 1: "It should look clear"
- A partner writes: the panel should look clear
- Clear to whom, from where, under what light?
- Nobody can prove it, so nobody can fail it
- Your client cannot accept it either
Speaker notes: Here is a real first draft of a requirement. The panel should look clear. It sounds reasonable. Now try to test it. Clear to whom? From how far away? Under shop lights, through safety glasses? Nobody can prove it, which means nobody can ever say you missed it, and your client can never say you met it. Today we turn wishes into sentences that can fail.
Image: A sticky note reading "should look clear" stuck on a factory control screen.
---
## Slide 2: Three parts, every time
- The need, stated so it is true or false
- The reason, and who needs it
- The check: a test, a measurement, or an action
- No check means it is a wish
Speaker notes: A requirement has three parts. The need, written so it is either true or false. The reason, meaning who needs it and what goes wrong without it. And the check, which is a named test, a measurement with the passing number, or a person doing a named action. If you cannot fill in the check, rewrite the row. Requirements and design are about eighteen percent of the WebXam, so this is exam material too.
Image: A three-column table with the headers Need, Reason, Checked by.
---
## Slide 3: The wish, rewritten
- REQ-11: state text contrast at least 7:1
- Why: operators read from a distance, in glare
- Checked by: the contrast formula, every color pair
- Now it can fail
Speaker notes: Here is the same wish as a requirement. State text has a contrast ratio of at least seven to one against its background. Why: operators read the panel from a distance under glare. Checked by: a formula from the web accessibility guidelines, run on every color pair. The important part is the last line. Now it can fail, and a requirement that can fail is one you can prove.
Image: A before-and-after card: a vague sentence crossed out, a precise one beneath it.
---
## Slide 4: The check, as code
```csharp
double ratio = Ratio(text, back);
string verdict = ratio >= 7.0 ? "meets REQ-11" : "fails REQ-11";
```
```
alarm tile, white on red     7.3:1  meets REQ-11
stale tile, ink on yellow    13.8:1  meets REQ-11
grey caption on white        3.5:1  fails REQ-11
```
Speaker notes: This is the check, running. Each color becomes a luminance between zero and one. The ratio is the lighter plus point zero five over the darker plus point zero five. White on the course red is seven point three, which passes. Ink on yellow is thirteen point eight. The grey caption looks fine on your monitor, and it fails at three point five. That is why a requirement names a check instead of an opinion. The full program is in the lecture notes.
Image: None. This slide is code.
---
## Slide 5: A requirement checked by subtraction
```
sampled 14:03:27  age 1.0 s  fresh
sampled 14:03:23  age 5.0 s  fresh
sampled 14:03:22  age 6.0 s  STALE, may not be shown as live
```
Speaker notes: REQ-02 says a value whose sample is more than five seconds old is never shown as live. The check is subtraction: the panel's clock minus the sample's timestamp. Look at the middle line. Exactly five point zero seconds is fresh, because the requirement says more than five. A requirement that says about five seconds could never decide that row. Yours has to.
Image: None. This slide is code.
---
## Slide 6: The wrong way: a check that only counts
- The loader refuses a reason under 20 characters
- "seems right" is refused
- "seems right to all of us" is accepted
- A program counts; a person judges
Speaker notes: The project's loader refuses a limit with no reason. Load a thresholds file whose oven reason is seems right, and it prints: Sensor oven-temp has no reason for its limits. Write why these numbers, in a sentence an operator can read. Good. But its rule is a length, twenty characters. Seems right to all of us is twenty four characters, and it is accepted. So this requirement needs two checks: the loader, and a person reading the reason at the design review.
Image: A refusal message on a terminal next to a checklist with a person's initials.
---
## Slide 7: Constraints are requirements you did not choose
- Gloves: large buttons, far apart
- Glare and distance: big words, high contrast
- Sampling once a second: stale limit of seconds
- A pullable cable: a NO CONNECTION state
Speaker notes: Some requirements are written by the environment. Operators wear gloves, so buttons are large and far apart. The screen sits under shop lights, so words are big and contrast is high. The sensor samples once a second, so the stale limit is several seconds, not one. And someone can pull a cable, so the panel needs a no connection state and alarms that survive it. You do not choose these. You design around them.
Image: A gloved hand reaching toward a touchscreen on a machine.
---
## Slide 8: Inputs, outputs, and the parts list
- Input: one JSON reply, about once a second
- Output: word, shape, and color per tile
- Parts: Pi, power, network, probe, simulator
- Safety brief before anyone opens a kit
Speaker notes: Inputs and outputs are requirements too. The input is one reply from the Pi's service, in JSON, about once a second. The output is what the operator sees, and every tile shows its state three ways. The hardware has requirements as well, so you list every part and where it comes from. Before anyone opens a bench kit, we read the safety brief aloud: ESD precautions, power off before wiring, no mains voltage, and a signed agreement on file.
Image: A bench kit laid out on an ESD mat, each part labelled.
---
## Slide 9: The operator's workplace
- Minor labor laws limit tasks for workers under 18
- Accessibility laws require reasonable accommodation
- Your panel never decides who may operate
- Official sources only; this is not legal advice
Speaker notes: Laws shape who stands at a machine. Minor labor laws limit which tasks and machines workers under eighteen may be assigned. Accessibility laws require reasonable accommodation so a qualified person can do the job. Your panel respects both by never deciding who operates, and by not relying on color alone. We cite the official sources in the resources file, and this is not legal advice.
Image: A workplace poster board with a blank space where the official notices go.
---
## Slide 10: What you are about to build
- Build 1: kickoff, ten requirements with checks
- A constraints table and an input and output table
- Build 2: Lab U8-01, the bench check
- Twelve of twelve self-checks, simulator first
Speaker notes: In build one you open the HMI panel project. Your pair writes at least ten requirements, each with a reason and a check, plus a constraints table and an input and output table. In build two you run Lab U8-01, the bench check. You start the simulator on port 8700 and make its self-check print twelve of twelve. Pi steps happen only with me present and your agreement on file.
Image: A requirements table half filled in, next to a terminal showing a passing self-check.
---

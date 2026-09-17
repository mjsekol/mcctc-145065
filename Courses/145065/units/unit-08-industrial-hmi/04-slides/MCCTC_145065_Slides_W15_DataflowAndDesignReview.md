# Dataflow Diagrams and the Design Review
---
## Slide 1: Who catches the pulled cable?
- A reading crosses five places
- Each place can fail
- Someone must catch each failure
- If you cannot point at them, nobody does
Speaker notes: A reading from the oven crosses five places before an operator sees it: the sensor, the Pi's service, the network, your code, and the screen. Every one of them can fail. Somebody has to catch each failure and decide what the operator sees. If you cannot point at the part of your design that catches a pulled cable, nothing catches it. Today you draw where you point.
Image: A cable unplugged from a small computer, with a question mark over it.
---
## Slide 2: Boxes and labelled arrows
- Each box is a layer with one job
- Each arrow says what crosses it
- The network arrow names the contract
- Every arrow points toward the operator
Speaker notes: A dataflow diagram is boxes and arrows. Each box is a layer with one job. Each arrow is labelled with what crosses it. The network arrow names the contract: get slash api slash readings, JSON, about once a second. And every arrow points toward the operator. This panel only watches, so nothing flows back toward a machine.
Image: A simple four-box flow from Pi service to parser to rules to view.
---
## Slide 3: One reading, four shapes
```
1 network  176 characters of text arrive
2 parser   ok=True value=236
3 rules    within=False state=ALARM
4 view     ALARM HIGH  236.0 C
```
Speaker notes: This program traces one reading through the layers. It arrives as a hundred and seventy six characters of text. The parser turns it into a number and an ok flag. The rules turn that into a state, alarm. The view turns the state into words on a screen. What crosses each arrow changes shape. Draw your diagram that way, one box per line.
Image: None. This slide is code.
---
## Slide 4: Every failure gets a layer
```
view:   212.4 C, live
rules:  MISSING (the sensor said ok:false)
parser: MISSING (ok:true but no number)
parser: MISSING (the reply is not valid JSON)
```
Speaker notes: The same parser, fed four replies. A good one reaches the view. A sensor that reported ok false becomes missing. A reply that says ok but has no number becomes missing at the parser. A reply cut off in the middle is not valid JSON, and it becomes missing at the parser too. Every failure became a named result at a named layer. None reached the screen as a number.
Image: None. This slide is code.
---
## Slide 5: The failure table
- Failure, caught in, becomes, operator sees
- At least six rows
- Include the Pi's clock being wrong
- Include your own program stalling
Speaker notes: The part of the diagram that makes it reviewable is the failure table. Four columns: the failure, the layer and class that catches it, what it becomes, and what the operator sees. At least six rows. Do not skip the uncomfortable ones: a Pi whose clock is wrong, and your own program stalling. The lecture notes have a finished table for a different system, a school weather station.
Image: A four-column table with the first row filled in.
---
## Slide 6: The wrong way: trusting the layer before
```csharp
double value = doc.RootElement.GetProperty("sensors")[0].GetProperty("value").GetDouble();
```
```
Unhandled exception. System.Collections.Generic.KeyNotFoundException: The given key was not present in the dictionary.
```
Speaker notes: Here is the wrong way. GetProperty assumes the field is there. The reply broke the contract, and instead of becoming no data at the parser, the failure became a crash. On a panel, a crash is a window that disappears. The other wrong way is drawn, not typed: an arrow from the panel back to the Pi, labelled reset the service. Which requirement does that break?
Image: None. This slide is code.
---
## Slide 7: Why the layers stay separate
- The parser owns trust in the text
- The rules own time and limits
- The view owns what may appear
- Each assumes only what it was promised
Speaker notes: Each layer may assume only what the layer before it guaranteed. The parser trusts nothing about the text. The rules may assume they got a number or were told there was none, and they own time and limits. The view may assume it got one of four states, and it owns what may appear on screen. When each layer keeps its promise, a failure stops where it is caught.
Image: Three relay handoffs, each with a clearly labelled baton.
---
## Slide 8: The design review
- Four minutes: requirements, diagram, screens, limit
- Reviewers write questions before speaking
- An operator and a maintenance lead
- Every question gets an answer and a decision
Speaker notes: Tomorrow you present your design before it is finished, because that is when changes are cheap. Four minutes: your top requirements and their checks, the diagram, the screens, and your oven limit. One reviewer plays the operator, one plays the maintenance lead, and they write their questions before they speak. Every question gets an answer and a decision: change it, or keep it with a reason.
Image: A small group around a laptop, one person pointing at a diagram.
---
## Slide 9: Questions to expect
- Operator: how do I know this number is live?
- Operator: what do I press, with gloves on?
- Lead: what happens when my Pi reboots?
- Lead: does your screen touch my machine?
Speaker notes: Expect questions like these. The operator asks how they know a number is live, and what to press when the alarm goes off with gloves on. The maintenance lead asks what happens when the Pi reboots, and whether your screen ever sends anything to the machine. If you can answer those from your diagram, your design is ready to review.
Image: Two speech bubbles, one from a person in safety glasses, one from a person holding a wrench.
---
## Slide 10: What you are about to build
- Build 1: DATAFLOW.md, with a failure table
- Render the starter view and list its failures
- Sketch your own screen
- Build 2: the WebXam practice test
Speaker notes: In build one you draw your dataflow diagram on paper first, then type it into DATAFLOW dot md with at least six failure rows. Render the starter's view in its six scenes, list every requirement each picture fails, and sketch your own screen. That is the material for tomorrow's review. Build two is the WebXam practice test, closed, on paper.
Image: A hand-drawn flow diagram next to a sketched operator screen.
---

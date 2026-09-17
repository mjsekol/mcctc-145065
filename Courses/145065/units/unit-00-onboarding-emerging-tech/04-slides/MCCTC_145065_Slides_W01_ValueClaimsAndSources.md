# Value Claims and Their Sources
---
## Slide 1: A number with no owner
- "3D printing cuts costs 60 percent for all parts"
- It sounds like research
- Who measured it
- Can you open the source
Speaker notes: This morning's bell ringer. That sentence has everything research has, except research. A precise number, a confident verb, and no owner. Your brief has to argue that a technology is worth money to someone. Today is how you do that without writing sentences like this one.
Image: A floating percentage sign with a question mark where its source label should be.
---
## Slide 2: Value is value to someone
- "IoT is valuable" means nothing
- Name the buyer
- Name what they save or earn
- Name how long until it pays back
Speaker notes: A technology is not valuable in general. It is valuable to a particular buyer, for a particular reason, over a particular time. Every value sentence in your brief names the buyer. For our composite shop, the buyer is the Line 3 supervisor, and the value is downtime that does not happen.
Image: A single machine on a shop floor with a small price tag and a calendar beside it.
---
## Slide 3: Every claim has an owner
- Government and standards bodies: no stake in your purchase
- Academic studies: trust them if you can read the method
- News: only as good as the report it cites
- Vendors: a claim, not evidence. Label it.
- A chatbot answer is a lead, never a source
Speaker notes: Before a number goes in your brief, ask who measured it and whether you can open the source. Each kind of source gains something different from you. A vendor gains your purchase. A news site gains your attention. And a chatbot can describe a report that does not exist, so anything it names, you go and open yourself.
Image: A row of five source cards, each labeled with its type and a small scale icon.
---
## Slide 4: Your own numbers are allowed, labelled
```python
kit_cost = 1800.00                # ASSUMPTION
install_hours = 16                # ASSUMPTION
labor_rate = 38.00                # ASSUMPTION
downtime_hours_avoided = 10       # ASSUMPTION: from the shop's own log
cost_per_downtime_hour = 450.00   # ASSUMPTION

upfront = kit_cost + install_hours * labor_rate
annual_savings = downtime_hours_avoided * cost_per_downtime_hour
payback_months = upfront / annual_savings * 12
print(f"Upfront cost:    ${upfront:,.2f}")
print(f"Savings a year:  ${annual_savings:,.2f}")
print(f"Payback:         {payback_months:.1f} months")
```
Speaker notes: When you cannot find a source you can open, you can still argue value, with your buyer's own numbers labelled as assumptions. Every number here is invented for our composite shop, and the file says so on every line. That is honest. Anyone can challenge an assumption by name.
Image: None. This slide is code.
---
## Slide 5: The honest result
```
Upfront cost:    $2,408.00
Savings a year:  $4,500.00
Payback:         6.4 months
```
Speaker notes: So what did we learn. Not that sensors pay back in six months. We learned that for this buyer, under these five assumptions, the payback is 6.4 months. And if you rerun it with four hours of downtime avoided instead of ten, it is sixteen months. One input moves the whole answer, so that is the number the buyer should measure first.
Image: None. This slide is code.
---
## Slide 6: Now delete the times twelve
```python
payback_months = upfront / annual_savings
```
Speaker notes: I am removing the times twelve. It looks like a harmless cleanup. Predict the output before I run it.
Image: None. This slide is code.
---
## Slide 7: Good news that is wrong
```
Upfront cost:    $2,408.00
Savings a year:  $4,500.00
Payback:         0.5 months
```
Speaker notes: No error. A sensor kit that pays for itself in two weeks. Upfront divided by yearly savings is in years, and the label says months. It is off by a factor of twelve, and it is exactly the kind of number that ends up in a sales pitch, because good news does not get double checked. Always write the unit, and always ask, really?
Image: None. This slide is code.
---
## Slide 8: How to cite in this course
- Number sources, cite with [1] in the text
- One line per source: publisher, title, URL
- Add the type and what it supports
- Write that you opened it
Speaker notes: The citation format is in the notes and the template. Numbered sources, bracket numbers in your text, and one line per source with a type and what it supports. Opened in Week 1 means you looked. The checker in the project folder finds any figure with no owner. It cannot tell whether your source says what you claim. Only you opening it can.
Image: A short numbered source list with bracketed citation markers linking to it.
---
## Slide 9: Writing for a busy reader
- Recommendation first
- One idea per paragraph
- Numbers in a table
- Assumption written next to every number that is yours
Speaker notes: The supervisor may read only your summary. So the recommendation goes first. One idea per paragraph. More than two numbers, use a table. And label your own numbers every single time, even when it feels repetitive. That label is what makes your argument checkable.
Image: A one-page document with a highlighted summary at the top and a small table below.
---
## Slide 10: What you are about to build
- Build 1: find three sources and log them
- At least one is not a vendor
- Build 2: draft the brief and your value model
- Run brief_check.py and record the result
Speaker notes: Build 1 is research. Three sources in the log, each with who published it and whether you could see how any number was measured. AI tools are allowed and logged, and anything they name, you open. Build 2 drafts the architecture and value sections and your value model. Run the checker today even though it will fail. Tomorrow it has to pass.
Image: A sources log table with three filled rows beside a terminal running brief_check.py.

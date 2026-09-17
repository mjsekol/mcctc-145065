# Paired Demo Checklist · Tool Crib on the Web
## 145065 Object-Oriented Programming · Unit 4 Project · Week 8, Friday, Build 2

**Why this sheet exists.** A demo shows whether you can explain what you built, and that is the one
thing nobody else can do for you. Your partner scores you on this sheet. The instructor spot-checks
some demos. You swap roles when you finish.

Print one per student. The presenter hands this sheet to the partner before starting.

| Role | Name, as it appears on the class roster |
|---|---|
| Presenter | |
| Partner (scorer and timer) | |

Write nothing else about either person on this sheet.

---

## The five minutes

The partner times it. Stop the presenter at 5:00, even mid-sentence.

| Minutes | What the presenter shows |
|---|---|
| 0:00-0:30 | The problem, in one sentence, in the attendant's words |
| 0:30-1:30 | The dashboard, a filtered tool list, and one tool's page. Name the requirement each one shows. |
| 1:30-2:30 | A good checkout: the form, the redirect, the confirmation, and a refresh that saves nothing |
| 2:30-3:30 | A refused checkout: a tool already out, and a tool past calibration, with the messages |
| 3:30-4:30 | One attack from `ATTACK_LOG.md`, sent live to their own app, and the line of code that stopped it |
| 4:30-5:00 | One thing they would change, then the question below |

**Common ways a demo goes wrong.** The server was not started before the timer. The store copy
already has the demo tool checked out, so the "good checkout" is refused. The `SECRET_KEY` changed
since the form was loaded, so the POST gets 403. Start the app, load the form once, and check the
dashboard before you hand this sheet over.

---

## The question

The instructor chooses one. Tick it. The presenter answers in under 30 seconds without looking
anything up.

- [ ] 1. "Show me the line that stops a tool from going out twice."
- [ ] 2. "What happens if someone deletes the `required` attribute and submits?"
- [ ] 3. "Why does your app redirect after saving?"
- [ ] 4. "What would a broken JSON file look like to the attendant?"

---

## The ten-point checklist

Tick each one you saw. One point each.

- [ ] 1. Finished inside five minutes
- [ ] 2. Stated the problem in the client's terms
- [ ] 3. Named the requirement each screen shows
- [ ] 4. Showed the redirect and the refresh
- [ ] 5. Showed two different refusals with their messages
- [ ] 6. Sent a real attack to their own app
- [ ] 7. Pointed at the line of code that stopped it
- [ ] 8. Every page shown extends the same layout
- [ ] 9. Named one change they would make
- [ ] 10. Answered the question correctly without looking it up

**Score: ______ / 10**

---

## One sentence from the partner

Write the one thing that was clearest in this demo, or the one thing you still do not understand
about this app.

&nbsp;

______________________________________________________________________________________

&nbsp;

______________________________________________________________________________________

---

Partner's initials: ______  Instructor spot-check: ______

Riverside Fabrication is a composite: an invented shop used for teaching. Attacks go to your own app
on 127.0.0.1 and nowhere else.

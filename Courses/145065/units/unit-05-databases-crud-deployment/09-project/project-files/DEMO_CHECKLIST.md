# Demo Recording Checklist · Tool Crib Live
## 145065 Object-Oriented Programming · Unit 5 Project · Week 10, Friday, commit window

**Why this sheet exists.** Your recording is the Demonstration dimension, 10 points. It shows that
the app is live, that it does what the client asked, and that you can explain how. Nobody else can do
that last part for you. Use this sheet twice: once to plan the recording, and once to check it before
you commit it. Your instructor scores the recording on the same ten points.

Print one per student.

| Role | Name, as it appears on the class roster |
|---|---|
| Presenter | |
| Checked by (a classmate, or you) | |

Write nothing else about either person on this sheet.

---

## Before you press record

- The app is running on this year's target, and `/health` shows the version you are submitting.
- You have a fresh copy of the starting data, so the tool you check out is not already out.
- `data/tools_import_bad.csv` and `data/tools_import.csv` are ready, and the good file has not been
  loaded yet.
- `schema.sql`, `ER_DIAGRAM`, and `USER_TEST.md` are open in tabs.
- Your screen shows nothing personal: no email, no messages, no other accounts. Close them.
- Use only the invented badges and tools from your seed data. Type nothing real into the app.

**Common ways a recording goes wrong.** The form's token expired because the server restarted after
the page loaded, so the POST answers 403: reload the form first. The good import file was already
loaded, so it is refused for duplicate tags: rebuild the database first. The recorder captured one
window and the browser was in another: do a ten-second test recording. The recording ran past five
minutes because you read the code aloud: point, name, move on.

---

## The five minutes

Time it. Stop at 5:00, even mid-sentence.

| Minutes | What you show |
|---|---|
| 0:00-0:30 | The live URL, and `/health` showing 1.0.1 |
| 0:30-1:30 | A checkout, a return, and a void with its confirmation |
| 1:30-2:15 | The import: the bad file refused with line numbers, then the good file loaded |
| 2:15-3:00 | The report, and one number checked against your hand calculation |
| 3:00-3:45 | `schema.sql` and your ER diagram: point at one foreign key and one constraint the database enforces |
| 3:45-4:30 | `USER_TEST.md`: the problem your tester found that you fixed, and the fix |
| 4:30-5:00 | What you would change for version 1.1, and why it is a MINOR version |

---

## The ten-point checklist

Tick each one the recording shows. One point each.

- [ ] 1. Five minutes or less, with the live URL shown first
- [ ] 2. `/health` shows the submitted version
- [ ] 3. Create, update, and delete shown, with the delete confirmed
- [ ] 4. The import refused a bad file and named the lines
- [ ] 5. One report number checked against a hand calculation
- [ ] 6. A foreign key and a database constraint named
- [ ] 7. The tester's problem and the fix shown
- [ ] 8. The version change explained with MAJOR, MINOR, PATCH
- [ ] 9. Nothing real typed into the app on screen
- [ ] 10. Voice and screen both clear

**Score: ______ / 10**

---

## Where the recording goes

Record your screen and your voice with the recorder on the lab image [VERIFY which one]. Commit the
file to your repository if it is under the size your instructor sets. If it is larger, commit a link
to where your instructor told you to put it. The last commit must be inside the Week 10, Friday
commit window.

---

Checker's initials: ______  Instructor spot-check: ______

Riverside Fabrication is a composite: an invented shop used for teaching. Your outside tester is a
real person, so the recording shows their role, never their name.

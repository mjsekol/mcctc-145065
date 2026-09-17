# The Server's Rules Are the Real Rules
---
## Slide 1: The form said required
- The sign-up form marks the name required
- The browser will not submit it blank
- A blank sign-up is saved anyway
- How did it get in
Speaker notes: Here is a thing that happens on real sites. The form will not let you submit a blank name. And yet the database fills with blank names. Nobody broke the browser. They skipped it. Watch me do it to yesterday's lab app with one script.
Image: A sign-up form with a red required marker, and a list of saved entries with one blank row.
---
## Slide 2: One request took the site down
- A script posts every rule broken
- The server saves the record
- The store refuses to load its own file
- Every page answers 503 for everyone
Speaker notes: That was send raw, from the lab folder, against the Part 1 app. No browser. The server saved a severity called apocalyptic. The store checks its file on every request, refused it, and the whole site went dark. The Unit 3 backup habit saved us. I restored the dot bak file. This is why today exists.
Image: A single arrow striking a server icon, with a row of browser windows all showing 503.
---
## Slide 3: The browser checks are a courtesy
- required, maxlength, pattern: hints for honest people
- A request does not need your page
- The server repeats every rule
- A validator returns clean values and messages
- Empty messages means allowed
Speaker notes: Here is the concept. Keep the HTML hints, because they help honest people fix mistakes before sending. They do not protect anything. On the server, a validator takes the raw form and gives back two things: the clean values and a dictionary of messages. An empty dictionary means yes.
Image: A browser with a thin dotted fence, and a server with a solid wall behind it.
---
## Slide 4: The rules as code
```python
BADGE_PATTERN = r"[TS]-[0-9]{4}"   # T or S, a hyphen, four digits
DOWNTIME_MAX = 1440                # minutes in one day


def badge_ok(text):
    return re.fullmatch(BADGE_PATTERN, text.strip().upper()) is not None


def downtime_ok(minutes):
    return 0 <= minutes and minutes <= DOWNTIME_MAX


def lockout_problem(severity, locked_out):
    return severity == "critical" and not locked_out
```
Speaker notes: Three shapes of rule for Line 3 at our composite shop, Riverside Fabrication. A pattern for the badge. A range for downtime, two relational tests joined by and. And a rule across two fields: critical, and not locked out. The badges are invented. Note fullmatch. That word matters in five minutes.
Image: None. This slide is code.
---
## Slide 5: The program prints its own truth table
```
severity  locked_out  refused
critical  True        False
critical  False       True
high      True        False
high      False       False
```
Speaker notes: Every combination of the two inputs, and the result for each. Only one row is refused: critical and not locked out. This is the exam's logical operators and compound conditions, used for a reason a technician would care about. Put a table like this in your own tests.
Image: None. This slide is code.
---
## Slide 6: Test the edges
```
'T-1041'     badge_ok=True
' s-2003 '   badge_ok=True
'T-104'      badge_ok=False
'T-10415'    badge_ok=False
'X-1041'     badge_ok=False
   -1 downtime_ok=False
    0 downtime_ok=True
   90 downtime_ok=True
 1440 downtime_ok=True
 1441 downtime_ok=False
```
Speaker notes: The lowercase badge with spaces passes because we clean before we check. One digit short fails. One digit long fails. And for downtime, the test values sit on both sides of both edges. Range bugs live at the edges, so the edges are what you test.
Image: None. This slide is code.
---
## Slide 7: Swap fullmatch for match
```python
def badge_ok(text):
    return re.match(BADGE_PATTERN, text.strip().upper()) is not None
```
Speaker notes: One word changes. Match instead of fullmatch. Every valid badge still passes. Predict which of the five test badges changes its answer.
Image: None. This slide is code.
---
## Slide 8: A badge nobody holds gets in
```
'T-1041'     badge_ok=True
' s-2003 '   badge_ok=True
'T-104'      badge_ok=False
'T-10415'    badge_ok=True
'X-1041'     badge_ok=False
```
Speaker notes: T 10415 now passes. Match only checks that the text starts with the pattern. It starts with a valid badge, so the extra digit is ignored. Why would the browser's pattern attribute have refused it? Because pattern always checks the whole value. So your manual test in the browser passes, and the server is wrong. Only a test that skips the browser finds this.
Image: None. This slide is code.
---
## Slide 9: Habits that keep the layers agreeing
- Use fullmatch for whole-value rules
- Test one step past every edge
- Return every message at once
- One constant feeds the hint and the check
Speaker notes: Match is the name everyone remembers, which is why this bug is common. Use fullmatch. Test one past each edge. Send back every problem at once, so a person fixes them in one pass. And write each limit once, as a constant, so the HTML hint and the server check cannot drift apart.
Image: Two gears labeled browser and server, turning together from one shared shaft labeled constants.
---
## Slide 10: What you are about to build
- Lab U04-02 Part 2, steps 8 to 12
- Write every rule in validation.py
- Run it against the provided tests
- send_raw.py now gets 400 and four refusals
Speaker notes: Build 1 is Lab U04-02 Part 2. You write every rule in validation dot py, against tests that are already written. When you finish, run send raw again. This time the server answers 400 with four refused lines, and the store file is unchanged. The self-check should show 32 of 36.
Image: A terminal showing Server answered 400 followed by four lines beginning refused.

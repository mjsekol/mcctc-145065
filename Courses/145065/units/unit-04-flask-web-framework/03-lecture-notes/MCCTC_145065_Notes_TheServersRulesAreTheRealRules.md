# Lecture Notes: The Server's Rules Are the Real Rules
## 145065 Object-Oriented Programming · Unit 4 · Week 8, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W08_ServerRules.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W08_ServerRules.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.

**Competencies:** 5.5.1 develop programs using data validation techniques. 5.3.3 write code that
uses logical operators (`and`, `or`, `not`). 5.3.4 write code that uses relational operators and
compound conditions. 5.2.4 write code that applies string operations (pattern matching).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every badge and record is
invented.

---

## Why this exists

Yesterday's form had `required` on the title. The browser refused to submit it empty. It is tempting
to believe that means the title is checked.

It does not. **A request does not have to come from your page.** A script, a command-line tool, or a
browser's developer tools can send any fields with any values straight to your server. The browser's
checks never run for those requests.

In class, one script sent one request with every rule broken to the lab app from yesterday. The
server saved it. The store then refused to load its own file, and every page answered 503 for
everyone. One request took the whole site down. The lab handout records that run.

So the rule for the rest of the course: **the browser's checks are a courtesy for honest people. The
server's checks are the rules.**

This is also the one day this semester that logical and relational operators are taught in Python on
a real rule. Those competencies sit in the heaviest outcome on the WebXam.

---

## The concept in plain language

Every rule the browser enforces, the server enforces again. The HTML attributes (`required`,
`minlength`, `maxlength`, `pattern`, `min`, `max`) stay, because they help honest people fix a mistake
before sending. They are hints, not protection.

On the server, a **validator** is a function that takes the raw form and returns two things:

- the **clean values**: trimmed, converted to the right types
- a **dictionary of messages**, one per field that broke a rule

**An empty dictionary means the input is allowed.** Anything else means the route answers 400, shows
the messages, and saves nothing.

The rules come in four shapes:

| Shape | Example | Python tools |
|---|---|---|
| a pattern | a badge is `T` or `S`, a hyphen, four digits | `re.fullmatch` |
| a range | downtime is 0 to 1440 minutes | `<=`, `and` |
| a list | severity is one of four words | `in` |
| a rule across two fields | a critical issue must have the machine locked out | `and`, `not` |

**`re.fullmatch`** checks that the **whole** text matches a pattern. That word, whole, is where
today's bug lives.

---

## Worked example 1: the rules as code

```python
# rules_demo.py
# The server's rules, written as code you can test without a browser.
import re

BADGE_PATTERN = r"[TS]-[0-9]{4}"   # T or S, a hyphen, four digits
DOWNTIME_MAX = 1440                # minutes in one day


def badge_ok(text):
    # fullmatch: the WHOLE text must match the pattern, not only its start.
    return re.fullmatch(BADGE_PATTERN, text.strip().upper()) is not None


def downtime_ok(minutes):
    # Two relational tests joined by a logical operator.
    return 0 <= minutes and minutes <= DOWNTIME_MAX


def lockout_problem(severity, locked_out):
    # A compound rule across two fields.
    return severity == "critical" and not locked_out


for badge in ["T-1041", " s-2003 ", "T-104", "T-10415", "X-1041"]:
    print(f"{badge!r:12} badge_ok={badge_ok(badge)}")
for minutes in [-1, 0, 90, 1440, 1441]:
    print(f"{minutes:5} downtime_ok={downtime_ok(minutes)}")
print("severity  locked_out  refused")
for severity in ["critical", "high"]:
    for locked_out in [True, False]:
        print(f"{severity:9} {locked_out!s:11} {lockout_problem(severity, locked_out)}")
```

Output:

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
severity  locked_out  refused
critical  True        False
critical  False       True
high      True        False
high      False       False
```

Read it in three parts.

- **The badge.** `' s-2003 '` passes because the code trims the spaces and uppercases it first. That
  is cleaning, and it happens before the check. `T-104` is too short. `T-10415` is too long.
- **The range.** The test values sit on both sides of both edges: -1 and 0, 1440 and 1441. Edges are
  where range bugs hide, so edges are what you test.
- **The compound rule.** The last block is a **truth table**, printed by the program. It lists every
  combination of the two inputs. Only one row is refused: critical, and not locked out.

The pattern uses `[0-9]` instead of `\d`. In Python, `\d` also matches digits from other writing
systems, and a badge should only ever contain the ten digits 0 to 9.

---

## Worked example 2: a validator that returns clean values and messages

This example is a gaming tournament sign-up, with invented gamertags.

```python
# signup_rules.py
# A validator returns clean values and a dictionary of messages.
# An empty dictionary means the input is allowed.
import re

TAG_PATTERN = r"[A-Za-z0-9_]{3,16}"
TEAM_MIN, TEAM_MAX = 1, 5


def validate_signup(form):
    clean, errors = {}, {}

    tag = form.get("gamertag", "").strip()
    if re.fullmatch(TAG_PATTERN, tag) is None:
        errors["gamertag"] = "Use 3 to 16 letters, digits, or underscores."
    clean["gamertag"] = tag

    size_text = form.get("team_size", "").strip()
    if not re.fullmatch(r"[0-9]{1,2}", size_text):
        errors["team_size"] = "Team size must be a whole number."
    else:
        size = int(size_text)
        if size < TEAM_MIN or size > TEAM_MAX:
            errors["team_size"] = f"Team size must be {TEAM_MIN} to {TEAM_MAX}."
        clean["team_size"] = size

    team_name = form.get("team_name", "").strip()
    # A compound rule across two fields: a team of more than one needs a name.
    if clean.get("team_size", 0) > 1 and not team_name:
        errors["team_name"] = "A team needs a name."
    clean["team_name"] = team_name

    return clean, errors


print(validate_signup({"gamertag": "night_owl", "team_size": "3", "team_name": "Owls"}))
print(validate_signup({"gamertag": "no", "team_size": "9"}))
print(validate_signup({"gamertag": "solo_ace", "team_size": "1"}))
print(validate_signup({"gamertag": "duo_ace", "team_size": "2"}))
```

Output:

```
({'gamertag': 'night_owl', 'team_size': 3, 'team_name': 'Owls'}, {})
({'gamertag': 'no', 'team_size': 9, 'team_name': ''}, {'gamertag': 'Use 3 to 16 letters, digits, or underscores.', 'team_size': 'Team size must be 1 to 5.', 'team_name': 'A team needs a name.'})
({'gamertag': 'solo_ace', 'team_size': 1, 'team_name': ''}, {})
({'gamertag': 'duo_ace', 'team_size': 2, 'team_name': ''}, {'team_name': 'A team needs a name.'})
```

Three things to notice.

- The second sign-up broke three rules, and **all three** messages came back. A person fixes every
  problem in one pass instead of one per submit.
- `team_size` came back as the number `3`, not the text `"3"`. The validator converts, so the route
  never does.
- The size is checked for digits **before** `int()` runs. `int("nine")` would crash. The pattern
  check turns that crash into a message.

The size range uses `or`: too small **or** too big. The downtime range in example 1 used `and`: at
least 0 **and** at most 1440. Both say the same kind of thing from opposite sides. Pick the one that
reads most clearly, and test the edges either way.

---

## Worked example 3: the browser's checks do not run

```python
# no_browser.py
# The form's HTML says required and maxlength="16". A request that never
# touched the form ignores both. Only the server's check runs.
from flask import Flask, abort, request

app = Flask(__name__)
FORM_HTML = '<input name="gamertag" required maxlength="16">'
SAVED = []


@app.post("/trusting")
def trusting():
    SAVED.append(request.form.get("gamertag", ""))     # trusts the browser
    return "saved"


@app.post("/checking")
def checking():
    tag = request.form.get("gamertag", "").strip()
    if not 3 <= len(tag) <= 16:                         # the server's own rule
        abort(400)
    SAVED.append(tag)
    return "saved"


client = app.test_client()                              # no browser anywhere
for route in ["/trusting", "/checking"]:
    for tag in ["", "x" * 500]:
        response = client.post(route, data={"gamertag": tag})
        print(f"{route:10} length {len(tag):3} -> {response.status_code}")
print("saved lengths:", [len(t) for t in SAVED])
```

Output:

```
/trusting  length   0 -> 200
/trusting  length 500 -> 200
/checking  length   0 -> 400
/checking  length 500 -> 400
saved lengths: [0, 500]
```

The HTML said `required` and `maxlength="16"`. The trusting route saved an empty tag and a
500-character tag anyway, because no browser was involved. The checking route refused both. The HTML
never changed. Only the server's rule made a difference.

`3 <= len(tag) <= 16` is a **chained comparison**. Python reads it as
`3 <= len(tag) and len(tag) <= 16`.

---

## The wrong version, and the output it produces

In `rules_demo.py`, change `re.fullmatch` to `re.match` in `badge_ok`. The first five lines become:

```
'T-1041'     badge_ok=True
' s-2003 '   badge_ok=True
'T-104'      badge_ok=False
'T-10415'    badge_ok=True
'X-1041'     badge_ok=False
```

**`T-10415` now passes.** No crash. No message. A badge that does not exist lands in the record.

`re.match` checks only that the text **starts** with the pattern. `T-10415` starts with `T-1041`, a
valid badge, so it matches, and the extra `5` is ignored. `re.fullmatch` requires the pattern to
cover the whole text, from the first character to the last.

Here is the part that makes this bug hard to find. The HTML `pattern` attribute always checks the
whole value. So in a browser, `T-10415` is refused, and your manual test passes. Only a request that
skips the browser reaches the server's `re.match`. **The two layers disagree, and only a test that
talks to the server finds it.**

---

## Why the wrong version is tempting

`re.match` is the name you remember, and it is what many tutorials show. It works for every valid
badge you try, and for most invalid ones too: `T-104` and `X-1041` are still refused. The only
inputs it lets through are ones that start valid and keep going, and nobody types those while
testing by hand.

The habits that prevent it:

- use `re.fullmatch` for any rule about what a whole value looks like
- test the values **one step past** each edge: one character too short, one too long
- write the rule once, as a constant, and use that constant in both the HTML hint and the server
  check, so they cannot drift apart

---

## Vocabulary

| Term | What it means |
|---|---|
| **Validation** | checking that input follows the rules before the program uses it |
| **Validator** | a function that returns clean values and a dictionary of messages |
| **Client-side check** | a rule the browser applies, such as `required`; a hint, not protection |
| **Server-side check** | a rule your Python code applies; the only check every request meets |
| **Pattern (regular expression)** | a description of what text must look like, such as `[TS]-[0-9]{4}` |
| **`re.fullmatch`** | matches only if the pattern covers the whole text |
| **Compound condition** | two or more tests joined by `and`, `or`, or `not` |
| **Truth table** | a table of every combination of inputs and the result for each |
| **Edge value** | a value exactly at, or one step past, a limit |

---

## Self-check

**Question 1.** A form has `<input name="hours" type="number" min="1" max="72">`. Your route converts
the value with `int()` and saves it. Name two different requests that would get past this, and what
each one does.

**Question 2.** Write a compound condition, using `and` and `not`, that is true when a tool may go on
a shelf only if it is `returned` and not `damaged`. Use the variables `returned` and `damaged`, both
`True` or `False`. Then list the one row of its truth table that gives `True`.

**Question 3.** Which values would you test for a rule that says "a title is 5 to 80 characters," and
why those?

---

### Answers

**1.** Any request sent without the browser skips `min` and `max`. For example: `hours=500` is saved as
500, because nothing on the server checks the range. `hours=three` makes `int()` raise a
`ValueError`, which becomes a 500 error because the route never checked the text first. The fix is a
server-side check: digits only, then the range, with a message for each.

**2.** `returned and not damaged`. The only row that gives `True` is `returned` is `True` and
`damaged` is `False`.

**3.** 4 and 5 characters, and 80 and 81 characters, because the bugs in a range live at its edges.
Also an empty title and a title of only spaces, since a title that is blank after trimming should be
refused.

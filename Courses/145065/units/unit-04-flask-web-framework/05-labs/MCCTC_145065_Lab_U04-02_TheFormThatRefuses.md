# Lab U04-02: The Form That Refuses
## 145065 Object-Oriented Programming · Unit 4 · Week 8

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Week 8, Monday through Thursday, one
part a day. **Competencies:** 5.5.7 (read inputs), 5.6.6 (design inputs and processes), 5.5.1 (data
validation), 5.3.3 (logical operators), 5.3.4 (relational operators and compound conditions), 5.2.4
(string pattern matching), 9.3.1 (identify vulnerabilities: cross-site scripting, injection), 9.3.3
(secure coding: escaping, validation, CSRF prevention).

Files: `lab-u04-02-files/`. The app is last week's finished app plus one form, with four parts taken
out, one per day. Every removed part is marked with a `TODO` that names its lab part.

**Riverside Fabrication is a composite**, an invented shop. Every record is invented. **Every attack in
this lab is sent to your own app on 127.0.0.1 and to nothing else.** That rule is in the Lab
Acceptable Use and Safety Agreement.

---

## The scenario

Last week the maintenance log went on the web, read-only. This week technicians log a new issue on a
form. The moment a page accepts input, every value in the request is a stranger's value. This lab is
about making the server refuse everything it should, and show everything as text.

## What you will build

A form that saves a good issue and redirects, refuses a bad one with messages a person can follow,
shows a script tag in a title as text, and refuses a form that did not come from your site.

---

## Starter code

Copy `lab-u04-02-files/` into your repository. The form needs a place to write, so point the app at a
copy of the store, not the original. PowerShell:

```
Copy-Item data\line3_log.json $env:TEMP\line3_copy.json
$env:STORE_PATH = "$env:TEMP\line3_copy.json"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python app.py --port 8680
```

Then, in another terminal from the lab folder:

```
python selfcheck_u04_02.py
```

It reports `14 of 36 self-checks passed`. The Week 7 pages already work. Read `app.py`,
`validation.py`, and `security.py`. Each `TODO` names its part.

---

## Part 1: the form posts, saves, and redirects · Monday

### Step 1. Point the app at a copy of the store

Do the setup above. **Never run the form against `data/line3_log.json`.** A copy protects the original.

### Step 2. See the blank form

Open `/issues/new`. The form shows. Submit it. Right now the POST answers 501, because `create_issue`
is not written.

### Step 3. Read the plan in `create_issue`

Open `app.py` and read the `TODO` in `create_issue`. It lists six steps in order.

### Step 4. Write `create_issue`

Follow the six steps: get the store, validate the form, answer 400 with the form and the person's
answers if there are errors, otherwise save, flash a message, and redirect with code 303.

**Observable result:** a good issue lands on its own page with "Issue 8 logged. Thank you."

### Step 5. Prove the redirect

On the new issue's page, press refresh. A browser may ask whether to send the form again. Because the
POST answered 303, refreshing loads a page and saves nothing.

**Observable result:** no second issue is saved.

### Step 6. Run the self-check

**Observable result:** every "Carried" and Part 1 line is PASS (18 of 36 so far).

### Step 7. Commit

**Acceptance criteria, Part 1.** Every Part 1 line is PASS. A good issue saves once and redirects.

---

## Part 2: the server's rules · Tuesday

### Step 8. See a raw request take the site down

With the app running against a fresh copy of the store, in a second terminal:

```
python send_raw.py --port 8680
```

`send_raw.py` sends a form with a real badge and every other field broken, the way a request with no
browser would. Right now `validation.py` accepts anything, so the bad issue is saved. Reload the
dashboard.

**Observable result:** the whole site answers 503. The terminal shows
`[store] StoreFormatError: issues[7]: unknown severity 'apocalyptic'`. One raw request saved a record
the store refuses to load. Restore the store copy from its `.bak` file, which the store wrote before
the save.

### Step 9. Read the tests

Open `test_app.py` and read `ValidationTests`. Those tests are the specification for `validate_issue`.

### Step 10. Write the rules

In `validation.py`, write one block per field, in `FIELD_ORDER`. Each block reads the raw value, sets a
message in `errors` when a rule fails, and sets `clean`. The rules: the badge matches `[TS]-[0-9]{4}`
after trim and upper, and is on the list; the machine is on the list; the title is 5 to 80 characters
on one line; the description is 10 to 1000 characters; the severity is a known value; downtime is a
whole number 0 to 1440 using `[0-9]`, not `\d`; and a critical issue must be locked out.

### Step 11. Send the raw request again

```
python send_raw.py --port 8680
```

**Observable result:** the server answers 400 and lists the refused fields. Nothing is saved.

### Step 12. Run the self-check

**Observable result:** every Part 2 line is PASS (32 of 36 so far).

**Acceptance criteria, Part 2.** Every Part 2 line is PASS. `send_raw.py` is refused with 400.

---

## Part 3: input is data, never code · Wednesday

### Step 13. Find the template that trusts input

A comment in one template says a title is marked safe "so a supervisor can use formatting." Find it.
Send a title with a script in it and see what happens:

```
python send_raw.py --port 8680 --title "<script>document.title='owned'</script>"
```

Open the issue it saved. The tab title changes: the script ran.

**Observable result:** the raw `<script>` tag is in the page source.

### Step 14. Fix it

Remove the `| safe` from that template. Send the same title again and open the issue.

**Observable result:** the page shows `&lt;script&gt;` as text. The tab title does not change.

### Step 15. Run the attacks

```
python attack_demo.py --port 8680
```

**Observable result:** attacks 3 and 4 (the stored script and the attribute breakout) pass, meaning the
attack failed as it should. Every Part 3 line in the self-check is PASS (33 of 36 so far).

**Acceptance criteria, Part 3.** Every Part 3 line is PASS. The page source shows escaped text, never a
raw script tag. Your README names the template that had the problem and why its comment was wrong.

---

## Part 4: forms prove where they came from · Thursday

### Step 16. Read the plan in `check_csrf`

Open `security.py`. `check_csrf` lets every request through right now. Read its `TODO`.

### Step 17. Write `check_csrf`

A request whose method is safe passes untouched. Otherwise the form's token must match the session's,
compared with `secrets.compare_digest`. No match, or no token, is a 403. Your notes say why you compare
with `compare_digest` and not `==`.

**Observable result:** the form still works for you, because the page includes the token.

### Step 18. Break it two ways

First, delete the hidden `csrf_token` input from `templates/issue_form.html`, load the form, and submit.
403. Put it back. Then stop the server, start it again with no `SECRET_KEY` set, load the form, and
submit. 403 again, for a different reason: the new key cannot read the old session.

**Observable result:** both give 403. Write both reasons in your README.

### Step 19. Run every attack

```
python attack_demo.py --port 8680
```

**Observable result:** `6 of 6 attacks failed as they should.`

### Step 20. Run everything

```
python selfcheck_u04_02.py
python -m unittest
```

**Observable result:** `36 of 36 self-checks passed`, and 36 tests OK.

**Acceptance criteria, full lab.**
- [ ] `python selfcheck_u04_02.py` prints `36 of 36 self-checks passed`
- [ ] `python attack_demo.py --port 8680` prints `6 of 6 attacks failed as they should.`
- [ ] `python -m unittest` reports 36 tests, OK
- [ ] Your README names both reasons a form can get 403
- [ ] You ran every attack against your own app only
- [ ] Committed and pushed

---

## If it breaks

### 1. Every POST answers 403

**Cause:** the form is missing the hidden `csrf_token` input, or the `SECRET_KEY` changed between
loading the form and sending it. Restarting without a fixed key does that. Set `SECRET_KEY` once and
keep it for the session.

### 2. The form passes in the browser and fails on the server

That is the design. The browser's checks are hints. The server's checks are the rules.

### 3. `BadRequestKeyError: 400 Bad Request`

**Cause:** you read `request.form["name"]` for a field the browser did not send, such as an unticked
checkbox. Use `request.form.get("name")` and test the result.

### 4. Refreshing after a POST sends it again

**Cause:** the route rendered a page instead of redirecting. `create_issue` must answer a 303 redirect.

### 5. The whole site answers 503 after you submit a form

**Cause:** a form saved a record the store refuses to load, because a rule is missing. Restore the store
copy from its `.bak` file and finish the rule. This is what step 8 shows on purpose.

### 6. Trailing whitespace in rendered HTML fails web-check

**Cause:** an empty error line left spaces behind. The template uses `{{-` to strip them. Match the
anchor's `issue_form.html`.

---

## Stretch goal

The downtime rule uses `[0-9]`, not `\d`. Find out why. In a Python shell, compare
`re.fullmatch(r"[0-9]{1,4}", "٣٠")` with `re.fullmatch(r"\d{1,4}", "٣٠")`, and try `int("٣٠")`. Write in
your README what `\d` matches that `[0-9]` does not, and why that matters for a downtime field.

---

## Submission checklist

- [ ] `36 of 36 self-checks passed`
- [ ] `6 of 6 attacks failed as they should.`
- [ ] 36 tests OK
- [ ] README names both 403 reasons and the escaping fix
- [ ] Attacks sent only to your own app on 127.0.0.1
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Part 2 not reached by the end of Tuesday, or the student is editing `test_app.py` to pass | SCAFFOLDED |
| Steady progress, questions about the rules or the token | STANDARD |
| 36 of 36 before Thursday's Build 1 is half over | EXTENDED |
| The student says forms are not real programming | APPLIED |

---

## SCAFFOLDED

**Changed sections:**
- **Part 2:** the student receives three of the seven rule blocks written (badge, machine, severity)
  and writes the other four.
- **Checkpoints:** show the self-check after Part 1, Part 2, and Part 3.
- **Keep Part 4.** The token is the point.

**Acceptance criteria:** 36 of 36 self-checks, 6 of 6 attacks refused, both 403 reasons in the README.

**Grading:** same 100-point scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a defense the lab did not teach.

**Added requirement.** Add a `Content-Security-Policy` header to every response that allows the page's
own styles and scripts and nothing from other sites. Read the anchor's `w10_deploy/app.py`
`SECURITY_HEADERS` for the exact policy string, and the OWASP page on the header, and cite both. Then,
in your README, name one thing the policy blocks that escaping alone does not.

**Acceptance criteria:** all STANDARD criteria; the header is on every response; a test checks it; the
README names what the header adds beyond escaping.

**Grading:** same scale.

---

## APPLIED

**For the student who says forms are not real programming.** The same validation, at the command line.

**Changed scenario.** Write `intake.py`, a command-line tool that reads a CSV of proposed issues (you
invent at least four rows, one good and three each breaking a different rule) and applies the same
rules `validate_issue` uses, printing for each row whether it is accepted or which rules it broke, then
importing only the accepted rows into a copy of the store. Reuse `validation.py` unchanged.

**Acceptance criteria:** every good row is accepted and every bad row is refused with the right
message; you reused `validation.py` without editing it; a rule that fails in the CSV would fail the same
way in the form.

**Grading:** same scale. Requirements Fit is judged on whether the command-line rules match the form's
rules exactly.

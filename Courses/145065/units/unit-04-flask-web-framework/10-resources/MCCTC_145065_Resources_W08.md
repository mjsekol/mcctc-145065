# Additional Resources · Week 8
## 145065 Object-Oriented Programming · Unit 4 · Week 8
### Topic: forms and Post/Redirect/Get, server-side validation and regular expressions, escaping and cross-site scripting, injection, and cross-site request forgery

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**Three program rules apply to every resource below.**

- **No personal data goes into any AI tool or any website.** That includes the regular expression
  tester in section 5. Test your patterns on invented badges and tool tags only.
- **Every attack you practice this week goes to your own app on 127.0.0.1, and to nothing else.**
  Not a classmate's app, not the school's site, not a site from a video. This rule is in the Lab
  Acceptable Use and Safety Agreement. Several resources below show attacks. Reading about an attack is
  fine. Sending one to a system you do not own is not, and it can be a crime.
- **Nothing here needs an account, a payment, or an AI service.**

---

## The week at a glance

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Flask Quickstart: request data, redirects, flashing | Mon | On-level | 25 min |
| 2 | Automate the Boring Stuff 3e, chapter 9 | Tue | On-level | 45 min |
| 3 | Python `re` documentation, and the Regular Expression HOWTO | Tue | On-level | 20 min |
| 4 | Flask: Security Considerations | Wed, Thu | On-level | 25 min |
| 5 | Practice: regex101 | Tue | On-level | 30 min |
| 6 | OWASP cheat sheets: input validation, XSS, CSRF | Tue-Thu | Extension | 20 min each |
| 7 | Videos: Computerphile on XSS and on CSRF | Wed, Thu | Remediation | under 20 min each, [VERIFY] length |
| 8 | Industry connection: injection is still on the list | Wed, Fri | Extension | 30 min |
| 9 | Flask-WTF's CSRF page, for comparison | Thu | Extension | 15 min |
| 10 | Side quest: SQ-23 or SQ-02 | Fri | Extension | one to two blocks |

---

## 1. Primary reading: the request, the redirect, the flash

**Flask documentation, "Quickstart"** · `https://flask.palletsprojects.com/en/stable/quickstart/` ·
**Opened.**

You read the top half last week. This week, read these sections:

| Section | Matches |
|---|---|
| HTTP Methods | Monday. One URL, two methods. |
| Accessing Request Data, "The Request Object" | Monday. Find what happens when a key is not in `request.form`. That is Monday's deliberate error. |
| Redirects and Errors | Monday |
| Message Flashing | Monday. "Issue 8 logged. Thank you." is a flashed message. |

**A warning before you read the Sessions section.** Its example writes the secret key directly in the
code. That is fine for a documentation example and wrong for your app. On Thursday your `SECRET_KEY`
comes from the environment, and no key appears in any file you commit.

**Time.** 25 minutes. **Level.** On-level.

---

## 2. Primary reading: regular expressions

**Automate the Boring Stuff with Python, 3rd edition, chapter 9, "Text Pattern Matching with Regular
Expressions"** · `https://automatetheboringstuff.com/3e/chapter9.html` · **Opened.**

**What it is.** A free book chapter that builds regular expressions up from nothing: character
classes, quantifiers, matching at the start and end of a string, and verbose mode.

**Why this one.** Tuesday's badge rule is a pattern. This chapter explains every character in it,
with examples that are not about a shop floor, so you see the idea twice.

**Read these sections:** "The Syntax of Regular Expressions," "Qualifier Syntax," "Quantifier Syntax,"
and "Matching at the Start and End of a String."

**The failure mode to watch for.** The chapter uses `search()` in many examples. A validator needs
the whole value to match, not a piece of it. Tuesday's deliberate error is that difference.

**Time.** 45 minutes. **Level.** On-level.

---

## 3. Official documentation: the `re` module

**Python documentation, "re: Regular expression operations"** ·
`https://docs.python.org/3/library/re.html` · **Opened.**

**Read two parts, not the whole page.**

- The section **"search() vs. match()"**. It shows `match()` checking only the start of a string,
  `search()` checking anywhere, and `fullmatch()` checking the entire string. Say which one Tuesday's
  validator uses, and why.
- The entry for **`\d`** under the special sequences. For ordinary text patterns it matches any
  Unicode decimal digit, which is more than `0` to `9`. That is Tuesday's "ahead" question about why
  the lab writes `[0-9]`.

**Python documentation, "Regular Expression HOWTO"** ·
`https://docs.python.org/3/howto/regex.html` · **Opened.**

A gentler introduction from the same documentation. Use it if the reference page feels dense.

**Time.** 20 minutes. **Level.** On-level. The HOWTO is remediation.

---

## 4. Official documentation: what Flask protects, and what it leaves to you

**Flask documentation, "Security Considerations"** ·
`https://flask.palletsprojects.com/en/stable/web-security/` · **Opened.**

**What it is.** The Flask maintainers' own list of web security problems and which ones Flask
handles.

**Why this one.** Two sections match this week exactly.

- **Cross-Site Scripting (XSS).** It says Flask configures Jinja to escape every value unless told
  otherwise, and then lists the places you still have to be careful. It also warns about attributes
  without quotes. Check your templates against that warning.
- **Cross-Site Request Forgery (CSRF).** It explains why a cookie is sent even with a request another
  site started, and why Flask does not add a token for you.

**Read later, in Week 10:** "Security Headers" and "Set-Cookie options."

**Time.** 25 minutes. **Level.** On-level.

---

## 5. Practice: regex101

`https://regex101.com/` · **Opened.**

**What it is.** A free, browser-based regular expression tester. Type a pattern and some test text,
and it highlights every match and explains each part of the pattern. No account is needed to use the
tester.

**Why this one.** You see a pattern fail before your validator does. Paste your badge pattern. Then
type ten test values, five that should pass and five that should not, and watch which ones light up.

**Three cautions.**

- **Check the flavor.** The page loaded with a PHP flavor selected when this file was written. Choose
  Python in the flavor list if it is offered. Flavors differ in small ways that matter.
- **The tester matches pieces of text by default.** To test the way `re.fullmatch` works, anchor your
  pattern with `^` and `$` in the tester, and remember why your Python code does not need them.
- **Do not use "Save & Share."** It publishes your pattern and your test text at a link. Test text is
  invented badges only, never a real name.

**Time.** 30 minutes. **Level.** On-level.

---

## 6. The security community's references

All three are from the OWASP Cheat Sheet Series, a free set of references written by security
practitioners.

**OWASP, "Input Validation Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html` · **Opened.**

For Tuesday. It explains allowlist validation, where you define exactly what is allowed and refuse
everything else. It also states plainly that validation in the browser can be bypassed and must be
repeated on the server. Find that sentence. It is this week's sentence in OWASP's words.

**OWASP, "Cross Site Scripting Prevention Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html` ·
**Opened.**

For Wednesday. Read "Introduction," "Framework Security," and the start of "Output Encoding." Its
opening point is that no single technique stops cross-site scripting. Compare that with Wednesday's
line: escaping protects display, validation protects meaning, and you need both.

**OWASP, "Cross-Site Request Forgery Prevention Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html`
· **Opened.**

For Thursday. Read "Introduction" and the "Synchronizer Token Pattern" part of "Token-Based
Mitigation." The lab's `security.py` is a hand-written version of that pattern. Find one requirement
the cheat sheet sets for the token, and show where `security.py` meets it.

**Time.** 20 minutes each. **Level.** Extension. These are long pages written for working developers.
Read the named sections only.

---

## 7. Videos, under 20 minutes

**Computerphile, "Cracking Websites with Cross Site Scripting - Computerphile"** ·
`https://www.youtube.com/watch?v=L5l9lSnNMxg` · **[VERIFY]**.

**Computerphile, "Cross Site Request Forgery - Computerphile"** ·
`https://www.youtube.com/watch?v=vRBihr41JTo` · **[VERIFY]**.

**Status of both.** The titles and the channel were confirmed through YouTube's public embed
information while this file was written. The running times were not confirmed from YouTube. Check each
is under 20 minutes before you assign it.

**What they are.** Short explanations from a university-affiliated computer science channel. The
first shows how text typed into a form becomes script on someone else's screen. The second shows how
another site can make your browser submit a form to a site you are signed in to.

**Why these.** Wednesday and Thursday are the two hardest ideas in the unit, and both make more sense
when you see them than when you read them. Watch one before the day it matches, or after, if the lecture did not land.

**Honest note.** Both videos are several years old. The attacks have not changed. Some of the web
pages and browsers they show have.

**Level.** Remediation. YouTube may be blocked on the school network.

---

## 8. Industry connection: injection is still on the list

**CISA and FBI, "Secure by Design Alert: Eliminating Cross-Site Scripting Vulnerabilities"** ·
`https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-cross-site-scripting-vulnerabilities`
· **Opened.**

**What it is.** A public alert from two US government agencies to companies that make software. It
calls cross-site scripting a preventable class of defect and asks makers to remove it at the source.
Among its recommendations are web frameworks that encode output automatically, code review, and
adversarial testing.

**OWASP Top 10, "Injection"** · `https://top10.owasp.org/2025/A05_2025-Injection/` · **Opened.**

**What it is.** The injection category from the current edition of the OWASP Top 10. It groups
cross-site scripting and SQL injection together, and its first recommendation is a safe interface
that keeps data separate from commands.

**Why these.** You spent this week doing three things the alert asks professionals to do: use a
framework that escapes by default, review generated code for the defect, and attack your own app
before anyone else does. That is not classroom busywork. It is what the agencies are asking the
industry for.

**Write three sentences.** Name one recommendation from the alert. Say where your tool crib app
already follows it. Say where it does not yet.

**Time.** 30 minutes. **Level.** Extension.

---

## 9. For Thursday's "ahead" task: Flask-WTF

**Flask-WTF documentation, "CSRF Protection"** · `https://flask-wtf.readthedocs.io/en/latest/csrf/`
· **Opened.**

**What it is.** The documentation for a widely used Flask extension that adds CSRF protection to
every form. Its hidden input is named `csrf_token`, the same name the lab uses.

**Why this one.** Thursday's ahead task compares the lab's hand-written `security.py` with an
extension. **Read it. Do not install it.** The lab does not use it, and adding a package to the lab
image is your instructor's decision. Write the
tradeoff in your decision log: what the extension does for you, and what writing it by hand taught you
that the extension would have hidden.

**Time.** 15 minutes. **Level.** Extension.

---

## 10. Side quests

Both are in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**SQ-23 · The Form That Fights Back.** ★★★, two blocks. Build a form, then attack your own form: empty
fields, absurdly long input, script tags, SQL-shaped strings, emoji, and right-to-left text. It is done
when every attack is handled with a message a normal person would understand, nothing crashes, and
your README documents each attack and its defense. The catalog says it plainly: never attack a site
you do not own.

**Why it fits this week.** It is Project M7 taken further. The catalog lists it under 145010, so your
instructor offers it to students who submitted the Unit 4 project early. Your tool crib form is a good
target, on 127.0.0.1.

**SQ-02 · The Regex Wrangler.** ★★, one to two blocks. Write a program that reads a block of messy
text you really have, such as a copied schedule or a list of assignment titles, and pulls out every
item matching one pattern: times, dollar amounts, or anything else with a shape. It is done when it
finds every match in your sample, you can explain each character of your pattern, and your README
shows the input and output side by side. The stretch goal is to find the case your pattern misses.

**Why it fits this week.** For a student who liked Tuesday. The catalog's starting point is the `re`
documentation in section 3. **Before you choose your sample text, strip out every real name, number,
and address.** A group chat export is full of other people's personal data, and it does not belong in
a repository.

**Level.** Extension, both.

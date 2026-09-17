# Lecture Notes: Forms Prove Where They Came From
## 145065 Object-Oriented Programming · Unit 4 · Week 8, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W08_CrossSiteRequestForgery.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W08_CrossSiteRequestForgery.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.

**Competencies:** 9.3.3 implement secure coding concepts (cross-site request forgery prevention).
9.3.1 identify application vulnerabilities (session and cookie attacks).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

---

## Why this exists

Your browser keeps cookies for each site you use. It sends a site's cookies with **every** request to
that site. It does that even when the request was started by a different site.

Picture this. You are using the shop's maintenance app in one tab. In another tab, you open some
other page. That page contains a hidden form that posts to the maintenance app, and a line of script
that submits it the moment the page loads. Your browser sends the request, with your cookies. The
maintenance app sees a normal POST from your session, and it cannot tell that you never meant it.

That is **cross-site request forgery**, usually shortened to CSRF. The attacker never sees your
screen or your cookies. They only need your browser to send a request on their behalf.

Modern browsers have made this harder. A cookie's `SameSite` setting, which the anchor sets to `Lax`,
tells the browser to hold the cookie back on many cross-site requests, including a POST from another
site's form [VERIFY the current default and behavior in the lab's browser]. That is real protection,
and it is also a default you do not control on the visitor's machine and a line another developer can
change. So the token stays: it is the defense your own code guarantees, and `SameSite` is a second
layer on top of it. Defense in depth means you do not rely on either one alone.

---

## The concept in plain language

The defense is a **CSRF token**: a long random value that proves a form came from your own site, in
this session.

1. When your site sends a form, it puts a random token in a hidden field.
2. The same token is stored in the person's **session**.
3. When a POST arrives, the server compares the token in the form with the token in the session.
4. If there is no token in the session, or the two do not match, the server refuses with **403
   Forbidden**.

The other site cannot read your page, so it cannot learn the token, so it cannot put the right one in
its forged form.

Three details make it work.

- **The session is signed with `SECRET_KEY`.** Flask stores the session in a cookie and signs it. A
  visitor can read that cookie, but cannot change it without the signature failing. The key must be
  secret, so it comes from the **environment**, never from the code. A key in the code ends up in
  your repository, and then it is not secret.
- **Compare with `secrets.compare_digest`,** never with `==`. An `==` comparison can stop at the
  first character that differs, so the time it takes leaks a little about how much of a guess was
  right. `compare_digest` takes the same time no matter where the difference is.
- **The token is not a password.** It proves the form came from this site in this session. It does
  nothing against a person who is really using the site, and it does not say who that person is. That
  would need logins, which this course's app does not have.

---

## Worked example 1: the token in action

```python
# csrf_demo.py
# Every form carries a random token that also lives in the signed session.
# A POST without the matching token is refused with 403.
import os
import secrets

from flask import Flask, abort, render_template_string, request, session

app = Flask(__name__)
# The key signs the session cookie. It comes from the environment, never the code.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

FORM = """<form method="post" action="/issues/new">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <input name="title" aria-label="Title">
  <button type="submit">Log it</button>
</form>"""


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.before_request
def check_csrf():
    if request.method == "POST":
        expected = session.get("csrf_token")
        sent = request.form.get("csrf_token", "")
        if not expected or not secrets.compare_digest(sent, expected):
            abort(403)


app.jinja_env.globals["csrf_token"] = csrf_token


@app.get("/issues/new")
def new_issue_form():
    return render_template_string(FORM)


@app.post("/issues/new")
def create_issue():
    # A template escapes the typed title. Never paste it into an f-string.
    return render_template_string("Saved: {{ title }}", title=request.form.get("title", ""))
```

`@app.before_request` runs before **every** view, so one check covers every POST in the app.
`app.jinja_env.globals` makes `csrf_token()` available in every template.

Through the test client, one session loaded the form, then posted with its token, then posted
without it. A second session, a different "browser," posted the first session's token:

```
token length 43
with token: 200 Saved: Belt &lt;i&gt;squeal&lt;/i&gt;
no token: 403
someone else sends your token: 403
```

- The token is 43 characters of random text. `token_urlsafe(32)` makes 32 random bytes and writes them
  in a form that is safe inside a URL or a form field.
- With the token, the save worked, and the typed title was escaped, as on Wednesday.
- Without it, 403.
- The last line matters most. The second session had the **right token**, copied from the first. It
  was still refused, because its own session held no token. A token only counts in the session it was
  made for.

---

## Worked example 2: signed, not secret

```python
# signed_not_secret.py
# Flask's session cookie is signed, not encrypted. You can read it.
# You cannot change it without the server noticing.
import base64
import json
import os
import secrets

from flask import Flask, session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)


@app.get("/start")
def start():
    session["csrf_token"] = "demo-token-for-reading"
    return "ok"


@app.get("/check")
def check():
    return f"token in session: {'csrf_token' in session}"


client = app.test_client()
client.get("/start")
cookie = client.get_cookie("session").value
data_part = cookie.split(".")[0]
data_part += "=" * (-len(data_part) % 4)
print("readable:", json.loads(base64.urlsafe_b64decode(data_part)))
print(client.get("/check").get_data(as_text=True))

# Change one character of the cookie, as a visitor might try to.
flipped = ("f" if cookie[0] != "f" else "e") + cookie[1:]
client.set_cookie("session", flipped)
print(client.get("/check").get_data(as_text=True))
```

Output:

```
readable: {'csrf_token': 'demo-token-for-reading'}
token in session: True
token in session: False
```

Anyone holding the cookie can decode it and read what is inside. That is why nothing secret belongs
in a session. When the cookie was changed by one character, the signature no longer matched, and
Flask treated the session as empty.

This is also why the token being readable is fine. **The person using the site is allowed to see
their own token.** The other site is not, because a browser does not let one site read another site's
pages or cookies.

---

## Worked example 3: where the key comes from

```python
# key_source.py
# Where did the key come from? Print the source, never the key.
import os
import secrets

from_env = os.environ.get("SECRET_KEY")
key = from_env or secrets.token_hex(32)
print("key came from:", "the environment" if from_env else "a new random value")
print("key length:", len(key))
```

Run it in PowerShell three times: with no key set, after setting one, and after removing it.

```
python key_source.py
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python key_source.py
Remove-Item Env:SECRET_KEY
python key_source.py
```

Output:

```
key came from: a new random value
key length: 64
key came from: the environment
key length: 64
key came from: a new random value
key length: 64
```

The second line of commands makes a random key and stores it in the environment **of that terminal
only**, without ever printing it. Close the terminal and it is gone. Command Prompt sets a variable with
`set NAME=value`, and a macOS or Linux terminal uses `export NAME=value`.

With no key in the environment, the program makes a **new random key every time it starts**. That
keeps the app safe, and it has a cost, which the next section shows.

---

## The wrong version, and the error it produces

Delete the hidden `csrf_token` input from the form. Load the form in a browser and submit it. The page
is:

```
Forbidden
You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.
```

The protection worked. The template forgot its half. **This is the most common Week 8 problem**: a
new form without the hidden input, and every POST from it refused. Every form that posts needs:

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

### The same 403, for a different reason

Put the input back. Start the app with no `SECRET_KEY` set, load the form, then restart the app and
submit the form you already loaded. This script does the same thing without a browser. It sits next
to `csrf_demo.py`, and it changes the key the way a restart with no key set does:

```python
# restart_demo.py
# The same session and the same valid token, before and after the key changes.
import re
import secrets

from csrf_demo import app

client = app.test_client()
page = client.get("/issues/new").get_data(as_text=True)
token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)

response = client.post("/issues/new", data={"csrf_token": token, "title": "Belt squeal"})
print("before restart:", response.status_code)

app.config["SECRET_KEY"] = secrets.token_hex(32)     # what a restart with no key does
response = client.post("/issues/new", data={"csrf_token": token, "title": "Belt squeal"})
print("after the key changed:", response.status_code)
```

Output, run with no `SECRET_KEY` in the environment:

```
before restart: 200
after the key changed: 403
```

The restart made a new random key. The session cookie was signed with the old key, so the server can
no longer read it. `session.get("csrf_token")` is `None`, and the check refuses the POST. The
technician who had the form open sees `Forbidden` with nothing wrong on their side.

The fix: set `SECRET_KEY` in the environment before you start the app, so every restart uses the
same key.

---

## Why the wrong version is tempting

The hidden input is invisible on the page. When you build a new form by copying the visible fields
from a sketch, the one field nobody can see is the one that gets left out. The form looks complete.

The key problem is tempting for the opposite reason. Writing the key into the code makes restarts
work, and it feels harmless in a class project. Then the file is committed, the repository is shared,
and the key is public. Anyone with the key can sign their own session cookie.

The habits:

- every form that posts gets the hidden token input; check it first when a form answers 403
- the key comes from the environment; no key appears in any file
- compare tokens with `secrets.compare_digest`

---

## Vocabulary

| Term | What it means |
|---|---|
| **Cross-site request forgery (CSRF)** | another site making your browser send a request to a site you use, with your cookies |
| **CSRF token** | a random value in each form and in the session that proves the form came from this site |
| **Session** | data Flask keeps for one visitor between requests, stored in a signed cookie |
| **Cookie** | a small piece of data a site asks the browser to send back with every request to that site |
| **Signed** | protected against changes by a signature made with a secret key; still readable |
| **`SECRET_KEY`** | the key Flask signs sessions with; comes from the environment |
| **Environment variable** | a named value set outside the program, in the terminal or the server's settings |
| **`secrets.compare_digest`** | compares two values in the same time wherever they differ |
| **403 Forbidden** | the server understood the request and refuses to carry it out |

---

## Self-check

**Question 1.** You add a new form for closing an issue. Every submit answers `Forbidden`. Other forms
in the app work. What do you check first, and why that?

**Question 2.** A classmate says, "The token is in the page source, so anyone can read it. That makes
it useless." Explain why the token still protects the app.

**Question 3.** Why does `check_csrf` use `secrets.compare_digest(sent, expected)` instead of
`sent == expected`?

---

### Answers

**1.** Check that the new form has the hidden input,
`<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`. The other forms work, so the
key and the check are fine. The one thing that differs is the new template, and a form without the
token is refused with 403 on every POST.

**2.** Only the person using the site can see their own page source. The attacking site's page runs
in the same browser, but the browser does not let one site read another site's pages, so it cannot
learn the token. A token copied into a different session is also refused, because it must match the
token stored in that session.

**3.** `==` can stop at the first character that differs, so the time it takes reveals a little about
how much of a guessed token was right. `compare_digest` takes the same time wherever the difference
is, so timing reveals nothing.

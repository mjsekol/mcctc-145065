# Input Is Data, Never Code
---
## Slide 1: A username that changes the page
- A game site shows your username
- Someone signs up with a name full of tags
- Everyone who views their profile runs their code
- The site never checked what a name contains
Speaker notes: Imagine a game site that prints usernames on a leaderboard. Someone registers a name that is really a piece of HTML. Now everyone who opens the leaderboard runs that person's code. Nobody hacked a password. The page did the attacker's work. Today you learn why, and the one habit that stops it.
Image: A leaderboard with one row whose name is a jumble of angle brackets, glowing launch red.
---
## Slide 2: One mistake, many languages
- Typed text should stay a value
- Pasting it into code makes it code
- HTML, templates, SQL: same mistake
- Pass it as a value instead
Speaker notes: Here is the concept. An injection is text that should have been a value, pasted into text that is code. Your app writes three languages: HTML, Jinja templates, and SQL starting in Week 9. The mistake has the same shape in all three, and so does the fix.
Image: Three code windows labeled HTML, Jinja, SQL, each with a typed value dropped into a slot.
---
## Slide 3: The three shapes
- HTML: never an f-string or `| safe`
- HTML safe: `{{ title }}` in a template
- Template: never `render_template_string(f"...")`
- Template safe: pass `q=q` as a value
- SQL, Week 9: use `?` parameters
Speaker notes: This is the table from your notes. The middle row has its own name, server-side template injection. When typed text becomes part of the template itself, the server runs any template syntax inside it. We are not demonstrating that one today. Learn to recognize it from the rule.
Image: A three-row table with a red column labeled pasted and a blue column labeled passed.
---
## Slide 4: Jinja escapes by default
```python
ISSUES = {9: {"id": 9, "title": "<script>document.title='owned'</script>"}}


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    return render_template("issue.html", issue=ISSUES[issue_id])


print(escape("Bracket <b> & \"quotes\" 'too'"))
```
Speaker notes: Issue 9 on Line 3 has a title somebody typed, and it is a script. Riverside Fabrication is a composite, and this record is invented. The template shows it with a plain double-brace title. The print line uses markupsafe escape, the same function Jinja uses.
Image: None. This slide is code.
---
## Slide 5: Shown as text, run never
```
Bracket &lt;b&gt; &amp; &#34;quotes&#34; &#39;too&#39;
<h1>Issue 9: &lt;script&gt;document.title=&#39;owned&#39;&lt;/script&gt;</h1>
raw script tag in page: False
```
Speaker notes: Every special character is replaced with a code that only displays. The reader sees the title exactly as typed, angle brackets and all. The browser runs nothing. I will open the page source so you can see the codes yourself. Your job is not to add escaping. Jinja already does it. Your job is to not turn it off.
Image: None. This slide is code.
---
## Slide 6: Pasted versus passed
```
/pasted  <p>Welcome back, <img src=x onerror=alert(1)></p>
/passed  <p>Welcome back, &lt;img src=x onerror=alert(1)&gt;</p>
```
Speaker notes: Same typed name, two routes. The first put it in an f-string. The page now holds a real image tag whose error handler runs code. The second passed it to a template as a value, and it is text. That is why no view in this course returns an f-string with anything a person typed.
Image: None. This slide is code.
---
## Slide 7: Add one filter
```html
<h1>Issue {{ issue.id }}: {{ issue.title | safe }}</h1>
```
Speaker notes: One change. I add pipe safe to the title. It sounds protective. Predict what happens when I load issue 9.
Image: None. This slide is code.
---
## Slide 8: The script is live
```
<h1>Issue 9: <script>document.title='owned'</script></h1>
raw script tag in page: True
```
Speaker notes: The raw script tag is in the page. Watch the browser tab. The title changes from Issue 9 to owned. That script ran. It runs for every person who opens this issue, because it is stored in the data. That is stored cross-site scripting. Safe means I promise this is HTML I trust. A person's typed title is never that. I remove it.
Image: None. This slide is code.
---
## Slide 9: Escaping and validation do different jobs
- Escaping decides how an allowed value shows
- Validation decides whether a value is allowed
- A title about a `<b>` tag is legitimate
- Severity apocalyptic escapes fine and is wrong
- You need both
Speaker notes: A technician may really need to report a problem with a b tag in a laser program. Refusing that title would be wrong. Store it as typed and show it escaped. A severity of apocalyptic has no dangerous characters, and it is still not a severity. Only validation catches it. One does not replace the other.
Image: Two shields side by side, one labeled display, one labeled meaning.
---
## Slide 10: What you are about to build
- Lab U04-02 Part 3, steps 13 to 15
- Find the template that turned escaping off
- Prove the attack with `send_raw.py --title`
- Fix it, then run attacks 3 and 4
Speaker notes: Build 1 is Lab U04-02 Part 3. One template in the lab app turns escaping off, and its comment claims that is fine. Find it. Prove the problem with send raw and a title, on your own server only. Fix it, run attack demo attacks 3 and 4, and check that the page source shows the escaped codes. Write in your README which file it was and why its comment was wrong.
Image: A page source view with an escaped script tag highlighted in launch blue.

# Forms Prove Where They Came From
---
## Slide 1: A page you never touched posts as you
- You are signed in to a site
- You open a different page in another tab
- It hides a form aimed at the first site
- Your browser sends it, with your cookies
Speaker notes: You are logged in somewhere in one tab. In another tab you open some random page. That page has a hidden form pointed at the first site, and a line of script that submits it. Your browser sends that request with your cookies attached, because that is what browsers do. The first site sees you. You never clicked anything.
Image: Two browser tabs, one plain page with a hidden form sending an arrow into the other tab.
---
## Slide 2: Cross-site request forgery
- Browsers send your cookies on every request to a site
- Even when another site started the request
- The server cannot tell you did not mean it
- The attacker never sees your screen
Speaker notes: That attack has a name, cross-site request forgery, CSRF. The attacker does not steal your cookies or see your page. They borrow your browser. Every form in our app that changes data is a target, so every one of them needs a defense.
Image: A browser icon carrying a cookie toward a server, with a shadowy hand pointing it there.
---
## Slide 3: The defense is a token
- Each form carries a random hidden token
- The same token lives in the session
- A POST must send the matching token
- No match means 403 Forbidden
- The other site cannot read your token
Speaker notes: Here is the concept. When our site sends a form, it includes a long random token. The same token is stored in the session. When a post arrives, the two must match. The attacking page cannot read our pages, so it cannot learn the token, so its forged form fails.
Image: A form and a session card, each holding the same token, joined by an equals sign.
---
## Slide 4: The token and the check
```python
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)


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
```
Speaker notes: The key that signs the session comes from the environment, never the code. The token is made once per session. Before every request, any post is checked. Compare digest takes the same time wherever two values differ, so timing leaks nothing about a guess. A plain double equals can stop at the first difference.
Image: None. This slide is code.
---
## Slide 5: With, without, and borrowed
```
token length 43
with token: 200 Saved: Belt &lt;i&gt;squeal&lt;/i&gt;
no token: 403
someone else sends your token: 403
```
Speaker notes: With the token, the Line 3 issue saved, and the typed title was escaped, like yesterday. Riverside Fabrication is still our composite shop. Without the token, 403. The last line is the one to think about. A second session sent the first session's correct token and was still refused, because a token only counts in its own session.
Image: None. This slide is code.
---
## Slide 6: The token is not a password
- It proves the form came from this site
- It proves nothing about who you are
- It does nothing against a real user
- The session is signed, not encrypted
Speaker notes: This is the misconception to kill today. The token is not a password. You can read your own token in the page source, and that is fine. The session cookie is signed, not encrypted, so a visitor can read it but not change it. Proving who someone is needs logins, and this app does not have them.
Image: A padlock crossed out next to a postmark stamp labeled from this site.
---
## Slide 7: Delete the hidden input
```html
<form method="post" action="/issues/new">
  <input name="title" aria-label="Title">
  <button type="submit">Log it</button>
</form>
```
Speaker notes: I delete one line from the form, the hidden token input. The page looks exactly the same, because that input was never visible. I load the form and submit it. Predict the page.
Image: None. This slide is code.
---
## Slide 8: Forbidden
```
Forbidden
You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.
```
Speaker notes: The protection worked. The template forgot its half. This is the most common Week 8 support call. When a form answers Forbidden, check the hidden input first. Now I put it back, and show you the same 403 for a completely different reason.
Image: None. This slide is code.
---
## Slide 9: Same 403, different reason
```
before restart: 200
after the key changed: 403
```
Speaker notes: No key in the environment means a new random key every time the app starts. The old session cookie was signed with the old key, so the server cannot read it anymore. No token in the session, so 403. The technician did nothing wrong. Name both reasons you have seen today. The fix for this one is setting SECRET KEY in the environment before you start.
Image: None. This slide is code.
---
## Slide 10: What you are about to build
- Lab U04-02 Part 4, steps 16 to 20
- Write check_csrf in security.py
- Break it twice on purpose, then repair it
- attack_demo.py: 6 of 6 attacks fail
- Self-check: 36 of 36
Speaker notes: Build 1 is Lab U04-02 Part 4. You write check CSRF in security dot py. The handout then has you break it twice on purpose and read what each break does, then repair it. Then attack demo sends six real attacks at your own server on 127.0.0.1, and all six must fail. The self-check must print 36 of 36. The lab is due at the end of today's block.
Image: A terminal reading 6 of 6 attacks failed as they should, beside a navy shield.

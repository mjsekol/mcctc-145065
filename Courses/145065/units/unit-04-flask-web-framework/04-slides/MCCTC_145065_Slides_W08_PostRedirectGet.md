# Post/Redirect/Get
---
## Slide 1: Resend the form
- You order food online
- The page hangs, so you refresh
- The browser asks: resend the form
- You click yes
- How many orders did you place
Speaker notes: Most of you have seen that box. The browser asks whether to send the form again, and nobody reads it. If the site was built the naive way, you have now ordered twice. Today your pages start accepting input, and you will build them so a refresh can never do that.
Image: A browser dialog asking to confirm form resubmission, with two identical receipts behind it.
---
## Slide 2: One URL, two methods
- GET shows the form and changes nothing
- POST sends the fields back
- The server saves, then answers 303
- The browser follows with a plain GET
Speaker notes: Here is the concept. The same address answers two methods. GET shows the form. POST carries what the person typed, in request dot form. After saving, the server does not send a page. It sends 303 See Other and an address. The browser goes there with a GET. That is Post, Redirect, Get.
Image: A three-step arrow diagram: POST, 303 with Location, GET, on a navy background.
---
## Slide 3: The form
```html
<form action="{{ url_for('create_issue') }}" method="post">
  <label for="title">Short title</label>
  <input id="title" name="title" type="text" required>
  <input id="locked-out" name="locked_out" type="checkbox" value="yes">
  <label for="locked-out">The machine is locked out</label>
  <button type="submit">Log the issue</button>
</form>
```
Speaker notes: This is the Line 3 new issue form. Riverside Fabrication is our composite shop. Each input's name becomes a key in request dot form. The checkbox sends its value, yes, but only when it is ticked. Hold on to that.
Image: None. This slide is code.
---
## Slide 4: The route
```python
@app.post("/issues/new")
def create_issue():
    title = request.form.get("title", "").strip()
    # An unticked checkbox sends nothing at all, so .get() with a test.
    locked_out = request.form.get("locked_out") == "yes"
    ISSUES.append({"id": len(ISSUES) + 1, "title": title, "locked_out": locked_out})
    # 303 See Other: "go GET this page now." Post/Redirect/Get.
    return redirect(url_for("issue_detail", issue_id=len(ISSUES)), code=303)
```
Speaker notes: Read, save, redirect. There is no validation today, on purpose. Tomorrow adds every rule. The locked out line is the one to study. Get returns None when the field is missing, and None equals yes is False.
Image: None. This slide is code.
---
## Slide 5: What came back
```
303 /issues/1
200 Issue 2: Guard &lt;b&gt;interlock&lt;/b&gt; trips (locked out: True)
```
Speaker notes: The first post answered 303 with the new issue's address. The second had the box ticked, and I followed the redirect. Locked out is True. And look at the title. I typed a b tag, and the page shows it as text, because it went through a template. That is Wednesday arriving early.
Image: None. This slide is code.
---
## Slide 6: Without the redirect
```
200 Saved issue 1
200 Saved issue 2
200 Saved issue 3
3 issues saved
```
Speaker notes: This version answered the post with a page instead of a redirect. I sent the same post three times, which is what a refresh and a yes does. Three identical issues. No error anywhere. With the redirect, refresh repeats the GET, and a GET saves nothing.
Image: None. This slide is code.
---
## Slide 7: Now read the box directly
```python
    locked_out = request.form["locked_out"] == "yes"
```
Speaker notes: One change. Square brackets instead of get. I submit the form with the box unticked. Predict what the technician sees.
Image: None. This slide is code.
---
## Slide 8: Bad Request, and no clue
```
Bad Request
The browser (or proxy) sent a request that this server could not understand.
```
Speaker notes: That is the whole page. The terminal shows one request line with 400, and nothing names the field. Turn on TRAP BAD REQUEST ERRORS while developing and the traceback ends with KeyError locked out. An unticked box sends nothing at all. Not no, not False. Nothing.
Image: None. This slide is code.
---
## Slide 9: Two habits from today
- Read optional fields with `.get()` and a test
- End every successful POST with a 303
- What the page shows is not what it sends
- Remove the trap setting when you finish
Speaker notes: You tested with the box ticked, so it worked. That is why this bug ships. Read fields with get unless the field is truly required and checked. And end every successful post with a redirect. The trap setting is for finding bugs. While it is on, a bad request becomes a 500, so take it out.
Image: A checklist card with two large checkmarks, navy and launch blue.
---
## Slide 10: What you are about to build
- Lab U04-02 Part 1, steps 1 to 7
- Run the app against a copy of the store
- The new issue form posts, saves, and redirects
- Refresh must not save a ninth issue
Speaker notes: Build 1 is Lab U04-02, The Form That Refuses, Part 1. Step 1 shows you how to run against a copy of the store, so your real file stays clean. A good issue lands on its own page with Issue 8 logged, thank you. Refresh that page and confirm no ninth issue appears. The self-check should show 18 of 36 when you finish.
Image: A browser showing an issue page with a confirmation banner, and a refresh icon crossed out.

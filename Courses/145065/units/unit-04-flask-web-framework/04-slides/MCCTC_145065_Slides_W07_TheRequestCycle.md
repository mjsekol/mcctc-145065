# The Request Cycle
---
## Slide 1: Page not found, but whose fault
- A friend sends you a link
- You get Page Not Found
- Was the address wrong, or the record gone
- Today you learn to tell the difference
Speaker notes: You have all clicked a link and hit a not found page. From the outside, every 404 looks the same. From the inside, there are two completely different 404s, and they send you to different files. By the end of today, one line of output will tell you which one you have.
Image: A phone showing a Not Found page, with two arrows leading to two different question marks.
---
## Slide 2: A route is a rule
- A URL pattern
- The methods it accepts
- One function Flask calls on a match
- The decorator registers it once, at load time
Speaker notes: Here is the idea. A route has three parts. The decorator line above your function does not call the function. It runs once, when the file loads, and writes an entry into a lookup table. The URL pattern is the key. Your function is the value. Flask searches that table for every request.
Image: A two-column lookup table: URL patterns on the left, function names on the right.
---
## Slide 3: Two rules and a trace
```python
@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    title = ISSUES.get(issue_id)
    if title is None:
        abort(404)
    return f"Issue {issue_id}: {title}"


@app.get("/issues")
def list_issues():
    status = request.args.get("status")
    if status is not None and status not in STATUSES:
        abort(400)
    return f"Listing issues, status: {status or 'any'}"
```
Speaker notes: This is routes demo, with Line 3 issues. Riverside Fabrication is a composite, an invented shop. The int converter turns the text 3 into the number 3. The second view reads the query string, the part after the question mark. A status it does not know is a bad request. The full file in your notes also prints a trace line after every request.
Image: None. This slide is code.
---
## Slide 4: Six requests
```
[trace] GET /issues/3 -> issue_detail -> 200
[trace] GET /issues/2 -> issue_detail -> 404
[trace] GET /issues/three -> None -> 404
[trace] GET /issues -> list_issues -> 200
[trace] GET /issues?status=open -> list_issues -> 200
[trace] GET /issues?status=everything -> list_issues -> 400
```
Speaker notes: Each line says the method, the path, the function that ran, and the status. Look at lines two and three. Both are 404. What does None mean on line three? It means no function ran. The converter refused the word three, no rule matched, and Flask answered by itself. On line two, your function ran and decided issue 2 does not exist.
Image: None. This slide is code.
---
## Slide 5: Two kinds of 404
- Endpoint None: no rule matched
- Open the route pattern and its converter
- Endpoint is your view: your code said no
- Open the lookup inside the view
Speaker notes: This is the habit for the rest of the unit. Before you touch any code, read the endpoint. None sends you to the decorator line. A function name sends you inside that function, to the data or the lookup. Same status code, different file.
Image: A fork in a path, one sign reading rule, the other reading view.
---
## Slide 6: The table fills before any request
```
registering rules...
done. The table now holds:
  GET  /checkouts/<int:checkout_id>     -> checkout_detail
  GET  /static/<path:filename>          -> static
  GET  /tools/<tag>                     -> tool_detail
```
Speaker notes: This is from rule table, in your notes. No request has been sent, and the table is already full. The static rule is one Flask adds for stylesheets. So your program does run top to bottom, once, to fill the table. After that, Flask calls your functions in whatever order requests arrive.
Image: None. This slide is code.
---
## Slide 7: Remove the converter
```python
@app.get("/issues/<issue_id>")
def issue_detail(issue_id):
    title = ISSUES.get(issue_id)
    if title is None:
        abort(404)
    return f"Issue {issue_id}: {title}"
```
Speaker notes: One change. I delete int and the colon. Nothing else. Predict what happens to issue 3, which definitely exists.
Image: None. This slide is code.
---
## Slide 8: Issue 3 is now missing
```
[trace] GET /issues/3 -> issue_detail -> 404
[trace] GET /issues/2 -> issue_detail -> 404
[trace] GET /issues/three -> issue_detail -> 404
[trace] GET /issues -> list_issues -> 200
[trace] GET /issues?status=open -> list_issues -> 200
[trace] GET /issues?status=everything -> list_issues -> 400
```
Speaker notes: No crash. No traceback. Issue 3 answers 404. Without the converter, issue id arrives as the text 3, and the dictionary key is the number 3. They are never equal. Now compare line three with the earlier run. The word three used to reach None. Now it reaches issue detail. Use only the trace lines to explain why.
Image: None. This slide is code.
---
## Slide 9: Why nobody notices
- The page loads, the rule matches
- No error prints anywhere
- Every URL is text
- The converter makes it a number
Speaker notes: This bug is tempting because every piece you can see works. The mismatch is a type, and types are invisible in an address bar. When a record you know exists answers 404 and the endpoint is your view, print the type of the value your view received.
Image: The characters 3 in quotes and 3 without quotes, with a not-equal sign between them.
---
## Slide 10: What you are about to build
- Lab U04-01 Part 2, steps 3 to 6
- The rule for one issue, with its converter
- The status filter from the query string
- Unknown status shows the 400 page
Speaker notes: Build 1 is Lab U04-01 Part 2. You write the rule for one issue page, then the status filter on the issue list. When you ask for status everything, your app shows the 400 page with the words Unknown status. Every Part 2 line in the self-check must say PASS before you move on.
Image: A browser showing an issue list with a filter dropdown, and a small 400 page beside it.

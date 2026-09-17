# Routes Read the Store
---
## Slide 1: The file you wrote yourself
- You wrote the JSON file
- A classmate fixed one typo by hand
- They left a stray comma
- Now every page crashes
Speaker notes: You wrote the data file. You trust it. Then someone else opens it to fix a typo and leaves one extra comma. Your app has fifteen routes that read that file. What does the person at the machine see? Today you decide that answer on purpose.
Image: A JSON file with one extra comma circled in launch red, and a broken page behind it.
---
## Slide 2: Routes ask for clean objects
- The store reads and checks the file
- It hands routes objects, never raw dictionaries
- Problems raise a StoreError
- One handler turns that into a 503 page
Speaker notes: Here is today's idea. The route never opens the file. It asks the store. The store is your Unit 3 pattern: a version number, every field typed, every reference checked, and never pickle, because loading a pickle can run hidden code. If anything is wrong, the store raises its own exception, and one handler answers for every route.
Image: A pipeline: file, store with a checklist, clean objects, route, page.
---
## Slide 3: The store, one request at a time
```python
def get_store():
    """Read the store once per request, so a change to the file shows next time."""
    if "store" not in g:
        g.store = IssueStore(app.config["STORE_PATH"])
    return g.store


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    issue = get_store().get_issue(issue_id)
    if issue is None:
        abort(404)
    return f"Issue {issue.id} on {issue.equipment}: {issue.severity}, {issue.status_label}"
```
Speaker notes: g is Flask's scratch space for one request. It starts empty every time, so every request reads the file fresh. The route asks for issue 3 and gets an Issue object back. Every value in that text was already checked against a fixed list, which is why this f-string is safe.
Image: None. This slide is code.
---
## Slide 4: One handler for every route
```python
@app.errorhandler(StoreError)
def store_unavailable(error):
    print(f"[store] {type(error).__name__}: {error}", file=sys.stderr)
    return "The maintenance log is unavailable. Tell your supervisor.", 503
```
Speaker notes: Registered once, this covers every route, including the ones you have not written yet. The details go to the server log, for you. The user gets one sentence they can act on, with status 503, which means the server is running but something it needs is not.
Image: None. This slide is code.
---
## Slide 5: Clean file, clean answers
```
200 Issue 3 on CV-01: critical, Open
404
```
Speaker notes: With the clean Line 3 file, issue 3 answers 200. Riverside Fabrication is a composite, and every record in the file is invented. Issue 99 does not exist, so the route calls abort 404. Notice Open with a capital O. The file stores lowercase open. The Issue object knows how to show its own status.
Image: None. This slide is code.
---
## Slide 6: Add one comma
- Copy the store file first
- Line 52: a second comma after 90
- Request issue 3
- Then comment out the handler and request again
Speaker notes: I keep a clean copy before I break anything. In the copy, line 52 gets a second comma after downtime minutes 90. I request issue 3 with the handler in place. Then I comment out the handler and request it again. Predict both results.
Image: A text editor showing line 52 with two commas, highlighted.
---
## Slide 7: With the handler
```
[store] StoreFormatError: Not valid JSON: Expecting property name enclosed in double quotes: line 52 column 30 (char 2221)
503 The maintenance log is unavailable. Tell your supervisor.
```
Speaker notes: The first line is the server log. It names the exception, the line, and the column. That is for you. The second line is what the user gets. A supervisor can act on that sentence without knowing anything about JSON.
Image: None. This slide is code.
---
## Slide 8: Without the handler
```
[date and time] ERROR in app: Exception on /issues/3 [GET]
Traceback (most recent call last):
...
store.StoreFormatError: Not valid JSON: Expecting property name enclosed in double quotes: line 52 column 30 (char 2221)
```
Speaker notes: Now the status is 500. The terminal prints a full traceback, and I have cut the middle. The user sees a generic Internal Server Error page. Both versions refused the bad file. Which one should a supervisor see? Which one should you see? The handler gives each person the right one.
Image: None. This slide is code.
---
## Slide 9: What else touches that file
- A person editing by hand
- A save cut off halfway
- An old backup in an old format
- Valid JSON with a negative downtime
Speaker notes: I wrote the file, so it is fine. That is the trap. Ask the Unit 3 question every time: what else can touch that file? The last bullet matters most. A negative downtime is perfectly valid JSON. Only a store that checks meaning catches it, and in the lab you write that check.
Image: Four small arrows pointing at one file icon, each labeled with a source.
---
## Slide 10: What you are about to build
- Lab U04-01 Part 4, steps 13 to 16
- The StoreError handler and its 503 page
- Two store checks: equipment and downtime
- Finish with 33 of 33 self-checks
Speaker notes: Build 1 is Lab U04-01 Part 4. You add the StoreError handler, then two checks in the store: an issue must point at real equipment, and downtime cannot be negative. The self-check must print 33 of 33, and the unit tests must report 25 tests OK. The whole lab is due at the end of today's block.
Image: A terminal line reading 33 of 33 self-checks passed, navy background.

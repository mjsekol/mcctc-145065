# Deploying Moves the Configuration, Not the Laptop
---
## Slide 1: It works on my machine
- The app runs perfectly on your laptop
- Your friend opens the link
- Every page says something went wrong
- Your laptop was never the problem
Speaker notes: Everyone has said it works on my machine. Today we find out why that sentence is so common. Your laptop has a database file, a key, and settings you set this morning. The server has none of them until you give them to it.
Image: A laptop with a green check beside a phone showing an error page, launch red.
---
## Slide 2: Same code, different everything else
- The code: the same commit
- The web server: a production WSGI server
- The database: a server, through DATABASE_URL
- The settings: the host's environment
Speaker notes: This is today's idea. A deploy runs the same code with different configuration. Flask's development server prints its own warning not to use it in production. The server side of this table, gunicorn, PostgreSQL, and the host's settings, was not run on our build machine, so treat every detail as verify until your instructor confirms this year's target.
Image: A two-column comparison card, laptop on the left and server on the right, with the code row highlighted.
---
## Slide 3: Rehearse it first
```
$env:APP_ENV = "production"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:DATABASE_PATH = "$env:TEMP\line3_rehearsal.db"
python manage.py init --db $env:DATABASE_PATH
python serve_local.py --port 8688
```
Speaker notes: Before the real deploy, start the app on your own machine the way the server will. Production settings, a real random key, a database in your temp folder, never in a repository. serve_local.py uses Python's standard library, so it needs no new package. It is a reference server, fine on your own machine, not for the internet. Use the port your lab handout names.
Image: None. This slide is code.
---
## Slide 4: What the rehearsal printed
```
Production-style server on http://127.0.0.1:8688  (APP_ENV=production, debug=False). Ctrl+C stops it.
[date and time] INFO line3: GET /health -> health 200 (1.0 ms)
[date and time] INFO line3: GET / -> dashboard 200 (14.2 ms)
[date and time] INFO line3: GET /issues/abc -> None 404 (2.0 ms)
[date and time] INFO line3: GET /trace -> None 404 (0.2 ms)
```
```
{"database":"ok","status":"ok","version":"1.0.0"}
```
Speaker notes: Production, debug false. Health answered two hundred and the JSON underneath. A bad issue address got the site's own not found page. And trace is gone, as it should be. The date and time on each line are masked here. This is the check list in miniature.
Image: None. This slide is code.
---
## Slide 5: init-if-empty is the only safe build step
- init: builds a new database, refuses an existing one
- init --force: deletes every record, every deploy
- init-if-empty: builds once, then changes nothing
- Build command: install requirements, then init-if-empty
Speaker notes: The build command runs on every deploy. Put init force in it, and every record the shop entered is gone each time you deploy, while the log cheerfully says created the tables. Put init-if-empty in it, and the first deploy builds the tables, and every deploy after prints already has tables, nothing changed. The exact build command for this year's host is verify.
Image: Three buttons labeled init, init --force, and init-if-empty, with the force button outlined in launch red.
---
## Slide 6: SQLite now, PostgreSQL on the server
- Placeholders: ? becomes %s [VERIFY]
- Ids: GENERATED ALWAYS AS IDENTITY [VERIFY]
- Foreign keys: always enforced [VERIFY]
- LIKE: case-sensitive, so the lab lowers both sides [VERIFY]
- Location: a separate server through DATABASE_URL [VERIFY]
Speaker notes: Every cell on the PostgreSQL side is marked verify, because PostgreSQL was not installed where these materials were built. The lab's POSTGRES.md lists eighteen differences. These five come first. Because every query lives in db.py, the switch touches one file. Remember Monday of last week: SQLite accepted orphans all week, and PostgreSQL will not.
Image: Two database cylinders labeled SQLite and PostgreSQL with five connecting lines, one per difference.
---
## Slide 7: Point it at an empty database
```
python -c "import sqlite3; sqlite3.connect(r'$env:TEMP\line3_empty.db').close()"
$env:DATABASE_PATH = "$env:TEMP\line3_empty.db"
```
```
503 /health {"database":"unavailable","status":"error","version":"1.0.0"}
500 /
```
Speaker notes: This is what a live app sees when the build skipped init-if-empty. The file exists and has no tables. Health answers five oh three, and the home page answers five hundred. The page says something went wrong on our side, with no traceback. Where is the traceback? Read the terminal.
Image: None. This slide is code.
---
## Slide 8: The terminal has the answer
```
[date and time] ERROR app: health check: database unavailable
Traceback (most recent call last):
  ...
sqlite3.OperationalError: no such table: equipment
[date and time] INFO line3: GET /health -> health 503 (4.0 ms)
[date and time] ERROR app: Exception on / [GET]
Traceback (most recent call last):
  ...
sqlite3.OperationalError: no such table: issues
[date and time] INFO line3: GET / -> dashboard 500 (6.7 ms)
```
Speaker notes: The dots replace the frames in the middle of each traceback. No such table. The app did everything right. The visitor saw nothing internal, and the health check told the truth. The configuration was wrong. On a real host this lives in the host's log, and where that log is shown is verify for this year's host. In your starter, health still says ok on this empty file. That is the bug you fix in Part 3.
Image: None. This slide is code.
---
## Slide 9: Prove it with a checklist
- /health answers ok with the version
- Create, edit, and delete a record live
- Cookies marked Secure and HttpOnly
- /trace answers 404, bad addresses show your 404 page
- Tick each item from a real check
Speaker notes: DEPLOY.md ends with a check list, and every tick has to come from something you actually did on the live app, not from memory. If a page fails, read the log. Then finish your data dictionary in Build 2, because tomorrow's tester reads it.
Image: A clipboard with five checked boxes, navy and launch blue.
---
## Slide 10: What you are about to build
- Lab U05-02, Part 3: steps 13 through 18
- Make the health check tell the truth
- Run the rehearsal and write this year's deploy steps
- Write DEPLOY_NOTES.md, with no secret values
- Target: 99 of 101 self-checks pass
Speaker notes: Part 3 fixes the health check so an empty database answers five oh three. Then you rehearse, and the rehearsal must answer health with status ok and version one point oh point oh. You write the deploy steps for the target on the board, and DEPLOY_NOTES.md names the target and every environment variable, with no values for secrets. In Build 2 you deploy your tool crib and write DEPLOY.md and DATA_DICTIONARY.md.
Image: A browser tab showing a JSON health answer with status ok, navy background.

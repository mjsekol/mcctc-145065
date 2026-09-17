# One request, start to finish · stage w07_routes

Riverside Fabrication is a composite: an invented shop with invented records.

**Why trace one request.** Every Flask bug you meet in Weeks 7-10 lives at one of the steps
below. If you can name the step, you know which file to open. A blank page, a 404 you did not
expect, and a value that shows up as `&lt;` are three different steps, not one mystery.

The request traced here is `GET /issues/3`, sent by `save_pages.py` to `python app.py --port 8650`.

## The steps

| Step | Where it happens | What happens for `GET /issues/3` |
|---|---|---|
| 1. The browser builds a request | the browser | Method `GET`, path `/issues/3`, headers such as `Host: 127.0.0.1:8650` and `Accept` |
| 2. The server receives it | Werkzeug, inside `app.run()` | Reads the bytes from the socket and builds a `request` object |
| 3. Flask matches the path to a rule | the URL map built from every `@app.get(...)` | `/issues/<int:issue_id>` matches. The `int` converter turns `"3"` into `3`. `/issues/three` would not match anything, so it is a 404 before your code runs |
| 4. Hooks run before the view | `@app.before_request` | `start_timer()` records the time in `g` |
| 5. The view function runs | `issue_detail(issue_id=3)` | Asks `get_store()` for the data. The store reads and validates `data/line3_log.json`, then returns an `Issue` object |
| 6. The view decides the answer | `issue_detail` | Issue 3 exists, so it renders. A missing issue calls `abort(404)` and jumps to the 404 handler |
| 7. The template builds HTML | `templates/issue_detail.html`, which extends `base.html` | Jinja fills the blocks. Every `{{ value }}` is escaped |
| 8. Hooks run after the view | `@app.after_request` | `log_request()` prints the trace line below |
| 9. The response goes back | Werkzeug | Status `200`, `Content-Type: text/html; charset=utf-8`, the HTML body |
| 10. The browser renders it | the browser | Then it requests `/static/line3.css`, which is a second, separate request |

## What the server printed

A real run of `python app.py --port 8650` while `python save_pages.py --port 8650` fetched each
page. The `[trace]` line is from `log_request()`. The line after it is Werkzeug's own log.

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8650
Press CTRL+C to quit
[trace] GET / -> dashboard -> 200 text/html (2971 bytes, 6.9 ms)
127.0.0.1 - - [date and time] "GET / HTTP/1.1" 200 -
[trace] GET /issues -> list_issues -> 200 text/html (3636 bytes, 3.0 ms)
127.0.0.1 - - [date and time] "GET /issues HTTP/1.1" 200 -
[trace] GET /issues?status=closed -> list_issues -> 200 text/html (2359 bytes, 0.5 ms)
127.0.0.1 - - [date and time] "GET /issues?status=closed HTTP/1.1" 200 -
[trace] GET /issues/3 -> issue_detail -> 200 text/html (1701 bytes, 2.2 ms)
127.0.0.1 - - [date and time] "GET /issues/3 HTTP/1.1" 200 -
[trace] GET /equipment -> list_equipment -> 200 text/html (2387 bytes, 1.7 ms)
127.0.0.1 - - [date and time] "GET /equipment HTTP/1.1" 200 -
[trace] GET /equipment/OV-01 -> equipment_detail -> 200 text/html (2168 bytes, 1.9 ms)
127.0.0.1 - - [date and time] "GET /equipment/OV-01 HTTP/1.1" 200 -
[trace] GET /trace?machine=PB-01 -> trace -> 200 text/html (1733 bytes, 1.9 ms)
127.0.0.1 - - [date and time] "GET /trace?machine=PB-01 HTTP/1.1" 200 -
[trace] GET /issues?status=everything -> list_issues -> 400 text/html (1247 bytes, 1.1 ms)
127.0.0.1 - - [date and time] "GET /issues?status=everything HTTP/1.1" 400 -
[trace] GET /issues/999 -> issue_detail -> 404 text/html (1196 bytes, 0.4 ms)
127.0.0.1 - - [date and time] "GET /issues/999 HTTP/1.1" 404 -
```

Werkzeug prints the date and time of each request where this copy shows `[date and time]`. It was masked here because the course carries no calendar dates. Nothing else was changed.

Read the two failures closely. `status=everything` reached `list_issues`, which refused it with
400: the rule matched, and your code said no. `/issues/999` also reached `issue_detail`, which
found nothing and answered 404. Compare `/issues/three`: that never reaches `issue_detail` at all.
No rule matched, so the trace line shows the endpoint as `None`. This line came from a separate
run through Flask's test client:

```
[trace] GET /issues/three -> None -> 404 text/html (1196 bytes, 3.8 ms)
```

## Where each kind of bug lives

| What you see | Step | Look in |
|---|---|---|
| 404 for a page you wrote | 3 | the rule text and its converter in `@app.get(...)` |
| 405 Method Not Allowed | 3 | the methods the rule accepts |
| 500 and a traceback in the terminal | 5 to 7 | the view, the store, or a template variable |
| 503 "maintenance log is unavailable" | 5 | the JSON file: `store.py` names the broken record in the terminal |
| Text shows as `&lt;b&gt;` | 7 | working as designed: escaping stopped HTML from running |
| The page has no styling | 10 | the stylesheet request, not the page request |

## See it yourself

Open `/trace` in the browser. It shows the method, path, matched rule, function, query
arguments, and three request headers for the request that built that page. Add `?machine=PB-01`
to the address and reload.

The `/trace` page exists for teaching. The Week 10 stage removes it: a live application does not
describe its requests to strangers.

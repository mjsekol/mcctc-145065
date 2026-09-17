"""
save_pages.py · save every page this stage serves, so web-check can read them

Why this exists: tools/web-check reads files, and Flask builds each page on
every request. This asks your running server for each page, including every
page a form produces, saves the HTML the server sent, points the /static/
links at a local copy, and copies static/.

This script creates, edits, and deletes records. Run the server against a
throwaway database, never the one you care about:

    python manage.py init --db %TEMP%\\line3_pages.db
    set DATABASE_PATH=%TEMP%\\line3_pages.db
    python app.py --port 8680

Then, in another terminal:

    python save_pages.py --port 8680

Then, from the repository root:

    node tools/web-check/check.js <path to this folder>/saved/*.html

Standard library only. A cookie jar keeps one session, so the form token works.
"""

import argparse
import http.cookiejar
import pathlib
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')

NEW_ISSUE = {
    "reported_by": "T-1057",
    "equipment": "LC-01",
    "title": "Chiller alarm on start-up",
    "description": "The chiller shows a low-flow alarm for two minutes after start, then clears.",
    "severity": "medium",
    "downtime_minutes": "10",
}
BAD_ISSUE = dict(NEW_ISSUE, reported_by="T-10", title="abc", severity="critical",
                 downtime_minutes="2000")
EDIT = {
    "equipment": "PB-01",
    "title": "Back gauge drifts 2 mm after warm-up",
    "description": "Parts from the second hour measure long. Re-zeroing fixes it for forty minutes.",
    "severity": "medium",
    "status": "in_progress",
    "downtime_minutes": "25",
}


class Browser:
    """One cookie jar. urllib follows a 303 redirect with a GET, as a browser does."""

    def __init__(self, base):
        self.base = base
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def request(self, path, data=None):
        body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
        try:
            with self.opener.open(self.base + path, data=body, timeout=5) as response:
                return response.status, response.geturl(), response.read()
        except urllib.error.HTTPError as error:
            payload = error.read()
            error.close()
            return error.code, self.base + path, payload

    def post(self, path, data):
        _, _, form = self.request("/issues/new")
        token = TOKEN.search(form.decode("utf-8")).group(1)
        return self.request(path, dict(data, csrf_token=token))


def main():
    parser = argparse.ArgumentParser(description="Save every page for web-check")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--out", default=str(HERE / "saved"))
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    browser = Browser(f"http://127.0.0.1:{args.port}")
    try:
        browser.request("/")
    except urllib.error.URLError as error:
        print(f"Could not reach port {args.port}. Is app.py running? ({error.reason})")
        return 1

    def save(name, status, url, body):
        html = body.decode("utf-8").replace('"/static/', '"static/')
        (out / name).write_text(html, encoding="utf-8", newline="\n")
        print(f"{status} {url.replace(browser.base, '')} -> {name}")

    for name, path in [
        ("dashboard.html", "/"),
        ("issues.html", "/issues"),
        ("issues-filtered.html", "/issues?q=guard&status=open&equipment=CV-01"),
        ("issues-no-match.html", "/issues?q=%27+OR+%271%27%3D%271"),
        ("issue-form.html", "/issues/new"),
        ("issue-detail.html", "/issues/3"),
        ("issue-edit.html", "/issues/1/edit"),
        ("issue-delete-confirm.html", "/issues/3/delete"),
        ("equipment.html", "/equipment"),
        ("equipment-detail.html", "/equipment/OV-01"),
        ("reports.html", "/reports"),
        ("trace.html", "/trace?machine=PB-01"),
        ("error-400.html", "/issues?status=everything"),
        ("error-404.html", "/issues/999"),
    ]:
        save(name, *browser.request(path))

    save("issue-form-errors.html", *browser.post("/issues/new", BAD_ISSUE))
    save("issue-created.html", *browser.post("/issues/new", NEW_ISSUE))
    save("issue-edit-errors.html", *browser.post("/issues/1/edit", dict(EDIT, severity="critical",
                                                                        downtime_minutes="-3")))
    save("issue-updated.html", *browser.post("/issues/1/edit", EDIT))
    save("note-errors.html", *browser.post("/issues/1/notes",
                                           {"badge": "X-1", "note": "ok", "minutes_spent": "0"}))
    save("note-added.html", *browser.post("/issues/1/notes",
                                          {"badge": "T-1041", "note": "Re-zeroed the back gauge.",
                                           "minutes_spent": "15"}))
    save("issue-deleted.html", *browser.post("/issues/6/delete", {}))
    save("error-403.html", *browser.request("/issues/1/delete", {}))
    # The token check runs before Flask looks at the method, so send a token to reach the 405.
    save("error-405.html", *browser.post("/reports", {}))

    shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

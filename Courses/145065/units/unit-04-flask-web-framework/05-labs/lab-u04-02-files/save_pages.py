"""
save_pages.py · save every page this stage serves, so web-check can read them

Why this exists: tools/web-check reads files, and Flask builds each page on
every request. This asks your running server for each page, including the
pages a form produces, saves the HTML the server sent, points the /static/
links at a local copy, and copies static/.

This script SUBMITS the form, so run the server against a copy of the store:

    $env:STORE_PATH = "$env:TEMP\\line3_copy.json"   (after copying data\\line3_log.json there)
    python app.py --port 8651

Then, in another terminal:

    python save_pages.py --port 8651

Then, from the repository root:

    node tools/web-check/check.js Courses/145065/anchor-project/crud-app/w08_forms/saved/*.html

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

GOOD = {
    "reported_by": "T-1057",
    "equipment": "LC-01",
    "title": "Chiller alarm on start-up",
    "description": "The chiller shows a low-flow alarm for two minutes after start, then clears.",
    "severity": "medium",
    "downtime_minutes": "10",
}
BAD = {
    "reported_by": "T-10",
    "equipment": "LC-01",
    "title": "abc",
    "description": "The chiller shows a low-flow alarm for two minutes after start, then clears.",
    "severity": "critical",
    "downtime_minutes": "2000",
}


class Browser:
    """The parts of a browser this needs: one cookie jar, and redirects followed like a browser."""

    def __init__(self, base):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(self.jar))

    def request(self, path, data=None):
        body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
        try:
            with self.opener.open(self.base + path, data=body, timeout=5) as response:
                return response.status, response.geturl(), response.read()
        except urllib.error.HTTPError as error:
            payload = error.read()
            error.close()
            return error.code, self.base + path, payload

    def token(self):
        _, _, body = self.request("/issues/new")
        return TOKEN.search(body.decode("utf-8")).group(1)


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
        ("issue-form.html", "/issues/new"),
        ("issue-detail.html", "/issues/3"),
        ("equipment.html", "/equipment"),
        ("equipment-detail.html", "/equipment/OV-01"),
        ("trace.html", "/trace?machine=PB-01"),
        ("error-400.html", "/issues?status=everything"),
        ("error-404.html", "/issues/999"),
    ]:
        save(name, *browser.request(path))

    # A refused form: four problems at once.
    save("issue-form-errors.html", *browser.request("/issues/new", dict(BAD, csrf_token=browser.token())))
    # A good form: urllib follows the 303 to the new issue, which shows the confirmation.
    save("issue-created.html", *browser.request("/issues/new", dict(GOOD, csrf_token=browser.token())))
    # A forged form with no token.
    save("error-403.html", *browser.request("/issues/new", GOOD))

    shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

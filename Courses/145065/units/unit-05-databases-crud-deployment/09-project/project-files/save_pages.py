r"""
save_pages.py · save the pages your running app serves, so web-check can read them

Adapted for the Unit 5 project, Tool Crib Live, from the Unit 4 project's
save_pages.py and anchor-project/crud-app/w10_deploy/save_pages.py. Copy it
into your toolcrib-web folder.

Why this exists: tools/web-check reads files, and Flask builds each page on
every request. This script asks your running server for each page, saves the
HTML exactly as the server sent it, points the /static/ links at a local copy,
and copies your static/ folder next to the saved pages.

WHAT YOU EDIT
  PAGES        one line per GET page: (file name, path). Include a 400 and a 404.
  FORM_STEPS   one line per form the script sends: (file name, path, answers, token?).
               These are the pages a form produces: a refused form, the page
               after a save, an edit, a return, a void, and a 403.
  TOKEN_PAGE   a page that has a form on it, so the script can read your token.
The defaults use the routes the project spec suggests. Change them to yours.

{new} in a FORM_STEPS path is replaced by the checkout number of the last
form that redirected to an address ending in a number, so the edit, return,
and void steps act on the checkout the script created.

THE FORM STEPS CHANGE YOUR DATABASE. Run the server against a throwaway
database, never the one you care about. Rebuild it before a second run,
or the "created" step is refused because the tool is already out.

How to run it. Start your app in one terminal, stating the port. For the
production-style rehearsal (PowerShell):

    $env:APP_ENV = "production"
    $env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
    $env:DATABASE_PATH = "$env:TEMP\toolcrib_pages.db"
    python manage.py init --db $env:DATABASE_PATH --force
    python serve_local.py --port 8680

Then, in a second terminal, from your toolcrib-web folder:

    python save_pages.py --port 8680

To save pages somewhere other than saved/, add --out <folder>.

To save one page by itself, name it with --page FILE PATH. This skips the
PAGES list and the form steps for that run. Repeat --page for more pages.
The 500 page is saved this way: start serve_local.py again with
DATABASE_PATH pointing at a file that has no tables, then

    python save_pages.py --port 8680 --page error-500.html /

Then, from the course repository root:

    node tools/web-check/check.js <path to your toolcrib-web folder>/saved/*.html

Only point this at your own server on 127.0.0.1. Standard library only.
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
NUMBER_AT_END = re.compile(r"/(\d+)$")

# EDIT THIS LIST for your routes: (file name to save as, path to ask for).
PAGES = [
    ("dashboard.html", "/"),
    ("tools.html", "/tools"),
    ("tool-detail.html", "/tools/TC-101"),
    ("checkouts.html", "/checkouts"),
    ("checkouts-search.html", "/checkouts?q=latch"),
    ("checkout-detail.html", "/checkouts/2"),
    ("checkout-form.html", "/checkouts/new"),
    ("checkout-edit.html", "/checkouts/2/edit"),
    ("checkout-void-confirm.html", "/checkouts/2/void"),
    ("reports.html", "/reports"),
    ("error-400.html", "/checkouts?status=everything"),
    ("error-404.html", "/tools/TC-999"),
]

# EDIT THIS: a GET page whose form carries your CSRF token.
TOKEN_PAGE = "/checkouts/new"

# EDIT THIS LIST for your forms: (file name, path, answers, send the token?).
# Use invented records from your own seed data. Never type real information.
NEW_CHECKOUT = {"badge": "T-1057", "tool": "TC-201", "hours": "8", "note": "Case hinge is stiff"}
FORM_STEPS = [
    ("checkout-form-errors.html", "/checkouts/new",
     {"badge": "T-9999", "tool": "", "hours": "96", "note": ""}, True),
    ("checkout-created.html", "/checkouts/new", NEW_CHECKOUT, True),
    ("checkout-edit-errors.html", "/checkouts/{new}/edit", {"hours": "96", "note": ""}, True),
    ("checkout-updated.html", "/checkouts/{new}/edit", {"hours": "10", "note": "Hinge oiled"}, True),
    ("return-errors.html", "/checkouts/{new}/return", {}, True),
    ("checkout-returned.html", "/checkouts/{new}/return", {"condition": "good"}, True),
    ("checkout-voided.html", "/checkouts/{new}/void", {}, True),
    # No token: another site's forged form. Your app should answer 403.
    ("error-403.html", "/checkouts/new", NEW_CHECKOUT, False),
]


class Browser:
    """The parts of a browser this needs: one cookie jar, and redirects followed like a browser."""

    def __init__(self, base):
        self.base = base
        self.jar = http.cookiejar.CookieJar()
        # ProxyHandler({}) keeps requests to 127.0.0.1 away from any proxy setting.
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(self.jar))

    def request(self, path, data=None):
        """GET when data is None, otherwise a form POST. Returns (status, final URL, body bytes)."""
        body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
        try:
            with self.opener.open(self.base + path, data=body, timeout=10) as response:
                return response.status, response.geturl(), response.read()
        except urllib.error.HTTPError as error:
            # 400, 403, 404, 500: the server still sent a page, and that page is what we save.
            payload = error.read()
            error.close()
            return error.code, self.base + path, payload

    def token(self):
        """Load TOKEN_PAGE and read this session's CSRF token from it."""
        _, _, body = self.request(TOKEN_PAGE)
        match = TOKEN.search(body.decode("utf-8"))
        if match is None:
            raise SystemExit(f"No csrf_token field on {TOKEN_PAGE}. Check TOKEN_PAGE.")
        return match.group(1)


def save(out, browser, name, status, url, body):
    html = body.decode("utf-8").replace('"/static/', '"static/')
    (out / name).write_text(html, encoding="utf-8", newline="\n")
    print(f"{status} {url.replace(browser.base, '')} -> {name}")


def run_form_steps(out, browser):
    new = None
    for name, path, answers, send_token in FORM_STEPS:
        if "{new}" in path:
            if new is None:
                print(f"Skipped {name}: no earlier step created a record, so {{new}} has no value.")
                continue
            path = path.replace("{new}", new)
        data = dict(answers)
        if send_token:
            data["csrf_token"] = browser.token()
        status, url, body = browser.request(path, data)
        save(out, browser, name, status, url, body)
        match = NUMBER_AT_END.search(urllib.parse.urlsplit(url).path)
        if match:
            new = match.group(1)


def main():
    parser = argparse.ArgumentParser(description="Save the pages your app serves, for web-check")
    parser.add_argument("--port", type=int, required=True, help="the port your app is running on")
    parser.add_argument("--out", default=str(HERE / "saved"), help="folder for the saved pages")
    parser.add_argument("--page", nargs=2, action="append", metavar=("FILE", "PATH"),
                        help="save only this page and skip the form steps; repeat for more")
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    browser = Browser(f"http://127.0.0.1:{args.port}")
    try:
        browser.request("/")
    except urllib.error.URLError as error:
        print(f"Could not reach port {args.port}. Is your app running? ({error.reason})")
        return 1

    for name, path in args.page or PAGES:
        save(out, browser, name, *browser.request(path))
    if not args.page:
        run_form_steps(out, browser)

    # The saved pages link to static/..., so a copy of your stylesheet goes with them.
    if (HERE / "static").is_dir():
        shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

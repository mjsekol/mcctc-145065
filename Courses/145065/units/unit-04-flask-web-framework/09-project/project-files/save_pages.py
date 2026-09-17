"""
save_pages.py · save the pages your running app serves, so web-check can read them

Adapted from anchor-project/crud-app/w08_forms/save_pages.py for the Unit 4
project, Tool Crib on the Web. Copy it into your toolcrib-web folder.

Why this exists: tools/web-check reads files, and Flask builds each page on
every request. This script asks your running server for each page in PAGES,
saves the HTML exactly as the server sent it, points the /static/ links at a
local copy, and copies your static/ folder next to the saved pages.

What you edit: the PAGES list below. One line per page, (file name, path).
Include your error pages too: a 400 and a 404 are ordinary requests with a bad
value. A page that answers with an error status is still saved, and the status
is printed so you can check it is the one you meant.

How to run it. Start your app in one terminal, stating the port:

    python app.py --port 8680

Then, in a second terminal, from your toolcrib-web folder:

    python save_pages.py --port 8680

To save one page by itself, for example the 503 page from a second server
pointed at a broken copy of your store, name it on the command line. This
replaces the PAGES list for that run:

    python save_pages.py --port 8681 --page error-503.html /

Then, from the course repository root:

    node tools/web-check/check.js <path to your toolcrib-web folder>/saved/*.html

Pages a form produces (the refused form, the page after a good checkout, the
403 page) need a POST with your CSRF token. This script sends GET requests only.
Adding those steps is your edit to make, and the Browser class below keeps
one session in a cookie jar so a token from one request works in the next.

Only point this at your own server on 127.0.0.1. Standard library only.
"""

import argparse
import http.cookiejar
import pathlib
import shutil
import urllib.error
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent

# EDIT THIS LIST for your routes: (file name to save as, path to ask for).
PAGES = [
    ("dashboard.html", "/"),
    ("tools.html", "/tools"),
    ("tools-filtered.html", "/tools?category=Measuring"),
    ("tool-detail.html", "/tools/TC-101"),
    ("checkouts.html", "/checkouts"),
    ("checkouts-filtered.html", "/checkouts?status=late"),
    ("checkout-detail.html", "/checkouts/1"),
    ("checkout-form.html", "/checkouts/new"),
    ("error-400.html", "/checkouts?status=everything"),
    ("error-404.html", "/tools/TC-999"),
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
            with self.opener.open(self.base + path, data=body, timeout=5) as response:
                return response.status, response.geturl(), response.read()
        except urllib.error.HTTPError as error:
            # 400, 403, 404, 503: the server still sent a page, and that page is what we save.
            payload = error.read()
            error.close()
            return error.code, self.base + path, payload


def save(out, browser, name, status, url, body):
    html = body.decode("utf-8").replace('"/static/', '"static/')
    (out / name).write_text(html, encoding="utf-8", newline="\n")
    print(f"{status} {url.replace(browser.base, '')} -> {name}")


def main():
    parser = argparse.ArgumentParser(description="Save the pages your app serves, for web-check")
    parser.add_argument("--port", type=int, required=True, help="the port your app is running on")
    parser.add_argument("--out", default=str(HERE / "saved"), help="folder for the saved pages")
    parser.add_argument("--page", nargs=2, action="append", metavar=("FILE", "PATH"),
                        help="save only this page; repeat for more")
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    browser = Browser(f"http://127.0.0.1:{args.port}")
    try:
        browser.request("/")
    except urllib.error.URLError as error:
        print(f"Could not reach port {args.port}. Is app.py running? ({error.reason})")
        return 1

    for name, path in args.page or PAGES:
        save(out, browser, name, *browser.request(path))

    # The saved pages link to static/..., so a copy of your stylesheet goes with them.
    if (HERE / "static").is_dir():
        shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

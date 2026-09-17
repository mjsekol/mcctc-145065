"""
save_pages.py · save every page this stage serves, so web-check can read them

Why this exists: tools/web-check reads files, and Flask builds each page on
every request. This asks your running server for each page, saves the HTML the
server sent, points the /static/ links at a local copy, and copies static/.

Start the server in one terminal, then in another:

    python save_pages.py --port 8680

Then run web-check on the saved folder. From the course repository root:

    node tools/web-check/check.js <path to this folder>/saved/*.html

Standard library only. The same pattern as 145010 Unit 5's save_page.py.
"""

import argparse
import pathlib
import shutil
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent

# (saved file name, path on the server)
PAGES = [
    ("dashboard.html", "/"),
    ("issues.html", "/issues"),
    ("issues-closed.html", "/issues?status=closed"),
    ("issue-detail.html", "/issues/3"),
    ("equipment.html", "/equipment"),
    ("equipment-detail.html", "/equipment/OV-01"),
    ("trace.html", "/trace?machine=PB-01"),
    ("error-400.html", "/issues?status=everything"),
    ("error-404.html", "/issues/999"),
]


def fetch(opener, url):
    try:
        with opener.open(url, timeout=5) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        # An error page is still a page worth checking.
        body = error.read()
        error.close()
        return error.code, body


def main():
    parser = argparse.ArgumentParser(description="Save every page for web-check")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--out", default=str(HERE / "saved"))
    args = parser.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    base = f"http://127.0.0.1:{args.port}"
    for name, path in PAGES:
        try:
            status, body = fetch(opener, base + path)
        except urllib.error.URLError as error:
            print(f"Could not reach {base}. Is app.py running on port {args.port}? ({error.reason})")
            return 1
        html = body.decode("utf-8").replace('"/static/', '"static/')
        (out / name).write_text(html, encoding="utf-8", newline="\n")
        print(f"{status} {path} -> {name}")
    shutil.copytree(HERE / "static", out / "static", dirs_exist_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

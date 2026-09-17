"""
attack_demo.py · send real attacks at a running w08 server and report what happened

Every attack here is one a Gate 2 or a real attacker would try. Each one is
expected to fail. The script prints PASS when the server defended itself and
FAIL when it did not. ATTACKS.md records a real run and explains each result.

Run the server against a copy of the store (the script saves one issue), then:

    python attack_demo.py --port 8651

Only ever point this at your own server on 127.0.0.1.
Standard library only.
"""

import argparse
import http.cookiejar
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')
NEW_ID = re.compile(r"/issues/(\d+)$")

GOOD = {
    "reported_by": "T-1062",
    "equipment": "WR-01",
    "title": "Torch cable jacket worn",
    "description": "The jacket is worn through near the wrist joint. No bare wire is visible yet.",
    "severity": "medium",
    "downtime_minutes": "0",
}


class Browser:
    def __init__(self, base):
        self.base = base
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def request(self, path, data=None):
        body = urllib.parse.urlencode(data).encode("utf-8") if data is not None else None
        try:
            with self.opener.open(self.base + path, data=body, timeout=5) as response:
                return response.status, response.geturl(), response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            text = error.read().decode("utf-8")
            error.close()
            return error.code, self.base + path, text

    def token(self):
        return TOKEN.search(self.request("/issues/new")[2]).group(1)


results = []


def report(name, ok, detail):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"      {detail}")


def main():
    parser = argparse.ArgumentParser(description="Attack your own w08 server")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    you = Browser(base)
    try:
        you.request("/")
    except urllib.error.URLError as error:
        print(f"Could not reach {base}. Is app.py running? ({error.reason})")
        return 1

    # 1. Cross-site request forgery: another site's hidden form posts here.
    #    It cannot read your token, so it sends none.
    status, _, _ = you.request("/issues/new", GOOD)
    report("1. Forged POST with no token", status == 403, f"server answered {status}")

    # 2. A token from someone else's session.
    attacker = Browser(base)
    stolen = attacker.token()
    you.token()
    status, _, _ = you.request("/issues/new", dict(GOOD, csrf_token=stolen))
    report("2. POST carrying another session's token", status == 403, f"server answered {status}")

    # 3. Stored cross-site scripting: a script in the title, saved for every
    #    supervisor who opens the log. The save is allowed. The script must never run.
    attack = "<script>document.title='owned'</script>"
    status, url, _ = you.request("/issues/new", dict(GOOD, title=attack, csrf_token=you.token()))
    match = NEW_ID.search(url)
    if status == 200 and match:
        _, _, page = you.request(f"/issues/{match.group(1)}")
        raw_present = attack in page
        escaped = "&lt;script&gt;document.title=&#39;owned&#39;&lt;/script&gt;" in page
        report("3. Stored script in a title", escaped and not raw_present,
               f"saved as issue {match.group(1)}; raw tag in page: {raw_present}; "
               f"escaped text in page: {escaped}")
    else:
        report("3. Stored script in a title", False, f"unexpected answer {status} at {url}")

    # 4. Breaking out of an attribute: the badge is echoed into value="...".
    attack = '"><img src=x onerror=alert(1)>'
    status, _, page = you.request("/issues/new", dict(GOOD, reported_by=attack, csrf_token=you.token()))
    report("4. Attribute breakout in the badge field",
           status == 400 and "<img src=x" not in page and "&#34;&gt;&lt;img" in page,
           f"server answered {status}; raw tag in page: {'<img src=x' in page}")

    # 5. A value the drop-down never offered, shaped like SQL injection.
    status, _, page = you.request("/issues/new",
                                  dict(GOOD, equipment="PB-01' OR '1'='1", csrf_token=you.token()))
    report("5. Tampered machine code", status == 400 and "Choose a machine from the list." in page,
           f"server answered {status}")

    # 6. Skipping the browser's checks: values the form's hints would block.
    status, _, page = you.request("/issues/new", dict(
        GOOD, title="x" * 500, downtime_minutes="-500", severity="apocalyptic",
        csrf_token=you.token()))
    report("6. Values the browser hints would have blocked", status == 400 and "There are 3 problems" in page,
           f"server answered {status}")

    print(f"\n{results.count(True)} of {len(results)} attacks failed as they should.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

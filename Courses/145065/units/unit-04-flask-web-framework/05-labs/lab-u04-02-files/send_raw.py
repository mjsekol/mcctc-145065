"""
send_raw.py · Lab U04-02 · send a form the way no browser would

Your form has required, minlength, maxlength, pattern, min, and max. Those
hints stop an honest person in a browser. This script is not a browser. It
loads the form once (to get a session and its token, if the page has one),
then posts whatever is in RAW below, straight to your server.

Start your app in one terminal, then in another:

    python send_raw.py --port 8680
    python send_raw.py --port 8680 --title "<b>Bold</b> title"

Only ever point this at your own server on 127.0.0.1.
Standard library only.
"""

import argparse
import html
import http.cookiejar
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# The badge and machine are real. Every other value breaks a rule the browser
# would have enforced.
RAW = {
    "reported_by": "T-1041",
    "equipment": "PB-01",
    "title": "abc",                    # minlength is 5
    "description": "Too short",        # minlength is 10
    "severity": "apocalyptic",         # not one of the radio buttons
    "downtime_minutes": "-500",        # min is 0
}

# With --title, every other field is valid, so only the title is being tested.
VALID_EXCEPT_TITLE = {
    "reported_by": "T-1041",
    "equipment": "PB-01",
    "description": "Sent by send_raw.py to test how a title is shown.",
    "severity": "low",
    "downtime_minutes": "0",
}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Report a redirect instead of following it, so you see the 303 itself."""

    def redirect_request(self, *args, **kwargs):
        return None


TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')
FIELD_ERROR = re.compile(
    r'<p class="field-error"[^>]*><span class="visually-hidden">Error: </span>(.*?)</p>')


def main():
    parser = argparse.ArgumentParser(description="Post raw form values to your own server")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--title", help="send this title, with every other field valid")
    args = parser.parse_args()

    base = f"http://127.0.0.1:{args.port}"
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), NoRedirect(),
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        with opener.open(base + "/issues/new", timeout=5) as page:
            form_html = page.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        print(f"The form page itself answered {error.code}. Open {base}/ in a browser and read "
              f"your server's terminal before sending anything.")
        error.close()
        return 1
    except urllib.error.URLError as error:
        print(f"Could not reach {base}. Is your app running on port {args.port}? ({error.reason})")
        return 1

    data = dict(RAW) if args.title is None else dict(VALID_EXCEPT_TITLE, title=args.title)
    found = TOKEN.search(form_html)
    if found:
        data["csrf_token"] = found.group(1)
    print(f"Sending {len(data)} fields to /issues/new, "
          f"token {'included' if found else 'not found in the form'}")

    body = urllib.parse.urlencode(data).encode("utf-8")
    location = None
    try:
        with opener.open(base + "/issues/new", data=body, timeout=5) as answer:
            status, text = answer.status, answer.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status, text = error.code, error.read().decode("utf-8")
        location = error.headers.get("Location")
        error.close()

    print(f"Server answered {status}")
    if location:
        print(f"It redirected to {location}. The issue was SAVED.")
    messages = FIELD_ERROR.findall(text)
    for message in messages:
        print(f"  refused: {html.unescape(message)}")
    if status == 200 and not messages:
        print("A page came back with no redirect and no error messages. Read your create_issue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

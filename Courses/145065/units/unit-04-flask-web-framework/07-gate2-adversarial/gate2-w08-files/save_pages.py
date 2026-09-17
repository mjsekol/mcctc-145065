import argparse, http.cookiejar, pathlib, re, shutil, urllib.error, urllib.parse, urllib.request
HERE = pathlib.Path(__file__).parent
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--out", default=str(HERE/"saved")); a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    base = f"http://127.0.0.1:{a.port}"
    def save(name, path, data=None):
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        try:
            with op.open(base+path, data=body, timeout=5) as r: status, url, raw = r.status, r.geturl(), r.read()
        except urllib.error.HTTPError as e: status, url, raw = e.code, base+path, e.read(); e.close()
        (out/name).write_text(raw.decode("utf-8").replace('"/static/','"static/'), encoding="utf-8", newline="\n")
        print(status, path, "->", name); return url, raw.decode("utf-8")
    save("board.html", "/")
    save("request.html", "/requests/1")
    save("form.html", "/requests/new")
    _, form = save("form-blank.html", "/requests/new")
    tok = TOKEN.search(form).group(1)
    save("form-errors.html", "/requests/new", {"part":"", "title":"no","quantity":"0","priority":"","note":"","csrf_token":tok})
    save("error-404.html", "/requests/999")
    # a forged POST with no token -> 403
    save("error-403.html", "/requests/new", {"part":"BRG-14","title":"forged request here","quantity":"1","priority":"routine","note":""})
    shutil.copytree(HERE/"static", out/"static", dirs_exist_ok=True)
if __name__ == "__main__": main()

import argparse, http.cookiejar, pathlib, shutil, urllib.error, urllib.parse, urllib.request
HERE = pathlib.Path(__file__).parent
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--out", default=str(HERE/"saved")); a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    base = f"http://127.0.0.1:{a.port}"
    def save(name, path):
        try:
            with op.open(base+path, timeout=5) as r: status, raw = r.status, r.read()
        except urllib.error.HTTPError as e: status, raw = e.code, e.read(); e.close()
        (out/name).write_text(raw.decode("utf-8").replace('"/static/','"static/'), encoding="utf-8", newline="\n")
        print(status, path, "->", name)
    save("events.html", "/")
    save("event.html", "/events/3")
    save("report.html", "/report")
    save("error-404.html", "/events/6")
    shutil.copytree(HERE/"static", out/"static", dirs_exist_ok=True)
if __name__ == "__main__": main()

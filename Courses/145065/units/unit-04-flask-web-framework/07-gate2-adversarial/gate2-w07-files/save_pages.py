import argparse, pathlib, shutil, urllib.error, urllib.request
HERE = pathlib.Path(__file__).parent
PAGES = [("board.html","/"),("note.html","/notes/2"),("machines.html","/machines"),
         ("machine.html","/machines/OV-01"),("error-404.html","/nope")]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--out", default=str(HERE/"saved")); a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    base = f"http://127.0.0.1:{a.port}"
    for name, path in PAGES:
        try:
            with op.open(base+path, timeout=5) as r: status, body = r.status, r.read()
        except urllib.error.HTTPError as e: status, body = e.code, e.read(); e.close()
        (out/name).write_text(body.decode("utf-8").replace('"/static/','"static/'), encoding="utf-8", newline="\n")
        print(status, path, "->", name)
    shutil.copytree(HERE/"static", out/"static", dirs_exist_ok=True)
if __name__ == "__main__": main()

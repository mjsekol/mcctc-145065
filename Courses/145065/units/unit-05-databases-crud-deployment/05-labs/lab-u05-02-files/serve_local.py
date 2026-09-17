"""
serve_local.py · a production-style run on your own machine, with no new packages

Why this exists: you should see the app start the way it starts on the
server, with APP_ENV=production, a required SECRET_KEY, debug off, and the
Flask development server nowhere in sight, before you deploy. Render uses
gunicorn, which does not run on Windows, and neither gunicorn nor waitress is
installed on this machine. Python's standard library includes a WSGI server,
wsgiref, and that is enough for a rehearsal.

Be honest about what it is: wsgiref is a reference server. It has no worker
processes, no timeouts, and no protection against slow clients. It is fine on
127.0.0.1 for testing. It is not for the internet.

PowerShell:

    $env:APP_ENV = "production"
    $env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
    $env:DATABASE_PATH = "$env:TEMP\\line3_rehearsal.db"
    python manage.py init --db $env:DATABASE_PATH
    python serve_local.py --port 8681

This rehearsal serves plain HTTP on 127.0.0.1, so it sets COOKIE_SECURE=0.
Otherwise the browser would refuse to send the session cookie back and every
form would fail its token check. Render serves HTTPS, so leave COOKIE_SECURE
unset there.
"""

import argparse
import logging
import os
import pathlib
import socket
import socketserver
import sys
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server


class ThreadingWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    """One thread per request, so a slow page does not block the next one."""
    daemon_threads = True


class QuietHandler(WSGIRequestHandler):
    """The app logs every request itself. Skip wsgiref's second copy."""

    def log_message(self, format, *args):
        pass


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Production-style local run")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    if os.environ.get("APP_ENV") != "production":
        print("Set APP_ENV=production first. This script rehearses the production settings.")
        return 1
    os.environ.setdefault("COOKIE_SECURE", "0")

    from app import create_app
    from config import ConfigError

    try:
        app = create_app()
    except ConfigError as error:
        print(f"Refusing to start: {error}")
        return 1
    if not app.config["DATABASE_URL"] and not pathlib.Path(app.config["DATABASE_PATH"]).exists():
        print(f"No database at {app.config['DATABASE_PATH']}. Run: python manage.py init --db <path>")
        return 1
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use. Pick another or stop that server.")
        return 1

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    with make_server("127.0.0.1", args.port, app, server_class=ThreadingWSGIServer,
                     handler_class=QuietHandler) as server:
        print(f"Production-style server on http://127.0.0.1:{args.port}  "
              f"(APP_ENV={app.config['APP_ENV']}, debug={app.debug}). Ctrl+C stops it.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

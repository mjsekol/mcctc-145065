"""
wsgi.py · the entry point a production server imports

A production WSGI server (gunicorn on Render, waitress on Windows) needs one
object to call for every request. This file builds it once, from the
environment, and logs to standard output, where Render shows it.

    gunicorn wsgi:app                                   [VERIFY on Render]
    waitress-serve --listen=127.0.0.1:8681 wsgi:app     [VERIFY: waitress is not installed here]

If SECRET_KEY is missing in production, create_app() raises ConfigError here
and the server refuses to start. That is the point: a server that starts with
a guessable key is worse than one that does not start.
"""

import logging

from app import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
app = create_app()

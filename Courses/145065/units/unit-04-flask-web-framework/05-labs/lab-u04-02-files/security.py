"""
security.py · Line 3 Maintenance Log · Lab U04-02 STARTER

Cross-site request forgery (CSRF) protection, written out by hand so you can
see every moving part.

The attack: you are signed in to a site. Another page you visit contains a
hidden form that posts to that site. Your browser sends the request, with your
cookies, and the site cannot tell you did not mean it.

The defense: every form this site sends carries a random token that is also
stored in your session. A POST that does not return the same token is refused
with 403. The other page cannot read your token, so it cannot forge the form.

Flask signs the session cookie with SECRET_KEY, so a visitor can read the
cookie but cannot change it without the change being detected.

In a larger project you would reach for a library. Flask-WTF's CSRFProtect is
the common choice [VERIFY: it is not installed on this machine, and its
current setup steps should be checked before a lab uses it].
"""

import secrets

from flask import abort, request, session

TOKEN_FIELD = "csrf_token"
UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def csrf_token():
    """The token for this session, created on first use. Templates call this."""
    if TOKEN_FIELD not in session:
        session[TOKEN_FIELD] = secrets.token_urlsafe(32)
    return session[TOKEN_FIELD]


def check_csrf():
    """Run before every request. Refuse any state-changing request without the token.

    TODO Part 4, steps 16-18. Right now this lets every request through.
      1. A request whose method is not in UNSAFE_METHODS passes untouched.
      2. expected is the token in the session. sent is the form's TOKEN_FIELD value, or "".
      3. If there is no expected token, or sent does not match it, abort(403).
         Compare with secrets.compare_digest, never with == or !=. Your notes say why.
    """
    return


def init_security(app):
    app.before_request(check_csrf)
    app.jinja_env.globals["csrf_token"] = csrf_token
    # The session cookie cannot be read by page scripts, and a link from another
    # site does not carry it on a POST.
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

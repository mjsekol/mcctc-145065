# Settings Come from the Environment
---
## Slide 1: The password on a sticky note
- Your account password, on a note
- The note is stuck to your laptop
- Your laptop goes to school every day
- A secret in your code is that note
Speaker notes: Nobody here would stick their password to the outside of their laptop. Putting a secret key in your code is the same thing, except the laptop is your GitHub repository, and every old commit keeps a copy. Today your app stops carrying its secrets around.
Image: A laptop with a sticky note on the lid reading SECRET_KEY, launch red outline.
---
## Slide 2: The code is shared. The configuration is not.
- Same code on your laptop and the server
- Different database, secret, and cookie settings
- Settings come from environment variables
- os.environ holds them in Python
Speaker notes: This is today's idea. The server runs the exact commit you pushed. What changes is the configuration, and it comes from the environment, the named values the operating system hands a program when it starts. Start the same code with different environment variables and it behaves differently, with no edit.
Image: One code file with two arrows, one to a laptop and one to a server, each with its own settings card.
---
## Slide 3: Refuse to start
```python
def load_config(environ):
    app_env = environ.get("APP_ENV", "development")
    secret = environ.get("SECRET_KEY", "")
    if app_env == "production":
        if not secret:
            raise ConfigError("SECRET_KEY is not set. Production refuses to start without it.")
        if len(secret) < MIN_SECRET_LENGTH:
            raise ConfigError(f"SECRET_KEY is shorter than {MIN_SECRET_LENGTH} characters.")
    return {"APP_ENV": app_env, "SECRET_KEY": secret, "DEBUG": False}
```
Speaker notes: In production, no key means no start. A short key means no start. Debug is false no matter what. The function takes the environment as an argument, so a test can pass in a plain dictionary. Minimum length here is thirty-two characters.
Image: None. This slide is code.
---
## Slide 4: Three environments, three answers
```
Refusing to start: SECRET_KEY is not set. Production refuses to start without it.
Refusing to start: SECRET_KEY is shorter than 32 characters.
starts: production debug False key length 64
```
Speaker notes: No key, refused. The key password one two three, refused. A sixty-four character key, starts, with debug off. The key in the demo is nine f repeated, which is only a stand-in. A real key comes from the secrets module, gets pasted into the host's settings once, and never goes in a file.
Image: None. This slide is code.
---
## Slide 5: A fallback so it always starts
```python
def load_config(environ):
    return {
        "APP_ENV": environ.get("APP_ENV", "development"),
        "SECRET_KEY": environ.get("SECRET_KEY", "dev-secret-change-me"),
        "DEBUG": environ.get("FLASK_DEBUG", "1") == "1",
    }
```
```
starts: {'APP_ENV': 'production', 'SECRET_KEY': 'dev-secret-change-me', 'DEBUG': True}
```
Speaker notes: Here is the wrong way, and it is tempting because it always works. Production started. The key is the one written in the repository. And debug is on, because nobody set FLASK_DEBUG. No error, no warning. It starts, and that is the problem.
Image: None. This slide is code.
---
## Slide 6: What a published key allows
```
app with the published key -> supervisor
app with its own long key  -> nobody
```
Speaker notes: We signed a session cookie that says role supervisor, using the published key, the way an outsider who read your repository could. We sent it to two apps. The app using the published key believed it. The app with its own long key rejected it. Your CSRF token lives in that same session cookie. The full script is in today's notes.
Image: None. This slide is code.
---
## Slide 7: Make a real key
- Run: python -c "import secrets; print(secrets.token_hex(32))"
- 64 hex characters from secure random bytes
- Paste it into the host's settings once
- Never into a file, commit, chat, or AI tool
Speaker notes: The secrets module is built for keys. The random module is built for games, and its output can be predicted. Thirty-two random bytes become sixty-four hex characters. When you share a screenshot or a log, show the key's length, never the key.
Image: A key icon beside a masked field of dots, navy.
---
## Slide 8: Hardening, one door at a time
- Debug off everywhere, the secret required and long
- Secure and HttpOnly cookies, security headers
- A 64 KB request limit, no tracebacks on pages
- The /trace page removed, dependencies pinned
- A health route the host can check
Speaker notes: This is nine point three point four in one list. Each item closes a door. Debug off, because Flask's debugger runs code from an error page. Secure cookies travel only over HTTPS. Headers tell the browser what the page may load. Big requests are refused. Errors show plain words. Pinned versions make every update a choice you test. Walk the lab's config.py docstring with me now.
Image: A row of doors, each closed and labeled with one hardening item, navy and launch blue.
---
## Slide 9: One factory, three sets of settings
- create_app() builds the app from configuration
- Tests call it with test settings
- serve_local.py calls it with production settings
- The live server calls it through wsgi.py
Speaker notes: The application factory is why the route decorators became a table. A decorator needs an app when the file is imported, and a factory has no app until it runs. One function, three sets of settings, and your tests never touch your real database.
Image: A factory icon with three output conveyors labeled test, rehearsal, and server.
---
## Slide 10: What you are about to build
- Lab U05-02, Part 2: steps 7 through 12
- Production refuses a missing or short key
- Cookies default to Secure in production
- Entry points refuse to start when unsafe
- Target: 98 of 101 self-checks pass
Speaker notes: Part 2 makes the lab's config.py refuse. When you finish, start serve_local.py with APP_ENV set to production and no key, and it must print Refusing to start, SECRET_KEY is not set. In Build 2 you add config.py, a factory, and a health route to your tool crib, pin Flask and Werkzeug, and search your repository for any secret.
Image: A terminal showing a Refusing to start message, navy background, launch red text.

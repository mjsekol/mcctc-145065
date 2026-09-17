# Standing on Someone Else's Code
---
## Slide 1: You asked for one package
- One install command
- Seven packages arrived
- You chose one of them
- Who wrote the other six, and on what terms
Speaker notes: Today you install Flask. You will type one package name, and seven packages will land in your project. You did not pick six of them. You did not read their terms. By the end of today you will have done both, and you will know why a company cares.
Image: One small box labeled flask unpacking into seven boxes, navy and launch blue.
---
## Slide 2: A framework calls you
- A library waits for you to call it
- A framework runs the loop and calls your functions
- Flask decides when your function runs
- The request decides which one
Speaker notes: Unit 4 is where your objects go on a web page. You will not write the web server. Flask does that. Here is the shift. Until now your program decided what ran next. From today, a browser asks for a page, and Flask calls the one function you attached to that page. You write the function. Flask picks the moment.
Image: A loop arrow labeled Flask with three small function boxes it points to.
---
## Slide 3: What came with Flask
```python
from importlib.metadata import metadata, requires, version

print(f"flask {version('flask')}  {license_of('flask')}")
for requirement in requires("flask"):
    if ";" in requirement:
        continue
    name = requirement.split(">")[0].split("=")[0].strip()
    print(f"  needs {name} {version(name)}  {license_of(name)}")
```
Speaker notes: This is licenses.py, shortened. The license_of function is in your notes. It asks each installed package for its own metadata: its version, and the license it says it carries. Predict how many lines it prints before I run it.
Image: None. This slide is code.
---
## Slide 4: Seven lines, seven sets of terms
```
flask 3.1.3  BSD-3-Clause
  needs blinker 1.9.0  MIT License
  needs click 8.4.2  BSD-3-Clause
  needs itsdangerous 2.2.0  BSD License
  needs jinja2 3.1.6  BSD License
  needs markupsafe 3.0.3  BSD-3-Clause
  needs werkzeug 3.1.8  BSD-3-Clause
```
Speaker notes: This is the build machine's output. Your version numbers may be different. Look at itsdangerous and jinja2. They say BSD License with no number. That means the metadata does not say which variant. The package's own LICENSE file does, and opening it is your first lab task.
Image: None. This slide is code.
---
## Slide 5: What permissive licenses are for
- BSD and MIT are permissive licenses
- You may use, change, and share the code
- Company internal tools are included
- Keep the copyright notice and license text
- For class work, school policy comes first
Speaker notes: I am describing what these licenses are for, not giving legal advice. Permissive means the authors allow a lot. It does not mean they ask for nothing. Keeping the notice and the license text with the code is a condition. When someone says it is open source so anything goes, that is the part they forgot.
Image: A document icon with a checkmark list: use, change, share, keep the notice.
---
## Slide 6: The smallest Flask app
```python
from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Line 3 Maintenance Log is running."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8680, debug=False)
```
Speaker notes: Line 3 belongs to Riverside Fabrication, which is a composite, an invented shop we use all semester. Your file never calls home. Flask calls it when a browser asks for the slash page. Two habits start today. State the port every time. Keep debug off, because the debug error page includes a console that runs Python for anyone who reaches it.
Image: None. This slide is code.
---
## Slide 7: One rule, one 404
- `GET /` answers 200 with the message
- `GET /issues` answers 404
- No rule exists for issues yet
- Tomorrow: the rule
Speaker notes: I open the slash page and the message appears. Then I ask for slash issues and get a 404. Nothing is broken. There is no rule for that address, so none of my code ran. Rules are tomorrow's whole lesson.
Image: A browser window showing the running message, and a second showing Not Found.
---
## Slide 8: Now name the file flask.py
```
Traceback (most recent call last):
  File "...\shadow\flask.py", line 3, in <module>
    from flask import Flask
  File "...\shadow\flask.py", line 3, in <module>
    from flask import Flask
ImportError: cannot import name 'Flask' from 'flask' (consider renaming '...\\shadow\\flask.py' if it has the same name as a library you intended to import)
```
Speaker notes: Same code. The only change is the file name. Which flask did Python import? Python looks in your own folder first. It found your file, and your file has no Flask in it. The same line shows twice because the file imported itself. Read the hint in parentheses aloud. It tells you the fix.
Image: None. This slide is code.
---
## Slide 9: Names are shared space
- Python searches your folder before installed packages
- Your flask.py hides the real Flask
- Same trap: random.py, json.py, email.py
- Name files after what your program does
Speaker notes: This is the cheapest bug you will ever meet, if you know it exists. The name that describes your practice file is the library's name. That is why it collides. When an import fails in a way that makes no sense, check your file names first, and delete any pycache folder next to the renamed file.
Image: Two folders side by side, a project folder and site-packages, each holding a file named flask.py.
---
## Slide 10: What you are about to build
- Lab U04-01 Part 1, steps 1 and 2
- Install Flask into your project environment
- Start the lab app on port 8680
- Write LICENSES.md: seven packages, versions, licenses
- Open two LICENSE files and name the variant
Speaker notes: Build 1 is Lab U04-01, Line 3 on the Web, Part 1. You install Flask, start the lab app on port 8680, and see the Line 3 dashboard. Then you write a license table with a row for every package. The two rows that say BSD License are not finished until you open the package's LICENSE file and name the variant. The self-check shows eight Part 1 lines as PASS when you are done.
Image: A two-column table titled LICENSES.md with seven rows, two of them highlighted in launch blue.

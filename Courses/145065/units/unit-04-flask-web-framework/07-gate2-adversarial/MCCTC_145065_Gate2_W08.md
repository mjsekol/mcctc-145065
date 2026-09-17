# Gate 2: Adversarial Review · Week 8
## 145065 Object-Oriented Programming · Unit 4 · Week 8, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this code. You are reviewing it, and
you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may and should run the app and read every file. You may send
requests to your own copy on 127.0.0.1 and to nothing else. You may not ask a model whether the code is
correct, because a model is what is being reviewed.

**This is a generated Flask app with a form. It has one injection vulnerability, and four other
defects.** You review it with the Five-Dimension Code Review, one planted defect per dimension:

| Dimension | The question to ask |
|---|---|
| **Correctness** | Does it do what the spec says, on every input and boundary? |
| **Security** | Could a stranger inject something, or read or break what they should not? |
| **Readability** | Would the next person be misled by a name or a comment? |
| **Performance** | Does it do unnecessary or repeated work? |
| **Requirements Fit** | Did it build what the spec asked for, no more and no less? |

**Exactly five defects, one per dimension. At least one is subtle. One is arguable: defend either side
with a sound reason.** The code runs, the form works, and the tests a careless author wrote would pass.

**Everything is invented.** Riverside Fabrication is a composite shop. Every part and request is
invented.

The code is in `gate2-w08-files/`. Run it against a copy of the store:

```
Copy-Item data\requests.json $env:TEMP\parts_copy.json
$env:STORE_PATH = "$env:TEMP\parts_copy.json"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python requests_app.py --port 8680
```

Open `http://127.0.0.1:8680/`. Read `requests_app.py` and every file in `templates/`.

---

## PART A: The requirements spec the code was built from

> Build a **Line 3 Parts Request** form in Flask. A technician requests a replacement part.
>
> 1. `GET /` shows every open request with the part's name, quantity, and priority.
> 2. `GET /requests/new` shows the form. `POST /requests/new` checks it and saves it.
> 3. The server refuses bad input with 400 and a message per problem: the part must be one on the
>    list; the reason is **5 to 60 characters**; the quantity is a whole number 1 to 99; the priority is
>    one of the three. The note is optional.
> 4. **Every value a person typed is shown as text.** A note that contains a script tag must never run.
> 5. Every POST carries a CSRF token, or it is refused with 403.
> 6. **After a successful save, redirect to the new request's page**, so a refresh does not send it
>    twice.

---

## What to hand in

For each defect: its **dimension**, the **file and line**, **what is wrong**, **what a person on Line 3
would experience**, and the **fix**. Then one line naming the defect you were least sure about and why.

The injection is real. Find a way to prove it on your own copy, and write the request you sent.

---

## PART B: The code

In `gate2-w08-files/`. Start with `requests_app.py`, then the templates. No defect is marked.

---

## Scoring · 5 points, double penalty on the security miss

| Found | Points |
|---|---|
| Each defect correctly located and explained | 1 |
| The arguable defect: full point for either side with a sound reason | 1 |
| **Missing the security defect** | **minus 1 on top of the 0 for that defect** |

Five points possible. The security defect is the injection. Missing it is the worst outcome, so it
costs its point and one more. Prove it with a request, do not only describe it.

"""
validation.py · Line 3 Maintenance Log · Lab U04-02 STARTER

The server's rules for a new issue. The form in templates/issue_form.html
carries matching hints (required, minlength, maxlength, pattern, min, max) so a
person hears about a mistake before sending. Those hints are a courtesy. Anyone
can delete them in the browser's developer tools or send a request with no
browser at all, so every rule is enforced again here, where it counts.

The constants below are used by both this file and the template, so the two
layers cannot drift apart. test_app.py checks that they match.

validate_issue(form, equipment_codes, badges) returns (clean, errors):
    clean   a dict of converted values, only meaningful when errors is empty
    errors  a dict of field name -> message, in the order the form shows them
"""

import re

from models import SEVERITIES

TITLE_MIN, TITLE_MAX = 5, 80
DESCRIPTION_MIN, DESCRIPTION_MAX = 10, 1000
DOWNTIME_MAX = 1440  # minutes in one day
# A badge is T (technician) or S (supervisor), a hyphen, and four digits.
# The same text is the HTML pattern attribute, which is anchored for you.
BADGE_PATTERN = r"[TS]-[0-9]{4}"
# [0-9], not \d: in Python \d also matches digits from other scripts, such as "٣".
WHOLE_NUMBER = re.compile(r"[0-9]{1,4}")

FIELD_ORDER = ["reported_by", "equipment", "title", "description", "severity",
               "downtime_minutes", "locked_out"]


def validate_issue(form, equipment_codes, badges):
    """TODO Part 2. Right now this accepts anything. That is the bug you fix.

    Write one block per field, in FIELD_ORDER. Each block reads the raw value,
    sets errors[field] to a message when a rule fails, and sets clean[field].
    test_app.py's ValidationTests are the specification: read them first.
    """
    errors = {}
    clean = {}
    for name in FIELD_ORDER:
        clean[name] = (form.get(name) or "").strip()
    raw = clean["downtime_minutes"]
    clean["downtime_minutes"] = int(raw) if raw.isdecimal() else 0   # TODO: refuse, never guess
    clean["locked_out"] = form.get("locked_out") == "yes"
    ordered = {name: errors[name] for name in FIELD_ORDER if name in errors}
    return clean, ordered

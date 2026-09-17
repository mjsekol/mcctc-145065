"""
validation.py · Line 3 Maintenance Log · Lab U05-01 starter, unchanged from the reference stage w09

The server's rules. The forms carry matching hints, and the database carries
CHECK constraints for the rules that matter most. Three layers, one set of
numbers: the constants below feed the templates, and test_app.py checks that
schema.sql agrees with them.

    validate_issue(form, equipment_codes, badges, editing=False)
    validate_note(form, badges)
    validate_import_row(row, equipment_codes, badges)

Each returns (clean, errors). errors is a dict of field -> message in form order.
"""

import re
from datetime import datetime

from models import SEVERITIES, STATUSES

TITLE_MIN, TITLE_MAX = 5, 80
DESCRIPTION_MIN, DESCRIPTION_MAX = 10, 1000
DOWNTIME_MAX = 1440          # minutes in one day
NOTE_MIN, NOTE_MAX = 3, 500
NOTE_MINUTES_MIN, NOTE_MINUTES_MAX = 1, 720   # one work note covers at most 12 hours
SEARCH_MAX = 60
BADGE_PATTERN = r"[TS]-[0-9]{4}"
# [0-9], not \d: in Python \d also matches digits from other scripts, such as "٣".
WHOLE_NUMBER = re.compile(r"[0-9]{1,4}")
UTC_TIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")

ISSUE_FIELDS = ["reported_by", "equipment", "title", "description", "severity",
                "status", "downtime_minutes", "locked_out"]


def _badge(form, badges, errors, field="reported_by"):
    badge = (form.get(field) or "").strip().upper()
    if not badge:
        errors[field] = "Enter your badge number."
    elif not re.fullmatch(BADGE_PATTERN, badge):
        errors[field] = "Enter a badge like T-1041: T or S, a hyphen, then four digits."
    elif badge not in badges:
        errors[field] = "That badge is not on the Line 3 list."
    return badge


def _whole_number(raw, low, high, field, label, errors):
    raw = (raw or "").strip()
    if not WHOLE_NUMBER.fullmatch(raw):
        errors[field] = f"Enter {label} as a whole number, {low} to {high}."
        return None
    value = int(raw)
    if not (low <= value and value <= high):
        errors[field] = f"{label.capitalize()} must be between {low} and {high}."
    return value


def validate_issue(form, equipment_codes, badges, editing=False):
    """A new issue, or an edit to one. An edit keeps its reporter and may change status."""
    errors = {}
    clean = {}

    if not editing:
        clean["reported_by"] = _badge(form, badges, errors)

    code = form.get("equipment") or ""
    if not code:
        errors["equipment"] = "Choose the machine."
    elif code not in equipment_codes:
        errors["equipment"] = "Choose a machine from the list."
    clean["equipment"] = code

    title = (form.get("title") or "").strip()
    if not TITLE_MIN <= len(title) <= TITLE_MAX:
        errors["title"] = f"Write a title between {TITLE_MIN} and {TITLE_MAX} characters."
    elif "\n" in title or "\r" in title:
        errors["title"] = "Keep the title on one line."
    clean["title"] = title

    description = (form.get("description") or "").strip()
    if not DESCRIPTION_MIN <= len(description) <= DESCRIPTION_MAX:
        errors["description"] = (
            f"Describe what you saw in {DESCRIPTION_MIN} to {DESCRIPTION_MAX} characters."
        )
    clean["description"] = description

    severity = form.get("severity") or ""
    if severity not in SEVERITIES:
        errors["severity"] = "Choose a severity."
    clean["severity"] = severity

    if editing:
        status = form.get("status") or ""
        if status not in STATUSES:
            errors["status"] = "Choose a status."
        clean["status"] = status
    else:
        clean["status"] = "open"

    clean["downtime_minutes"] = _whole_number(
        form.get("downtime_minutes"), 0, DOWNTIME_MAX, "downtime_minutes",
        "downtime in minutes", errors)

    locked_out = form.get("locked_out") == "yes"
    clean["locked_out"] = locked_out
    # The software records a lockout a person performed. It never switches equipment.
    if severity == "critical" and not locked_out:
        errors["locked_out"] = "A critical issue needs the machine locked out first. Lock it out, then tick the box."

    return clean, {name: errors[name] for name in ISSUE_FIELDS if name in errors}


def validate_note(form, badges):
    errors = {}
    clean = {"badge": _badge(form, badges, errors, field="badge")}
    note = (form.get("note") or "").strip()
    if not NOTE_MIN <= len(note) <= NOTE_MAX:
        errors["note"] = f"Write the note in {NOTE_MIN} to {NOTE_MAX} characters."
    clean["note"] = note
    clean["minutes_spent"] = _whole_number(
        form.get("minutes_spent"), NOTE_MINUTES_MIN, NOTE_MINUTES_MAX, "minutes_spent",
        "time spent in minutes", errors)
    order = ["badge", "note", "minutes_spent"]
    return clean, {name: errors[name] for name in order if name in errors}


def validate_search(raw):
    """A search box is input too. Trim it and cap its length. Its content is
    never trusted: db.py sends it as a parameter, never as SQL."""
    return (raw or "").strip()[:SEARCH_MAX]


def _utc_time(raw, field, errors, required):
    raw = (raw or "").strip()
    if not raw:
        if required:
            errors[field] = f"{field} is required."
        return None
    if not UTC_TIME.fullmatch(raw):
        errors[field] = f"{field} must look like 2025-11-10T07:42:00Z."
        return None
    try:
        datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        errors[field] = f"{field} is not a real date and time."
        return None
    return raw


def validate_import_row(row, equipment_codes, badges):
    """One CSV row. The same rules as the form, plus the fields only an import sets."""
    locked = (row.get("locked_out") or "").strip().lower()
    form = {
        "reported_by": row.get("reported_by"),
        "equipment": (row.get("equipment_code") or "").strip(),
        "title": row.get("title"),
        "description": row.get("description"),
        "severity": (row.get("severity") or "").strip(),
        "status": (row.get("status") or "").strip(),
        "downtime_minutes": row.get("downtime_minutes"),
        "locked_out": "yes" if locked == "yes" else "",
    }
    reporter_errors = {}
    reporter = _badge(form, badges, reporter_errors)
    clean, errors = validate_issue(form, equipment_codes, badges, editing=True)
    errors = {**reporter_errors, **errors}
    clean["reported_by"] = reporter
    if locked not in ("yes", "no"):
        errors["locked_out"] = "locked_out must be yes or no."
    clean["reported_at"] = _utc_time(row.get("reported_at"), "reported_at", errors, required=True)
    clean["closed_at"] = _utc_time(row.get("closed_at"), "closed_at", errors, required=False)
    if not errors:
        if clean["status"] == "closed" and clean["closed_at"] is None:
            errors["closed_at"] = "A closed issue needs closed_at."
        elif clean["status"] != "closed" and clean["closed_at"] is not None:
            errors["closed_at"] = "Only a closed issue has closed_at."
        elif clean["closed_at"] is not None and clean["closed_at"] < clean["reported_at"]:
            errors["closed_at"] = "closed_at cannot be before reported_at."
    return clean, errors

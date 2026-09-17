"""
store.py · Line 3 Maintenance Log · Lab U04-02 starter, unchanged from the reference

Reads and now writes the Unit 3-style JSON store: one versioned file,
validated on load, backed up before every write, replaced in one step.

What changed since w07: add_issue(). It appends one record, keeps the previous
file as line3_log.json.bak, and writes through a temporary file so a crash in
the middle never leaves half a file behind.

What a JSON file cannot do well, and why Week 9 brings a database: two
requests that save at the same moment can each read the old file and each
write their own version, so one issue disappears. The lock below stops that
inside one server process. It does nothing for two processes, and a real
deployment runs several. A database handles that for you.

Never pickle. json.load can only build plain data. pickle.load can run code.
"""

import json
import os
import pathlib
import shutil
import threading
from datetime import datetime, timezone

from models import ROLES, SEVERITIES, STATUSES, Equipment, Issue, Technician

SUPPORTED_VERSION = 2
_write_lock = threading.Lock()


class StoreError(Exception):
    """Base class: anything wrong with the store."""


class StoreMissingError(StoreError):
    """The file is not there."""


class StoreFormatError(StoreError):
    """The file is there, but its contents break the format."""


def _require(record, field, kind, where):
    """Return record[field] if it exists and has the right type."""
    if field not in record:
        raise StoreFormatError(f"{where}: missing field '{field}'")
    value = record[field]
    # bool is a subclass of int in Python, so True would pass an int check.
    if kind is int and isinstance(value, bool):
        raise StoreFormatError(f"{where}: '{field}' must be a whole number")
    if not isinstance(value, kind):
        raise StoreFormatError(f"{where}: '{field}' has the wrong type")
    return value


def _parse_time(text, where):
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise StoreFormatError(f"{where}: reported_at is not an ISO 8601 time") from None


class IssueStore:
    """Access to the maintenance log file."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self._equipment = {}
        self._technicians = {}
        self._issues = {}
        self.load()

    def _read_raw(self):
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise StoreMissingError(f"No store at {self.path}") from None
        try:
            raw = json.loads(text)
        except json.JSONDecodeError as error:
            raise StoreFormatError(f"Not valid JSON: {error}") from None
        if not isinstance(raw, dict):
            raise StoreFormatError("The top level must be an object")
        return raw

    def load(self):
        raw = self._read_raw()
        version = raw.get("format_version")
        if version != SUPPORTED_VERSION:
            raise StoreFormatError(
                f"format_version is {version!r}; this program reads version {SUPPORTED_VERSION}"
            )

        equipment = {}
        for n, rec in enumerate(_require(raw, "equipment", list, "store")):
            where = f"equipment[{n}]"
            item = Equipment(
                code=_require(rec, "code", str, where),
                name=_require(rec, "name", str, where),
                cell=_require(rec, "cell", str, where),
                kind=_require(rec, "kind", str, where),
            )
            if item.code in equipment:
                raise StoreFormatError(f"{where}: duplicate code {item.code}")
            equipment[item.code] = item

        technicians = {}
        for n, rec in enumerate(_require(raw, "technicians", list, "store")):
            where = f"technicians[{n}]"
            tech = Technician(
                badge=_require(rec, "badge", str, where),
                display_name=_require(rec, "display_name", str, where),
                role=_require(rec, "role", str, where),
            )
            if tech.role not in ROLES:
                raise StoreFormatError(f"{where}: unknown role {tech.role!r}")
            technicians[tech.badge] = tech

        issues = {}
        for n, rec in enumerate(_require(raw, "issues", list, "store")):
            where = f"issues[{n}]"
            issue = Issue(
                id=_require(rec, "id", int, where),
                equipment=_require(rec, "equipment", str, where),
                title=_require(rec, "title", str, where),
                description=_require(rec, "description", str, where),
                severity=_require(rec, "severity", str, where),
                status=_require(rec, "status", str, where),
                reported_by=_require(rec, "reported_by", str, where),
                reported_at=_parse_time(_require(rec, "reported_at", str, where), where),
                downtime_minutes=_require(rec, "downtime_minutes", int, where),
                locked_out=_require(rec, "locked_out", bool, where),
            )
            if issue.equipment not in equipment:
                raise StoreFormatError(f"{where}: unknown equipment {issue.equipment!r}")
            if issue.reported_by not in technicians:
                raise StoreFormatError(f"{where}: unknown badge {issue.reported_by!r}")
            if issue.severity not in SEVERITIES:
                raise StoreFormatError(f"{where}: unknown severity {issue.severity!r}")
            if issue.status not in STATUSES:
                raise StoreFormatError(f"{where}: unknown status {issue.status!r}")
            if issue.downtime_minutes < 0:
                raise StoreFormatError(f"{where}: downtime_minutes cannot be negative")
            if issue.id in issues:
                raise StoreFormatError(f"{where}: duplicate id {issue.id}")
            issues[issue.id] = issue

        self._equipment, self._technicians, self._issues = equipment, technicians, issues

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def add_issue(self, clean, now=None):
        """Append one validated issue and return its new id.

        `clean` must come from validation.validate_issue. This method trusts
        it for types and ranges, and still refuses unknown references,
        because a store should never hold a record that points at nothing."""
        if clean["equipment"] not in self._equipment:
            raise StoreFormatError(f"unknown equipment {clean['equipment']!r}")
        if clean["reported_by"] not in self._technicians:
            raise StoreFormatError(f"unknown badge {clean['reported_by']!r}")
        now = now or datetime.now(timezone.utc)
        with _write_lock:
            raw = self._read_raw()
            new_id = max((rec["id"] for rec in raw["issues"]), default=0) + 1
            raw["issues"].append({
                "id": new_id,
                "equipment": clean["equipment"],
                "title": clean["title"],
                "description": clean["description"],
                "severity": clean["severity"],
                "status": "open",
                "reported_by": clean["reported_by"],
                "reported_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "downtime_minutes": clean["downtime_minutes"],
                "locked_out": clean["locked_out"],
            })
            self._write_raw(raw)
            self.load()
        return new_id

    def _write_raw(self, raw):
        """Backup, write to a temporary file, then swap it in with one call."""
        temp = self.path.with_name(self.path.name + ".tmp")
        backup = self.path.with_name(self.path.name + ".bak")
        # ensure_ascii=False keeps names like "Zoë" readable in the file. UTF-8 stores them.
        temp.write_text(json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        shutil.copy2(self.path, backup)
        os.replace(temp, self.path)

    # ------------------------------------------------------------------
    # Queries the routes use. Each returns clean objects, never raw dicts.
    # ------------------------------------------------------------------

    def all_equipment(self):
        return sorted(self._equipment.values(), key=lambda e: e.code)

    def equipment_codes(self):
        return set(self._equipment)

    def badges(self):
        return set(self._technicians)

    def get_equipment(self, code):
        return self._equipment.get(code)

    def get_technician(self, badge):
        return self._technicians.get(badge)

    def get_issue(self, issue_id):
        return self._issues.get(issue_id)

    def issues(self, status=None, equipment=None):
        """Most urgent first, then newest first."""
        found = [
            i for i in self._issues.values()
            if (status is None or i.status == status)
            and (equipment is None or i.equipment == equipment)
        ]
        found.sort(key=lambda i: i.reported_at, reverse=True)
        found.sort(key=lambda i: i.severity_rank, reverse=True)
        return found

    def open_issues(self):
        return [i for i in self.issues() if i.is_open]

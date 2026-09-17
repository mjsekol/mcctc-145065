"""
models.py · Line 3 Maintenance Log · Lab U05-02 STARTER

The objects db.py hands to the routes. Riverside Fabrication is a composite,
an invented shop, and every record here is invented.

Why convert database rows into objects at all: a row is whatever the database
driver returns, and SQLite and PostgreSQL drivers return different things. The
routes and templates only ever see these classes, so switching databases
changes db.py and nothing else.
"""

from dataclasses import dataclass
from datetime import datetime

SEVERITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "in_progress", "closed")
ROLES = ("technician", "supervisor")
STATUS_LABELS = {"open": "Open", "in_progress": "In progress", "closed": "Closed"}

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def parse_time(text):
    """Stored times are UTC text such as 2025-11-10T07:42:00Z. None stays None."""
    if text is None:
        return None
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


@dataclass(frozen=True)
class Equipment:
    id: int
    code: str
    name: str
    cell: str
    kind: str


@dataclass(frozen=True)
class Technician:
    id: int
    badge: str
    display_name: str
    role: str


@dataclass(frozen=True)
class Issue:
    id: int
    equipment_code: str
    equipment_name: str
    title: str
    description: str
    severity: str
    status: str
    reporter_badge: str
    reporter_name: str
    reported_at: datetime
    closed_at: datetime | None
    downtime_minutes: int
    locked_out: bool

    @property
    def is_open(self):
        return self.status != "closed"

    @property
    def status_label(self):
        return STATUS_LABELS[self.status]

    @property
    def hours_to_close(self):
        """A calculated field: None while the issue is still open."""
        if self.closed_at is None:
            return None
        return (self.closed_at - self.reported_at).total_seconds() / 3600


@dataclass(frozen=True)
class WorkNote:
    id: int
    technician_badge: str
    technician_name: str
    note: str
    minutes_spent: int
    created_at: datetime

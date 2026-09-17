"""
models.py · Line 3 Maintenance Log · stage w07_routes

The objects the routes hand to the templates. Riverside Fabrication is a
composite, an invented shop, and every record here is invented.

These are the same ideas you built in Units 1-3: a class bundles data with the
behavior that belongs to it. Dataclasses (Unit 2) write __init__ and __repr__
for you. frozen=True means a route cannot change a record by accident while it
is building a page.
"""

from dataclasses import dataclass
from datetime import datetime

SEVERITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "in_progress", "closed")
ROLES = ("technician", "supervisor")

# How each status reads on a page. The stored value stays short and fixed.
STATUS_LABELS = {"open": "Open", "in_progress": "In progress", "closed": "Closed"}


@dataclass(frozen=True)
class Equipment:
    code: str
    name: str
    cell: str
    kind: str


@dataclass(frozen=True)
class Technician:
    badge: str
    display_name: str
    role: str


@dataclass(frozen=True)
class Issue:
    id: int
    equipment: str
    title: str
    description: str
    severity: str
    status: str
    reported_by: str
    reported_at: datetime
    downtime_minutes: int
    locked_out: bool

    @property
    def is_open(self):
        """Open work is anything not closed. In progress still needs someone."""
        return self.status != "closed"

    @property
    def status_label(self):
        return STATUS_LABELS[self.status]

    @property
    def severity_rank(self):
        """Critical sorts first. A bigger number means more urgent."""
        return SEVERITIES.index(self.severity)

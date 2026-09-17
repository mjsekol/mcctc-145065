# work_orders.py
"""Work orders for the Line 3 maintenance team.

Implements the team's work order spec: validated work orders, an audited
close, and one board per shift. Riverside Fabrication is a composite shop,
and every order below is invented.

Usage:
    python work_orders.py
"""

import re

ORDER_ID_PATTERN = re.compile(r"WO-[0-9]{4}")
PRIORITY_LABELS = {1: "urgent", 2: "soon", 3: "routine"}


class WorkOrder:
    """One maintenance request for one machine."""

    def __init__(self, order_id, asset_tag, description, priority):
        # Validate everything up front so a bad order never exists.
        if not isinstance(order_id, str) or not ORDER_ID_PATTERN.fullmatch(order_id):
            raise ValueError(f"order id {order_id!r} must look like WO-0000")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must not be blank")
        if priority not in PRIORITY_LABELS:
            raise ValueError("priority must be 1 (urgent), 2 (soon), or 3 (routine)")
        self.order_id = order_id
        self.asset_tag = asset_tag
        self.description = description.strip()
        self.priority = priority
        self.status = "open"
        self._closed_by = None
        self._close_note = None

    def close(self, badge, note):
        """Close the order. A badge and a note are required for the audit trail."""
        if not isinstance(badge, str) or not badge.strip():
            raise ValueError("closing a work order requires a badge")
        if not isinstance(note, str) or not note.strip():
            raise ValueError("closing a work order requires a note")
        if self.status == "closed":
            raise RuntimeError(f"{self.order_id} is already closed")
        self.status = "closed"
        self._closed_by = badge.strip()
        self._close_note = note.strip()

    def reopen(self):
        """Reopen a closed order when the fix did not hold."""
        self.status = "open"
        self._closed_by = None
        self._close_note = None

    def closed_by(self):
        return self._closed_by

    def close_note(self):
        return self._close_note

    def __repr__(self):
        return f"WorkOrder({self.order_id!r}, {self.asset_tag!r}, priority={self.priority})"


def priority_label(order):
    """Return the human-readable priority for a work order."""
    return PRIORITY_LABELS[order.priority]


class WorkOrderBoard:
    """The work orders for one shift."""

    def __init__(self, name, orders=[]):
        self.name = name
        self._orders = orders

    def add(self, order):
        """Add an order to the board. Duplicate ids are refused."""
        for existing in self._orders:
            if existing.order_id == order.order_id:
                raise ValueError(f"{order.order_id} is already on the {self.name} board")
        self._orders.append(order)
        return order

    def find(self, order_id):
        """Return the order with this id, or None."""
        for order in self._orders:
            if order.order_id == order_id:
                return order
        return None

    def open_orders(self):
        """Return the open orders, most urgent first."""
        still_open = [order for order in self._orders if order.status == "open"]
        return sorted(still_open, key=lambda order: order.priority)

    def summary(self):
        """One line for the shift handoff."""
        open_now = self.open_orders()
        urgent = sum(1 for order in open_now if order.priority == 1)
        closed = len(self._orders) - len(open_now)
        return f"{self.name}: {len(open_now)} open ({urgent} urgent), {closed} closed"


def main():
    day = WorkOrderBoard("Day shift")
    day.add(WorkOrder("WO-1001", "L3-PRS-02", "Vibration above 7 mm/s", 1))
    day.add(WorkOrder("WO-1002", "L3-CNV-01", "Belt tracking drifts left", 3))
    day.add(WorkOrder("WO-1003", "L3-OVN-01", "Door seal worn", 2))
    day.find("WO-1002").close("tech-12", "Retensioned and re-tracked the belt")

    print(day.summary())
    for order in day.open_orders():
        print(f"  {order.order_id} [{priority_label(order)}] {order.asset_tag}: {order.description}")


if __name__ == "__main__":
    main()

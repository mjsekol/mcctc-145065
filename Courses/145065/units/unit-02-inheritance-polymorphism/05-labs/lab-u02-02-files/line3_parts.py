# line3_parts.py
# The machines for Lab U02-02. GIVEN. You do not change this file.
#
# Riverside Fabrication is a composite shop invented for this course.
# This is a deliberately small Machine class, so this lab is only about the
# layout. Your Lab U02-01 hierarchy can replace it later (see EXTENDED).


class Machine:
    """One piece of equipment on the line. It holds no other items."""

    def __init__(self, asset_tag, name, kind, rated_kw=0):
        self.asset_tag = asset_tag
        self.name = name
        self.kind = kind
        self.rated_kw = rated_kw  # 0 for equipment with no power, such as a rack

    def describe(self):
        return f"{self.asset_tag} {self.name} ({self.kind})"

    def __repr__(self):
        return f"Machine({self.asset_tag!r})"

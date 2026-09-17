# tool_crib.py
# Lab U01-02: The Tool Crib. STARTER.
#
# Part 2 (Wednesday) builds the Tool class and keeps two plain functions.
# Part 3 (Thursday) builds the ToolCrib class that holds Tool objects.
# Build only what your Part 1 diagram says. If the code needs something the
# diagram does not show, change the diagram first, in the same commit.
#
# Riverside Fabrication is a composite shop. Everything here is invented.
#
#     python tool_crib.py
#     python selfcheck_crib.py part2
#     python selfcheck_crib.py part3
#
# It runs now and prints one line. Nothing below does anything useful yet.

import re

OVERDUE_AFTER_MINUTES = 240            # a tool out longer than four hours gets chased
TAG_PATTERN = re.compile(r"TC-[0-9]{3}")  # crib tags look like TC-014


# ----- Part 2: the functions that stay functions -----
# Step 8 decides which of the eight procedural functions belong here.


# ----- Part 2: one tool -----

class Tool:
    """One tool in the crib."""

    def __init__(self, tag, name):
        # Step 9: refuse a bad tag or a blank name, then store them.
        pass


# ----- Part 3: the crib that holds the tools -----

class ToolCrib:
    """A named collection of tools, looked up by tag."""

    def __init__(self, name):
        # Step 14: refuse a blank name, then store it and an empty collection.
        pass


def main():
    print("Tool crib starter. Nothing is built yet.")


if __name__ == "__main__":
    main()

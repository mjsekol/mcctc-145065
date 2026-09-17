# shift_with_objects.py
# Lab U01-01, Part 2. STARTER.
#
# The same shift as press_tracker.py, rewritten to use your Machine class.
# Riverside Fabrication is a composite shop. Everything here is invented.
#
#     python shift_with_objects.py
#
# It runs now and prints only the two headings. Step 13 fills it in.

from machine import Machine


def main():
    print("First half of the shift")
    # TODO step 13: build press1 (L3-PRS-01, Press 1, 15 kW) and
    # press2 (L3-PRS-02, Press 2, 22 kW) as Machine objects.

    # TODO step 13: the same five events as press_tracker.py:
    #   start press1, record 45 minutes on press1, lock out press2 as tech-07,
    #   try to start press2, try to release press2's lock as tech-12.
    # Machine refuses with an exception. Catch each refusal and print it as
    #   "  refused: <the exception message>"

    # TODO step 14: the three lines added later, by three different people.
    # Write each one the only way the class allows, and see what happens:
    #   the "quick fix" that makes press2 run
    #   the setup script that sets press1 to -15 kW
    #   the typo that sets press1's "runing" to False

    print("End of the shift")
    # TODO step 13: print "  " + status_text() for each press.


if __name__ == "__main__":
    main()

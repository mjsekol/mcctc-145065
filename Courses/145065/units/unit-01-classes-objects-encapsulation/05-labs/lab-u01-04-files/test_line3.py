# test_line3.py
# Lab U01-04, Part 2: tests for a class. STARTER.
#
# The classes under test are in the line3/ folder: Machine and WorkCell.
# They were copied unchanged from the course's Line 3 plant model.
# Riverside Fabrication is a composite shop. Everything here is invented.
#
# Write your test plan (test_plan.md) BEFORE you write the tests below.
#
#     python -m unittest -v test_line3
#     python mutant_check.py
#
# It runs now: one example test, which passes.

import unittest

from line3 import Machine, WorkCell


def make_press(tag="L3-PRS-01"):
    """A fresh press. Every test builds its own, so no test depends on another."""
    return Machine(tag, "Press 1", rated_kw=15)


class MachineTests(unittest.TestCase):
    def test_new_machine_is_stopped_with_no_reading(self):
        press = make_press()
        self.assertFalse(press.is_running)
        self.assertIsNone(press.temperature_c)

    # TODO: one test method per row of your test plan for Machine.


class WorkCellTests(unittest.TestCase):
    def setUp(self):
        # setUp runs before EVERY test method in this class.
        self.cell = WorkCell("Forming")

    # TODO: one test method per row of your test plan for WorkCell.


if __name__ == "__main__":
    unittest.main()

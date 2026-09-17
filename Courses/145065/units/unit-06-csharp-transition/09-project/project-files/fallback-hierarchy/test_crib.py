"""unittest suite for the fallback hierarchy. Run: python -m unittest -v"""

import unittest

from crib import (Battery, CribItem, Drill, Grinder, HandTool, Kit, PoweredTool,
                  build_sample_crib, crib_report)


class HierarchyTests(unittest.TestCase):
    def test_three_levels(self):
        self.assertTrue(issubclass(Drill, PoweredTool))
        self.assertTrue(issubclass(PoweredTool, CribItem))

    def test_crib_item_cannot_be_built(self):
        with self.assertRaises(TypeError):
            CribItem("CRIB-009", "Thing")

    def test_powered_tool_is_abstract_in_its_comment_only(self):
        # PoweredTool supplies issues(), so abc sees nothing abstract left.
        # Nothing stops this line. Porting to C# is where that changes.
        tool = PoweredTool("CRIB-009", "Thing")
        self.assertEqual("powered", tool.kind)

    def test_tags_are_checked(self):
        self.assertTrue(CribItem.is_valid_tag("CRIB-001"))
        self.assertFalse(CribItem.is_valid_tag("crib-001"))
        with self.assertRaises(ValueError):
            Grinder("GRIND-1", "Angle Grinder")

    def test_hours_must_be_positive(self):
        drill = Drill("CRIB-001", "Cordless Drill")
        with self.assertRaises(ValueError):
            drill.log_hours(0)
        drill.log_hours(10)
        self.assertEqual(10, drill.hours_since_service)

    def test_check_out_twice_is_refused(self):
        grinder = Grinder("CRIB-002", "Angle Grinder")
        grinder.check_out("badge-31")
        with self.assertRaises(RuntimeError):
            grinder.check_out("badge-44")
        grinder.check_in()
        self.assertIsNone(grinder.checked_out_to)


class CompositionTests(unittest.TestCase):
    def test_a_drill_has_a_battery(self):
        drill = Drill("CRIB-001", "Cordless Drill")
        self.assertIsInstance(drill.battery, Battery)
        self.assertEqual(100, drill.battery.charge_percent)

    def test_battery_range(self):
        with self.assertRaises(ValueError):
            Battery(101)


class PolymorphismTests(unittest.TestCase):
    def test_sample_report(self):
        self.assertEqual(
            [
                "CRIB-001 Cordless Drill: service due (52 h)",
                "CRIB-001 Cordless Drill: battery low (12%)",
                "CRIB-002 Angle Grinder: guard missing, do not issue",
                "CRIB-003 Torque Wrench: calibration expired",
            ],
            crib_report(build_sample_crib()),
        )

    def test_nested_kits_count_recursively(self):
        setup = build_sample_crib()[2]
        self.assertEqual(2, setup.count_tools())


if __name__ == "__main__":
    unittest.main()

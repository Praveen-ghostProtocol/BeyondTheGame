"""Self-contained tests: python -m unittest discover -s tests -p 'test_b3*.py'"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models" / "b3"))
from scenario_model import (full_record_probability, aggregate_stock,
                            hypothetical_weekly_event_range, added_workload_minutes)


class B3WhatIfTests(unittest.TestCase):
    def test_chain_sensitivity(self):
        self.assertAlmostEqual(full_record_probability(.95, .8, 3, .9, .9), .393984)
        self.assertGreater(full_record_probability(.95, .8, 0, .9, .9),
                           full_record_probability(.95, .8, 3, .9, .9))
        self.assertAlmostEqual(full_record_probability(1, 0, 0, 1, 1), 1)
        self.assertEqual(full_record_probability(1, 0, 1, 1, 1), 0)

    def test_limits(self):
        for args in [(-.1, .8, 1, 1, 1), (1, 1.01, 2, 1, 1), (1, 1, -1, 1, 1)]:
            with self.assertRaises(ValueError):
                full_record_probability(*args)

    def test_aggregate_identity(self):
        toy = dict(available=31, issued=9, pending_inspection=2,
                   quarantine=3, external_repair=2, missing_unknown=1, retired=2)
        self.assertEqual(aggregate_stock(toy), (50, 48, 31))
        with self.assertRaises(ValueError):
            aggregate_stock({"available": 5})

    def test_workload(self):
        self.assertEqual(hypothetical_weekly_event_range(20, 22, 2), (40, 44))
        self.assertAlmostEqual(added_workload_minutes(44, 30), 22)
        with self.assertRaises(ValueError):
            added_workload_minutes(-1, 15)


if __name__ == "__main__":
    unittest.main()

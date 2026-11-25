import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('e1', Path(__file__).resolve().parents[1] / 'models/e1/analyze_trial.py')
e1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e1)


def row(run, rec, truth=('STORE', 'HOSTEL', 'USABLE')):
    keys = ('location', 'custodian', 'condition')
    return {'run': run, **{'truth_' + k: v for k, v in zip(keys, truth)}, **{'rec_' + k: v for k, v in zip(keys, rec)}}


class E1Analysis(unittest.TestCase):
    def test_unrecorded_and_wrong_fields_are_not_accountable(self):
        rows = [row('OLD', ('UNRECORDED', 'UNRECORDED', 'UNRECORDED')),
                row('NEW', ('STORE', 'HOSTEL', 'USABLE')),
                row('NEW', ('STORE', 'HOSTEL', 'DAMAGED')),
                row('NEW', ('', '', ''), truth=('', '', ''))]  # blank truth never counts as a match
        acc = e1.accountability(rows)
        self.assertEqual(acc['OLD']['full'], 0)
        self.assertEqual((acc['NEW']['full'], acc['NEW']['n'], acc['NEW']['condition']), (1, 3, 1))

    def test_blank_templates_report_not_measured(self):
        self.assertEqual(e1.accountability(e1.load('e1-audit.csv')), {})
        self.assertIsNone(e1.scans(e1.load('e1-scans.csv')))


if __name__ == '__main__':
    unittest.main()

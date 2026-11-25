"""Static quality checks for B4 specification and source-to-test links.

These tests validate research artifacts only; they are NOT field validation of the
hostel workflow or proof that a prototype meets the acceptance conditions.
"""
import csv
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B4=ROOT/'docs'/'first-principles'
EVIDENCE=ROOT/'docs'/'research'/'phase-a'/'a1-evidence-register.csv'


def load(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def ids(s):
    return [part.strip() for part in s.split(';') if part.strip()]


class B4SpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reqs=load(B4/'b4-requirements-register.csv')
        cls.tests=load(B4/'b4-acceptance-tests.csv')
        cls.traces=load(B4/'b4-evidence-to-requirement-traceability.csv')
        cls.evidence=load(EVIDENCE)
        cls.rids={row['id'] for row in cls.reqs}
        cls.tids={row['test_id'] for row in cls.tests}
        cls.eids={row['evidence_id'] for row in cls.evidence}

    def test_unique_stable_ids(self):
        self.assertEqual(40,len(self.reqs))
        self.assertEqual(40,len(self.rids))
        self.assertEqual(32,len(self.tests))
        self.assertEqual(32,len(self.tids))
        self.assertEqual(12,len(self.traces))
        self.assertEqual({f'B4-R{i:02d}' for i in range(1,41)},self.rids)
        self.assertEqual({f'B4-T{i:02d}' for i in range(1,33)},self.tids)

    def test_requirements_have_provenance_and_verification(self):
        for row in self.reqs:
            with self.subTest(req=row['id']):
                for f in ('group','priority','requirement','source_evidence',
                          'transformer_or_principle','verification','decision_status'):
                    self.assertTrue(row[f].strip(),f'missing {f}')
                self.assertIn(row['priority'],('P0','P1','P2'))
                self.assertIn('Proposed',row['decision_status'])
                for eid in ids(row['source_evidence']):
                    self.assertIn(eid,self.eids)
                for rid in ids(row['depends_on']):
                    self.assertIn(rid,self.rids)
                    self.assertNotEqual(rid,row['id'])

    def test_acceptance_cases_cover_p0_p1(self):
        covered=set()
        for row in self.tests:
            with self.subTest(test=row['test_id']):
                self.assertTrue(row['scenario'] and row['expected_behavior'])
                self.assertEqual('Not executed',row['evidence_status'])
                for rid in ids(row['requirement_ids']):
                    self.assertIn(rid,self.rids)
                    covered.add(rid)
        required={r['id'] for r in self.reqs if r['priority'] in ('P0','P1')}
        self.assertFalse(required-covered, f'unverified key requirements: {sorted(required-covered)}')

    def test_traceability_links_are_valid(self):
        for row in self.traces:
            with self.subTest(trace=row['trace_id']):
                for eid in ids(row['evidence_ids']):
                    self.assertIn(eid,self.eids)
                for rid in ids(row['requirement_ids']):
                    self.assertIn(rid,self.rids)
                for tid in ids(row['test_ids']):
                    self.assertIn(tid,self.tids)

    def test_documents_present(self):
        for name in ('b4-requirements-specification.md',
                     'b4-workflow-and-domain-contracts.md',
                     'b4-decision-register.md','b4-phase-c-handoff.md'):
            self.assertTrue((B4/name).exists())

    def test_primary_metric_and_caution_recorded(self):
        spec=(B4/'b4-requirements-specification.md').read_text(encoding='utf-8')
        self.assertIn('Strict verified equipment accountability',spec)
        self.assertIn('No measured baseline',spec)
        self.assertIn('not an authorized change',spec)
        self.assertIn('No retroactive imputation',spec)

if __name__=='__main__':
    unittest.main()

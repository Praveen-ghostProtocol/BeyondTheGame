"""C1 document contract tests. No prototype/user acceptance tests have been executed."""
from pathlib import Path
import csv, unittest
ROOT=Path(__file__).resolve().parents[1]
DES=ROOT/'docs'/'solution-design'
def read_rows(p):
    with p.open(newline='',encoding='utf8') as f: return list(csv.DictReader(f))
class TestC1DesignCoverage(unittest.TestCase):
    def test_all_40_b4_requirements_mapped_exactly(self):
        a=read_rows(ROOT/'docs'/'first-principles'/'b4-requirements-register.csv')
        b=read_rows(DES/'c1-requirements-coverage.csv')
        self.assertEqual(40,len(a)); self.assertEqual([r['id'] for r in a],[r['requirement_id'] for r in b]);
        for r in b:
            for k in ('alternative_A_candidate_mechanism','alternative_B_candidate_mechanism','alternative_C_candidate_mechanism'):
                self.assertTrue(r[k].strip())
                self.assertIn('not tested',r['evaluation_status'])
    def test_all_32_b4_scenarios_mapped_exactly(self):
        a=read_rows(ROOT/'docs'/'first-principles'/'b4-acceptance-tests.csv')
        b=read_rows(DES/'c1-scenario-design-matrix.csv')
        self.assertEqual(32,len(a)); self.assertEqual([r['test_id'] for r in a],[r['test_id'] for r in b]);
        for r in b:
            for k in ('A_physical_design_response','B_lightweight_design_response','C_integrated_design_response'):
                self.assertTrue(r[k].strip())
            self.assertIn('not executed',r['test_status'])
    def test_design_files_present(self):
        for n in ('c1-concept-development.md','c1-alternative-a-physical.md','c1-alternative-b-lightweight.md','c1-alternative-c-integrated.md','c1-c2-handoff.md'):
            self.assertTrue((DES/n).is_file(), n)
    def test_prototypes_are_explicitly_nonfunctional(self):
        for n in ('a-physical-forms.html','concept-gallery.html'):
            t=(ROOT/'prototypes'/'c1'/n).read_text(encoding='utf-8').lower()
            self.assertIn('no',t)
        t=(ROOT/'prototypes'/'c1'/'concept-gallery.html').read_text().lower()
        self.assertIn('no network request',t)
        self.assertIn('fictional',t)
    def test_no_measured_winner_claim(self):
        t=(DES/'c1-concept-development.md').read_text().lower()
        self.assertIn('none is assumed to win',t)
        self.assertIn('no baseline % has been measured',t)
if __name__=='__main__': unittest.main()

"""Phase C2 contract/analysis checks; synthetic in-memory fixtures, NOT field evidence."""
from pathlib import Path
import csv,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'models'/'c2'))
from evaluate import summarize

class TestC2(unittest.TestCase):
    def test_12_scenarios_linked_to_real_b4_ids(self):
        with (ROOT/'docs'/'solution-design'/'c2-scenario-protocol.csv').open() as f: rows=list(csv.DictReader(f))
        with (ROOT/'docs'/'first-principles'/'b4-acceptance-tests.csv').open() as f: b4={r['test_id'] for r in csv.DictReader(f)}
        self.assertEqual(12,len(rows))
        for r in rows:
            self.assertTrue(set(r['linked_B4_tests'].split(';')).issubset(b4))
    def test_unapproved_weights_sum_100(self):
        with (ROOT/'docs'/'solution-design'/'c2-proposed-criteria.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(100,sum(int(r['proposed_weight_percent_UNAPPROVED']) for r in rows))
    def test_unrun_is_not_zero(self):
        o=summarize([],[])
        self.assertEqual('NOT MEASURED',o['status'])
        for c in 'ABC':
            self.assertIsNone(o['by_concept'][c]['strict_accountability_rate'])
            self.assertIsNone(o['by_concept'][c]['task_success_rate'])
    def test_strict_triad_unknown_in_denominator(self):
        def r(name, vals):
            return {'concept_A_B_C':'A','source_type_OBSERVED_or_SIMULATED':'OBSERVED','eligible_Y_N':'Y',
              **{f'{k}_correct_Y_N_UNKNOWN_CONTRADICTED':v for k,v in zip(('location','custody','condition'),vals)}}
        audits=[r('a',('Y','Y','Y')),r('b',('Y','UNKNOWN','Y')),r('c',('Y','Y','CONTRADICTED'))]
        o=summarize([],audits)['by_concept']['A']
        self.assertEqual((o['eligible_audits'],o['strict_triad_correct'],o['unknown_audit_count'],o['contradicted_audit_count']),(3,1,1,1))
        self.assertAlmostEqual(1/3,o['strict_accountability_rate'])
    def test_simulations_never_become_measured(self):
        trials=[{'concept_A_B_C':'B','source_type_OBSERVED_or_SIMULATED':'SIMULATED','completed_Y_N':'Y','total_seconds':'12'}]
        self.assertEqual('NOT MEASURED',summarize(trials,[])['status'])
    def test_trials_and_setting_filter(self):
        trials=[{'trial_id':'t1','concept_A_B_C':'C','source_type_OBSERVED_or_SIMULATED':'OBSERVED','setting_STAGED_or_LIVE':'STAGED',
                 'completed_Y_N':'Y','total_seconds':'15','student_active_seconds':'7'},
                {'trial_id':'t2','concept_A_B_C':'C','source_type_OBSERVED_or_SIMULATED':'OBSERVED','setting_STAGED_or_LIVE':'STAGED',
                 'completed_Y_N':'N','total_seconds':'40','student_active_seconds':'10'},
                {'trial_id':'t3','concept_A_B_C':'C','source_type_OBSERVED_or_SIMULATED':'OBSERVED','setting_STAGED_or_LIVE':'LIVE',
                 'completed_Y_N':'Y','total_seconds':'30'}]
        a=summarize(trials,[],setting='STAGED')['by_concept']['C']
        self.assertEqual(2,a['observed_trials']);self.assertEqual(0.5,a['task_success_rate'])
        self.assertEqual(15,a['median_completed_total_seconds'])
        self.assertEqual(8.5,a['median_actor_active_seconds']['student'])
    def test_all_templates_header_only(self):
        for fn in ('c2-trial-log.csv','c2-independent-audit.csv','c2-cost-log.csv'):
            t=(ROOT/'data'/'templates'/fn).read_text().splitlines()
            self.assertEqual(1,len(t),f'{fn} has fabricated data lines')
    def test_gates_all_untested(self):
        with (ROOT/'docs'/'solution-design'/'c2-nonnegotiable-gates.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(8,len(rows));self.assertTrue(all(r['status']=='UNTESTED' for r in rows))

if __name__=='__main__':unittest.main()

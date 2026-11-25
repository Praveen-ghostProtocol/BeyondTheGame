"""C4 planning + evidence integrity tests, not performance trials."""
import csv,sys,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'models/c4'))
from prepare_trials import make_plan
from assess_readiness import assess,filtered_evidence,summarize_gates

class TestC4(unittest.TestCase):
    def setUp(self):
        with (ROOT/'docs/solution-design/c2-scenario-protocol.csv').open() as f:
            self.scenarios=[r['scenario_id'] for r in csv.DictReader(f)]
        with (ROOT/'data/templates/c4-gate-evidence.csv').open() as f:
            self.gates=list(csv.DictReader(f))
    def test_12_scenarios_and_216_planned_rows(self):
        rows=make_plan(self.scenarios)
        self.assertEqual(12,len(self.scenarios))
        self.assertEqual(216,len(rows))
        self.assertEqual(216,len({r['planned_trial_id'] for r in rows}))
    def test_counterbalance_each_scenario(self):
        rows=make_plan(self.scenarios)
        for sid in self.scenarios:
            these=[r for r in rows if r['scenario_id']==sid]
            self.assertEqual(18,len(these))
            self.assertEqual({'A':6,'B':6,'C':6},dict(Counter(r['concept_A_B_C'] for r in these)))
            self.assertEqual(6,len({r['order_sequence'] for r in these}))
            for pos in (1,2,3):
                self.assertEqual({'A':2,'B':2,'C':2},dict(Counter(r['concept_A_B_C'] for r in these if r['order_position_1_2_3']==pos)))
    def test_schedule_has_no_fabricated_trials(self):
        with (ROOT/'data/templates/c4-counterbalanced-trial-plan.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertTrue(rows)
        self.assertTrue(all(x['run_status']=='NOT_RUN' and x['study_approval_status']=='NOT_APPROVED' for x in rows))
        self.assertTrue(all(x['participant_code_TO_ASSIGN']=='' for x in rows))
    def test_eight_gates_per_concept_initially_unverified(self):
        self.assertEqual(24,len(self.gates))
        summary,warns=summarize_gates(self.gates)
        self.assertEqual([],warns)
        self.assertEqual([8]*3,[summary[k]['UNTESTED'] for k in 'ABC'])
    def test_unconsented_observation_dropped(self):
        trial={'source_type_OBSERVED_or_SIMULATED':'OBSERVED','trial_id':'TEST1','consent_and_permission_confirmed_Y_N':'N','evidence_reference':'EV1', 'setting_STAGED_or_LIVE':'STAGED','concept_A_B_C':'A'}
        accepted,_,warnings=filtered_evidence([trial],[])
        self.assertEqual([],accepted);self.assertTrue(warnings)
    def test_unreferenced_observation_dropped(self):
        trial={'source_type_OBSERVED_or_SIMULATED':'OBSERVED','trial_id':'TEST1','consent_and_permission_confirmed_Y_N':'Y','evidence_reference':'','setting_STAGED_or_LIVE':'STAGED','concept_A_B_C':'B'}
        accepted,_,warnings=filtered_evidence([trial],[])
        self.assertEqual([],accepted);self.assertTrue(warnings)
    def test_synthetic_simulation_never_measured(self):
        trial={'source_type_OBSERVED_or_SIMULATED':'SIMULATED','trial_id':'SYN1','consent_and_permission_confirmed_Y_N':'Y','evidence_reference':'SYN1','setting_STAGED_or_LIVE':'STAGED','concept_A_B_C':'A','completed_Y_N':'Y'}
        r=assess([trial],[],self.gates)
        self.assertEqual('NOT MEASURED',r['valid_observed_staged']['status'])
        self.assertTrue(all(not r['selection_readiness'][c]['ready_for_owner_selection'] for c in 'ABC'))
    def test_audit_requires_independent_evidence(self):
        audit={'source_type_OBSERVED_or_SIMULATED':'OBSERVED','audit_id':'T1','eligible_Y_N':'Y','concept_A_B_C':'C','setting_STAGED_or_LIVE':'LIVE','independent_checker_code':'','ground_truth_evidence_reference':'EV'}
        _,accepted,warnings=filtered_evidence([],[audit])
        self.assertEqual([],accepted);self.assertTrue(warnings)
    def test_gate_pass_without_evidence_downgraded(self):
        edited=[dict(row) for row in self.gates]
        edited[0]['status']='PASS'
        d,w=summarize_gates(edited)
        self.assertEqual(8,d['A']['UNTESTED']);self.assertTrue(w)
    def test_full_research_protocol_exists(self):
        for f in ('c4-controlled-trials-playbook.md','c4-owner-approval-batch.md','c4-design-review-and-provisional-selection.md','c4-c5-handoff.md'):
            self.assertTrue((ROOT/'docs/solution-design'/f).exists())

if __name__=='__main__':unittest.main()

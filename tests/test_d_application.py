"""Synthetic software tests against isolated SQLite DBs; not hostel field trials."""
import concurrent.futures
import hashlib
import http.client
import json
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from domain import KINDS, Problem, Store, analytics, now
from security import authenticate, create_user, password_hash, session
from server import Server, seed_demo
from http_transport import request as protocol_request

PASSWORD = 'synthetic-test-only-phrase'
HASH = password_hash(PASSWORD)


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'test.sqlite3')
        self.users = {}
        with self.store.transaction() as db:
            for role in ('admin', 'secretary', 'student', 'captain', 'checker', 'guard', 'maintenance', 'office'):
                user = {'id': 'TEST-' + role, 'username': role, 'role': role}
                self.users[role] = user
                db.execute('INSERT INTO users VALUES(?,?,?,?,1,?)', (user['id'], role, HASH, role, now()))
        self.sec = self.users['secretary']
        self.student = self.users['student']
        self.checker = self.users['checker']

    def tearDown(self):
        self.tmp.cleanup()

    def cmd(self, action, p, user=None, key=None):
        return self.store.command(user or self.sec, action, p, key or uuid.uuid4().hex)

    def get(self, kind, rid):
        with self.store.connect() as db:
            return self.store.get(db, kind, rid)

    def asset(self, aid='TEST-A', condition='USABLE'):
        return self.cmd('asset_create', {'id': aid, 'name': 'Synthetic racket', 'sport': 'Badminton', 'condition': condition})

    def request(self, ids=None, user=None, kit=None):
        return self.cmd('request_create', {'assets': ids or ['TEST-A'], 'purpose': 'Synthetic practice',
            'kit_id': kit, 'team': 'TEST-TEAM' if kit else None,
            'due_at': (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()}, user or self.student)

    def pickup(self, ids=None, user=None):
        user = user or self.student
        r = self.request(ids, user)
        return self.cmd('pickup', {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}, user)

    def receive(self, loan, ids=None):
        return self.cmd('return_receive', {'id': loan['id'], 'version': loan['version'], 'assets': ids or loan['remaining'],
            'physical_confirmed': True}, self.checker)

    def policy(self):
        p = self.get('settings', 'policy')
        return self.cmd('policy_update', {'version': p['version'], 'reference': 'SYNTHETIC OFFICE POLICY',
            'threshold_paise': 1000000, 'policy_confirmed': True, 'ordinary_self_pickup': True}, self.users['office'])

    def purchase(self, amount=3000000, quantity=2):
        return self.cmd('purchase_create', {'name': 'Synthetic bat', 'sport': 'Cricket', 'quantity': quantity,
            'amount_paise': amount, 'rationale': 'Synthetic need; not a real purchase'})

    def quotes(self, pr, n=3):
        for i in range(n):
            pr = self.cmd('purchase_quote', {'id': pr['id'], 'version': pr['version'], 'vendor': 'TEST-VENDOR-' + str(i),
                'amount_paise': 3000000, 'reference': 'SYNTHETIC-QUOTE'})
        return pr

    def approve_and_pay(self, pr):
        for _ in range(2):
            pr = self.cmd('purchase_advance', {'id': pr['id'], 'version': pr['version'], 'reference': 'SYNTHETIC AUTHORITY'}, self.users['office'])
        return pr

    def test_unknown_initial_condition_not_available(self):
        self.assertEqual('INSPECTION', self.asset(condition='UNKNOWN')['status'])

    def test_duplicate_permanent_identity_rejected(self):
        self.asset()
        with self.assertRaises(Problem): self.asset()

    def test_student_cannot_register_retire_or_edit_policy(self):
        a = self.asset()
        for action, p in [('asset_create', {'id': 'BAD'}), ('retire', {'id': a['id'], 'version': a['version'], 'reason': 'test'}),
                          ('policy_update', {'version': 1})]:
            with self.assertRaises(Problem) as err: self.cmd(action, p, self.student)
            self.assertEqual(403, err.exception.status)

    def test_request_permission_does_not_move_item(self):
        self.asset(); r = self.request()
        self.assertEqual('APPROVED', r['status'])
        self.assertEqual('STORE', self.get('assets', 'TEST-A')['custodian'])
        self.assertEqual('AVAILABLE', self.get('assets', 'TEST-A')['status'])

    def test_physical_confirmation_required(self):
        self.asset(); r = self.request()
        with self.assertRaises(Problem): self.cmd('pickup', {'id': r['id'], 'version': r['version']}, self.student)

    def test_atomic_concurrent_pickup_exactly_one_wins(self):
        self.asset()
        requests = [self.request(user=u) for u in (self.student, self.users['captain'])]
        def attempt(pair):
            r, u = pair
            try:
                self.cmd('pickup', {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}, u)
                return True
            except Problem: return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            results = list(ex.map(attempt, zip(requests, [self.student, self.users['captain']])))
        self.assertEqual(1, sum(results))
        self.assertEqual(1, self.store.snapshot(self.sec)['metrics']['active_loans'])

    def test_replayed_pickup_same_key_does_not_double_issue(self):
        self.asset(); r = self.request(); key = uuid.uuid4().hex
        p = {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}
        one = self.cmd('pickup', p, self.student, key)
        two = self.cmd('pickup', p, self.student, key)
        self.assertEqual(one, two)
        self.assertEqual(1, self.store.snapshot(self.sec)['metrics']['active_loans'])

    def test_idempotency_key_bound_to_payload(self):
        self.asset(); key = uuid.uuid4().hex
        self.cmd('damage_report', {'asset_id': 'TEST-A', 'description': 'Synthetic'}, self.student, key)
        with self.assertRaises(Problem) as err:
            self.cmd('damage_report', {'asset_id': 'TEST-A', 'description': 'Different'}, self.student, key)
        self.assertEqual(409, err.exception.status)

    def test_return_declaration_keeps_custody_and_not_available(self):
        self.asset(); loan = self.pickup()
        self.cmd('return_report', {'id': loan['id'], 'version': loan['version'], 'assets': ['TEST-A']}, self.student)
        a = self.get('assets', 'TEST-A')
        self.assertEqual('ISSUED', a['status']); self.assertEqual(self.student['id'], a['custodian'])
        self.assertTrue(a['return_reported'])

    def test_key_return_does_not_close_equipment_loan(self):
        self.asset(); loan = self.pickup()
        k = self.cmd('key_out', {'borrower': self.student['id']}, self.users['guard'])
        self.cmd('key_back', {'id': k['id'], 'version': k['version']}, self.users['guard'])
        self.assertEqual(['TEST-A'], self.get('loans', loan['id'])['remaining'])
        self.assertEqual('ISSUED', self.get('assets', 'TEST-A')['status'])

    def test_partial_kit_return_keeps_only_missing_outstanding(self):
        self.asset(); self.asset('TEST-B')
        kit = self.cmd('kit_create', {'id': 'TEST-KIT', 'name': 'Synthetic kit', 'sport': 'Cricket', 'assets': ['TEST-A', 'TEST-B'], 'lots': []})
        captain = self.users['captain']; r = self.request(user=captain, kit=kit['id'])
        self.assertEqual('REQUESTED', r['status'])
        r = self.cmd('request_approve', {'id': r['id'], 'version': r['version']})
        l = self.cmd('pickup', {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}, captain)
        l = self.receive(l, ['TEST-A'])
        self.assertEqual('PARTIAL', l['status']); self.assertEqual(['TEST-B'], l['remaining'])
        self.assertEqual('INSPECTION', self.get('assets', 'TEST-A')['status'])
        self.assertEqual('ISSUED', self.get('assets', 'TEST-B')['status'])

    def test_unavailable_kit_rolls_back_all_components_and_lots(self):
        self.asset(); self.asset('TEST-B', 'DAMAGED')
        self.cmd('lot_create', {'id': 'TEST-LOT', 'name': 'Shuttle', 'sport': 'Badminton', 'unit': 'pieces', 'quantity': 4})
        kit = self.cmd('kit_create', {'id': 'TEST-KIT', 'name': 'Synthetic', 'sport': 'Cricket', 'assets': ['TEST-A', 'TEST-B'], 'lots': [{'id': 'TEST-LOT', 'quantity': 2}]})
        r = self.request(user=self.users['captain'], kit=kit['id'])
        r = self.cmd('request_approve', {'id': r['id'], 'version': r['version']})
        with self.assertRaises(Problem): self.cmd('pickup', {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}, self.users['captain'])
        self.assertEqual('AVAILABLE', self.get('assets', 'TEST-A')['status'])
        self.assertEqual(4, self.get('lots', 'TEST-LOT')['quantity'])

    def test_consumable_negative_balance_rejected(self):
        l = self.cmd('lot_create', {'id': 'TEST-LOT', 'name': 'Shuttle', 'sport': 'Badminton', 'unit': 'pieces', 'quantity': 10})
        l = self.cmd('lot_adjust', {'id': l['id'], 'version': l['version'], 'delta': -3, 'reason': 'Synthetic use'})
        self.assertEqual(7, l['quantity'])
        with self.assertRaises(Problem): self.cmd('lot_adjust', {'id': l['id'], 'version': l['version'], 'delta': -8, 'reason': 'Synthetic use'})

    def test_borrower_cannot_receive_own_equipment(self):
        self.asset(); captain = self.users['captain']; loan = self.pickup(user=captain)
        with self.assertRaises(Problem): self.cmd('return_receive', {'id': loan['id'], 'version': loan['version'], 'assets': ['TEST-A'], 'physical_confirmed': True}, captain)

    def test_inspection_separate_from_receipt(self):
        self.asset(); l = self.pickup(); self.receive(l)
        a = self.get('assets', 'TEST-A'); self.assertEqual('INSPECTION', a['status'])
        a = self.cmd('inspect', {'id': a['id'], 'version': a['version'], 'condition': 'USABLE', 'notes': 'Synthetic condition check'}, self.checker)
        self.assertEqual('AVAILABLE', a['status'])

    def test_guard_has_no_condition_inspection_permission(self):
        a = self.asset(condition='UNKNOWN')
        with self.assertRaises(Problem) as e: self.cmd('inspect', {'id': a['id'], 'version': a['version'], 'condition': 'USABLE', 'notes': 'test'}, self.users['guard'])
        self.assertEqual(403, e.exception.status)

    def test_damage_preserves_actual_custody_and_unknown_fault(self):
        self.asset(); l = self.pickup(); old = self.get('assets', 'TEST-A')
        d = self.cmd('damage_report', {'asset_id': 'TEST-A', 'description': 'Synthetic break'}, self.student)
        a = self.get('assets', 'TEST-A')
        for k in ('custodian', 'location', 'loan_id'): self.assertEqual(old[k], a[k])
        self.assertEqual('QUARANTINE', a['status']); self.assertIsNone(d['occurrence_at']); self.assertEqual('NOT_INFERRED', d['blame'])
        self.assertEqual(['TEST-A'], self.get('loans', l['id'])['remaining'])

    def test_unidentified_damage_report_does_not_invent_asset(self):
        d = self.cmd('damage_report', {'description': 'Synthetic unknown racket'}, self.student)
        self.assertIsNone(d['asset_id']); self.assertEqual(0, self.store.snapshot(self.sec)['metrics']['total'])

    def test_repair_chain_requires_return_and_reinspection(self):
        a = self.asset(condition='DAMAGED')
        r = self.cmd('repair_create', {'asset_id': a['id'], 'version': a['version'], 'assessment': 'Synthetic damage', 'vendor': 'TEST-SHOP', 'cost_paise': 50000})
        for expected in ('APPROVED', 'AT_VENDOR', 'REPAIRED', 'RECEIVED'):
            r = self.cmd('repair_advance', {'id': r['id'], 'version': r['version'], 'reference': 'SYNTHETIC'})
            self.assertEqual(expected, r['stage'])
        a = self.get('assets', a['id']); self.assertEqual('INSPECTION', a['status'])
        self.cmd('inspect', {'id': a['id'], 'version': a['version'], 'condition': 'USABLE', 'notes': 'Synthetic reinspection'}, self.checker)
        self.assertEqual('CLOSED', self.get('repairs', r['id'])['stage'])

    def test_no_vendor_handoff_for_outstanding_borrowing(self):
        self.asset(); self.pickup(); self.cmd('damage_report', {'asset_id': 'TEST-A', 'description': 'Synthetic'}, self.student)
        a = self.get('assets', 'TEST-A')
        with self.assertRaises(Problem): self.cmd('repair_create', {'asset_id': a['id'], 'version': a['version'], 'assessment': 'Synthetic', 'vendor': 'TEST', 'cost_paise': 0})

    def test_maintenance_worker_cannot_approve_repair(self):
        a = self.asset(condition='DAMAGED')
        r = self.cmd('repair_create', {'asset_id': a['id'], 'version': a['version'], 'assessment': 'Synthetic', 'vendor': 'TEST', 'cost_paise': 0})
        with self.assertRaises(Problem): self.cmd('repair_advance', {'id': r['id'], 'version': r['version'], 'reference': 'test'}, self.users['maintenance'])

    def test_retired_not_in_active_stock_or_checkout(self):
        a = self.asset()
        self.cmd('retire', {'id': a['id'], 'version': a['version'], 'reason': 'Synthetic retirement'})
        r = self.request()
        with self.assertRaises(Problem): self.cmd('pickup', {'id': r['id'], 'version': r['version'], 'physical_confirmed': True}, self.student)
        self.assertEqual(0, self.store.snapshot(self.sec)['metrics']['categories'][0]['active'])

    def test_procurement_unconfirmed_policy_blocks_approval(self):
        pr = self.quotes(self.purchase())
        with self.assertRaises(Problem): self.cmd('purchase_advance', {'id': pr['id'], 'version': pr['version'], 'reference': 'TEST'}, self.users['office'])

    def test_three_distinct_quotes_required_at_threshold(self):
        self.policy(); pr = self.quotes(self.purchase(amount=1000000), 2)
        with self.assertRaises(Problem): self.cmd('purchase_advance', {'id': pr['id'], 'version': pr['version'], 'reference': 'TEST'}, self.users['office'])
        with self.assertRaises(Problem): self.cmd('purchase_quote', {'id': pr['id'], 'version': pr['version'], 'vendor': 'test-vendor-0', 'amount_paise': 5, 'reference': 'test'})

    def test_low_value_route_and_no_auto_payment(self):
        self.policy(); pr = self.quotes(self.purchase(amount=950000), 1)
        pr = self.cmd('purchase_advance', {'id': pr['id'], 'version': pr['version'], 'reference': 'SYNTHETIC OFFICE'}, self.users['office'])
        self.assertEqual('APPROVED', pr['stage']); self.assertEqual('REIMBURSEMENT', pr['route'])
        self.assertEqual(0, self.store.snapshot(self.sec)['metrics']['total'])

    def test_secretary_cannot_approve_financial_action(self):
        self.policy(); pr = self.quotes(self.purchase())
        with self.assertRaises(Problem) as e: self.cmd('purchase_advance', {'id': pr['id'], 'version': pr['version'], 'reference': 'TEST'})
        self.assertEqual(403, e.exception.status)

    def test_partial_procurement_receipt_only_enrolls_received_items(self):
        self.policy(); pr = self.approve_and_pay(self.quotes(self.purchase()))
        self.assertEqual(0, self.store.snapshot(self.sec)['metrics']['total'])
        pr = self.cmd('purchase_receive', {'id': pr['id'], 'version': pr['version'], 'quantity': 1,
            'asset_ids': ['RECEIPT-A'], 'physical_confirmed': True})
        self.assertEqual('PARTIAL_RECEIPT', pr['stage']); self.assertEqual(1, pr['received'])
        self.assertEqual('INSPECTION', self.get('assets', 'RECEIPT-A')['status'])

    def test_procurement_duplicate_id_rolls_back_entire_receipt(self):
        self.asset(); self.policy(); pr = self.approve_and_pay(self.quotes(self.purchase()))
        with self.assertRaises(Problem): self.cmd('purchase_receive', {'id': pr['id'], 'version': pr['version'], 'quantity': 2,
            'asset_ids': ['RECEIPT-A', 'TEST-A'], 'physical_confirmed': True})
        self.assertEqual(0, self.get('purchases', pr['id'])['received'])
        with self.assertRaises(Problem): self.get('assets', 'RECEIPT-A')

    def test_two_party_transfer_acceptance_changes_custody_only_after_accept(self):
        self.asset(); l = self.pickup(); recipient = self.users['captain']
        tr = self.cmd('transfer_offer', {'id': l['id'], 'version': l['version'], 'to': recipient['id'], 'location': 'TEST-ROOM'}, self.student)
        self.assertEqual(self.student['id'], self.get('assets', 'TEST-A')['custodian'])
        self.cmd('transfer_accept', {'id': tr['id'], 'version': tr['version'], 'physical_confirmed': True}, recipient)
        self.assertEqual(recipient['id'], self.get('assets', 'TEST-A')['custodian'])
        self.assertEqual(recipient['id'], self.get('loans', l['id'])['borrower'])

    def test_team_component_transfer_preserves_remaining_manifest(self):
        self.asset(); self.asset('TEST-B'); captain = self.users['captain']
        l = self.pickup(['TEST-A', 'TEST-B'], captain)
        tr = self.cmd('transfer_offer', {'id': l['id'], 'version': l['version'], 'to': self.student['id'],
            'assets': ['TEST-A'], 'location': 'TEST-ROOM'}, captain)
        self.cmd('transfer_accept', {'id': tr['id'], 'version': tr['version'], 'physical_confirmed': True}, self.student)
        self.assertEqual(['TEST-B'], self.get('loans', l['id'])['remaining'])
        self.assertEqual(captain['id'], self.get('assets', 'TEST-B')['custodian'])
        self.assertEqual(self.student['id'], self.get('assets', 'TEST-A')['custodian'])

    def test_offline_conflict_does_not_overwrite_asset(self):
        a = self.asset()
        c = self.cmd('conflict_record', {'asset_id': a['id'], 'description': 'Synthetic offline handover'}, self.student)
        self.assertEqual('PENDING', c['status']); self.assertEqual(a, self.get('assets', a['id']))

    def test_stale_version_prevents_silent_correction(self):
        a = self.asset()
        self.cmd('asset_correct', {'id': a['id'], 'version': a['version'], 'location': 'TEST-RACK', 'reason': 'Synthetic correction'})
        with self.assertRaises(Problem) as err: self.cmd('asset_correct', {'id': a['id'], 'version': a['version'], 'location': 'OTHER', 'reason': 'Stale'})
        self.assertEqual(409, err.exception.status)

    def test_event_history_append_only_and_correction_keeps_before(self):
        a = self.asset()
        self.cmd('asset_correct', {'id': a['id'], 'version': a['version'], 'location': 'TEST-RACK', 'reason': 'Synthetic correction'})
        with self.store.connect() as db:
            event = db.execute("SELECT detail FROM events WHERE action='correction_evidence'").fetchone()
            self.assertEqual('SPORTS_ROOM', json.loads(event[0])['before']['location'])
            with self.assertRaises(sqlite3.IntegrityError): db.execute('DELETE FROM events')

    def test_student_snapshot_excludes_other_borrowers_and_finance(self):
        self.asset(); self.pickup(user=self.users['captain']); self.purchase()
        s = self.store.snapshot(self.student)['data']
        self.assertEqual([], s['loans']); self.assertEqual([], s['purchases']); self.assertEqual([], s['users'])
        self.assertNotIn(self.users['captain']['id'], json.dumps(s['assets']))
        self.assertNotIn('last_actor', s['assets'][0])

    def test_strict_accountability_unknowns_in_denominator(self):
        sample = {k: [] for k in KINDS}
        obs = [{'unknown': False, 'matches': dict.fromkeys(('location','custodian','condition'), True)} for _ in range(6)]
        obs += [{'unknown': True, 'matches': dict.fromkeys(('location','custodian','condition'), False)} for _ in range(2)]
        obs += [{'unknown': False, 'matches': {'location': True, 'custodian': False, 'condition': True}} for _ in range(2)]
        sample['audits'] = [{'id': 'TEST-AUDIT', 'status': 'CLOSED', 'provenance': 'FIELD_CLAIM_REQUIRES_INDEPENDENT_CHECK',
            'snapshots': [{}] * 10, 'observations': obs, 'snapshot_at': now(), 'method': 'Synthetic arithmetic fixture'}]
        a = analytics(sample)['accountability']
        self.assertEqual(.6, a['rate']); self.assertEqual(10, a['denominator']); self.assertEqual(2, a['unknown']); self.assertEqual(2, a['contradicted'])

    def test_demo_audit_never_counts_as_field_accountability(self):
        sample = {k: [] for k in KINDS}
        sample['audits'] = [{'status': 'CLOSED', 'provenance': 'SIMULATED'}]
        self.assertEqual('NOT MEASURED', analytics(sample)['accountability']['status'])

    def test_audit_requires_independent_checker(self):
        self.asset()
        audit = self.cmd('audit_start', {'assets': ['TEST-A'], 'method': 'Synthetic'}, self.checker)
        with self.assertRaises(Problem) as e: self.cmd('audit_observe', {'id': audit['id'], 'version': audit['version'], 'asset_id': 'TEST-A',
            'location': 'SPORTS_ROOM', 'custodian': 'STORE', 'condition': 'USABLE', 'reference': 'TEST'}, self.sec)
        self.assertEqual(403, e.exception.status)

    def test_audit_full_path_and_no_inventory_overwrite(self):
        a = self.asset()
        audit = self.cmd('audit_start', {'assets': ['TEST-A'], 'method': 'Synthetic fixed sample'}, self.checker)
        audit = self.cmd('audit_observe', {'id': audit['id'], 'version': audit['version'], 'asset_id': 'TEST-A',
            'location': 'SPORTS_ROOM', 'custodian': 'STORE', 'condition': 'USABLE', 'reference': 'SYNTHETIC EVIDENCE'}, self.checker)
        self.cmd('audit_close', {'id': audit['id'], 'version': audit['version']}, self.checker)
        self.assertEqual(1.0, self.store.snapshot(self.sec)['metrics']['accountability']['rate'])
        self.assertEqual(a, self.get('assets', a['id']))

    def test_audit_moving_item_invalidates_snapshot(self):
        self.asset()
        audit = self.cmd('audit_start', {'assets': ['TEST-A'], 'method': 'Synthetic sample'}, self.checker)
        self.pickup()
        with self.assertRaises(Problem) as e: self.cmd('audit_observe', {'id': audit['id'], 'version': audit['version'], 'asset_id': 'TEST-A',
            'location': 'SPORTS_ROOM', 'custodian': 'STORE', 'condition': 'USABLE', 'reference': 'TEST'}, self.checker)
        self.assertEqual(409, e.exception.status)

    def test_incomplete_audit_cannot_drop_denominator(self):
        self.asset()
        a = self.cmd('audit_start', {'assets': ['TEST-A'], 'method': 'Synthetic'}, self.checker)
        with self.assertRaises(Problem): self.cmd('audit_close', {'id': a['id'], 'version': a['version']}, self.checker)

    def test_invalidated_account_cannot_mutate(self):
        with self.store.transaction() as db: db.execute('UPDATE users SET active=0 WHERE id=?', (self.student['id'],))
        with self.assertRaises(Problem) as e: self.cmd('damage_report', {'description': 'Test'}, self.student)
        self.assertEqual(401, e.exception.status)

    def test_persistence_reopen_and_no_seed_reset(self):
        self.asset()
        reopened = Store(self.store.path)
        self.assertEqual(1, reopened.snapshot(self.sec)['metrics']['total'])

    def test_category_denominators(self):
        sample = {k: [] for k in KINDS}
        sample['assets'] = [{'sport':'Badminton','status':'QUARANTINE' if i<2 else 'AVAILABLE'} for i in range(10)]
        sample['assets'] += [{'sport':'Football','status':'QUARANTINE' if i<3 else 'AVAILABLE'} for i in range(100)]
        m = analytics(sample)
        self.assertEqual([.2,.03], [c['unusable_share'] for c in m['categories']])
        self.assertTrue(m['reconciles'])

    def test_attribute_evidence_stays_independent_on_damage(self):
        self.asset(); self.pickup()
        before = self.get('assets', 'TEST-A')
        self.cmd('damage_report', {'asset_id': 'TEST-A', 'description': 'Synthetic'}, self.student)
        after = self.get('assets', 'TEST-A')
        self.assertEqual(before['evidence']['location'], after['evidence']['location'])
        self.assertEqual(before['evidence']['custodian'], after['evidence']['custodian'])
        self.assertNotEqual(before['evidence']['condition']['recorded_at'], after['evidence']['condition']['recorded_at'])

    def test_failed_repair_can_be_reassessed_without_restoring_stock(self):
        a = self.asset(condition='DAMAGED')
        r = self.cmd('repair_create', {'asset_id': a['id'], 'version': a['version'], 'assessment': 'Synthetic', 'vendor': 'TEST-SHOP', 'cost_paise': 0})
        for _ in range(4): r = self.cmd('repair_advance', {'id': r['id'], 'version': r['version'], 'reference': 'SYNTHETIC'})
        a = self.get('assets', a['id'])
        self.cmd('inspect', {'id': a['id'], 'version': a['version'], 'condition': 'DAMAGED', 'notes': 'Synthetic failure'}, self.checker)
        r = self.get('repairs', r['id']); self.assertEqual('REASSESS', r['stage'])
        r = self.cmd('repair_reassess', {'id': r['id'], 'version': r['version'], 'reason': 'Synthetic second assessment'})
        self.assertEqual('ASSESSED', r['stage']); self.assertEqual('QUARANTINE', self.get('assets', a['id'])['status'])

    def test_malformed_component_ids_rejected_without_type_error(self):
        with self.assertRaises(Problem) as e:
            self.cmd('request_create', {'assets': [{}]}, self.student)
        self.assertEqual(400, e.exception.status)

    def test_one_physical_key_cannot_be_handed_out_twice(self):
        self.cmd('key_out', {'borrower': self.student['id'], 'key_code': 'TEST-KEY'}, self.users['guard'])
        with self.assertRaises(Problem) as e:
            self.cmd('key_out', {'borrower': self.users['captain']['id'], 'key_code': 'TEST-KEY'}, self.users['guard'])
        self.assertEqual(409, e.exception.status)


class HTTPTests(DomainTests):
    # Reuse fixture/helpers, not the entire inherited domain test catalogue.
    def setUp(self):
        super().setUp()
        self.cookie = ''; self.csrf = ''

    def tearDown(self):
        super().tearDown()

    def http(self, path, payload=None, headers=None, method=None):
        h = {'Cookie': self.cookie, 'X-CSRF-Token': self.csrf, 'Content-Type':'application/json', **(headers or {})}
        status, hdr, body = protocol_request(self.store, method or ('POST' if payload is not None else 'GET'),
            path, json.dumps(payload).encode() if payload is not None else b'', h)
        return status, hdr, json.loads(body) if hdr.get('Content-Type','').startswith('application/json') else body

    def sign_in(self, role='student'):
        status, headers, body = self.http('/api/login', {'username': role, 'password': PASSWORD})
        self.assertEqual(200, status)
        self.cookie = headers['Set-Cookie'].split(';')[0]; self.csrf = body['csrf']

    def test_http_unauthenticated_and_private_paths(self):
        self.assertEqual(401, self.http('/api/state')[0])
        for path in ('/private/live.sqlite3', '/server.py', '/../schema.sql', '/.env'):
            self.assertEqual(404, self.http(path)[0])

    def test_http_csrf_and_cross_origin(self):
        self.sign_in()
        self.assertEqual(403, self.http('/api/command', {'action':'damage_report','payload':{'description':'Test'}}, {'X-CSRF-Token':''})[0])
        self.assertEqual(403, self.http('/api/command', {}, {'Origin':'https://untrusted.invalid'})[0])

    def test_http_cookie_and_csp(self):
        status, h, _ = self.http('/api/login', {'username':'student','password':PASSWORD})
        self.assertEqual(200, status); self.assertIn('HttpOnly', h['Set-Cookie']); self.assertIn('SameSite=Strict', h['Set-Cookie'])
        self.assertIn("default-src 'self'", h['Content-Security-Policy'])
        self.assertEqual('DENY', h['X-Frame-Options'])

    def test_http_authentication_rate_limit(self):
        for _ in range(8): self.assertEqual(401, self.http('/api/login', {'username':'not-a-user','password':'wrong'})[0])
        self.assertEqual(429, self.http('/api/login', {'username':'not-a-user','password':'wrong'})[0])

    def test_http_logout_revokes_token(self):
        self.sign_in(); self.assertEqual(200, self.http('/api/state')[0])
        self.assertEqual(200, self.http('/api/logout', {})[0]); self.assertEqual(401, self.http('/api/state')[0])

    def test_http_student_cannot_create_account(self):
        self.sign_in()
        self.assertEqual(403, self.http('/api/users', {'username':'attacker','password':PASSWORD,'role':'admin'})[0])

    def test_http_admin_creates_and_disables_account(self):
        self.sign_in('admin')
        s, _, u = self.http('/api/users', {'username':'test-resident','password':PASSWORD,'role':'student'})
        self.assertEqual(201, s)
        self.assertEqual(200, self.http('/api/users/update', {'id':u['id'],'role':'student','active':False})[0])
        self.assertEqual(401, self.http('/api/login', {'username':'test-resident','password':PASSWORD})[0])

    def test_http_password_change_revokes_sessions(self):
        self.sign_in()
        self.assertEqual(200, self.http('/api/account', {'current_password':PASSWORD,'password':'changed-synthetic-phrase'})[0])
        self.assertEqual(401, self.http('/api/state')[0])

    def test_http_public_export_whitelist(self):
        self.asset(); self.pickup(); self.sign_in('secretary')
        s, _, out = self.http('/api/export/aggregates')
        self.assertEqual(200, s)
        content = json.dumps(out)
        for value in ('TEST-student', 'TEST-secretary', 'username', 'password', 'loans', 'purpose'):
            self.assertNotIn(value, content)

    def test_http_real_command_end_to_end(self):
        self.asset(); self.sign_in()
        s, _, out = self.http('/api/command', {'action':'damage_report', 'payload':{'asset_id':'TEST-A','description':'Synthetic HTTP test'}}, {'Idempotency-Key':uuid.uuid4().hex})
        self.assertEqual(200, s); self.assertEqual('NOT_INFERRED', out['result']['blame'])
        self.assertEqual('QUARANTINE', self.get('assets','TEST-A')['status'])


# Avoid rerunning DomainTests via inheritance in the HTTP fixture class.
for _name in list(DomainTests.__dict__):
    if _name.startswith('test_'):
        setattr(HTTPTests, _name, None)


if __name__ == '__main__':
    unittest.main()

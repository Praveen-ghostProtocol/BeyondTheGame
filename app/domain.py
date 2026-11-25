"""Phase D domain service. All commands execute in one SQLite write transaction.

Implements B4 state/custody contracts and C4 owner policy; C3 remains an
independent synthetic regression model, never imported as an auth backend.
"""
import hashlib
import json
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROLES = {'admin', 'secretary', 'student', 'captain', 'checker', 'guard', 'maintenance', 'office'}
MANAGERS = {'admin', 'secretary'}
CHECKERS = MANAGERS | {'checker', 'captain'}
STATES = {'AVAILABLE', 'ISSUED', 'INSPECTION', 'QUARANTINE', 'REPAIR', 'UNKNOWN', 'RETIRED'}
CONDITIONS = {'USABLE', 'DAMAGED', 'UNKNOWN', 'REPAIR', 'RETIRED'}
KINDS = ('assets', 'lots', 'kits', 'requests', 'loans', 'transfers', 'damage', 'repairs',
         'purchases', 'keys', 'audits', 'conflicts', 'settings')


class Connection(sqlite3.Connection):
    """SQLite's default context commits but does not close; close deterministically."""
    def __exit__(self, *args):
        try:
            return super().__exit__(*args)
        finally:
            self.close()


class Problem(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def need(ok, message, status=400):
    if not ok:
        raise Problem(message, status)


def now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def text(p, key, default=None):
    value = p.get(key, default)
    need(isinstance(value, str) and 0 < len(value.strip()) <= 1500, f'{key} is required (maximum 1500 characters)')
    return value.strip()


def integer(p, key, minimum=1):
    value = p.get(key)
    need(type(value) is int and minimum <= value <= 100000000, f'{key} must be an integer >= {minimum}')
    return value


def ident(value):
    need(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value), 'Use an ID of 1–64 letters, digits, underscores or hyphens')
    return value


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript(Path(__file__).with_name('schema.sql').read_text())
            db.execute("INSERT OR IGNORE INTO meta VALUES('schema_version','1')")
            db.execute("INSERT OR IGNORE INTO meta VALUES('mode','LIVE')")
            db.execute("INSERT OR IGNORE INTO records VALUES('settings','policy',?,1,?)", (json.dumps({
                'threshold_paise': 1000000, 'policy_confirmed': False,
                'facility': 'Alaknanda Hostel', 'ordinary_self_pickup': True,
                'loan_hours': 24, 'audit_stale_hours': 168}), now()))

    def connect(self):
        db = sqlite3.connect(self.path, timeout=15, factory=Connection)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('PRAGMA synchronous=FULL')
        return db

    @contextmanager
    def transaction(self):
        db = self.connect()
        try:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get(self, db, kind, rid):
        row = db.execute('SELECT * FROM records WHERE kind=? AND id=?', (kind, rid)).fetchone()
        need(row is not None, f'{kind}: record not found', 404)
        return {**json.loads(row['data']), 'id': row['id'], 'version': row['version'], 'updated_at': row['updated_at']}

    def all(self, db, kind):
        return [{**json.loads(r['data']), 'id': r['id'], 'version': r['version'], 'updated_at': r['updated_at']}
                for r in db.execute('SELECT * FROM records WHERE kind=? ORDER BY updated_at DESC,id', (kind,))]

    def save(self, db, kind, obj, create=False):
        obj = dict(obj)
        rid = obj.pop('id', None) or kind[:3].upper() + '-' + uuid.uuid4().hex[:12]
        ident(rid)
        obj.pop('version', None)
        obj.pop('updated_at', None)
        if kind == 'assets':
            prior = db.execute("SELECT data FROM records WHERE kind='assets' AND id=?", (rid,)).fetchone()
            before = json.loads(prior[0]) if prior else {}
            evidence = dict(obj.get('evidence', before.get('evidence', {})))
            for attribute in ('location', 'custodian', 'condition'):
                if create or obj.get(attribute) != before.get(attribute):
                    evidence[attribute] = {'recorded_at': now(), 'actor': obj.get('last_actor'),
                        'source': obj.get('source', 'OPERATOR_RECORDED'), 'confidence': obj.get('verification', 'REPORTED')}
            obj['evidence'] = evidence
        if create:
            need(not db.execute('SELECT 1 FROM records WHERE kind=? AND id=?', (kind, rid)).fetchone(), 'ID already registered', 409)
            db.execute('INSERT INTO records VALUES(?,?,?,1,?)', (kind, rid, json.dumps(obj), now()))
        else:
            cur = db.execute('UPDATE records SET data=?,version=version+1,updated_at=? WHERE kind=? AND id=?',
                             (json.dumps(obj), now(), kind, rid))
            need(cur.rowcount == 1, 'Record not found', 404)
        return self.get(db, kind, rid)

    def event(self, db, user, action, target, detail):
        mode = db.execute("SELECT value FROM meta WHERE key='mode'").fetchone()[0]
        db.execute('INSERT INTO events(at,actor,role,action,target,detail,provenance) VALUES(?,?,?,?,?,?,?)',
                   (now(), user['id'], user['role'], action, target, json.dumps(detail),
                    'SIMULATED' if mode == 'DEMO' else 'OPERATOR_RECORDED'))

    def user_exists(self, db, uid):
        need(db.execute('SELECT 1 FROM users WHERE id=? AND active=1', (uid,)).fetchone(), 'Active resident account required')

    def command(self, user, action, p, operation_key):
        need(isinstance(p, dict), 'Expected an object')
        for field in ('assets', 'asset_ids'):
            if field in p:
                need(isinstance(p[field], list) and len(p[field]) <= 300 and
                     all(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value) for value in p[field]),
                     f'{field} must contain valid equipment IDs')
        if 'lots' in p:
            need(isinstance(p['lots'], list) and len(p['lots']) <= 30 and all(isinstance(x, dict) for x in p['lots']),
                 'Consumable manifest must contain lot objects')
        need(isinstance(operation_key, str) and 8 <= len(operation_key) <= 100, 'An idempotency key is required')
        fingerprint = hashlib.sha256(json.dumps([action, p], sort_keys=True).encode()).hexdigest()
        try:
            with self.transaction() as db:
                current = db.execute('SELECT role,active FROM users WHERE id=?', (user['id'],)).fetchone()
                need(current and current['active'] and current['role'] == user['role'], 'Account changed; sign in again', 401)
                previous = db.execute('SELECT * FROM operations WHERE actor=? AND key=?', (user['id'], operation_key)).fetchone()
                if previous:
                    need(previous['fingerprint'] == fingerprint, 'Operation key was already used for a different command', 409)
                    return json.loads(previous['result'])
                result = self.apply(db, user, action, p)
                self.event(db, user, action, result.get('id', action), {'input': {k: v for k, v in p.items() if k != 'password'}, 'result': result})
                db.execute('INSERT INTO operations VALUES(?,?,?,?)', (user['id'], operation_key, fingerprint, json.dumps(result)))
                return result
        except sqlite3.IntegrityError as exc:
            raise Problem('This record conflicts with an existing record', 409) from exc

    def apply(self, db, u, action, p):
        role, uid = u['role'], u['id']

        def permit(roles):
            need(role in roles, 'Your role cannot perform this action', 403)

        def get(kind, key='id'):
            return self.get(db, kind, text(p, key))

        def revision(obj):
            need(type(p.get('version')) is int and p['version'] == obj['version'], 'Record changed. Refresh and reconcile before retrying.', 409)

        def owned(obj):
            need(role in MANAGERS or obj.get('borrower') == uid, 'This borrowing belongs to another resident', 403)

        def store(obj, kind='assets'):
            return self.save(db, kind, obj)

        def mark(a, **fields):
            evidence = dict(a.get('evidence', {}))
            for attribute in ('location', 'custodian', 'condition'):
                if attribute in fields:
                    evidence[attribute] = {'recorded_at': now(), 'actor': uid, 'source': 'OPERATOR_RECORDED',
                        'confidence': fields.get('verification', a.get('verification', 'REPORTED'))}
            return store({**a, **fields, 'evidence': evidence, 'source': 'OPERATOR_RECORDED', 'recorded_at': now(), 'last_actor': uid})

        if action == 'asset_create':
            permit(MANAGERS)
            condition = p.get('condition', 'UNKNOWN')
            need(condition in {'USABLE', 'DAMAGED', 'UNKNOWN'}, 'Invalid initial condition')
            return self.save(db, 'assets', {'id': ident(text(p, 'id')), 'name': text(p, 'name'),
                'sport': text(p, 'sport'), 'location': text(p, 'location', 'SPORTS_ROOM'), 'custodian': 'STORE',
                'condition': condition, 'status': {'USABLE': 'AVAILABLE', 'DAMAGED': 'QUARANTINE', 'UNKNOWN': 'INSPECTION'}[condition],
                'source': 'OPERATOR_RECORDED', 'recorded_at': now(), 'last_actor': uid, 'eligible': True,
                'verification': 'REPORTED', 'cost_paise': integer(p, 'cost_paise', 0) if 'cost_paise' in p else 0}, True)
        if action == 'asset_correct':
            permit(MANAGERS)
            a = get('assets'); revision(a)
            need(not a.get('loan_id') and a['status'] not in {'ISSUED', 'REPAIR', 'RETIRED'}, 'Resolve active custody or repair before correcting')
            reason = text(p, 'reason')
            before = dict(a)
            changes = {k: text(p, k) for k in ('name', 'sport', 'location') if k in p}
            out = mark(a, **changes)
            self.event(db, u, 'correction_evidence', a['id'], {'before': before, 'after': out, 'reason': reason})
            return out
        if action == 'lot_create':
            permit(MANAGERS)
            return self.save(db, 'lots', {'id': ident(text(p, 'id')), 'name': text(p, 'name'), 'unit': text(p, 'unit'),
                'quantity': integer(p, 'quantity', 0), 'sport': text(p, 'sport'), 'location': 'SPORTS_ROOM'}, True)
        if action == 'lot_adjust':
            permit(MANAGERS | {'captain', 'checker'})
            a = get('lots'); revision(a)
            qty = p.get('delta')
            need(type(qty) is int and qty != 0 and abs(qty) <= 1000000, 'Nonzero integer delta required')
            need(a['quantity'] + qty >= 0, 'Not enough consumable stock', 409)
            text(p, 'reason')
            return store({**a, 'quantity': a['quantity'] + qty}, 'lots')
        if action == 'kit_create':
            permit(MANAGERS)
            ids = p.get('assets')
            need(isinstance(ids, list) and 0 < len(ids) <= 100 and len(ids) == len(set(ids)), 'Unique kit components required')
            for aid in ids:
                self.get(db, 'assets', aid)
            lots = p.get('lots', [])
            need(isinstance(lots, list) and len(lots) <= 30, 'Invalid consumable manifest')
            need(len({x.get('id') for x in lots}) == len(lots), 'Duplicate consumable lot')
            for line in lots:
                self.get(db, 'lots', text(line, 'id')); integer(line, 'quantity')
            return self.save(db, 'kits', {'id': ident(text(p, 'id')), 'name': text(p, 'name'),
                'sport': text(p, 'sport'), 'assets': ids, 'lots': lots}, True)
        if action == 'borrow_now':
            permit(MANAGERS | {'student', 'captain', 'checker'})
            need(self.get(db, 'settings', 'policy')['ordinary_self_pickup'],
                 'Routine self-pickup is disabled; secretary authorization is required', 403)
            need(not p.get('kit_id') and not p.get('team') and p.get('borrower', uid) == uid,
                 'Direct borrowing is for your own individual equipment only', 403)
            need(p.get('physical_confirmed') is True, 'Confirm that you are taking the equipment now')
            # Create the internal authorization record and checkout in ONE transaction.
            # Reuse availability/role rules without exposing a request step to residents.
            r = self.apply(db, u, 'request_create', {**p, 'borrower': uid})
            return self.apply(db, u, 'pickup', {'id': r['id'], 'version': r['version'],
                'physical_confirmed': True, 'location': p.get('location') or 'SPORTS_GROUND'})
        if action == 'request_create':
            permit(MANAGERS | {'student', 'captain', 'checker'})
            kit = self.get(db, 'kits', p['kit_id']) if p.get('kit_id') else None
            ids = kit['assets'] if kit else p.get('assets', [])
            need(isinstance(ids, list) and 0 < len(ids) <= 100 and len(set(ids)) == len(ids), 'Choose unique equipment IDs')
            for aid in ids:
                self.get(db, 'assets', aid)
            borrower = p.get('borrower', uid)
            need(borrower == uid or role in MANAGERS, 'Cannot request as another resident', 403)
            self.user_exists(db, borrower)
            team = text(p, 'team') if p.get('team') else None
            need(not team or role in MANAGERS | {'captain'}, 'Captain role required for team responsibility', 403)
            due = text(p, 'due_at')
            try:
                dt = datetime.fromisoformat(due.replace('Z', '+00:00'))
                need(dt.tzinfo and dt > datetime.now(timezone.utc), 'Return time must be in the future')
            except ValueError as exc:
                raise Problem('Invalid return time') from exc
            policy = self.get(db, 'settings', 'policy')
            status = 'REQUESTED' if kit or team or not policy['ordinary_self_pickup'] else 'APPROVED'
            return self.save(db, 'requests', {'assets': ids, 'kit_id': kit['id'] if kit else None, 'lots': kit['lots'] if kit else [],
                'borrower': borrower, 'team': team, 'purpose': text(p, 'purpose'), 'due_at': due,
                'status': status, 'created_at': now(), 'approval_basis': 'ROUTINE_24H_POLICY' if status == 'APPROVED' else None}, True)
        if action in {'request_approve', 'request_deny', 'request_cancel'}:
            r = get('requests'); revision(r)
            need(r['status'] in {'REQUESTED', 'APPROVED'}, 'Request is already finalized', 409)
            if action == 'request_cancel':
                owned(r)
            else:
                permit(MANAGERS)
            if action == 'request_deny':
                text(p, 'reason')
            return store({**r, 'status': {'request_approve': 'APPROVED', 'request_deny': 'DENIED', 'request_cancel': 'CANCELLED'}[action],
                          'decision_by': uid, 'decision_at': now(), 'reason': p.get('reason')}, 'requests')
        if action == 'pickup':
            r = get('requests'); revision(r); owned(r)
            need(r['status'] == 'APPROVED', 'Request must be approved before collection', 409)
            need(p.get('physical_confirmed') is True, 'Confirm actual physical collection')
            assets = [self.get(db, 'assets', aid) for aid in r['assets']]
            need(all(a['status'] == 'AVAILABLE' and a['condition'] == 'USABLE' and not a.get('loan_id') for a in assets),
                 'One or more components are unavailable. Nothing has been issued.', 409)
            for line in r['lots']:
                lot = self.get(db, 'lots', line['id'])
                need(lot['quantity'] >= line['quantity'], 'Insufficient kit consumables. Nothing has been issued.', 409)
                store({**lot, 'quantity': lot['quantity'] - line['quantity']}, 'lots')
            loan = self.save(db, 'loans', {'request_id': r['id'], 'borrower': r['borrower'], 'team': r['team'],
                'assets': r['assets'], 'remaining': r['assets'], 'lots_issued': r['lots'], 'due_at': r['due_at'],
                'status': 'ACTIVE', 'issued_at': now(), 'returned': [], 'pickup_source': 'BORROWER_DECLARATION' if uid == r['borrower'] else 'CUSTODIAN_CONFIRMATION'}, True)
            for a in assets:
                mark(a, status='ISSUED', custodian=r['team'] or r['borrower'], location=p.get('location') or 'SPORTS_GROUND',
                     loan_id=loan['id'], verification='REPORTED')
            store({**r, 'status': 'COLLECTED', 'loan_id': loan['id']}, 'requests')
            return loan
        if action == 'return_report':
            loan = get('loans'); revision(loan); owned(loan)
            ids = p.get('assets')
            need(isinstance(ids, list) and ids and len(ids) == len(set(ids)) and set(ids) <= set(loan['remaining']), 'Select outstanding loan components')
            for aid in ids:
                a = self.get(db, 'assets', aid)
                need(a.get('loan_id') == loan['id'] and not a.get('return_reported'), 'Return already reported or custody changed', 409)
                mark(a, return_reported=True, verification='RETURN_DECLARED_NOT_RECEIVED')
            return store({**loan, 'status': 'RETURN_REPORTED', 'return_reported_at': now()}, 'loans')
        if action == 'return_receive':
            permit(CHECKERS)
            loan = get('loans'); revision(loan)
            need(loan['borrower'] != uid, 'A separate checker must receive your return', 403)
            ids = p.get('assets')
            need(p.get('physical_confirmed') is True, 'Physical receipt confirmation is required')
            need(isinstance(ids, list) and ids and len(set(ids)) == len(ids) and set(ids) <= set(loan['remaining']), 'Select physically received components only')
            for aid in ids:
                a = self.get(db, 'assets', aid)
                need(a.get('loan_id') == loan['id'], 'Component custody changed; reconcile first', 409)
                mark(a, status='INSPECTION' if a['condition'] != 'DAMAGED' else 'QUARANTINE', location='SPORTS_ROOM',
                     custodian='STORE', condition='UNKNOWN' if a['condition'] != 'DAMAGED' else 'DAMAGED',
                     return_reported=False, loan_id=None, last_borrower=loan['borrower'], verification='PHYSICAL_RECEIPT')
            remaining = [x for x in loan['remaining'] if x not in ids]
            return store({**loan, 'remaining': remaining, 'returned': loan['returned'] + ids,
                'status': 'PARTIAL' if remaining else 'RETURNED', 'closed_at': now() if not remaining else None}, 'loans')
        if action == 'inspect':
            permit(CHECKERS)
            a = get('assets'); revision(a)
            need(a['status'] in {'INSPECTION', 'QUARANTINE', 'UNKNOWN'} and not a.get('loan_id'), 'Receive equipment and finish vendor custody before inspection', 409)
            need(a.get('last_borrower') != uid, 'Use a checker separate from the borrower', 403)
            result = p.get('condition')
            need(result in {'USABLE', 'DAMAGED', 'UNKNOWN'}, 'Choose usable, damaged or unknown')
            text(p, 'notes')
            out = mark(a, condition=result, status={'USABLE': 'AVAILABLE', 'DAMAGED': 'QUARANTINE', 'UNKNOWN': 'INSPECTION'}[result],
                       verification='AUTHORIZED_INSPECTION', inspected_by=uid, inspected_at=now())
            for r in self.all(db, 'repairs'):
                if r['asset_id'] == a['id'] and r['stage'] == 'RECEIVED':
                    store({**r, 'stage': 'CLOSED' if result == 'USABLE' else 'REASSESS', 'inspection_at': now()}, 'repairs')
            return out
        if action == 'transfer_offer':
            loan = get('loans'); revision(loan); owned(loan)
            need(loan['status'] in {'ACTIVE', 'PARTIAL'}, 'Transfers require active, unreturned components', 409)
            to = text(p, 'to'); self.user_exists(db, to)
            need(to != loan['borrower'], 'Choose a different recipient')
            ids = p.get('assets', loan['remaining'])
            need(isinstance(ids, list) and ids and all(isinstance(x, str) for x in ids) and len(set(ids)) == len(ids)
                 and set(ids) <= set(loan['remaining']), 'Choose distinct outstanding components')
            return self.save(db, 'transfers', {'loan_id': loan['id'], 'from': loan['borrower'], 'to': to,
                'assets': ids, 'loan_version': loan['version'], 'status': 'PENDING', 'location': text(p, 'location'), 'created_at': now()}, True)
        if action in {'transfer_accept', 'transfer_reject'}:
            tr = get('transfers'); revision(tr)
            need(tr['to'] == uid, 'Only the receiving resident can accept or reject custody', 403)
            need(tr['status'] == 'PENDING', 'Transfer already resolved', 409)
            if action == 'transfer_accept':
                need(p.get('physical_confirmed') is True, 'Confirm physical receipt')
                loan = self.get(db, 'loans', tr['loan_id'])
                need(loan['version'] == tr['loan_version'] and loan['status'] in {'ACTIVE', 'PARTIAL'} and loan['borrower'] == tr['from'], 'Custody changed; request a fresh transfer', 409)
                selected = tr['assets']
                remainder = [aid for aid in loan['remaining'] if aid not in selected]
                if remainder:
                    next_loan = self.save(db, 'loans', {'request_id': loan['request_id'], 'borrower': uid, 'team': None,
                        'assets': selected, 'remaining': selected, 'returned': [], 'lots_issued': [], 'due_at': loan['due_at'],
                        'status': 'ACTIVE', 'issued_at': now(), 'transferred_from': loan['id']}, True)
                    store({**loan, 'remaining': remainder, 'transferred': loan.get('transferred', []) + selected}, 'loans')
                else:
                    next_loan = store({**loan, 'borrower': uid, 'team': None}, 'loans')
                for aid in selected:
                    a = self.get(db, 'assets', aid)
                    need(a['status'] == 'ISSUED' and not a.get('return_reported'), 'Return or damage requires reconciliation', 409)
                    mark(a, custodian=uid, location=tr['location'], loan_id=next_loan['id'])
            return store({**tr, 'status': 'ACCEPTED' if action == 'transfer_accept' else 'REJECTED', 'resolved_at': now()}, 'transfers')
        if action == 'damage_report':
            permit(ROLES - {'office', 'maintenance'})
            aid = p.get('asset_id')
            if aid:
                a = self.get(db, 'assets', aid)
                need(a['status'] != 'RETIRED', 'Item is retired')
                # Preserve location, custodian and active loan: discovery is not return.
                mark(a, status='QUARANTINE', condition='DAMAGED', verification='REPORTED_DAMAGE')
            return self.save(db, 'damage', {'asset_id': aid, 'description': text(p, 'description'),
                'discovered_at': now(), 'occurrence_at': None, 'blame': 'NOT_INFERRED', 'reporter': uid,
                'status': 'OPEN', 'source': 'USER_REPORT', 'location_note': text(p, 'location', 'UNKNOWN')}, True)
        if action == 'damage_acknowledge':
            permit(MANAGERS)
            d = get('damage'); revision(d)
            return store({**d, 'status': 'ACKNOWLEDGED', 'acknowledged_by': uid, 'notes': text(p, 'notes')}, 'damage')
        if action == 'repair_create':
            permit(MANAGERS)
            a = get('assets', 'asset_id'); revision(a)
            need(a['status'] == 'QUARANTINE' and not a.get('loan_id'), 'Receive damaged equipment before opening repair', 409)
            need(not any(r['asset_id'] == a['id'] and r['stage'] not in {'CLOSED', 'CANCELLED'} for r in self.all(db, 'repairs')), 'An active repair case already exists', 409)
            return self.save(db, 'repairs', {'asset_id': a['id'], 'stage': 'ASSESSED', 'assessment': text(p, 'assessment'),
                'vendor': text(p, 'vendor'), 'created_at': now(), 'cost_paise': integer(p, 'cost_paise', 0)}, True)
        if action == 'repair_advance':
            r = get('repairs'); revision(r)
            chain = {'ASSESSED': 'APPROVED', 'APPROVED': 'AT_VENDOR', 'AT_VENDOR': 'REPAIRED', 'REPAIRED': 'RECEIVED'}
            need(r['stage'] in chain, 'No further repair step; perform separate inspection', 409)
            permit(MANAGERS if r['stage'] == 'ASSESSED' else MANAGERS | {'maintenance'})
            text(p, 'reference')
            a = self.get(db, 'assets', r['asset_id'])
            stage = chain[r['stage']]
            if stage == 'AT_VENDOR':
                need(not a.get('loan_id'), 'Active loan must be reconciled first', 409)
                mark(a, status='REPAIR', custodian=r['vendor'], location='REPAIR_SHOP', condition='REPAIR')
            if stage == 'RECEIVED':
                mark(a, status='INSPECTION', custodian='STORE', location='SPORTS_ROOM', condition='UNKNOWN')
            return store({**r, 'stage': stage, stage.lower() + '_at': now(), stage.lower() + '_reference': p['reference']}, 'repairs')
        if action in {'repair_reassess', 'repair_cancel'}:
            permit(MANAGERS)
            r = get('repairs'); revision(r)
            need(r['stage'] in ({'REASSESS'} if action == 'repair_reassess' else {'ASSESSED', 'APPROVED', 'REASSESS'}),
                 'Receive vendor-held equipment before cancellation; reassessment needs a failed inspection', 409)
            return store({**r, 'stage': 'ASSESSED' if action == 'repair_reassess' else 'CANCELLED',
                'reassessment_reason': text(p, 'reason'), 'decision_at': now()}, 'repairs')
        if action == 'retire':
            permit(MANAGERS)
            a = get('assets'); revision(a)
            need(not a.get('loan_id') and a['status'] not in {'ISSUED', 'REPAIR', 'RETIRED'}, 'Resolve outstanding custody first', 409)
            need(not any(r['asset_id'] == a['id'] and r['stage'] not in {'CLOSED', 'CANCELLED', 'REASSESS'} for r in self.all(db, 'repairs')), 'Resolve active repair first', 409)
            return mark(a, status='RETIRED', condition='RETIRED', retirement_reason=text(p, 'reason'), retired_at=now())
        if action == 'purchase_create':
            permit(MANAGERS)
            return self.save(db, 'purchases', {'name': text(p, 'name'), 'sport': text(p, 'sport'), 'quantity': integer(p, 'quantity'),
                'amount_paise': integer(p, 'amount_paise'), 'rationale': text(p, 'rationale'), 'stage': 'NEED',
                'quotes': [], 'received': 0, 'created_at': now()}, True)
        if action == 'purchase_quote':
            permit(MANAGERS)
            r = get('purchases'); revision(r)
            need(r['stage'] == 'NEED', 'Quotations are locked after approval', 409)
            quote = {'vendor': text(p, 'vendor'), 'amount_paise': integer(p, 'amount_paise'), 'reference': text(p, 'reference')}
            need(quote['vendor'].casefold() not in {x['vendor'].casefold() for x in r['quotes']}, 'Use distinct quotation vendors')
            return store({**r, 'quotes': r['quotes'] + [quote]}, 'purchases')
        if action == 'purchase_advance':
            permit({'office', 'admin'})
            r = get('purchases'); revision(r)
            policy = self.get(db, 'settings', 'policy')
            need(policy['policy_confirmed'], 'Office must confirm procurement policy before approval', 409)
            if r['stage'] == 'NEED':
                need(len(r['quotes']) >= (3 if r['amount_paise'] >= policy['threshold_paise'] else 1), 'Required distinct quotations are missing', 409)
                next_stage = 'APPROVED'
            elif r['stage'] == 'APPROVED':
                next_stage = 'PAYMENT_RECORDED'
            else:
                raise Problem('Use physical receipt to enroll purchased stock', 409)
            return store({**r, 'stage': next_stage, next_stage.lower() + '_at': now(),
                next_stage.lower() + '_by': uid, next_stage.lower() + '_reference': text(p, 'reference'),
                'route': 'OFFICE_PAYMENT' if r['amount_paise'] >= policy['threshold_paise'] else 'REIMBURSEMENT'}, 'purchases')
        if action == 'purchase_receive':
            permit(MANAGERS)
            r = get('purchases'); revision(r)
            need(r['stage'] in {'PAYMENT_RECORDED', 'PARTIAL_RECEIPT'}, 'Record approval and payment provenance first', 409)
            need(p.get('physical_confirmed') is True, 'Confirm actual stock received')
            qty = integer(p, 'quantity')
            need(qty <= r['quantity'] - r['received'], 'Receipt exceeds outstanding order', 409)
            if p.get('lot_id'):
                lot = self.get(db, 'lots', p['lot_id'])
                store({**lot, 'quantity': lot['quantity'] + qty}, 'lots')
            else:
                ids = p.get('asset_ids')
                need(isinstance(ids, list) and len(ids) == qty and len(set(ids)) == qty, 'Provide one unique asset ID for each received item')
                for aid in ids:
                    self.save(db, 'assets', {'id': ident(aid), 'name': r['name'], 'sport': r['sport'], 'location': 'SPORTS_ROOM',
                        'custodian': 'STORE', 'condition': 'UNKNOWN', 'status': 'INSPECTION', 'eligible': True,
                        'verification': 'PHYSICAL_RECEIPT', 'source': 'PROCUREMENT_RECEIPT', 'recorded_at': now(),
                        'last_actor': uid, 'purchase_id': r['id'], 'cost_paise': r['amount_paise'] // r['quantity']}, True)
            received = r['received'] + qty
            return store({**r, 'received': received, 'stage': 'RECEIVED' if received == r['quantity'] else 'PARTIAL_RECEIPT',
                          'last_receipt_at': now()}, 'purchases')
        if action == 'key_out':
            permit({'guard'} | MANAGERS)
            borrower = text(p, 'borrower'); self.user_exists(db, borrower)
            key_code = text(p, 'key_code', 'SPORTS_ROOM')
            active_keys = [k for k in self.all(db, 'keys') if k['status'] == 'OUT']
            need(not any(k['borrower'] == borrower for k in active_keys), 'Resident already has a key session', 409)
            need(not any(k['key_code'] == key_code for k in active_keys), 'This physical key is already signed out. Overlapping equipment access does not require a second key handout.', 409)
            return self.save(db, 'keys', {'borrower': borrower, 'key_code': key_code,
                'status': 'OUT', 'out_at': now(), 'equipment_verified': False}, True)
        if action == 'key_back':
            permit({'guard'} | MANAGERS)
            r = get('keys'); revision(r)
            need(r['status'] == 'OUT', 'Key session is already closed', 409)
            return store({**r, 'status': 'RETURNED', 'back_at': now(), 'equipment_verified': False}, 'keys')
        if action == 'audit_start':
            permit(CHECKERS)
            ids = p.get('assets')
            need(isinstance(ids, list) and ids and len(set(ids)) == len(ids) and len(ids) <= 300, 'Select distinct audit assets')
            snapshots = []
            for aid in ids:
                a = self.get(db, 'assets', aid)
                need(a['eligible'] and a['status'] != 'RETIRED', 'Only eligible active durable items enter strict accountability')
                snapshots.append(a)
            return self.save(db, 'audits', {'snapshot_at': now(), 'method': text(p, 'method'),
                'snapshots': snapshots, 'observations': [], 'status': 'OPEN', 'created_by': uid,
                'provenance': 'SIMULATED' if db.execute("SELECT value FROM meta WHERE key='mode'").fetchone()[0] == 'DEMO' else 'FIELD_CLAIM_REQUIRES_INDEPENDENT_CHECK'}, True)
        if action == 'audit_observe':
            permit(CHECKERS)
            r = get('audits'); revision(r)
            need(r['status'] == 'OPEN', 'Audit is closed', 409)
            aid = text(p, 'asset_id')
            a = next((a for a in r['snapshots'] if a['id'] == aid), None)
            need(a is not None, 'Asset is outside this snapshot')
            need(not any(o['asset_id'] == aid for o in r['observations']), 'Observation already captured; keep original evidence')
            need(a.get('last_actor') != uid and a.get('custodian') != uid, 'Independent checker must differ from record operator and custodian', 403)
            need(self.get(db, 'assets', aid)['version'] == a['version'], 'Asset changed since snapshot; start a new audit', 409)
            need((datetime.now(timezone.utc) - datetime.fromisoformat(r['snapshot_at'])).total_seconds() <= 900, 'Snapshot expired after 15 minutes; start a new audit', 409)
            actual = {k: text(p, k) for k in ('location', 'custodian', 'condition')}
            need(actual['condition'] in CONDITIONS, 'Invalid observed condition')
            observations = r['observations'] + [{'asset_id': aid, 'actual': actual, 'checker': uid, 'observed_at': now(),
                'reference': text(p, 'reference'), 'unknown': any(actual[k] == 'UNKNOWN' or a.get(k) in {None, '', 'UNKNOWN'} for k in actual),
                'matches': {k: actual[k] == a.get(k) and actual[k] != 'UNKNOWN' for k in actual}}]
            return store({**r, 'observations': observations}, 'audits')
        if action == 'audit_close':
            permit(CHECKERS)
            r = get('audits'); revision(r)
            need(r['status'] == 'OPEN', 'Audit already closed', 409)
            need(len(r['observations']) == len(r['snapshots']), 'Keep all sampled items in the denominator; record unknowns before closing')
            return store({**r, 'status': 'CLOSED', 'closed_at': now()}, 'audits')
        if action == 'conflict_record':
            permit(ROLES - {'guard', 'office', 'maintenance'})
            return self.save(db, 'conflicts', {'asset_id': text(p, 'asset_id'), 'description': text(p, 'description'),
                'reporter': uid, 'status': 'PENDING', 'created_at': now(), 'no_state_overwrite': True}, True)
        if action == 'conflict_resolve':
            permit(MANAGERS)
            c = get('conflicts'); revision(c)
            need(c['status'] == 'PENDING', 'Already reconciled', 409)
            return store({**c, 'status': 'RESOLVED', 'resolution': text(p, 'resolution'), 'resolved_by': uid, 'resolved_at': now()}, 'conflicts')
        if action == 'policy_update':
            permit({'admin', 'office'})
            r = self.get(db, 'settings', 'policy'); revision(r)
            text(p, 'reference')
            threshold = integer(p, 'threshold_paise')
            need(type(p.get('policy_confirmed')) is bool and type(p.get('ordinary_self_pickup')) is bool, 'Policy confirmation and self-pickup must be booleans')
            return store({**r, 'threshold_paise': threshold, 'policy_confirmed': p['policy_confirmed'],
                'ordinary_self_pickup': p['ordinary_self_pickup'], 'confirmation_reference': p['reference'], 'confirmed_by': uid}, 'settings')
        raise Problem('Unknown command', 404)

    def snapshot(self, user):
        with self.connect() as db:
            db.execute('BEGIN')
            u = user; role = u['role']; uid = u['id']
            data = {k: self.all(db, k) for k in KINDS}
            mode = db.execute("SELECT value FROM meta WHERE key='mode'").fetchone()[0]
            metrics = analytics(data)
            if role not in MANAGERS:
                data['purchases'] = data['purchases'] if role == 'office' else []
                data['keys'] = data['keys'] if role == 'guard' else [k for k in data['keys'] if k['borrower'] == uid]
                if role not in CHECKERS:
                    data['requests'] = [r for r in data['requests'] if r['borrower'] == uid]
                    data['loans'] = [r for r in data['loans'] if r['borrower'] == uid]
                    data['audits'] = []
                data['transfers'] = [r for r in data['transfers'] if uid in {r['from'], r['to']}]
                if role not in CHECKERS | {'maintenance'}:
                    data['repairs'] = []
                    data['damage'] = [r for r in data['damage'] if r['reporter'] == uid]
                data['conflicts'] = [r for r in data['conflicts'] if r['reporter'] == uid]
                # Shared catalog has no borrower identity or historic personal records.
                if role not in CHECKERS:
                    data['assets'] = [{k: v for k, v in a.items() if k not in {'last_actor', 'last_borrower', 'inspected_by', 'custodian', 'loan_id'}} |
                        {'custodian': 'YOU' if a.get('custodian') == uid else ('STORE' if a.get('custodian') == 'STORE' else 'PRIVATE_CUSTODIAN')} for a in data['assets']]
                    for asset in data['assets']:
                        asset['evidence'] = {k: {f: value for f, value in v.items() if f != 'actor'} for k, v in asset.get('evidence', {}).items()}
            users = [{'id': r['id'], 'role': r['role'], 'active': bool(r['active']),
                      **({'username': r['username']} if role == 'admin' else {})}
                     for r in db.execute('SELECT id,username,role,active FROM users')]
            if role in MANAGERS:
                data['users'] = users
            else:
                data['users'] = []
            if role in MANAGERS | {'office'}:
                data['events'] = [dict(r) | {'detail': json.loads(r['detail'])} for r in db.execute('SELECT * FROM events ORDER BY seq DESC LIMIT 300')]
            else:
                data['events'] = [dict(r) | {'detail': {}} for r in db.execute('SELECT * FROM events WHERE actor=? ORDER BY seq DESC LIMIT 100', (uid,))]
            return {'user': user, 'data': data, 'metrics': metrics, 'mode': mode, 'server_time': now()}


def analytics(data):
    assets = data['assets']
    counts = {s: sum(a['status'] == s for a in assets) for s in sorted(STATES)}
    categories = []
    for sport in sorted({a['sport'] for a in assets}):
        active = [a for a in assets if a['sport'] == sport and a['status'] != 'RETIRED']
        unavailable = sum(a['status'] in {'QUARANTINE', 'REPAIR', 'INSPECTION', 'UNKNOWN'} for a in active)
        categories.append({'sport': sport, 'active': len(active), 'available': sum(a['status'] == 'AVAILABLE' for a in active),
                           'unusable_or_unknown': unavailable, 'unusable_share': unavailable / len(active) if active else None})
    audits = [a for a in data['audits'] if a['status'] == 'CLOSED' and a['provenance'] != 'SIMULATED']
    latest = audits[0] if audits else None
    accountability = {'status': 'NOT MEASURED', 'numerator': None, 'denominator': 0, 'rate': None}
    if latest:
        obs = latest['observations']; n = len(latest['snapshots'])
        strict = sum(not o['unknown'] and all(o['matches'].values()) for o in obs)
        assessable = sum(not o['unknown'] for o in obs)
        accountability = {'status': 'INDEPENDENT_OPERATOR_RECORDED', 'numerator': strict, 'denominator': n,
            'rate': strict / n if n else None, 'assessable': assessable, 'unknown': sum(o['unknown'] for o in obs),
            'contradicted': sum(not o['unknown'] and not all(o['matches'].values()) for o in obs),
            'conditional_accuracy': strict / assessable if assessable else None,
            'snapshot_at': latest['snapshot_at'], 'method': latest['method'], 'audit_id': latest['id']}
    active_loans = [l for l in data['loans'] if l['remaining']]
    overdue = sum(datetime.fromisoformat(l['due_at'].replace('Z', '+00:00')) < datetime.now(timezone.utc) for l in active_loans)
    finalized = [r for r in data['requests'] if r['status'] in {'COLLECTED', 'DENIED'}]
    lead = [(datetime.fromisoformat(r['inspection_at']) - datetime.fromisoformat(r['created_at'])).total_seconds() / 3600
            for r in data['repairs'] if r['stage'] == 'CLOSED' and r.get('inspection_at')]
    return {'total': len(assets), 'counts': counts, 'reconciles': sum(counts.values()) == len(assets), 'categories': categories,
        'active_loans': len(active_loans), 'overdue': overdue, 'accountability': accountability,
        'fulfilment': {'collected': sum(r['status'] == 'COLLECTED' for r in finalized), 'decided_requests': len(finalized),
                      'service_window': 'NOT DEFINED; not a timed fulfilment rate'},
        'repair_lead_hours': sum(lead) / len(lead) if lead else None, 'repair_lead_n': len(lead),
        'baseline': 'NOT MEASURED', 'tournament_burden': 'NOT MEASURED; target <=60 seconds', 'fines': 'NO AUTOMATIC FINES'}

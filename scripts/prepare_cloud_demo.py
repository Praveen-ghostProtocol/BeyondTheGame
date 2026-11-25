"""Prepare private one-time cloud demo bootstrap, using the existing domain seed.

Run locally once; outputs in ignored app/private/. Never print passwords or upload
this directory. This script does not connect to Supabase or alter a live DB.
"""
import json
import secrets
import sys
import base64
import hashlib
import hmac
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from domain import Store
from server import seed_demo


def literal(value):
    if value is None:
        return 'NULL'
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def scram_verifier(password):
    salt = secrets.token_bytes(16)
    salted = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 4096)
    stored = hashlib.sha256(hmac.digest(salted, b'Client Key', 'sha256')).digest()
    server = hmac.digest(salted, b'Server Key', 'sha256')
    b64 = lambda value: base64.b64encode(value).decode()
    return 'SCRAM-SHA-256$4096:' + b64(salt) + '$' + b64(stored) + ':' + b64(server)


def main():
    private = ROOT / 'app/private'
    private.mkdir(parents=True, exist_ok=True)
    config_path = private / 'cloud-provisioning.json'
    if config_path.exists():
        print('Private cloud bootstrap already exists; preserving credentials.')
        return
    password = secrets.token_urlsafe(24)
    runtime_password = secrets.token_urlsafe(36)
    db_path = private / 'cloud-bootstrap.sqlite3'
    if db_path.exists():
        raise SystemExit('Bootstrap database already exists; inspect before regenerating.')
    store = Store(db_path)
    seed_demo(store, password)
    lines = ["SELECT pg_advisory_xact_lock(2311202601);",
             "DO $$ BEGIN IF EXISTS(SELECT 1 FROM btg.users) THEN RAISE EXCEPTION 'Cloud bootstrap requires empty app tables'; END IF; END $$;"]
    with store.connect() as db:
        for table in ('users', 'records', 'events'):
            columns = [row['name'] for row in db.execute('PRAGMA table_info(' + table + ')')]
            for row in db.execute('SELECT * FROM ' + table):
                values = ','.join(literal(row[column]) for column in columns)
                lines.append('INSERT INTO btg.' + table + '(' + ','.join(columns) + ') VALUES(' + values + ');')
    lines.append("SELECT setval(pg_get_serial_sequence('btg.events','seq'),(SELECT max(seq) FROM btg.events),true);")
    (private / 'cloud-seed.sql').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    role = ["CREATE ROLE btg_runtime LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS PASSWORD " + literal(scram_verifier(runtime_password)) + ';',
            'GRANT USAGE ON SCHEMA btg,extensions TO btg_runtime;',
            'GRANT SELECT ON btg.meta TO btg_runtime;',
            'GRANT SELECT,INSERT,UPDATE ON btg.users,btg.records TO btg_runtime;',
            'GRANT SELECT,INSERT,UPDATE,DELETE ON btg.sessions,btg.login_attempts TO btg_runtime;',
            'GRANT SELECT,INSERT ON btg.events,btg.operations TO btg_runtime;',
            'GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA btg TO btg_runtime;']
    for table in ('meta', 'users', 'records', 'sessions', 'login_attempts', 'events', 'operations'):
        role.append('CREATE POLICY backend_only ON btg.' + table +
                    ' FOR ALL TO btg_runtime USING (true) WITH CHECK (true);')
    (private / 'cloud-role.sql').write_text('\n'.join(role) + '\n', encoding='utf-8', newline='\n')
    config_path.write_text(json.dumps({'runtime_password': runtime_password,
                                      'project_ref': 'ivobrmuuyjacsnplcfdd'}, indent=2), encoding='utf-8')
    (private / 'cloud-access.txt').write_text('HOSTED DEMONSTRATION ONLY — SYNTHETIC DATA\n'
        'Usernames: admin, secretary, student, captain, checker, guard, maintenance, office\n'
        'Password: ' + password + '\nDo not use these accounts for real resident records.\n', encoding='utf-8')
    print('Prepared private cloud bootstrap and demo credentials. No secrets printed.')


if __name__ == '__main__':
    main()

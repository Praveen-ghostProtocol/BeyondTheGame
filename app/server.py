"""Run with Python 3.11+: python app/server.py --demo (isolated synthetic DB).

Production uses TLS at a trusted reverse proxy and --secure-cookies --origin.
Only explicit static assets are served; database and Python source stay private.
"""
import argparse
import getpass
import hashlib
import hmac
import json
import logging
import os
import secrets
import sqlite3
import sys
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from domain import MANAGERS, Problem, Store, need, now, text
from security import authenticate, create_user, demo_session, is_demo, password_hash, session, verify

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / 'static'
DEFAULT_PRIVATE = ROOT / 'private'


def seed_demo(store, password):
    with store.connect() as db:
        need(db.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0, 'Demo seed requires an empty database; existing data is preserved')
        db.execute("UPDATE meta SET value='DEMO' WHERE key='mode'")
    users = {role: create_user(store, role, password, role) for role in ('admin', 'secretary', 'student', 'captain', 'checker', 'guard', 'maintenance', 'office')}
    sec = users['secretary']
    mix = [('BD', 'Badminton racket', 'Badminton', 4), ('CB', 'Cricket bat', 'Cricket', 2),
           ('CH', 'Cricket helmet', 'Cricket', 2), ('CP', 'Batting pad set', 'Cricket', 1),
           ('FB', 'Football', 'Football', 3), ('VB', 'Volleyball', 'Volleyball', 3)]
    for prefix, name, sport, count in mix:
        for n in range(1, count + 1):
            aid = f'{prefix}-{n:03}'
            store.command(sec, 'asset_create', {'id': aid, 'name': name, 'sport': sport,
                'condition': 'DAMAGED' if aid == 'BD-004' else 'USABLE', 'location': 'SPORTS_ROOM'}, secrets.token_hex(16))
    store.command(sec, 'lot_create', {'id': 'LOT-SHUTTLE', 'name': 'Practice shuttlecocks', 'unit': 'pieces', 'sport': 'Badminton', 'quantity': 24}, secrets.token_hex(16))
    store.command(sec, 'kit_create', {'id': 'KIT-CRICKET', 'name': 'Cricket match kit', 'sport': 'Cricket',
        'assets': ['CB-001', 'CB-002', 'CH-001', 'CH-002', 'CP-001'], 'lots': []}, secrets.token_hex(16))
    store.command(users['student'], 'damage_report', {'asset_id': 'BD-004', 'description': 'Synthetic demo: loose racket strings require assessment.'}, secrets.token_hex(16))
    return users


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, store, origin=None, secure=False):
        self.store = store
        self.origin = origin or f'http://{address[0]}:{address[1]}'
        self.secure = secure
        super().__init__(address, Handler)


class Handler(BaseHTTPRequestHandler):
    server_version = 'BeyondTheGame/1.0'

    def log_message(self, fmt, *args):
        # Never include request bodies, cookies, credentials or query values.
        logging.info('%s %s', self.command, urlsplit(self.path).path)

    def reply(self, value, status=200, cookie=None, content_type='application/json; charset=utf-8'):
        raw = json.dumps(value, ensure_ascii=False).encode() if content_type.startswith('application/json') else value
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Permissions-Policy', 'camera=(self), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        if cookie:
            self.send_header('Set-Cookie', cookie)
        self.end_headers()
        self.wfile.write(raw)

    def token(self):
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
        except Exception:
            return ''
        return cookie['btg_session'].value if 'btg_session' in cookie else ''

    def auth(self, mutation=False):
        user, csrf = session(self.server.store, self.token())
        if mutation:
            need(hmac.compare_digest(csrf, self.headers.get('X-CSRF-Token', '')), 'Session confirmation missing; reload and retry', 403)
        return user, csrf

    def cookie(self, token, clear=False):
        return f'btg_session={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={0 if clear else 43200}' + ('; Secure' if self.server.secure else '')

    def do_GET(self):
        try:
            path = urlsplit(self.path).path
            if path == '/api/health':
                self.reply({'status': 'ok', 'schema': 1}); return
            if path == '/api/state':
                user, csrf = self.auth()
                self.reply({**self.server.store.snapshot(user), 'csrf': csrf}); return
            if path == '/api/export/aggregates':
                user, _ = self.auth()
                need(user['role'] in MANAGERS | {'office'}, 'Aggregate export is restricted', 403)
                state = self.server.store.snapshot(user)
                metrics = state['metrics']
                # Public export whitelist: no transactions, identities, notes, refs or free-text methods.
                a = metrics['accountability']
                self.reply({'provenance': state['mode'], 'generated_at': now(), 'inventory': {'total': metrics['total'], 'counts': metrics['counts']},
                    'accountability': {k: a[k] for k in ('status', 'numerator', 'denominator', 'rate')}, 'baseline': 'NOT MEASURED',
                    'field_improvement': 'NOT MEASURED'}); return
            files = {'/': ('index.html', 'text/html; charset=utf-8'), '/index.html': ('index.html', 'text/html; charset=utf-8'),
                     '/style.css': ('style.css', 'text/css; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
                     '/scanner.js': ('scanner.js', 'text/javascript; charset=utf-8'), '/favicon.svg': ('favicon.svg', 'image/svg+xml')}
            files['/vendor/jsQR.js'] = ('vendor/jsQR.js', 'text/javascript; charset=utf-8')
            files['/vendor/qrcode.js'] = ('vendor/qrcode.js', 'text/javascript; charset=utf-8')
            need(path in files, 'Not found', 404)
            name, mime = files[path]
            self.reply((STATIC / name).read_bytes(), content_type=mime)
        except Problem as exc:
            self.reply({'error': str(exc)}, exc.status)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            logging.exception('GET failed')
            self.reply({'error': 'Server error; check local operator log'}, 500)

    def do_POST(self):
        try:
            # Explicit origin allowlist also protects localhost from browser DNS rebinding.
            parsed = urlsplit(self.server.origin)
            need(self.headers.get('Host') == parsed.netloc, 'Unexpected application host', 403)
            need(self.headers.get('Origin') in {None, self.server.origin}, 'Cross-origin requests are not accepted', 403)
            need(self.headers.get('Content-Type', '').split(';')[0] == 'application/json', 'Use application/json', 415)
            try:
                length = int(self.headers.get('Content-Length', '0'))
            except ValueError as exc:
                raise Problem('Invalid body length') from exc
            need(0 < length <= 65536, 'Body must contain 1–65536 bytes', 413)
            try:
                p = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeDecodeError) as exc:
                raise Problem('Invalid JSON') from exc
            need(isinstance(p, dict), 'Expected a JSON object')
            path = urlsplit(self.path).path
            store = self.server.store
            if path == '/api/login':
                result, error, status = authenticate(store, p.get('username'), p.get('password'), self.client_address[0])
                if error:
                    self.reply({'error': error}, status); return
                self.reply({'user': result['user'], 'csrf': result['csrf']}, cookie=self.cookie(result['token'])); return
            if path == '/api/demo-login':
                result = demo_session(store, p.get('role'))
                self.reply({'user': result['user'], 'csrf': result['csrf']}, cookie=self.cookie(result['token'])); return
            user, _ = self.auth(mutation=True)
            need(path == '/api/logout' or not is_demo(user),
                 'Demo mode is view-only, so real hostel records stay untouched. Watch the demo video to see this step.', 403)
            if path == '/api/logout':
                with store.transaction() as db:
                    db.execute('DELETE FROM sessions WHERE token_hash=?', (hashlib.sha256(self.token().encode()).hexdigest(),))
                self.reply({'ok': True}, cookie=self.cookie('', True)); return
            if path == '/api/users':
                need(user['role'] == 'admin', 'Administrator required', 403)
                self.reply(create_user(store, text(p, 'username'), text(p, 'password'), text(p, 'role'), user), 201); return
            if path == '/api/account':
                with store.transaction() as db:
                    row = db.execute('SELECT password FROM users WHERE id=?', (user['id'],)).fetchone()
                    need(verify(p.get('current_password'), row[0]), 'Current password is incorrect', 403)
                    db.execute('UPDATE users SET password=? WHERE id=?', (password_hash(p.get('password')), user['id']))
                    db.execute('DELETE FROM sessions WHERE user_id=?', (user['id'],))
                    store.event(db, user, 'password_change', user['id'], {'sessions_revoked': True})
                self.reply({'ok': True}, cookie=self.cookie('', True)); return
            if path == '/api/users/update':
                need(user['role'] == 'admin', 'Administrator required', 403)
                from domain import ROLES
                need(p.get('role') in ROLES and type(p.get('active')) is bool, 'Valid role and active boolean required')
                need(p.get('id') != user['id'], 'Use another administrator to change your account')
                with store.transaction() as db:
                    cur = db.execute('UPDATE users SET role=?,active=? WHERE id=?', (p['role'], int(p['active']), text(p, 'id')))
                    need(cur.rowcount == 1, 'User not found', 404)
                    db.execute('DELETE FROM sessions WHERE user_id=?', (p['id'],))
                    store.event(db, user, 'user_update', p['id'], {'role': p['role'], 'active': p['active']})
                self.reply({'ok': True}); return
            need(path == '/api/command', 'Not found', 404)
            result = store.command(user, text(p, 'action'), p.get('payload', {}), self.headers.get('Idempotency-Key', ''))
            self.reply({'result': result})
        except Problem as exc:
            self.reply({'error': str(exc)}, exc.status)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            logging.exception('POST failed')
            self.reply({'error': 'Server error; operation rolled back. Refresh before retrying.'}, 500)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--db', type=Path)
    parser.add_argument('--demo', action='store_true', help='Use isolated synthetic demo database; never seeds a live DB')
    parser.add_argument('--init', action='store_true', help='Initialize live database and administrator then exit')
    parser.add_argument('--origin', help='Exact browser-facing origin, including scheme and port')
    parser.add_argument('--secure-cookies', action='store_true')
    parser.add_argument('--backup', type=Path, help='Create consistent private SQLite backup then exit')
    args = parser.parse_args()
    dbpath = args.db or DEFAULT_PRIVATE / ('demo.sqlite3' if args.demo else 'live.sqlite3')
    store = Store(dbpath)
    if args.backup:
        args.backup.parent.mkdir(parents=True, exist_ok=True)
        need(not args.backup.exists(), 'Backup destination already exists')
        with store.connect() as src, sqlite3.connect(args.backup) as dst:
            src.backup(dst)
        print('Consistent backup created. Keep it private.'); return
    with store.connect() as db:
        count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        mode = db.execute("SELECT value FROM meta WHERE key='mode'").fetchone()[0]
    if args.init:
        need(count == 0, 'Database already initialized')
        username = input('Administrator username (use a role code): ').strip()
        password = getpass.getpass('Password (12+ characters): ')
        need(password == getpass.getpass('Confirm password: '), 'Passwords do not match')
        create_user(store, username, password, 'admin')
        print('Administrator created. Start server without --init.'); return
    if args.demo and count == 0:
        password = os.environ.get('BTG_DEMO_PASSWORD') or secrets.token_urlsafe(18)
        seed_demo(store, password)
        DEFAULT_PRIVATE.mkdir(parents=True, exist_ok=True)
        (DEFAULT_PRIVATE / 'demo-access.txt').write_text('LOCAL DEMONSTRATION ONLY\nUsernames: admin, secretary, student, captain, checker, guard, maintenance, office\nPassword: ' + password + '\n', encoding='utf-8')
        print('Isolated demo created. Local credentials: app/private/demo-access.txt', flush=True)
    elif args.demo:
        need(mode == 'DEMO', '--demo cannot run a live database')
    else:
        need(count > 0, 'Initialize first: python app/server.py --init')
        need(mode == 'LIVE', 'Demo databases require --demo')
    need(args.host in {'127.0.0.1', 'localhost'} or (args.origin and args.secure_cookies), 'Network binding requires --origin and --secure-cookies behind HTTPS')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    server = Server((args.host, args.port), store, args.origin, args.secure_cookies)
    print(f'Beyond the Game: {server.origin} | {"DEMO — SYNTHETIC DATA" if args.demo else "LIVE"}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    try:
        main()
    except Problem as exc:
        sys.exit(str(exc))

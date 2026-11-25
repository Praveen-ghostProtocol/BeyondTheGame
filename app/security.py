"""Password hashing and persisted session authentication (no third-party runtime)."""
import hashlib
import hmac
import secrets
import time
import uuid

from domain import Problem, ROLES, need, now

ITERATIONS = 310000


def password_hash(password):
    need(isinstance(password, str) and 12 <= len(password) <= 256, 'Use a password of 12–256 characters')
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), ITERATIONS).hex()
    return f'pbkdf2_sha256${ITERATIONS}${salt}${digest}'


def verify(password, encoded):
    if not isinstance(password, str) or len(password) > 256:
        return False
    _, rounds, salt, expected = encoded.split('$')
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), int(rounds)).hex()
    return hmac.compare_digest(digest, expected)


def create_user(store, username, password, role, actor=None):
    from domain import ident
    ident(username)
    need(role in ROLES, 'Invalid role')
    encoded = password_hash(password)
    with store.transaction() as db:
        need(not db.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone(), 'Username already exists', 409)
        uid = 'U-' + uuid.uuid4().hex[:12]
        db.execute('INSERT INTO users VALUES(?,?,?,?,1,?)', (uid, username, encoded, role, now()))
        result = {'id': uid, 'username': username, 'role': role}
        if actor:
            store.event(db, actor, 'user_create', uid, {'role': role})
        return result


def authenticate(store, username, password, client):
    username = username.strip() if isinstance(username, str) else ''
    key = hashlib.sha256((client + '|' + username.casefold()).encode()).hexdigest()
    with store.transaction() as db:
        attempt = db.execute('SELECT * FROM login_attempts WHERE key=?', (key,)).fetchone()
        if attempt and attempt['failures'] >= 8 and attempt['until'] > time.time():
            return None, 'Too many attempts. Try again in 15 minutes.', 429
        row = db.execute('SELECT * FROM users WHERE username=? COLLATE NOCASE', (username,)).fetchone()
        # Constant-cost missing-user path.
        encoded = row['password'] if row else f'pbkdf2_sha256${ITERATIONS}$' + '00' * 16 + '$' + '00' * 32
        valid = verify(password, encoded)
        if not row or not row['active'] or not valid:
            failures = attempt['failures'] + 1 if attempt and attempt['until'] > time.time() else 1
            db.execute('INSERT OR REPLACE INTO login_attempts VALUES(?,?,?)', (key, failures, time.time() + 900))
            return None, 'Username or password is incorrect', 401
        db.execute('DELETE FROM login_attempts WHERE key=?', (key,))
        db.execute('DELETE FROM sessions WHERE expires<?', (time.time(),))
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        db.execute('INSERT INTO sessions VALUES(?,?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), row['id'], csrf, time.time() + 43200))
        return {'token': token, 'csrf': csrf, 'user': {'id': row['id'], 'username': row['username'], 'role': row['role']}}, None, 200


DEMO_ROLES = ('student', 'secretary')


def demo_session(store, role):
    """Password-free, view-only reviewer session; demo users are created on first use."""
    need(role in DEMO_ROLES, 'Choose student or secretary')
    username = 'demo-' + role
    unusable = password_hash(secrets.token_urlsafe(32))  # nobody can sign in with a password
    with store.transaction() as db:
        row = db.execute('SELECT id,username,role FROM users WHERE username=?', (username,)).fetchone()
        if not row:
            uid = 'U-' + uuid.uuid4().hex[:12]
            db.execute('INSERT INTO users VALUES(?,?,?,?,1,?)', (uid, username, unusable, role, now()))
            row = {'id': uid, 'username': username, 'role': role}
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        db.execute('INSERT INTO sessions VALUES(?,?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), row['id'], csrf, time.time() + 7200))
        return {'token': token, 'csrf': csrf, 'user': {'id': row['id'], 'username': row['username'], 'role': row['role']}}


def is_demo(user):
    return user['username'].startswith('demo-')


def session(store, token):
    with store.connect() as db:
        row = db.execute('SELECT s.csrf,u.id,u.username,u.role FROM sessions s JOIN users u ON u.id=s.user_id '
                         'WHERE s.token_hash=? AND s.expires>? AND u.active=1',
                         (hashlib.sha256(token.encode()).hexdigest(), time.time())).fetchone()
        need(row is not None, 'Sign in to continue', 401)
        return {'id': row['id'], 'username': row['username'], 'role': row['role']}, row['csrf']

"""Supabase PostgreSQL adapter reusing the tested lifecycle domain service.

Only the Vercel backend uses this module. No database secret reaches the browser.
Connections use TLS, no prepared statements, and transaction-local schema state.
"""
import os
from contextlib import contextmanager

from domain import Problem, Store, need

WRITE_LOCK = 2311202601


class Row(dict):
    """SQLite-style named and positional access over a psycopg tuple."""
    def __init__(self, columns, values):
        super().__init__(zip(columns, values))
        self.values_tuple = tuple(values)

    def __getitem__(self, key):
        return self.values_tuple[key] if isinstance(key, int) else super().__getitem__(key)


class Cursor:
    def __init__(self, cursor):
        self.cursor = cursor

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def wrap(self, row):
        return Row([c.name for c in self.cursor.description], row) if row is not None else None

    def fetchone(self):
        return self.wrap(self.cursor.fetchone())

    def fetchall(self):
        return [self.wrap(row) for row in self.cursor.fetchall()]

    def __iter__(self):
        for row in self.cursor:
            yield self.wrap(row)


def translate(sql):
    """Translate the small, audited SQLite query surface used by existing code."""
    sql = sql.replace(' COLLATE NOCASE', '')
    if sql.lstrip().upper().startswith('INSERT OR REPLACE INTO LOGIN_ATTEMPTS'):
        sql = ('INSERT INTO login_attempts (key,failures,until) VALUES(?,?,?) '
               'ON CONFLICT(key) DO UPDATE SET failures=EXCLUDED.failures,until=EXCLUDED.until')
    result = []
    quote = None
    index = 0
    while index < len(sql):
        char = sql[index]
        if quote:
            result.append(char)
            if char == quote:
                if index + 1 < len(sql) and sql[index + 1] == quote:
                    result.append(quote)
                    index += 1
                else:
                    quote = None
        elif char in {"'", '"'}:
            quote = char
            result.append(char)
        else:
            result.append('%s' if char == '?' else char)
        index += 1
    return ''.join(result)


class Connection:
    def __init__(self, dsn):
        import psycopg
        self.raw = psycopg.connect(dsn, sslmode='require', connect_timeout=8,
                                  prepare_threshold=None, autocommit=True)
        try:
            self.raw.execute('BEGIN')
            self.raw.execute('SET LOCAL search_path TO btg, extensions, pg_catalog')
            self.raw.execute("SET LOCAL statement_timeout = '15000ms'")
            self.raw.execute("SET LOCAL lock_timeout = '10000ms'")
        except Exception:
            self.raw.close()
            raise

    def execute(self, sql, params=()):
        normalized = sql.strip().rstrip(';').upper()
        if normalized == 'BEGIN IMMEDIATE':
            return Cursor(self.raw.execute('SELECT pg_advisory_xact_lock(%s)', (WRITE_LOCK,)))
        if normalized == 'BEGIN':
            # Match SQLite's stable read snapshot across every kind/metric query.
            return Cursor(self.raw.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ'))
        import psycopg
        try:
            return Cursor(self.raw.execute(translate(sql), params or None))
        except psycopg.IntegrityError as exc:
            raise Problem('This operation conflicts with an existing database record', 409) from exc

    def commit(self):
        self.raw.execute('COMMIT')

    def rollback(self):
        self.raw.execute('ROLLBACK')

    def close(self):
        self.raw.close()

    def __enter__(self):
        return self

    def __exit__(self, kind, value, traceback):
        try:
            self.rollback() if kind else self.commit()
        finally:
            self.close()


class PostgresStore(Store):
    def __init__(self, dsn=None):
        self.dsn = dsn or os.environ.get('BTG_DATABASE_URL', '')
        need(self.dsn, 'Hosted database is not configured', 503)
        need(self.dsn.startswith(('postgres://', 'postgresql://')), 'Invalid hosted database configuration', 503)
        # Schema creation and demo bootstrap are explicit deployment operations.
        # Never create a local SQLite file or run migrations on a cold start.

    def connect(self):
        return Connection(self.dsn)

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

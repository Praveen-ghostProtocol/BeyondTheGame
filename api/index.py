"""Vercel Python function: same HTTP routes, sessions and domain rules."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from domain import Problem
from postgres_store import PostgresStore
from server import Handler


def allowed_origins(environ=None):
    env = environ if environ is not None else os.environ
    origins = set()
    for item in (env.get('BTG_APP_ORIGIN', ''), env.get('VERCEL_URL', ''),
                 env.get('VERCEL_PROJECT_PRODUCTION_URL', '')):
        if item:
            origin = item if item.startswith('https://') else 'https://' + item
            parsed = urlsplit(origin)
            if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password:
                origins.add('https://' + parsed.netloc)
    return origins


class Unconfigured:
    def __getattr__(self, name):
        raise Problem('Hosted database is not configured yet', 503)


class handler(Handler):
    def __init__(self, request, client_address, server):
        origins = allowed_origins()
        try:
            store = PostgresStore()
        except Problem:
            store = Unconfigured()
        config = SimpleNamespace(store=store, origin=next(iter(origins), ''), secure=True)
        self.allowed_origins = origins
        super().__init__(request, client_address, config)

    def parse_request(self):
        if not super().parse_request():
            return False
        host_origin = 'https://' + self.headers.get('Host', '')
        if host_origin not in self.allowed_origins:
            self.reply({'error': 'Unexpected deployment host'}, 403)
            return False
        self.server.origin = host_origin
        parsed = urlsplit(self.path)
        route = parse_qs(parsed.query).get('route', [])
        if parsed.path in {'/api/index', '/api/index.py'} and route:
            self.path = '/api/' + route[0]
        return True

    def do_GET(self):
        if urlsplit(self.path).path == '/api/ready':
            try:
                with self.server.store.connect() as db:
                    mode = db.execute("SELECT value FROM meta WHERE key='mode'").fetchone()[0]
                    version = db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0]
                self.reply({'status': 'ready', 'database': 'Supabase PostgreSQL', 'schema': version, 'mode': mode})
            except Problem as exc:
                self.reply({'error': str(exc)}, exc.status)
            except Exception:
                # Never include connection strings or credentials in a readiness response.
                self.reply({'error': 'Database is not ready'}, 503)
            return
        super().do_GET()

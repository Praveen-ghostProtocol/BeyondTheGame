"""Reviewer demo: password-free student/secretary sessions that cannot change records."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from http_transport import request
from domain import Store


class DemoMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'demo.sqlite3')

    def tearDown(self):
        self.tmp.cleanup()

    def post(self, path, payload, cookie='', csrf=''):
        body = json.dumps(payload).encode()
        h = {'Content-Type': 'application/json', 'Origin': 'http://127.0.0.1:8000', 'Cookie': cookie, 'X-CSRF-Token': csrf}
        status, headers, raw = request(self.store, 'POST', path, body, h)
        return status, headers, json.loads(raw)

    def demo(self, role):
        status, headers, body = self.post('/api/demo-login', {'role': role})
        self.assertEqual(200, status)
        return headers['Set-Cookie'].split(';')[0], body

    def test_roles_and_reuse(self):
        c1, b1 = self.demo('student')
        _, b2 = self.demo('student')
        _, b3 = self.demo('secretary')
        self.assertEqual(('demo-student', 'student'), (b1['user']['username'], b1['user']['role']))
        self.assertEqual(b1['user']['id'], b2['user']['id'])  # one demo user per role
        self.assertEqual('secretary', b3['user']['role'])
        status, _, state = request(self.store, 'GET', '/api/state', headers={'Cookie': c1})
        self.assertEqual(200, status)

    def test_other_roles_refused(self):
        for role in ('admin', 'checker', None):
            self.assertEqual(400, self.post('/api/demo-login', {'role': role})[0])

    def test_view_only(self):
        cookie, body = self.demo('secretary')
        status, _, out = self.post('/api/command', {'action': 'asset_create', 'payload': {'id': 'X-001', 'name': 'x', 'sport': 'x'}}, cookie, body['csrf'])
        self.assertEqual(403, status)
        self.assertIn('view-only', out['error'])
        self.assertEqual(200, self.post('/api/logout', {}, cookie, body['csrf'])[0])


if __name__ == '__main__':
    unittest.main()

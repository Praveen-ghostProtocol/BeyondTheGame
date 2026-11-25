"""Cloud transport/security contracts; real remote DB checks are separate."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from domain import Problem
from postgres_store import Cursor, PostgresStore, Row, translate

spec = importlib.util.spec_from_file_location('btg_cloud_api', ROOT / 'api/index.py')
cloud = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cloud)


class CloudContracts(unittest.TestCase):
    def test_parameter_placeholders_do_not_rewrite_quoted_literals(self):
        self.assertEqual("SELECT '?' AS literal, %s AS value", translate("SELECT '?' AS literal, ? AS value"))
        self.assertEqual("SELECT 'it''s ?', %s", translate("SELECT 'it''s ?', ?"))

    def test_login_attempt_upsert_preserves_one_row_per_bucket(self):
        query = translate('INSERT OR REPLACE INTO login_attempts VALUES(?,?,?)')
        self.assertIn('ON CONFLICT(key) DO UPDATE', query)
        self.assertEqual(3, query.count('%s'))

    def test_case_insensitive_username_query_uses_pg_type(self):
        self.assertEqual('SELECT * FROM users WHERE username=%s',
                         translate('SELECT * FROM users WHERE username=? COLLATE NOCASE'))
        self.assertIn('username extensions.citext', (ROOT / 'database/postgres-schema.sql').read_text())

    def test_named_and_positional_row_access_stays_compatible(self):
        row = Row(['id', 'role'], ['TEST', 'student'])
        self.assertEqual('TEST', row[0]); self.assertEqual('student', row['role'])
        self.assertEqual({'id':'TEST','role':'student'}, dict(row))

    def test_no_host_database_creates_sqlite_fallback(self):
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(Problem) as error: PostgresStore()
        self.assertEqual(503, error.exception.status)

    def test_only_explicit_https_deployment_origins_allowed(self):
        origins = cloud.allowed_origins({'BTG_APP_ORIGIN':'https://btg.example',
            'VERCEL_URL':'btg-unique.vercel.app','VERCEL_PROJECT_PRODUCTION_URL':'btg.vercel.app'})
        self.assertEqual({'https://btg.example','https://btg-unique.vercel.app','https://btg.vercel.app'}, origins)
        self.assertNotIn('https://attacker.invalid', origins)

    def test_embedded_credentials_cannot_form_an_allowed_origin(self):
        self.assertEqual(set(), cloud.allowed_origins({'BTG_APP_ORIGIN':'https://user:pass@host.invalid'}))

    def test_cloud_data_is_private_with_rls_and_restricted_role(self):
        sql = (ROOT / 'database/postgres-schema.sql').read_text()
        for table in ('meta','users','sessions','login_attempts','records','events','operations'):
            self.assertIn('ALTER TABLE btg.' + table + ' ENABLE ROW LEVEL SECURITY', sql)
        self.assertIn('REVOKE ALL ON SCHEMA btg FROM PUBLIC,anon,authenticated', sql)

    def test_write_serialization_and_stable_read_snapshot(self):
        source = (ROOT / 'app/postgres_store.py').read_text()
        self.assertIn('pg_advisory_xact_lock', source)
        self.assertIn('REPEATABLE READ', source)
        self.assertIn('prepare_threshold=None', source)
        self.assertIn("sslmode='require'", source)

    def test_public_build_has_no_private_or_source_paths(self):
        from subprocess import run
        r = run([sys.executable, str(ROOT / 'scripts/build_vercel.py')], capture_output=True)
        self.assertEqual(0, r.returncode)
        files = {p.relative_to(ROOT / 'public').as_posix() for p in (ROOT / 'public').rglob('*') if p.is_file()}
        self.assertEqual({'index.html','style.css','app.js','scanner.js','favicon.svg','vendor/jsQR.js','vendor/qrcode.js'}, files)

    def test_secret_files_are_excluded_from_deployment(self):
        ignore = (ROOT / '.vercelignore').read_text()
        self.assertIn('app/private', ignore); self.assertIn('.env*', ignore)
        config = json.loads((ROOT / 'vercel.json').read_text())
        self.assertIn('app/private/**', config['functions']['api/index.py']['excludeFiles'])


if __name__ == '__main__':
    unittest.main()

# Vercel + Supabase deployment

Deployed and checked on 25 November 2026. This supersedes the earlier blocked-publication status in the local pilot handoff.

- Application: https://beyond-the-game-omega.vercel.app
- Repository: https://github.com/Praveen-ghostProtocol/BeyondTheGame
- Vercel project: `beyond-the-game`, Mumbai function region (`bom1`).
- Supabase: separate free BeyondTheGame project, Mumbai (`ap-south-1`), reference `ivobrmuuyjacsnplcfdd`.
- Current data mode: **DEMO**. All inventory and events are synthetic.

## Architecture and credentials

Vercel serves an explicit static asset allowlist and routes `/api/*` to `api/index.py`. The API reuses the local domain and authentication services through `app/postgres_store.py`. PostgreSQL transactions use a transaction pooler, TLS, transaction-local schema selection and a shared advisory write lock. Multi-query reads use repeatable-read snapshots. There is no cloud SQLite fallback or database migration during requests.

The private `btg` schema has RLS enabled on every table. Anonymous and authenticated Supabase API roles cannot access it. The restricted `btg_runtime` database role has only necessary table grants; event rewriting/deletion is prohibited. Supabase Auth is not the application's identity provider: existing PBKDF2 passwords, persisted HttpOnly/Secure sessions, CSRF checks and domain role checks remain in use.

`BTG_DATABASE_URL` is a sensitive **server-side** Vercel production/preview environment variable. `BTG_APP_ORIGIN` is the canonical HTTPS application origin. No database password, session, seed credential, `.env` or private artifact belongs in GitHub or the static output. Generated demonstration access instructions are available locally in `app/private/cloud-access.txt`.

Public schema source is `database/postgres-schema.sql`. `scripts/prepare_cloud_demo.py` prepares private seed/role artifacts for a new empty demonstration environment; it refuses overwriting existing provisioning files. It does not run automatically during deployment. Back up data before administrative changes; backup/restore drills and load certification remain pending.

## Build and publication

Python is pinned to 3.12 for Vercel and psycopg binary to 3.3.9. `python scripts/build_vercel.py` copies only seven named frontend files into ignored `public/`. `.vercelignore` and function exclusions omit private data, tests and research files. Source uploads used the same explicit deployment allowlist.

Deployment `dpl_GFwFmakXytgGL6htRZkJX6mb6fEc` reached READY and owns the canonical domain. The project was deployed by source upload, **not an automatic GitHub integration**. Future repository pushes do not by themselves redeploy this project. Redeploy using the Vercel project/CLI or deliberately configure its Git integration. Keep the exact project, team and environment scope when setting variables.

GitHub connector access was installed for **BeyondTheGame only**, and publication succeeded as separate research, backend, Stitch UI, verification and normalization commits. Local main was synchronized to those published commits while preserving the original local history on `local-development-history`.

## Executed verification

- Local Python discovery: **101 tests passed**, including 11 PostgreSQL adapter/deployment contract tests. These contract tests do not replace a live database integration test.
- Earlier recorded JavaScript verification: 31 C3 mechanism tests, 13 QR tests and 31 Chromium application assertions passed; see `docs/testing/phase-d-verification.md` for scope.
- Hosted `/api/ready`: HTTP 200, Supabase PostgreSQL schema 2, DEMO.
- Hosted login and role-specific state succeeded for secretary and checker; logout returned to the sign-in screen.
- A browser-created request for synthetic asset `BD-001` completed checkout, return declaration, independent checker receipt and inspection. Request `REQ-c7ae90bc22d3`; loan `LOA-4f06b5a82b7d`. PostgreSQL independently confirmed RETURNED loan and AVAILABLE asset. Inspection notes explicitly state that no physical equipment was inspected. Audit entries remain SIMULATED.
- RLS security advisor returned no findings at provisioning. Anonymous schema access and runtime event-update privilege were checked and denied.

This is a hosted software smoke check, **not field validation, a physical stock audit, a camera/printed-label test or evidence of improved accountability**. No printable stock batch has been generated for real enrollment. Phone-camera checks, real IDs, participant trials, deployment protection from a fresh anonymous device, restoration and operational load testing remain pending. `final/` remains reserved.

## Local server recovery

The execution sandbox's server process/loopback was not reliably accessible from the user's browser. A persistent local browser connection has **not** been certified. Double-click `Start-Local.cmd` on the host computer to start the demonstration outside that sandbox and open the browser; the launcher reuses a healthy server and writes logs to `app/private/`. Alternatively run `python app/server.py --demo` in a terminal you keep open. The hosted application works independently of that local process.

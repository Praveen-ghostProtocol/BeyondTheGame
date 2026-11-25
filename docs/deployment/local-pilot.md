# Local pilot and deployment handoff

> Update, 25 November 2026: GitHub publication and Vercel + Supabase hosting now succeeded. Read [the current cloud guide](vercel-supabase.md). The blocked-connection account below is historical. The host launcher `Start-Local.cmd` is provided; local browser reachability still needs host-side confirmation.

The full application is implemented and has synthetic automated verification. Actual deployment networking, physical scanning and field use remain separate checks. Do not confuse the isolated demonstration with enrolled hostel stock.

## Start and access

From the nested repository root, run `python app/server.py --demo`, then visit `http://127.0.0.1:8000`. Read the generated `app/private/demo-access.txt` locally. The developer test credentials are not the generated local demo credentials. Demonstration inventory is synthetic and does not represent current hostel counts.

For actual enrollment initialize a separate live DB using `python app/server.py --init` and then run `python app/server.py`. The administrator provisions individual accounts, including secretary, independent checker, guard and office. No live account, ID scan, room number or real borrowing has been created during this implementation.

## Physical readiness work

1. Coordinate actual operating permission and consent. Confirm guard duties remain limited to key handling.
2. Walk through resident pickup/return, captain kit checkout and checker inspection using actual equipment.
3. Register actual IDs/locations/condition. No trial-mix count is a stock audit.
4. Verify the app over intended network/HTTPS and on the intended phones. Camera API needs HTTPS outside localhost.
5. Test a single reversible printed ID/QR at 100% print scale and suitable quiet zone. Check lighting, label positioning, scanning and manual fallback. No codes have been physically printed or attached by the developer.
6. Only then prepare actual registered-asset label batches. Demo label sheets must not be used as real stock labels.
7. Run actual independent baseline/audit and consented matched C4 scenarios. Record failures, task burden and limitations; do not prefill the previous workbooks with software-test data.

## Host checks

Verify network routing, exact `--origin`, browser-facing Host forwarding, HTTPS, Secure cookies, port restrictions, stop/restart persistence, a consistent backup and restoration procedure, simultaneous device access and account revocation. Bind a network interface only behind an approved trusted proxy. A configured production-capable server/managed identity is appropriate before broader public deployment; the supplied standard-library server is intentionally a bounded local implementation.

Public website hosting, cloud credentials, institutional SSO, email/SMS notifications and load certification were not part of the available configured environment and have not been performed. Notifications are visible as in-app queues and overdue counts; no messages are sent externally.

## GitHub publication status

Repository target: https://github.com/Praveen-ghostProtocol/BeyondTheGame.git

On 25 November 2026 the connected GitHub metadata reported `push: true`, but the first attempted contents write returned **HTTP 403: Resource not accessible by integration**. No remote file or commit was created by that call. Direct Git HTTPS access also could not resolve `github.com` in the execution environment. Work is preserved in local meaningful Git commits, with origin configured. No successful push is claimed.

Once the GitHub integration's repository Contents write access or the local Git network/credentials work, push the existing branch with `git push -u origin main`. The handoff Git bundle contains full history and can be cloned in a Git-enabled environment. Do not force-push if someone has initialized the remote in the meantime; fetch and reconcile existing history first.

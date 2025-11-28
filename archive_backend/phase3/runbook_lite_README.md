MarSci Lite — Phase 3 (Staging) Remediation — LITE-ONLY
=====================================================
This package follows ONLY the MarSci Lite Project blueprint (no OS systems or artifacts).
It contains minimal, secure staging artifacts suitable for small-team operations.

Files included:
- Dockerfile
- docker-compose.yml  (backend + redis)
- nginx/marsci_staging.conf  (Basic Auth + IP allowlist example)
- ops/gen_htpasswd.sh
- db/sqlite_create_audit.sql
- app/audit_sqlite.py
- app/metrics_simple.py
- app/rate_limit_notes.txt
- smoke_tests/run_smoke_tests.py

Deployment (recommended):
1. Place merged Phase2 backend code (app/) into this folder root.
2. Create ./data directory for sqlite DB persistence: mkdir -p data
3. Build & run:
   docker-compose build
   docker-compose up -d
4. Create htpasswd:
   chmod +x ops/gen_htpasswd.sh
   ./ops/gen_htpasswd.sh deployer StrongPass123! ./.htpasswd
   (Copy ./.htpasswd content to nginx host /etc/nginx/.htpasswd or mount into nginx container)
5. Start nginx with provided config (or use local reverse proxy). Ensure nginx can reach backend at http://backend:8000
6. Run smoke tests:
   python3 -m pip install requests
   python3 smoke_tests/run_smoke_tests.py

Security & Lite constraints:
- No external identity provider (Keycloak/Auth0) in Lite: use Basic Auth + IP allowlist for staging.
- Use nginx limit_req for rate-limiting (60 req/min).
- Audit events stored in a local sqlite DB (`/data/audit.db`).
- Metrics endpoint is simple JSON only; no Prometheus/OS-level monitoring included.
- This package intentionally omits OS-level automation, Helm, Kubernetes, and heavy tooling.

Acceptance criteria (Lite):
- Staging protected by Basic Auth and IP allowlist.
- TLS applied via nginx (CERTBOT) on ops side (not included).
- Rate-limit enforced (nginx).
- Audit events persisted (sqlite) and retrievable.
- Simple metrics endpoint accessible at /metrics.

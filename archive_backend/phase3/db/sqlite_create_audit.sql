-- db/sqlite_create_audit.sql
CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  user_id TEXT,
  role TEXT,
  action TEXT NOT NULL,
  kpi_set TEXT,
  ip_address TEXT,
  user_agent TEXT
);

# app/audit_sqlite.py
import os, aiosqlite, json
from datetime import datetime

DB_PATH = os.getenv("AUDIT_DB_PATH", "/data/audit.db")

async def ensure_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            user_id TEXT,
            role TEXT,
            action TEXT NOT NULL,
            kpi_set TEXT,
            ip_address TEXT,
            user_agent TEXT
        );""")
        await db.commit()

async def write_audit_event(user_id, role, action, kpi_set, ip, ua):
    await ensure_db()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO audit_events (ts, user_id, role, action, kpi_set, ip_address, user_agent)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (datetime.utcnow().isoformat()+"Z", user_id, role, action, json.dumps(kpi_set), ip, ua)
        )
        await db.commit()

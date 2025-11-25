# MarSci Lite — Backend (Phase2 + Phase3)
(C) 2025 Annop Sripuna

FastAPI backend for KPI anomaly detection, scoring engine, and audit logging.  
Designed for **local use**, lightweight, and ready for frontend integration.

---

## 📁 Project Structure

```
backend/
├── data/
│   └── roles.json
│
├── phase2/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   └── README_deploy.md
│
├── phase3/
│   ├── app/
│   ├── db/
│   ├── nginx/
│   ├── ops/
│   └── smoke_tests/
│
├── run_local.ps1
├── run_smoke_tests.ps1
├── requirements.txt
└── .gitignore
```

---

## 🚀 Run Backend (Local Mode)

### 1. Start server

```powershell
cd backend
.\run_local.ps1
```

Backend will start at:

```
http://localhost:8000
```

### 📌 API Endpoints

**Health check**  
`GET /healthz`

**Version**  
`GET /version`

**Analyze KPI**  
`POST /analyze`

### Example request

```json
{
  "kpi": "CTR",
  "window": 5,
  "values": [0.02, 0.025, 0.018, 0.03, 0.022],
  "role": "analyst"
}
```

### Example response

```json
{
  "kpi": "CTR",
  "severity": "Red",
  "benchmark_min": 0.0188,
  "benchmark_max": 0.0271,
  "summary": "High anomaly detected",
  "timestamp": "2025-11-25T20:02:17.452Z"
}
```

---

## 🔥 Smoke Test

```powershell
cd backend
.\run_smoke_tests.ps1
```

---

## 📝 Notes

- Local mode uses Python venv at `.venv/`
- `roles.json` auto-created if missing
- SQLite audit DB is **not** versioned (ignored in Git)
- Suitable for lightweight deployment, development, or POC

---

## 📄 License

(C) by **Annop Sripuna**  
All rights reserved.

# MarSci Lite — Phase 2 Stats Engine (FastAPI starter)
This is a starter backend implementing the Stats Engine per Phase 2 of the MarSci Lite Blueprint.
Endpoints:
- GET /health
- POST /analyze/  (payload: {kpi, window, values[]}) -> returns stats + severity
Run locally:
- python -m uvicorn app.main:app --reload
Docker:
- docker build -t marsci-phase2 .
- docker run -p 8000:8000 marsci-phase2
Tests: pytest

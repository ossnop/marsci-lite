MarSci Lite — Phase2 Backend Patch
Files included:
- app/engine.py
- app/models.py
- app/main.py
- app/ai/base_scoring.py
- app/ai/ai_hook.py
- tests/test_api.py

How to run:
1. Create virtualenv: python -m venv .venv
2. Activate: source .venv/bin/activate
3. Install: pip install fastapi uvicorn pytest
4. Run server: python -m uvicorn app.main:app --reload --port 8000
5. Run tests: pytest -q

Notes:
- This patch merges into the provided starter zip. The merged package is available at /mnt/data/marsci-lite-phase2-backend-merged.zip

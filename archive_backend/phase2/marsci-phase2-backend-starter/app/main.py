# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import KPIRequest
from app.engine import default_stats_engine
import logging

app = FastAPI(title="MarSci Lite Backend")

# basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("marsci")

# -- CORS (for local dev; tighten in staging)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": "0.1.0"}

@app.post("/analyze")
def analyze(request: KPIRequest):
    try:
        # simple validation: optional window vs values length
        if request.window is not None and len(request.values) != request.window:
            raise HTTPException(status_code=400, detail="Window length mismatch with values count")
        result = default_stats_engine.analyze(kpi=request.kpi, values=request.values)
        logger.info("Analyze run for KPI=%s severity=%s", result.get("kpi"), result.get("severity"))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Internal error in analyze")
        raise HTTPException(status_code=500, detail="Internal processing error")

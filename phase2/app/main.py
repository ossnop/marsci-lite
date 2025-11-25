# app/main.py
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.models import KPIInput
from app.engine import evaluate_kpi

RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))

app = FastAPI(title="MarSci Lite — Phase2 Backend")

logger = logging.getLogger("uvicorn.error")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat()+"Z"}

@app.get("/version")
async def version():
    return {"version": "phase2-backend-1.0", "build": os.getenv("BUILD_TAG", "local")}

@app.post("/analyze")
async def analyze(payload: KPIInput, request: Request):
    logger.info("analyze.request kpi=%s window=%d role=%s", payload.kpi, payload.window, payload.role)
    try:
        result = evaluate_kpi(payload.kpi, payload.window, payload.values)
        if "error" in result:
            logger.warning("validation failed: %s", result["error"])
            raise HTTPException(status_code=400, detail=result["error"])
        if payload.role != "admin":
            result.pop("raw_stats", None)
        try:
            logger.info("audit: analyze called kpi=%s role=%s ts=%s", payload.kpi, payload.role, datetime.utcnow().isoformat()+"Z")
        except Exception:
            logger.exception("audit log failed (non-blocking)")
        return JSONResponse(content={
            "kpi": result["kpi"],
            "severity": result["severity"],
            "benchmark_min": result["benchmark_min"],
            "benchmark_max": result["benchmark_max"],
            "summary": result["summary"],
            "timestamp": datetime.utcnow().isoformat()+"Z"
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("analyze: unexpected error")
        raise HTTPException(status_code=500, detail="internal error")

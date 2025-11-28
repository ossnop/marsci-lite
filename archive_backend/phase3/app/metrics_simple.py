# app/metrics_simple.py
import time
from fastapi import APIRouter, Request

router = APIRouter()

METRICS = {"requests": 0, "errors": 0, "last_request_ts": None}

@router.get("/metrics")
async def metrics():
    return METRICS

async def record_request(success: bool = True):
    METRICS["requests"] += 1
    if not success:
        METRICS["errors"] += 1
    METRICS["last_request_ts"] = time.time()

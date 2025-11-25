from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conlist, confloat
from typing import List, Optional
from app.models.stats import compute_stats, severity_from_sd_pct
router = APIRouter()
class AnalyzeRequest(BaseModel):
    kpi: str
    window: int
    values: conlist(confloat(), min_items=1)
    request_id: Optional[str] = None
class AnalyzeResponse(BaseModel):
    kpi: str
    window: int
    mean: float
    median: float
    sd: float
    iqr: float
    sd_pct: float
    severity: str
@router.post("/", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if req.window < 3 or req.window > 90:
        raise HTTPException(status_code=400, detail="window out of range")
    if len(req.values) != req.window:
        raise HTTPException(status_code=400, detail="length mismatch")
    mean, median, sd, iqr, sd_pct = compute_stats(req.values)
    severity = severity_from_sd_pct(sd_pct)
    return AnalyzeResponse(kpi=req.kpi, window=req.window, mean=mean, median=median, sd=sd, iqr=iqr, sd_pct=sd_pct, severity=severity)

# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class KPIInput(BaseModel):
    kpi: str = Field(..., description="KPI name (CTR, CPC, CPM, CVR, CPE, ER, CPV, View Rate)")
    window: int = Field(..., ge=3, le=90, description="Window length (days)")
    values: List[float] = Field(..., description="Numeric KPI time series values (length == window)")
    impressions: Optional[int] = Field(None, description="Optional: impressions for volume-aware logic")
    clicks: Optional[int] = Field(None, description="Optional: clicks")
    conversions: Optional[int] = Field(None, description="Optional: conversions")
    spend: Optional[float] = Field(None, description="Optional: spend")
    role: Optional[str] = Field("anon", description="role for masking (admin/analyst/anon)")

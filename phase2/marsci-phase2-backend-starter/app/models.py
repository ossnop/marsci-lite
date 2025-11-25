# app/models.py
from pydantic import BaseModel, validator
from typing import List, Optional

class KPIRequest(BaseModel):
    kpi: str
    window: Optional[int] = None
    values: List[float]

    @validator('values')
    def check_values_non_empty(cls, v):
        if not v or len(v) == 0:
            raise ValueError('values must contain at least one numeric value')
        return v

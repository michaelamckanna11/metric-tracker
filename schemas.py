from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MetricBase(BaseModel):
    url: str
    status_code: int = Field(..., ge=100, le=599)
    response_time: float = Field(..., gt=0 )

class MetricCreate(MetricBase):
    pass    

class MetricUpdate(BaseModel):
    url: Optional[str] = None
    status_code: Optional[int] = Field(None, ge=100, le=599)
    response_time: Optional[float] = Field(None, gt=0 )

class MetricResponse(MetricBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True # SQLAlchemy

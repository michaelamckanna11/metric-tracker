from pydantic import BaseModel

class MetricCreate(BaseModel):
    url: str
    status_code: int
    response_time: float
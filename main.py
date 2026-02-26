from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Metric
from schemas import MetricCreate

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# First POST endpoint
@app.post("/metrics")
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    db_metric = Metric(
        url=metric.url, 
        status_code=metric.status_code, 
        response_time=metric.response_time
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

# List all metrics
@app.get("/metrics")
def read_metrics(db: Session = Depends(get_db)):
    return db.query(Metric).all()

# Get a single metric by ID
@app.get("/metrics/{metric_id}")
def read_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric
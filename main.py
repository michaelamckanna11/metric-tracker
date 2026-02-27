from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Metric
from schemas import MetricCreate, MetricUpdate, MetricResponse

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# First POST endpoint
@app.post("/metrics", response_model=MetricResponse)
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
@app.get("/metrics", response_model=list[MetricResponse])
def read_metrics(db: Session = Depends(get_db)):
    return db.query(Metric).all()

# Get a single metric by ID
@app.get("/metrics/{metric_id}", response_model=MetricResponse)
def read_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

# Updating a single metric by ID
@app.put("/metrics/{metric_id}", response_model=MetricResponse)
def update_metric(metric_id: int, metric_update: MetricUpdate, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()

    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    if metric_update.url is not None:
        metric.url = metric_update.url
    if metric_update.status_code is not None:
        metric.status_code = metric_update.status_code
    if metric_update.response_time is not None:
        metric.response_time = metric_update.response_time

    db.commit()
    db.refresh(metric)

    return metric            
        

# Delete a metric by ID
@app.delete("/metrics/{metric_id}")
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(Metric).filter(Metric.id == metric_id).first()

    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    db.delete(metric)
    db.commit()

    return {"message": f"Metric {metric_id} deleted successfully"}
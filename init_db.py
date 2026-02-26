from database import Base, engine
from models import Metric

Base.metadata.create_all(bind=engine)
print("Tables created")
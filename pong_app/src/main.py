import os
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pong_state = {"pong": 0}
pong = 0
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@exercise-db-svc:5432/pingpong")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return "Service is up", 200

@app.get("/health")
def health_check():
    try:
        session = SessionLocal()
        session.execute(text('SELECT 1'))
        session.close()
    except Exception:
        return "Not Healthy", 500
    return "Service Healthy", 200

@app.get("/pingpong")
def status():
    session = SessionLocal()
    counter = session.query(Counter).first()
    if not counter:
        counter = Counter(count=1)
        session.add(counter)
        pongs = counter.count
    else:
        pongs = counter.count
        counter.count += 1
    session.commit()
    session.close()

    return {"pong_count": pongs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3030)), log_level="trace") 

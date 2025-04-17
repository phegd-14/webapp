from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:5173",  # Allow requests from this origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://myuser:password@fastapi-postgres:5432/fastapi_database"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Example model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    status = Column(String, index=True)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")
    
@app.get("/tasks")
def read_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        return {"tasks": [{"id": task.id, "name": task.name, "date": task.date, "status": task.status} for task in tasks]}
    finally:
        db.close()

class TaskCreate(BaseModel):
    name: str
    date: str
    status: str

@app.post("/tasks")
def create_task(task: TaskCreate):
    db = SessionLocal()
    try:
        new_task = Task(name=task.name, date=task.date, status=task.status)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"task": {"id": new_task.id, "name": new_task.name, "date": new_task.date, "status": new_task.status}}
    finally:
        db.close()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    db = SessionLocal()
    try:
        existing_task = db.query(Task).filter(Task.id == task_id).first()
        if not existing_task:
            return {"error": "Task not found"}
        existing_task.name = task.name
        existing_task.date = task.date
        existing_task.status = task.status
        db.commit()
        db.refresh(existing_task)
        return {"task": {"id": existing_task.id, "name": existing_task.name, "date": existing_task.date, "status": existing_task.status}}
    finally:
        db.close()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    try:
        existing_task = db.query(Task).filter(Task.id == task_id).first()
        if not existing_task:
            return {"error": "Task not found"}
        db.delete(existing_task)
        db.commit()
        return {"task_id": task_id, "status": "deleted"}
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
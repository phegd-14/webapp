from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

app = FastAPI()

# Configure allowed origins more specifically (adjust as needed for production)
origins = [
    "http://localhost:5173",  # Your frontend development origin
    # Add other allowed origins here if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database credentials from environment variables
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")  # Default to 'postgres' service name
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ.get("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    status = Column(String, index=True)

# Create tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Call create_tables when the application starts (can also be done separately)
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    try:
        # Try to make a minimal database query to check connectivity
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": f"not connected: {e}"}

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {"tasks": [{"id": task.id, "name": task.name, "date": task.date, "status": task.status} for task in tasks]}

class TaskCreate(BaseModel):
    name: str
    date: str
    status: str

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(name=task.name, date=task.date, status=task.status)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"task": {"id": new_task.id, "name": new_task.name, "date": new_task.date, "status": new_task.status}}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.name = task.name
    existing_task.date = task.date
    existing_task.status = task.status
    db.commit()
    db.refresh(existing_task)
    return {"task": {"id": existing_task.id, "name": existing_task.name, "date": existing_task.date, "status": existing_task.status}}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(existing_task)
    db.commit()
    return {"task_id": task_id, "status": "deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # Listen on all interfaces for Docker
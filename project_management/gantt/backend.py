from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Task(BaseModel):
    id: str
    name: str
    start_date: str
    duration: int
    dependencies: List[str] = []
    progress: int = 0

# In-memory storage
tasks: List[Task] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this root endpoint with appropriate service name
@app.get("/")
async def root():
    return {"message": "Gantt Chart Service"}

@app.post("/task")
async def create_task(task: Task):
    tasks.append(task)
    return {"status": "success"}

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

@app.put("/task/{task_id}")
async def update_progress(task_id: str, progress: int):
    for task in tasks:
        if task.id == task_id:
            task.progress = progress
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Project Management", 
                "subtopic": "Gantt Chart",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
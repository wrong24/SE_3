from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Task(BaseModel):
    id: str
    name: str
    duration: int
    parent_id: Optional[str] = None
    status: str = "pending"

# In-memory storage
tasks_db: List[Task] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "WBS Service is running"}

@app.post("/task/")
async def create_task(task: Task):
    tasks_db.append(task)
    return task

@app.get("/tasks/")
async def get_tasks():
    return {"tasks": tasks_db}

@app.put("/task/{task_id}")
async def update_task(task_id: str, status: str):
    for task in tasks_db:
        if task.id == task_id:
            task.status = status
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/complete_exercise/")
async def complete_exercise():
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={"topic": "Project Management", "subtopic": "WBS"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
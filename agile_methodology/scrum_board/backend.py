from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for scrum board
board = {
    "todo": [],
    "in_progress": [],
    "review": [],
    "done": []
}

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: str
    points: int

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
    return {"message": "Scrum board Service"}

@app.post("/task")
async def create_task(task: Task):
    board[task.status].append(task.dict())
    return {"status": "success"}

@app.put("/task/{task_id}")
async def move_task(task_id: str, new_status: str):
    for status in board:
        for task in board[status]:
            if task["id"] == task_id:
                task["status"] = new_status
                board[new_status].append(task)
                board[status].remove(task)
                return {"status": "success"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/board")
async def get_board():
    return board

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={"topic": "Agile Methodology", "subtopic": "Scrum Board"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
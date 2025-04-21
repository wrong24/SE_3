from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for sprint planning
current_sprint = {
    "stories": [],
    "start_date": None,
    "end_date": None,
    "capacity": 0,
    "allocated_points": 0
}

class SprintStory(BaseModel):
    id: str
    title: str
    points: int
    priority: str
    assigned_to: str

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
    return {"message": "Sprint Planning Service"}


@app.post("/sprint/init")
async def init_sprint(start_date: str, duration: int, capacity: int):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    current_sprint["start_date"] = start
    current_sprint["end_date"] = start + timedelta(days=duration)
    current_sprint["capacity"] = capacity
    return {"status": "success"}

@app.post("/sprint/add-story")
async def add_story(story: SprintStory):
    if current_sprint["allocated_points"] + story.points <= current_sprint["capacity"]:
        current_sprint["stories"].append(story.dict())
        current_sprint["allocated_points"] += story.points
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Exceeds sprint capacity")

@app.get("/sprint")
async def get_sprint():
    return current_sprint

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Agile Methodology", 
                "subtopic": "Sprint Planning",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# In-memory storage for burndown data
sprint_data = {
    "total_points": 0,
    "duration_days": 0,
    "daily_progress": {}
}

class DailyUpdate(BaseModel):
    date: str
    points_completed: int

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
    return {"message": "Burntdown Chart Service"}

@app.post("/sprint/init")
async def init_sprint(total_points: int, duration_days: int):
    sprint_data["total_points"] = total_points
    sprint_data["duration_days"] = duration_days
    sprint_data["daily_progress"] = {}
    return {"status": "success"}

@app.post("/sprint/update")
async def update_progress(update: DailyUpdate):
    sprint_data["daily_progress"][update.date] = update.points_completed
    return {"status": "success"}

@app.get("/sprint/burndown")
async def get_burndown():
    return sprint_data

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Agile Methodology", "subtopic": "Burndown Chart"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
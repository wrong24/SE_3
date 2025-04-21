from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# SDLC phases data
sdlc_data = {
    "phases": [
        {"name": "Requirements", "description": "Gathering and analyzing requirements", "status": "pending"},
        {"name": "Design", "description": "System and software design", "status": "pending"},
        {"name": "Implementation", "description": "Development and coding", "status": "pending"},
        {"name": "Testing", "description": "System and integration testing", "status": "pending"},
        {"name": "Deployment", "description": "Product delivery and maintenance", "status": "pending"}
    ]
}

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
    return {"message": "SLDC Service"}

@app.get("/phases")
async def get_phases():
    return sdlc_data["phases"]  

@app.post("/update/{phase}")
async def update_phase(phase: int):
    if 0 <= phase < len(sdlc_data["phases"]):
        sdlc_data["phases"][phase]["status"] = "completed"
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Invalid phase index")

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Project Management", 
                "subtopic": "SDLC",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
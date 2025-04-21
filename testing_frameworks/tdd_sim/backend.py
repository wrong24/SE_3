from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class TDDStage(BaseModel):
    test_code: str
    implementation: str
    stage: str  # red, green, or refactor

# Track TDD cycles
tdd_cycles: List[Dict] = []

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
    return {"message": "TDD Simulation Service"}

@app.post("/tdd/cycle")
async def submit_tdd_cycle(stage: TDDStage):
    tdd_cycles.append(stage.dict())
    return {"status": "success", "cycle_count": len(tdd_cycles)}

@app.get("/tdd/cycles")
async def get_tdd_cycles():
    return {"cycles": tdd_cycles}

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Testing Frameworks", 
                "subtopic": "TDD",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
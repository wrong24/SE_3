from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Risk(BaseModel):
    id: str
    description: str
    probability: float  # 0-1
    impact: int      # 1-5
    mitigation: str
    status: str = "Open"

# In-memory storage
risks: List[Risk] = []

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
    return {"message": "Risk Management Service"}

@app.post("/risk")
async def add_risk(risk: Risk):
    risks.append(risk)
    return {"status": "success"}

@app.get("/risks")
async def get_risks():
    return {"risks": risks}

@app.put("/risk/{risk_id}")
async def update_risk_status(risk_id: str, status: str):
    risk = next((r for r in risks if r.id == risk_id), None)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    risk.status = status
    return {"status": "success"}

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Project Management", "subtopic": "Risk Management"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class TestSuite(BaseModel):
    name: str
    tests: List[Dict]
    schedule: str

class TestResult(BaseModel):
    suite_name: str
    passed: int
    failed: int
    execution_time: float

# Store test suites and results
test_suites: List[TestSuite] = []
test_results: List[TestResult] = []

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
    return {"message": "Test Automation Service"}

@app.post("/suite")
async def create_suite(suite: TestSuite):
    test_suites.append(suite)
    return {"status": "success", "suite_count": len(test_suites)}

@app.get("/suites")
async def get_suites():
    return {"suites": test_suites}

@app.post("/results")
async def add_result(result: TestResult):
    test_results.append(result)
    return {"status": "success"}

@app.get("/results")
async def get_results():
    return {"results": test_results}

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Testing Frameworks", "subtopic": "Test Automation"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
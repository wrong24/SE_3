from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Simulated microservices for integration testing
services = {
    "auth": {"status": "up", "endpoint": "/auth"},
    "database": {"status": "up", "endpoint": "/db"},
    "api": {"status": "up", "endpoint": "/api"}
}

class TestCase(BaseModel):
    service_flow: List[str]
    expected_result: Dict

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
    return {"message": "Integration Testing Service"}

@app.get("/services")
async def get_services():
    return services

@app.post("/test/integration")
async def run_integration_test(test_case: TestCase):
    results = []
    success = True
    
    for service in test_case.service_flow:
        if service not in services:
            success = False
            results.append(f"Service {service} not found")
        elif services[service]["status"] != "up":
            success = False
            results.append(f"Service {service} is down")
        else:
            results.append(f"Service {service} responded successfully")
    
    return {
        "success": success,
        "results": results,
        "flow": test_case.service_flow
    }

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Testing Frameworks", "subtopic": "Integration Testing"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
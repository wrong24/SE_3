from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Resource(BaseModel):
    id: str
    name: str
    role: str
    availability: int  # hours per week
    assigned_tasks: List[str] = []

class Assignment(BaseModel):
    resource_id: str
    task_name: str
    hours_needed: int

# In-memory storage
resources: List[Resource] = []
assignments: List[Assignment] = []

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
    return {"message": "Resource Allocation Service"}

@app.post("/resource")
async def add_resource(resource: Resource):
    resources.append(resource)
    return {"status": "success"}

@app.get("/resources")
async def get_resources():
    return {"resources": resources}

@app.post("/assign")
async def assign_resource(assignment: Assignment):
    resource = next((r for r in resources if r.id == assignment.resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    total_assigned = sum(a.hours_needed for a in assignments 
                        if a.resource_id == assignment.resource_id)
    
    if total_assigned + assignment.hours_needed > resource.availability:
        raise HTTPException(status_code=400, detail="Resource overallocation")
    
    assignments.append(assignment)
    resource.assigned_tasks.append(assignment.task_name)
    return {"status": "success"}

@app.get("/assignments")
async def get_assignments():
    return {"assignments": assignments}

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Project Management", "subtopic": "Resource Allocation"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
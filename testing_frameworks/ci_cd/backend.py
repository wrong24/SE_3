from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Pipeline(BaseModel):
    name: str
    stages: List[str]
    tests: Dict
    deployment: Dict

class PipelineRun(BaseModel):
    pipeline_name: str
    status: str
    stage_results: Dict

# Store pipelines and runs
pipelines: List[Pipeline] = []
pipeline_runs: List[PipelineRun] = []

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
    return {"message": "CI/CD Service"}

@app.post("/pipeline")
async def create_pipeline(pipeline: Pipeline):
    pipelines.append(pipeline)
    return {"status": "success"}

@app.get("/pipelines")
async def get_pipelines():
    return {"pipelines": pipelines}

@app.post("/run")
async def run_pipeline(pipeline_name: str):
    pipeline = next((p for p in pipelines if p.name == pipeline_name), None)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    run = PipelineRun(
        pipeline_name=pipeline_name,
        status="running",
        stage_results={}
    )
    pipeline_runs.append(run)
    return {"status": "success", "run_id": len(pipeline_runs) - 1}

@app.get("/runs")
async def get_runs():
    return {"runs": pipeline_runs}

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Testing Frameworks", 
                "subtopic": "CI/CD",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for PRs and code changes
pull_requests: Dict[str, Dict] = {}
code_changes: Dict[str, str] = {
    "main": """def calculate_sum(a, b):
    return a + b"""
}

class PullRequest(BaseModel):
    title: str
    description: str
    source_branch: str
    target_branch: str
    changes: str
    status: str = "open"
    id: Optional[str] = None

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
    return {"message": "PR Merging Service"}

@app.post("/create-pr")
async def create_pull_request(pr: PullRequest):
    pr.id = str(uuid.uuid4())[:8]
    pull_requests[pr.id] = pr.dict()
    return {"status": "success", "pr_id": pr.id}

@app.get("/list-prs")
async def list_pull_requests():
    return {"pull_requests": list(pull_requests.values())}

@app.post("/review-pr/{pr_id}")
async def review_pull_request(pr_id: str, approve: bool):
    if pr_id not in pull_requests:
        raise HTTPException(status_code=404, detail="PR not found")
    
    if approve:
        pull_requests[pr_id]["status"] = "approved"
        code_changes["main"] = pull_requests[pr_id]["changes"]
    else:
        pull_requests[pr_id]["status"] = "rejected"
    
    return {"status": "success", "action": "approved" if approve else "rejected"}

@app.get("/code/{branch}")
async def get_code(branch: str):
    if branch not in code_changes:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {"code": code_changes[branch]}

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Collaboration Tools", 
                "subtopic": "PR & Merge",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
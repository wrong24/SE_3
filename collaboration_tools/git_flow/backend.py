from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for simulated git operations
repo_state = {
    "branches": {
        "main": [],
        "develop": [],
        "feature/new-feature": []
    },
    "current_branch": "main",
    "commits": []
}

class Commit(BaseModel):
    message: str
    branch: str
    hash: str

class Branch(BaseModel):
    name: str
    base: str

# Add this right after app = FastAPI()
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
    return {"message": "Git Flow Service"}

@app.post("/create-branch")
async def create_branch(branch: Branch):
    if branch.name in repo_state["branches"]:
        raise HTTPException(status_code=400, detail="Branch already exists")
    repo_state["branches"][branch.name] = repo_state["branches"][branch.base].copy()
    return {"status": "success", "message": f"Created branch {branch.name}"}

@app.post("/commit")
async def commit(commit: Commit):
    if commit.branch not in repo_state["branches"]:
        raise HTTPException(status_code=404, detail="Branch not found")
    repo_state["branches"][commit.branch].append(commit.dict())
    repo_state["commits"].append(commit.dict())
    return {"status": "success", "message": f"Committed to {commit.branch}"}

@app.post("/merge")
async def merge(source: str, target: str):
    if source not in repo_state["branches"] or target not in repo_state["branches"]:
        raise HTTPException(status_code=404, detail="Branch not found")
    repo_state["branches"][target].extend(repo_state["branches"][source])
    return {"status": "success", "message": f"Merged {source} into {target}"}

@app.get("/state")
async def get_state():
    return repo_state

@app.post("/complete_exercise")
async def complete_exercise(user_id: Optional[str] = None, start_time: Optional[float] = None):
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={
                "topic": "Collaboration Tools", 
                "subtopic": "Git Flow",
                "user_id": user_id,
                "start_time": start_time
            }
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
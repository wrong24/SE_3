from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for user stories
stories = []

class UserStory(BaseModel):
    id: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: List[str]
    priority: str
    status: str = "draft"

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
    return {"message": "User Stories Service"}

@app.post("/story")
async def create_story(story: UserStory):
    stories.append(story.dict())
    return {"status": "success"}

@app.get("/stories")
async def get_stories():
    return {"stories": stories}

@app.put("/story/{story_id}")
async def update_story(story_id: str, story: UserStory):
    for idx, existing_story in enumerate(stories):
        if existing_story["id"] == story_id:
            stories[idx] = story.dict()
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Story not found")

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={"topic": "Agile Methodology", "subtopic": "User Stories"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
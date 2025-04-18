from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for kanban board
board = {
    "backlog": [],
    "ready": [],
    "development": [],
    "testing": [],
    "done": []
}

class Card(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: str

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
    return {"message": "Kanban Service"}

@app.post("/card")
async def create_card(card: Card):
    board[card.status].append(card.dict())
    return {"status": "success"}

@app.put("/card/{card_id}")
async def move_card(card_id: str, new_status: str):
    for status in board:
        for card in board[status]:
            if card["id"] == card_id:
                card["status"] = new_status
                board[new_status].append(card)
                board[status].remove(card)
                return {"status": "success"}
    raise HTTPException(status_code=404, detail="Card not found")

@app.get("/board")
async def get_board():
    return board

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Agile Methodology", "subtopic": "Kanban"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import time
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for chat messages
chat_history: List[Dict] = []

class Message(BaseModel):
    sender: str
    content: str
    timestamp: float = None

@app.get("/")
async def root():
    return {"message": "Chat Simulation Service"}


@app.post("/send_message")
async def send_message(message: Message):
    try:
        message.timestamp = time.time()
        chat_history.append(message.dict())
        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@app.get("/get_messages")
async def get_messages():
    try:
        return {"messages": chat_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")

@app.delete("/clear_chat")
async def clear_chat():
    try:
        chat_history.clear()
        return {"status": "success", "message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat: {str(e)}")

@app.get("/chat_stats")
async def get_chat_stats():
    try:
        return {
            "total_messages": len(chat_history),
            "unique_users": len(set(msg["sender"] for msg in chat_history)),
            "last_message_time": max([msg["timestamp"] for msg in chat_history]) if chat_history else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chat stats: {str(e)}")

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Collaboration Tools", "subtopic": "Chat Simulation"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to update progress")
        return {"status": "success", "message": "Exercise completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing exercise: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
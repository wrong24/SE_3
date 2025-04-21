from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import requests
import time

app = FastAPI()

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('progress.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (topic_subtopic TEXT PRIMARY KEY,
                  completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

class Progress(BaseModel):
    topic: str
    subtopic: str
    user_id: Optional[str] = None
    start_time: Optional[float] = None

@app.get("/progress")
async def get_progress() -> List[str]:
    try:
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        c.execute('SELECT topic_subtopic FROM progress')
        items = c.fetchall()
        conn.close()
        return [item[0] for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/progress")
async def update_progress(progress: Progress):
    try:
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        topic_subtopic = f"{progress.topic}_{progress.subtopic}"
        c.execute('INSERT OR REPLACE INTO progress (topic_subtopic) VALUES (?)',
                 [topic_subtopic])
        conn.commit()
        conn.close()

        # If user_id is provided, notify integration API about completion
        if progress.user_id:
            try:
                # Calculate time spent if start_time is provided
                time_spent = 0
                if progress.start_time:
                    time_spent = time.time() - progress.start_time

                # Notify progress tracker API
                attempt_payload = {
                    "user_id": progress.user_id,
                    "lab_type": progress.subtopic,
                    "completion_status": "completed",
                    "time_spent": time_spent,
                    "errors_encountered": 0
                }
                requests.post(
                    "http://integration:8024/progress/lab-attempt",
                    json=attempt_payload,
                    timeout=5
                )
            except Exception as e:
                print(f"Failed to notify integration API: {e}")

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        c.execute('''
            SELECT 
                COUNT(*) as total_completed,
                COUNT(DISTINCT substr(topic_subtopic, 1, instr(topic_subtopic, '_')-1)) as topics_started
            FROM progress
        ''')
        stats = c.fetchone()
        conn.close()
        return {
            "total_completed": stats[0],
            "topics_started": stats[1],
            "total_exercises": 20
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
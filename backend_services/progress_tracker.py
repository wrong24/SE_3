from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import sqlite3
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Database initialization
def init_db():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_settings
                 (id TEXT PRIMARY KEY,
                  theme TEXT,
                  last_topic TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS topic_stats
                 (topic TEXT PRIMARY KEY,
                  visits INTEGER,
                  avg_completion_time REAL)''')
    conn.commit()
    conn.close()

init_db()

class UserSettings(BaseModel):
    user_id: str
    theme: str = "light"
    last_topic: str = None

class TopicStats(BaseModel):
    topic: str
    visits: int = 0
    avg_completion_time: float = 0.0

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
    return {"message": "Dashboard Service"}

@app.get("/dashboard/settings/{user_id}")
async def get_user_settings(user_id: str):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('SELECT theme, last_topic FROM user_settings WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {"theme": result[0], "last_topic": result[1]}
    return {"theme": "light", "last_topic": None}

@app.post("/dashboard/settings")
async def update_settings(settings: UserSettings):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO user_settings (id, theme, last_topic)
                 VALUES (?, ?, ?)''',
              (settings.user_id, settings.theme, settings.last_topic))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/dashboard/stats")
async def get_topic_stats():
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('SELECT * FROM topic_stats')
    stats = [{"topic": row[0], "visits": row[1], "avg_completion_time": row[2]}
             for row in c.fetchall()]
    conn.close()
    return {"stats": stats}

@app.post("/dashboard/track/{topic}")
async def track_topic_visit(topic: str):
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO topic_stats (topic, visits)
                 VALUES (?, COALESCE((SELECT visits + 1 FROM topic_stats WHERE topic = ?), 1))''',
              (topic, topic))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/dashboard/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    # Get user's progress
    progress_response = requests.get("http://localhost:9000/progress")
    if progress_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not fetch progress data")
    
    completed_items = progress_response.json()
    
    # Get topic statistics
    conn = sqlite3.connect('dashboard.db')
    c = conn.cursor()
    c.execute('SELECT topic, visits FROM topic_stats')
    stats = dict(c.fetchall())
    conn.close()
    
    # Generate recommendations based on progress and popularity
    recommendations = []
    for topic in ["Project Management", "Collaboration Tools", 
                  "Agile Methodology", "Testing Frameworks"]:
        topic_completion = len([item for item in completed_items 
                              if item.startswith(f"{topic}_")]) / 5 * 100
        popularity = stats.get(topic, 0)
        
        if topic_completion < 100:
            recommendations.append({
                "topic": topic,
                "completion": topic_completion,
                "popularity": popularity
            })
    
    # Sort by completion (ascending) and popularity (descending)
    recommendations.sort(key=lambda x: (x["completion"], -x["popularity"]))
    return {"recommendations": recommendations[:3]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9100)
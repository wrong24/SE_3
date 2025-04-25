from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import httpx # Use httpx for async requests
import time
import json

app = FastAPI(title="Project Management Backend")

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('progress.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (topic_subtopic TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()

init_db()

# Pydantic model for incoming progress updates from the client (via proxy)
class Progress(BaseModel):
    topic: str # Expected from client, maps to lab_name for API server
    subtopic: str # Expected from client, maps to lab_type for API server
    user_id: Optional[str] = None # Expected from client
    start_time: Optional[float] = None # Expected from client, used to calculate time_spent
    completion_status: Optional[bool] = True
    errors_encountered: Optional[List[str]] = None


# Define the URL for the Integration Proxy Service (where the backend will send API calls)
# Assuming the proxy is named 'integration' and listens internally on port 8024
PROXY_INTERNAL_API_URL = "http://integration:8024"

@app.get("/health")
async def health_check():
    """Health check endpoint for the backend service (Project Management)."""
    try:
        conn = sqlite3.connect('progress.db')
        conn.close()
        db_status = "reachable"
    except Exception as e:
        db_status = f"unreachable: {e}"

    # Also check if the proxy (for outgoing API calls) is reachable
    proxy_status = "unknown"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            # Ping the proxy's root or health endpoint
            proxy_resp = await client.get(PROXY_INTERNAL_API_URL, follow_redirects=True)
            proxy_resp.raise_for_status()
            proxy_status = f"reachable (status {proxy_resp.status_code})"
    except Exception as e:
        proxy_status = f"unreachable: {e}"


    return {
        "status": "healthy",
        "database": db_status,
        "proxy_for_api": proxy_status # Report proxy reachability for outgoing calls
    }


@app.get("/progress/")
async def root_progress():
    """Root endpoint for the progress path in the backend."""
    return {"message": "Project Management Service - Progress Endpoints"}

@app.get("/progress/lab-attempt")
async def get_completed_topic_subtopics() -> List[str]:
    """
    Get a list of all unique topic_subtopic combinations completed.
    Data is retrieved from the backend's local SQLite database.
    """
    try:
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        c.execute('SELECT topic_subtopic FROM progress')
        items = c.fetchall()
        conn.close()
        return [item[0] for item in items]
    except Exception as e:
        print(f"Database error in GET /progress/lab-attempt (backend): {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving completed items from backend.")

@app.post("/progress/lab-attempt")
async def update_progress_and_notify(progress: Progress):
    """
    Receives progress update from client (via proxy), records completion
    in the backend DB, and notifies the main API Server *via the proxy*.
    """
    try:
        # 1. Record completion in the backend's SQLite DB (simple log)
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        topic_subtopic = f"{progress.topic}_{progress.subtopic}"
        c.execute('INSERT OR IGNORE INTO progress (topic_subtopic) VALUES (?)',
                  [topic_subtopic])
        conn.commit()
        conn.close()
        print(f"Backend DB: Recorded completion for {topic_subtopic}")

        # 2. If user_id is provided, notify the main API Server *via the proxy*
        if progress.user_id:
            try:
                time_spent = 0
                if progress.start_time is not None:
                    time_spent = max(0, int(time.time() - progress.start_time))

                # Payload for the API Server (User Progress) - sent to the proxy
                attempt_payload = {
                    "user_id": progress.user_id,
                    "lab_name": progress.topic,
                    "lab_type": progress.subtopic,
                    "completion_status": progress.completion_status if progress.completion_status is not None else True,
                    "time_spent": time_spent,
                    "errors_encountered": progress.errors_encountered if progress.errors_encountered is not None else ["No Error"]
                }
                # The backend now calls a new internal endpoint on the proxy
                proxy_api_endpoint = f"{PROXY_INTERNAL_API_URL}/internal/api/progress/lab-attempt"
                print(f"Backend ({app.title}) attempting to notify API Server *via proxy* at {proxy_api_endpoint} with payload: {attempt_payload}")

                async with httpx.AsyncClient() as client:
                    # Send the payload to the proxy's internal API endpoint
                    response = await client.post(
                        proxy_api_endpoint,
                        json=attempt_payload,
                        timeout=15.0 # Timeout for the call to the proxy
                    )
                    response.raise_for_status() # Raise an exception for bad status codes from the proxy

                    print(f"Backend successfully notified API Server *via proxy*. Proxy responded with status: {response.status_code}")
                    # Optional: Log proxy response body if needed
                    # print(f"Proxy Response Body: {response.text}")


            except httpx.TimeoutException:
                print(f"Backend: Timeout notifying Proxy at {proxy_api_endpoint}")
            except httpx.ConnectError:
                 print(f"Backend: Connection error notifying Proxy at {proxy_api_endpoint}")
            except httpx.RequestError as e:
                 print(f"Backend: Request error notifying Proxy: {e}")
            except Exception as e:
                print(f"Backend: An unexpected error occurred during Proxy notification: {e}")


        return {"status": "success", "message": f"Progress recorded for {topic_subtopic} in backend DB and API server notification attempted via proxy (if user_id provided)."}

    except Exception as e:
        print(f"An unhandled error occurred in POST /progress/lab-attempt (backend): {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error processing progress update in backend: {e}")

@app.get("/stats")
async def get_backend_stats():
    """
    Get simple statistics from the backend's SQLite DB.
    Note: These stats are from the local log, not the main user progress data.
    """
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

        total_exercises = 20

        return {
            "total_completed_items_in_backend_db": stats[0],
            "unique_topics_in_backend_db": stats[1],
             "note": "Stats are from this backend's simple log. For full user stats, use the /progress/stats/{user_id} endpoint (exposed via the proxy/API server).",
            "total_exercises_defined": total_exercises
        }
    except Exception as e:
        print(f"Database error in GET /stats (backend): {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving backend stats.")


if __name__ == "__main__":
    import uvicorn
    # Project Management service runs on port 9000
    uvicorn.run(app, host="0.0.0.0", port=9000)

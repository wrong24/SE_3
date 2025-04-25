from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import httpx # Use httpx for async requests
import time
import json # Import json to parse response content if needed

app = FastAPI(title="Project Management Backend") # Added a title

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('progress.db')
    c = conn.cursor()
    # Simplified schema based on usage - stores unique completed topic_subtopics
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
    # These fields are part of the payload sent *to* the API server,
    # but we include them here in case the client sends them directly.
    # The backend will calculate time_spent if start_time is provided.
    completion_status: Optional[bool] = True
    errors_encountered: Optional[List[str]] = None


# Define the URL for the main API Server (User Progress Service on port 8000)
# This is the service the backend notifies about completed labs.
# Use the service name 'user-progress' and port 8000 as per architecture.
API_SERVER_URL = "http://user-progress:8000"

@app.get("/health")
async def health_check():
    """Health check endpoint for the backend service (Project Management)."""
    # Check if the local database is reachable
    try:
        conn = sqlite3.connect('progress.db')
        conn.close()
        db_status = "reachable"
    except Exception as e:
        db_status = f"unreachable: {e}"

    # Optionally, check if the API server is reachable (though not strictly required for backend health)
    api_server_status = "unknown"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            # Assuming the API server has a health check or root endpoint
            api_resp = await client.get(API_SERVER_URL, follow_redirects=True)
            api_resp.raise_for_status()
            api_server_status = f"reachable (status {api_resp.status_code})"
    except Exception as e:
        api_server_status = f"unreachable: {e}"


    return {
        "status": "healthy",
        "database": db_status,
        "api_server": api_server_status # Report API server reachability
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
    in the backend DB, and notifies the main API Server.
    """
    try:
        # 1. Record completion in the backend's SQLite DB (simple log)
        # This records the unique topic_subtopic combination.
        conn = sqlite3.connect('progress.db')
        c = conn.cursor()
        topic_subtopic = f"{progress.topic}_{progress.subtopic}"
        # Use INSERT OR IGNORE to record the first completion of this topic/subtopic
        c.execute('INSERT OR IGNORE INTO progress (topic_subtopic) VALUES (?)',
                  [topic_subtopic])
        conn.commit()
        conn.close()
        print(f"Backend DB: Recorded completion for {topic_subtopic}")

        # 2. If user_id is provided, notify the main API Server (User Progress)
        if progress.user_id:
            try:
                # Calculate time spent if start_time is provided by the client
                time_spent = 0
                if progress.start_time is not None: # Check explicitly for None
                    time_spent = max(0, int(time.time() - progress.start_time))
                # If start_time was not provided, time_spent remains 0.
                # The API server might handle this differently or require start_time.

                # Payload for the API Server (User Progress)
                # Map topic/subtopic from the client payload to lab_name/lab_type for the API server
                attempt_payload = {
                    "user_id": progress.user_id,
                    "lab_name": progress.topic,      # Map client's 'topic' to API server's 'lab_name'
                    "lab_type": progress.subtopic,   # Map client's 'subtopic' to API server's 'lab_type'
                    # Use the completion_status from the client payload, default is True
                    "completion_status": progress.completion_status if progress.completion_status is not None else True,
                    "time_spent": time_spent,
                    # Use the errors_encountered from the client payload, default is None or empty list
                    "errors_encountered": progress.errors_encountered if progress.errors_encountered is not None else ["No Error"]
                }
                print(f"Backend ({app.title}) attempting to notify API Server at {API_SERVER_URL}/progress/lab-attempt with payload: {attempt_payload}")

                # Use httpx for async POST request to the API Server
                async with httpx.AsyncClient() as client:
                    # The API Server endpoint for recording attempts is /progress/lab-attempt
                    # This assumes the API Server code has a POST endpoint at this exact path.
                    response = await client.post(
                        f"{API_SERVER_URL}/progress/lab-attempt",
                        json=attempt_payload,
                        timeout=15.0 # Increased timeout for API server call
                    )
                    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

                    print(f"Backend successfully notified API Server. Status: {response.status_code}")
                    # Optional: Log API server response body if needed
                    # print(f"API Server Response Body: {response.text}")


            except httpx.TimeoutException:
                print(f"Backend: Timeout notifying API Server at {API_SERVER_URL}/progress/lab-attempt")
                # Log error, but don't fail the main request as Backend DB update succeeded
            except httpx.ConnectError:
                 print(f"Backend: Connection error notifying API Server at {API_SERVER_URL}/progress/lab-attempt")
                 # Log error, but don't fail the main request
            except httpx.RequestError as e:
                 print(f"Backend: Request error notifying API Server: {e}")
                 # Log error, but don't fail the main request
            except Exception as e:
                print(f"Backend: An unexpected error occurred during API Server notification: {e}")
                 # Log error, but don't fail the main request

        # Return success response to the client (via proxy)
        return {"status": "success", "message": f"Progress recorded for {topic_subtopic} in backend DB and API server notification attempted (if user_id provided)."}

    except Exception as e:
        print(f"An unhandled error occurred in POST /progress/lab-attempt (backend): {e}")
        # Raise HTTPException for unhandled errors during the main process
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
        # These stats are based ONLY on the backend's simple log.
        c.execute('''
            SELECT
                COUNT(*) as total_completed,
                COUNT(DISTINCT substr(topic_subtopic, 1, instr(topic_subtopic, '_')-1)) as topics_started
            FROM progress
        ''')
        stats = c.fetchone()
        conn.close()

        # You might want to get the total exercises from a config or another service
        total_exercises = 20 # Example static value or get from elsewhere

        return {
            "total_completed_items_in_backend_db": stats[0], # Renamed for clarity
            "unique_topics_in_backend_db": stats[1],      # Renamed for clarity
             "note": "Stats are from this backend's simple log. For full user stats, use the /progress/stats/{user_id} endpoint (likely exposed via the proxy/API server).",
            "total_exercises_defined": total_exercises # Example value
        }
    except Exception as e:
        print(f"Database error in GET /stats (backend): {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving backend stats.")


if __name__ == "__main__":
    import uvicorn
    # Project Management service runs on port 9000
    uvicorn.run(app, host="0.0.0.0", port=9000)

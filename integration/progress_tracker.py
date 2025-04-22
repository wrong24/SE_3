from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from httpx import TimeoutException, ConnectError

app = FastAPI()
BASE_URL = "http://user-progress:8000"  # Updated port to match new configuration

@app.get("/")
async def root():
    return {"message": "Progress Tracker Service is running."}

@app.api_route("/progress", methods=["GET", "POST"])
@app.api_route("/progress/", methods=["GET", "POST"])
@app.api_route("/progress/{path:path}", methods=["GET", "POST"])
async def proxy_progress_tracking(path: str = "", request: Request = None):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            method = request.method
            url = f"{BASE_URL}/progress/{path}" if path else f"{BASE_URL}/progress/"
            body = await request.body()
            headers = dict(request.headers)

            resp = await client.request(method, url, content=body, headers=headers)
            return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
        except TimeoutException:
            raise HTTPException(status_code=504, detail="Request timed out while connecting to progress service")
        except ConnectError:
            raise HTTPException(status_code=503, detail="Unable to connect to progress service")

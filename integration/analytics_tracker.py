from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from httpx import TimeoutException, ConnectError

app = FastAPI()
BASE_URL = "http://user-analytics:8000"

@app.get("/")
async def root():
    return {"message": "Analytics Tracker Service is running."}

@app.api_route("/analytics", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/analytics/", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/analytics/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_user_analytics(path: str = "", request: Request = None):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            method = request.method
            url = f"{BASE_URL}/analytics/{path}" if path else f"{BASE_URL}/analytics/"
            body = await request.body()
            headers = dict(request.headers)
            # Remove headers that can cause issues
            headers.pop('host', None)
            headers.pop('content-length', None)
            # Ensure Content-Type is set for JSON
            if request.headers.get('content-type', '').startswith('application/json'):
                headers['content-type'] = 'application/json'

            resp = await client.request(method, url, content=body, headers=headers)
            return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
        except TimeoutException:
            raise HTTPException(status_code=504, detail="Request timed out while connecting to analytics service")
        except ConnectError:
            raise HTTPException(status_code=503, detail="Unable to connect to analytics service")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import pytest
import io
import sys
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class TestCase(BaseModel):
    function_code: str
    test_code: str

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
    return {"message": "Unit Testing Service"}

@app.post("/run_test")
async def run_test(test_case: TestCase):
    try:
        # Create test file content
        test_content = f"""
{test_case.function_code}

{test_case.test_code}
"""
        # Capture test output
        stdout = io.StringIO()
        sys.stdout = stdout
        
        # Run pytest
        pytest.main(["-v", "--tb=no", "-s", "-p", "no:warnings", 
                    "--disable-pytest-warnings", "-c", test_content])
        
        sys.stdout = sys.__stdout__
        test_output = stdout.getvalue()
        
        return {"output": test_output, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://localhost:9000/progress",
            json={"topic": "Testing Frameworks", "subtopic": "Unit Testing"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
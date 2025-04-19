from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import markdown
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# In-memory storage for markdown documents
documents = {}

class Document(BaseModel):
    title: str
    content: str

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
    return {"message": "Markdown Document Service"}

@app.post("/save")
async def save_document(doc: Document):
    documents[doc.title] = doc.content
    return {"status": "success", "message": "Document saved"}

@app.get("/document/{title}")
async def get_document(title: str):
    if title not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"content": documents[title]}

@app.get("/preview/{title}")
async def preview_document(title: str):
    if title not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    html_content = markdown.markdown(documents[title])
    return {"html": html_content}

@app.get("/list")
async def list_documents():
    return {"documents": list(documents.keys())}

@app.post("/complete_exercise")
async def complete_exercise():
    try:
        response = requests.post(
            "http://backend_services:9000/progress",
            json={"topic": "Collaboration Tools", "subtopic": "Markdown Documentation"}
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
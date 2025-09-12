from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel
import shutil

from rag import RAG
rag = RAG()

app = FastAPI()

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    rag.process_file(str(file_path))
    return {"message": f"Uploaded and processed {file.filename}"}

# ✅ Use JSON instead of Form
class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(req: AskRequest):
    answer, sources = rag.query(req.question)
    return {"answer": answer, "sources": sources}

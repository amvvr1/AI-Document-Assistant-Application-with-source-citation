from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from app.services.query_engine import QueryEngine
from app.database import init_db
from typing import List
from app.schemas import Response, ChatRequest
import os
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()


@app.on_event("startup")
def on_startup():
    global engine
    init_db()
    try:
        index = query_engine.load_index()
        engine = query_engine.build_query_engine(index=index)
        print("Index loaded from database.")
    except Exception as e:
        print(f"No existing index found, will build on first upload: {e}")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

engine = None

query_engine = QueryEngine()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status" : "running perfectly good"}

@app.post("/uploadmultiplefiles")
def create_upload_files(files: List[UploadFile] = File(...)):
    global engine
    uploaded_files = []
    file_paths = []

    os.makedirs("uploads", exist_ok=True)

    for file in files: 
        uploaded_files.append(file.filename)

        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(file_path)
    
    index = query_engine.build_index(file_paths=file_paths)

    engine = query_engine.build_query_engine(index=index)

    return {"message" : "files uploaded successfully and ready for querying",
             "filenames" : uploaded_files}

def clear_uploads():
    dir_path = Path("uploads")
    if dir_path.exists():
        for item in dir_path.iterdir():
            if item.is_file():
                item.unlink()
            else: 
                shutil.rmtree(item)



@app.post("/questions/", response_model=Response)
@limiter.limit("10/day")
def get_response(query: ChatRequest, request: Request):
    if engine is None:  
        raise HTTPException(status_code=400, detail="Please start by uploading documents first")

    response = engine.query(query.query)

    document_name = "Unknown"
    if response.source_nodes:
        document_name = response.source_nodes[0].node.metadata.get("filename", "Unknown")

    return {
        "answer": response.response,
        "document_name": document_name,
    }

  

@app.delete("/clear-uploads")
def delete_uploads_and_clear_index():
    global engine

    clear_uploads()

    engine = None
    
    return f"files cleared successfully"


@app.get("/uploaded-files/")
def list_uploaded_files():
    upload_directory = "uploads"
    
    try:
        files = os.listdir(upload_directory)
        return {"files" : files}
    
    except FileNotFoundError:
        return {"message" : "No Uploaded Files Found"}
    
    except Exception as e:
        return {"error" : str(e)}
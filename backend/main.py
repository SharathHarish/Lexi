from fastapi import FastAPI, UploadFile, File
from database import engine, Base
from services.parser import parse_file

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    text = parse_file(file)
    return {
        "filename": file.filename,
        "extracted_text": text[:500]  # preview only
    }


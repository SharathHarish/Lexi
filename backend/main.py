from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services.parser import FileParser

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1️⃣ Validate file type
    filename = file.filename
    extension = filename.split(".")[-1].lower()
    if extension not in ["pdf", "docx"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 2️⃣ Save uploaded file temporarily
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3️⃣ Parse file using FileParser
    try:
        text_content = FileParser.parse(file_path, extension)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")
    finally:
        file.file.close()

    # 4️⃣ Return parsed content (for now)
    return JSONResponse({
        "filename": filename,
        "extension": extension,
        "parsed_text": text_content[:500]  # limit preview to first 500 chars
    })

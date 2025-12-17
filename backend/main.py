from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil, os
from services.parser import FileParser
from services.template_engine import TemplateEngine
from typing import Dict
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simulate a simple in-memory DB
TEMPLATES_DB: Dict[str, Dict] = {}

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
    file.file.close()

    # 3️⃣ Parse file
    try:
        parsed_text = FileParser.parse(file_path, extension)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")

    # 4️⃣ Convert parsed text to template
    template_text, metadata = TemplateEngine.convert_to_template(parsed_text)

    # 5️⃣ Save template to "DB"
    template_id = str(uuid.uuid4())
    TEMPLATES_DB[template_id] = {
        "filename": filename,
        "extension": extension,
        "template_text": template_text,
        "metadata": metadata
    }

    # 6️⃣ Return response
    return JSONResponse({
        "template_id": template_id,
        "filename": filename,
        "extension": extension,
        "template_text": template_text[:500],  # preview
        "metadata": metadata
    })

@app.get("/templates")
async def get_templates():
    return TEMPLATES_DB

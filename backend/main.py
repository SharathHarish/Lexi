from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
from models import Template
from services.parser import parse_file
from services.template_engine import convert_to_template

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    raw_text = parse_file(file)
    template_text = convert_to_template(raw_text)

    template = Template(
        name=file.filename,
        content=template_text
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return {
        "id": template.id,
        "name": template.name,
        "preview": template.content[:300]
    }

@app.get("/templates")
def get_templates(db: Session = Depends(get_db)):
    return db.query(Template).all()

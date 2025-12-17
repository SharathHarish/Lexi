import pdfplumber
from docx import Document

def parse_file(file):
    # PDF parsing
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text

    # DOCX parsing
    if file.filename.endswith(".docx"):
        doc = Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

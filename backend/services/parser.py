# services/parser.py

from typing import Callable
import pdfplumber
from docx import Document

class FileParser:
    """
    FileParser provides an abstraction to parse multiple file formats.
    New formats can be added by registering a parser function.
    """
    _parsers: dict[str, Callable[[str], str]] = {}

    @classmethod
    def register_parser(cls, file_type: str, parser_func: Callable[[str], str]):
        """Register a parser function for a new file type."""
        cls._parsers[file_type.lower()] = parser_func

    @classmethod
    def parse(cls, file_path: str, file_type: str) -> str:
        """Parse a file based on its type."""
        parser = cls._parsers.get(file_type.lower())
        if not parser:
            raise ValueError(f"Unsupported file type: {file_type}")
        return parser(file_path)


# -----------------------
# Built-in parser functions
# -----------------------

def parse_docx(file_path: str) -> str:
    """Extract text from DOCX files."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_pdf(file_path: str) -> str:
    """Extract text from PDF files."""
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

# -----------------------
# Register built-in parsers
# -----------------------
FileParser.register_parser("docx", parse_docx)
FileParser.register_parser("pdf", parse_pdf)

# -----------------------
# Example: Adding a TXT parser in future
# -----------------------
def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# To enable TXT parsing later:
# FileParser.register_parser("txt", parse_txt)

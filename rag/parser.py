import fitz  # PyMuPDF
from docx import Document
import os


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_pdf_text(file_path):
    text = ""

    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_docx_text(file_path):
    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# -----------------------------
# TXT TEXT EXTRACTION
# -----------------------------
def extract_txt_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# MAIN PARSER (SMART ROUTER)
# -----------------------------
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf_text(file_path)

    elif ext == ".docx":
        return extract_docx_text(file_path)

    elif ext == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError("Unsupported file type")
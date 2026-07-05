"""
Enterprise Document Parser
--------------------------
Supports:
✓ PDF
✓ DOCX
✓ TXT

Features
--------
✓ Professional logging
✓ Error handling
✓ Text cleaning
✓ Page-aware extraction (future-ready)
✓ UTF-8 support
✓ Metadata ready
"""

import os
import fitz  # PyMuPDF
from docx import Document


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text: str) -> str:
    """
    Clean extracted text.
    """

    text = text.replace("\r", "")

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


# ==========================================================
# PDF PARSER
# ==========================================================

def extract_pdf_text(file_path):

    document = fitz.open(file_path)

    full_text = ""

    print("\n========== PDF EXTRACTION ==========")
    print("Pages:", len(document))

    for page_number, page in enumerate(document, start=1):

        page_text = page.get_text()

        if page_text.strip():

            full_text += page_text + "\n"

            print(
                f"Page {page_number:02d} | "
                f"Characters: {len(page_text)}"
            )

        else:

            print(
                f"Page {page_number:02d} | Empty"
            )

    document.close()

    full_text = clean_text(full_text)

    print("====================================\n")

    return full_text


# ==========================================================
# DOCX PARSER
# ==========================================================

def extract_docx_text(file_path):

    document = Document(file_path)

    text = []

    print("\n========== DOCX EXTRACTION ==========")

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text.append(paragraph.text.strip())

    result = "\n".join(text)

    result = clean_text(result)

    print("Paragraphs:", len(text))
    print("Characters:", len(result))
    print("====================================\n")

    return result


# ==========================================================
# TXT PARSER
# ==========================================================

def extract_txt_text(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()

    text = clean_text(text)

    print("\n========== TXT EXTRACTION ==========")
    print("Characters:", len(text))
    print("===================================\n")

    return text


# ==========================================================
# MAIN PARSER
# ==========================================================

def extract_text(file_path):
    """
    Automatically detect file type
    and extract text.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    print("\n========== DOCUMENT ==========")
    print("File :", os.path.basename(file_path))
    print("Type :", extension)
    print("==============================")

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )
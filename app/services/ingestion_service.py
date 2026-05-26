from pathlib import Path
from pypdf import PdfReader
import re


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text)


def extract_text_from_txt(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def clean_legal_text(text: str) -> str:
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("•", "-")
    return text.strip()


def load_document(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".txt"):
        raw_text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or TXT.")

    return clean_legal_text(raw_text)
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form
from app.services.ingestion_service import clean_legal_text
from app.services.chunking_service import chunk_legal_document
from app.services.embedding_service import generate_embeddings
from app.services.pinecone_service import index
from pypdf import PdfReader


router = APIRouter()


def extract_text_from_uploaded_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


@router.post("/")
async def upload_legal_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    jurisdiction: str = Form(...),
    category: str = Form(...),
    source_url: str = Form("uploaded-via-streamlit")
):
    upload_dir = Path("data/raw/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.lower().endswith(".pdf"):
        raw_text = extract_text_from_uploaded_pdf(str(file_path))
    elif file.filename.lower().endswith(".txt"):
        raw_text = file_path.read_text(encoding="utf-8")
    else:
        return {
            "status": "error",
            "message": "Unsupported file type. Upload PDF or TXT only."
        }

    cleaned_text = clean_legal_text(raw_text)
    chunks = chunk_legal_document(cleaned_text)

    if not chunks:
        return {
            "status": "error",
            "message": "No text chunks could be created from this document."
        }

    embeddings = generate_embeddings(chunks)
    regulation_id = str(uuid.uuid4())

    vectors = []

    for chunk_index, chunk_text in enumerate(chunks):
        vectors.append({
            "id": f"{regulation_id}-{chunk_index}",
            "values": embeddings[chunk_index],
            "metadata": {
                "regulation_id": regulation_id,
                "title": title,
                "jurisdiction": jurisdiction,
                "category": category,
                "source_url": source_url,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text
            }
        })

    index.upsert(vectors=vectors)

    return {
        "status": "success",
        "message": "Document uploaded and indexed successfully.",
        "filename": file.filename,
        "title": title,
        "jurisdiction": jurisdiction,
        "category": category,
        "chunks_uploaded": len(vectors),
        "regulation_id": regulation_id
    }
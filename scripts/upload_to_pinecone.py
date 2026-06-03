from pathlib import Path
import uuid

from app.services.ingestion_service import load_document
from app.services.chunking_service import chunk_legal_document
from app.services.embedding_service import generate_embeddings
from app.services.pinecone_service import index


DOCUMENTS = [
    {
        "file_path": "data/raw/gdpr_article_5.txt",
        "title": "GDPR Article 5 - Principles Relating to Processing of Personal Data",
        "jurisdiction": "European Union",
        "category": "Data Privacy",
        "source_url": "internal-demo-gdpr-article-5"
    },
    {
        "file_path": "data/raw/aml_guidance.txt",
        "title": "AML Customer Due Diligence Guidance",
        "jurisdiction": "United Kingdom",
        "category": "Anti-Money Laundering",
        "source_url": "internal-demo-aml-guidance"
    },
    {
        "file_path": "data/raw/esg_reporting.txt",
        "title": "ESG Reporting Compliance Guidance",
        "jurisdiction": "European Union",
        "category": "ESG Reporting",
        "source_url": "internal-demo-esg-reporting"
    },
    {
        "file_path": "data/raw/data_privacy_policy.txt",
        "title": "Internal Data Privacy Compliance Policy",
        "jurisdiction": "Global",
        "category": "Data Privacy",
        "source_url": "internal-demo-data-privacy-policy"
    }
]


def upload_document_to_pinecone(
    file_path: str,
    title: str,
    jurisdiction: str,
    category: str,
    source_url: str
):
    path = Path(file_path)

    if not path.exists():
        print(f"SKIPPED: File not found -> {file_path}")
        return

    if path.stat().st_size == 0:
        print(f"SKIPPED: Empty file -> {file_path}")
        return

    regulation_id = str(uuid.uuid4())

    text = load_document(file_path)
    chunks = chunk_legal_document(text)

    if not chunks:
        print(f"SKIPPED: No chunks created -> {file_path}")
        return

    generate_embeddings(chunks, input_type="passage")

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

    print(f"SUCCESS: Uploaded {len(vectors)} chunks")
    print(f"Title: {title}")
    print(f"Regulation ID: {regulation_id}")
    print("-" * 70)


def upload_all_documents():
    print("Starting Hydra Analytics document ingestion...")
    print(f"Documents configured: {len(DOCUMENTS)}")
    print("-" * 70)

    for document in DOCUMENTS:
        upload_document_to_pinecone(
            file_path=document["file_path"],
            title=document["title"],
            jurisdiction=document["jurisdiction"],
            category=document["category"],
            source_url=document["source_url"]
        )

    print("Document ingestion completed.")


if __name__ == "__main__":
    upload_all_documents()
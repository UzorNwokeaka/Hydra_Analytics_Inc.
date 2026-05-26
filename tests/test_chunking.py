from app.services.chunking_service import chunk_legal_document


def test_chunk_legal_document_returns_chunks():
    text = "This is a sample legal compliance document. " * 200

    chunks = chunk_legal_document(text)

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
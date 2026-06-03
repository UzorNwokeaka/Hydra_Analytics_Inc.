from app.services.chunking_service import chunk_legal_document


def test_chunk_legal_document_returns_list():
    text = "Personal data must be processed lawfully and securely. " * 100
    chunks = chunk_legal_document(text)

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_chunk_legal_document_handles_short_text():
    text = "Personal data must be protected."
    chunks = chunk_legal_document(text)

    assert len(chunks) == 1
    assert chunks[0] == text
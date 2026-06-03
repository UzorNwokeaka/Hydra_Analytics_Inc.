import os
from pinecone import Pinecone, ServerlessSpec
from app.config import settings


class DummyIndex:
    def query(self, *args, **kwargs):
        return {"matches": []}

    def upsert(self, *args, **kwargs):
        return {"upserted_count": 0}


_pc = None
_index = None


def is_testing_environment() -> bool:
    return (
        os.getenv("TESTING", "false").lower() == "true"
        or os.getenv("CI", "false").lower() == "true"
    )


def get_pinecone_client():
    global _pc

    if is_testing_environment():
        return None

    if not settings.PINECONE_API_KEY:
        raise ValueError(
            "PINECONE_API_KEY is missing. Add it to your environment variables."
        )

    if _pc is None:
        _pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    return _pc


def get_or_create_index():
    global _index

    if is_testing_environment():
        return DummyIndex()

    if _index is not None:
        return _index

    pc = get_pinecone_client()
    index_name = settings.PINECONE_INDEX_NAME

    existing_indexes = pc.list_indexes().names()

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=settings.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.PINECONE_CLOUD,
                region=settings.PINECONE_REGION
            )
        )

    _index = pc.Index(index_name)

    return _index


index = get_or_create_index()
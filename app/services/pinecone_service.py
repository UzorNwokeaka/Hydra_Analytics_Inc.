from pinecone import Pinecone, ServerlessSpec
from app.config import settings

if not settings.PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing. Add it to your environment variables.")

pc = Pinecone(api_key=settings.PINECONE_API_KEY)


def get_or_create_index():
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

    return pc.Index(index_name)


index = get_or_create_index()
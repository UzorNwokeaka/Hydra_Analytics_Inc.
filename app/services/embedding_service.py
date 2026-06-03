from pinecone import Pinecone
from app.config import settings


_local_model = None
_pc = None


def get_pinecone_client():
    global _pc

    if _pc is None:
        _pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    return _pc


def get_local_model():
    global _local_model

    if settings.IS_RENDER:
        raise RuntimeError(
            "Local Hugging Face embeddings are disabled on Render. "
            "Set EMBEDDING_PROVIDER=pinecone for cloud deployment."
        )

    if _local_model is None:
        from sentence_transformers import SentenceTransformer
        _local_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    return _local_model


def generate_local_embedding(text: str) -> list[float]:
    model = get_local_model()
    return model.encode(text).tolist()


def generate_local_embeddings(texts: list[str]) -> list[list[float]]:
    model = get_local_model()
    return model.encode(texts).tolist()


def generate_pinecone_embedding(text: str, input_type: str = "query") -> list[float]:
    pc = get_pinecone_client()

    embeddings = pc.inference.embed(
        model=settings.PINECONE_EMBEDDING_MODEL,
        inputs=[text],
        parameters={
            "input_type": input_type
        }
    )

    return embeddings[0]["values"]


def generate_pinecone_embeddings(
    texts: list[str],
    input_type: str = "passage"
) -> list[list[float]]:
    pc = get_pinecone_client()

    embeddings = pc.inference.embed(
        model=settings.PINECONE_EMBEDDING_MODEL,
        inputs=texts,
        parameters={
            "input_type": input_type
        }
    )

    return [item["values"] for item in embeddings]


def generate_embedding(text: str, input_type: str = "query") -> list[float]:
    if settings.EMBEDDING_PROVIDER.lower() == "pinecone":
        return generate_pinecone_embedding(text, input_type=input_type)

    return generate_local_embedding(text)


def generate_embeddings(
    texts: list[str],
    input_type: str = "passage"
) -> list[list[float]]:
    if settings.EMBEDDING_PROVIDER.lower() == "pinecone":
        return generate_pinecone_embeddings(texts, input_type=input_type)

    return generate_local_embeddings(texts)
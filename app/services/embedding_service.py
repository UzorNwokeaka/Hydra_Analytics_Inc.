from sentence_transformers import SentenceTransformer
from app.config import settings

_model = SentenceTransformer(settings.EMBEDDING_MODEL)


def generate_embedding(text: str) -> list[float]:
    return _model.encode(text).tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    return _model.encode(texts).tolist()
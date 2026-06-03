import os

IS_RENDER = os.getenv("RENDER", "false").lower() == "true"

_model = None


def get_model():
    global _model

    if IS_RENDER:
        raise RuntimeError(
            "Local Hugging Face embeddings are disabled on Render Free Tier. "
            "Use local ingestion or upgrade deployment resources."
        )

    if _model is None:
        from sentence_transformers import SentenceTransformer
        from app.config import settings
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)

    return _model


def generate_embedding(text: str) -> list[float]:
    model = get_model()
    return model.encode(text).tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts).tolist()
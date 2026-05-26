from app.services.embedding_service import generate_embedding
from app.services.pinecone_service import index


def build_metadata_filter(
    jurisdiction: str | None = None,
    category: str | None = None
) -> dict | None:
    filters = {}

    if jurisdiction:
        filters["jurisdiction"] = {"$eq": jurisdiction}

    if category:
        filters["category"] = {"$eq": category}

    return filters if filters else None


def semantic_search(
    query: str,
    top_k: int = 5,
    jurisdiction: str | None = None,
    category: str | None = None
):
    query_vector = generate_embedding(query)

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        filter=build_metadata_filter(jurisdiction, category)
    )

    return results.get("matches", [])